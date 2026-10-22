#!/usr/bin/env python3
"""Run the BenchShare black-box browser evidence suite against a fresh local DB."""
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def api_session_and_create(base: str, actor_id: int, payload: dict[str, Any], key: str) -> dict[str, Any]:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def request(method: str, path: str, body: dict[str, Any], headers: dict[str, str] | None = None):
        values = {"Content-Type": "application/json", "Origin": base, **(headers or {})}
        req = urllib.request.Request(base + path, data=json.dumps(body).encode(), method=method, headers=values)
        try:
            response = opener.open(req, timeout=5)
        except urllib.error.HTTPError as error:
            response = error
        raw = response.read()
        return response.status, json.loads(raw) if raw else None

    status, session = request("POST", "/api/session", {"actor_id": actor_id})
    if status != 201:
        raise AssertionError((status, session))
    status, created = request(
        "POST",
        "/api/reservations",
        payload,
        {"X-CSRF-Token": session["csrf"], "Idempotency-Key": key},
    )
    if status != 201:
        raise AssertionError((status, created))
    return {"opener": opener, "csrf": session["csrf"], "created": created}


def api_post(opener, base: str, csrf: str, path: str, body: dict[str, Any]):
    request = urllib.request.Request(
        base + path,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "Origin": base, "X-CSRF-Token": csrf},
    )
    try:
        response = opener.open(request, timeout=5)
    except urllib.error.HTTPError as error:
        response = error
    raw = response.read()
    return response.status, json.loads(raw) if raw else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--runtime-tree", required=True)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    screenshots = out / "screenshots"
    screenshots.mkdir()
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    db = out / "browser.db"
    ready = out / "ready.json"
    stdout = (out / "server-stdout.txt").open("w", encoding="utf-8")
    stderr = (out / "server-stderr.txt").open("w", encoding="utf-8")
    server = subprocess.Popen(
        [sys.executable, "-m", "benchshare", "--host", "127.0.0.1", "--port", str(port), "--db", str(db), "--ready-file", str(ready)],
        cwd=workspace,
        stdout=stdout,
        stderr=stderr,
        text=True,
    )
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not ready.exists() and server.poll() is None:
        time.sleep(0.05)
    if not ready.exists():
        server.terminate()
        raise RuntimeError(f"server failed before readiness: {server.returncode}")

    captures: list[dict[str, Any]] = []
    checks: dict[str, Any] = {}
    console_messages: list[str] = []
    page_errors: list[str] = []

    def capture(page, name: str, state: str, viewport: str, input_mode: str) -> None:
        path = screenshots / f"{name}.png"
        page.screenshot(path=str(path), full_page=True)
        if path.stat().st_size < 10_000 or path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise AssertionError(f"blank or invalid screenshot: {path}")
        captures.append({
            "name": name,
            "path": path.relative_to(out).as_posix(),
            "sha256": sha(path),
            "bytes": path.stat().st_size,
            "route": "/",
            "state": state,
            "viewport": viewport,
            "input_mode": input_mode,
            "runtime_tree_sha256": args.runtime_tree,
            "captured_at": now(),
        })

    started = now()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)

            boot_context = browser.new_context(viewport={"width": 1440, "height": 1000})
            boot_context.add_init_script("window.fetch = () => new Promise(() => {});")
            boot_page = boot_context.new_page()
            boot_page.goto(base, wait_until="domcontentloaded")
            boot_page.locator("#loading").filter(has_text="Loading workshop route").wait_for()
            capture(boot_page, "00-boot-loading", "boot-loading", "1440x1000", "none")
            boot_context.close()

            mobile_context = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = mobile_context.new_page()
            mobile_page.on("console", lambda message: console_messages.append(message.text) if message.type == "error" else None)
            mobile_page.on("pageerror", lambda error: page_errors.append(str(error)))
            mobile_page.goto(base, wait_until="networkidle")
            mobile_page.locator("#app").wait_for(state="visible")
            checks["mobile_no_session_no_overflow"] = mobile_page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
            capture(mobile_page, "02-mobile-no-session", "no-session-mobile", "390x844", "touch-layout")
            mobile_context.close()

            context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="no-preference")
            context.add_init_script("""(() => {
              const originalFetch = window.fetch.bind(window);
              window.__holdReservationRequest = false;
              window.__releaseReservationRequest = null;
              window.fetch = (input, init = {}) => {
                const url = typeof input === 'string' ? input : input.url;
                if (window.__holdReservationRequest && url === '/api/reservations' && init.method === 'POST') {
                  window.__holdReservationRequest = false;
                  return new Promise((resolve, reject) => {
                    window.__releaseReservationRequest = () => originalFetch(input, init).then(resolve, reject);
                  });
                }
                return originalFetch(input, init);
              };
            })();""")
            page = context.new_page()
            page.on("console", lambda message: console_messages.append(message.text) if message.type == "error" else None)
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.goto(base, wait_until="networkidle")
            page.locator("#app").wait_for(state="visible")

            checks["title"] = page.title()
            checks["one_h1"] = page.locator("h1").count() == 1
            checks["landmarks"] = {role: page.get_by_role(role).count() for role in ["banner", "navigation", "main", "contentinfo"]}
            checks["labeled_controls"] = page.evaluate("""() => [...document.querySelectorAll('input:not([type=hidden]),select,textarea')].every(el => !!el.labels?.length)""")
            checks["desktop_no_horizontal_overflow"] = page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
            capture(page, "01-desktop-no-session", "no-session-populated-equipment-empty-schedule", "1440x1000", "keyboard")

            page.keyboard.press("Tab")
            checks["skip_link_focused"] = page.evaluate("document.activeElement.classList.contains('skip-link')")
            page.keyboard.press("Enter")
            checks["skip_link_targets_main"] = page.evaluate("document.activeElement.id === 'main'")
            page.locator("#actor-id").focus()
            page.keyboard.press("End")
            page.keyboard.press("Tab")
            page.keyboard.press("Enter")
            page.locator("#role-badge").filter(has_text="Maya Chen").wait_for()
            checks["keyboard_session_started"] = True
            checks["member_approval_controls_absent"] = page.get_by_role("button", name="Approve").count() == 0
            page.locator("#reservation-list").filter(has_text="You have no reservations yet").wait_for()
            capture(page, "03-member-empty", "member-empty-reservation-list", "1440x1000", "keyboard")

            page.locator("#request-submit").focus()
            page.keyboard.press("Enter")
            page.locator("#purpose-error").filter(has_text="3 to 200").wait_for()
            checks["validation_focus"] = page.evaluate("document.activeElement.id")
            checks["validation_aria_invalid"] = page.locator("#purpose").get_attribute("aria-invalid") == "true"
            capture(page, "04-validation-error", "member-field-validation", "1440x1000", "keyboard")

            payload = page.evaluate("""() => ({
              equipment_id: Number(document.querySelector('#equipment-id').value),
              start_at: new Date(document.querySelector('#start-at').value).toISOString(),
              end_at: new Date(document.querySelector('#end-at').value).toISOString(),
              purpose: 'Build a keyboard-tested shelf bracket',
              training_ack: true
            })""")
            page.locator("#purpose").focus()
            page.keyboard.type(payload["purpose"])
            page.locator("#training-ack").focus()
            page.keyboard.press("Space")
            page.evaluate("window.__holdReservationRequest = true")
            page.locator("#request-submit").focus()
            page.keyboard.press("Enter")
            page.locator("#request-submit:disabled").filter(has_text="Sending").wait_for()
            checks["submitting_disabled"] = page.locator("#request-submit").is_disabled()
            capture(page, "05-member-submitting", "member-submitting-disabled", "1440x1000", "keyboard")
            page.evaluate("window.__releaseReservationRequest()")
            page.locator("#status").filter(has_text="Request sent").wait_for()
            checks["keyboard_member_request"] = True
            checks["success_focus_status"] = page.evaluate("document.activeElement.id === 'status'")
            member_rows = page.evaluate("fetch('/api/reservations').then(r => r.json())")
            first_id = member_rows["reservations"][0]["id"]
            capture(page, "06-member-success", "member-request-success-pending-ledger", "1440x1000", "keyboard")

            second = api_session_and_create(base, 2, payload, "browser-unauthorized-member")
            unauthorized_status, unauthorized_body = api_post(
                second["opener"], base, second["csrf"], f"/api/reservations/{first_id}/approve", {}
            )
            checks["member_approve_denied"] = {
                "status": unauthorized_status,
                "code": unauthorized_body["error"]["code"],
            }

            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(100)
            checks["mobile_no_horizontal_overflow"] = page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
            checks["mobile_equipment_horizontal"] = page.evaluate("getComputedStyle(document.querySelector('#equipment-list')).display === 'flex'")
            capture(page, "07-mobile-member", "member-pending-mobile", "390x844", "touch-layout")

            page.set_viewport_size({"width": 1440, "height": 1000})
            cancel = page.get_by_role("button", name="Cancel reservation")
            cancel.focus()
            page.keyboard.press("Enter")
            page.locator("#status").filter(has_text="Reservation cancelled").wait_for()
            checks["keyboard_member_cancel"] = True
            capture(page, "08-member-cancel-success", "member-cancel-success", "1440x1000", "keyboard")

            first_pending_id = second["created"]["reservation"]["id"]
            api_session_and_create(base, 1, payload, "browser-second-pending")

            page.locator("#sign-out").focus()
            page.keyboard.press("Enter")
            page.locator("#role-badge").filter(has_text="No session").wait_for()
            page.locator("#actor-id").focus()
            page.keyboard.press("Home")
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Tab")
            page.keyboard.press("Enter")
            page.locator("#role-badge").filter(has_text="Avery Brooks").wait_for()
            page.locator("#pending-list article").first.wait_for()
            capture(page, "09-coordinator-queue", "coordinator-two-pending", "1440x1000", "keyboard")

            first_approve = page.locator("#pending-list article").first.get_by_role("button", name="Approve")
            first_approve.focus()
            page.keyboard.press("Enter")
            page.locator("#status").filter(has_text="Request approved").wait_for()
            second_approve = page.locator("#pending-list article").first.get_by_role("button", name="Approve")
            second_approve.focus()
            page.keyboard.press("Enter")
            page.locator("#status").filter(has_text="Approval conflict with reservation").wait_for()
            checks["conflict_focus_status"] = page.evaluate("document.activeElement.id === 'status'")
            checks["conflict_identity_visible"] = str(first_pending_id) in page.locator("#status").inner_text()
            checks["keyboard_coordinator_approve_and_conflict"] = True
            capture(page, "10-coordinator-conflict", "coordinator-approval-conflict-refreshed", "1440x1000", "keyboard")

            remaining = page.locator("#pending-list article").first
            remaining.get_by_label("Rejection reason").focus()
            page.keyboard.type("Overlaps an approved reservation")
            remaining.get_by_role("button", name="Reject").focus()
            page.keyboard.press("Enter")
            page.locator("#status").filter(has_text="Request rejected").wait_for()
            page.locator("#pending-list").filter(has_text="No pending requests").wait_for()
            checks["keyboard_coordinator_reject"] = True
            capture(page, "11-coordinator-empty", "coordinator-empty-queue-after-decision", "1440x1000", "keyboard")
            context.close()

            reduced = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
            reduced_page = reduced.new_page()
            reduced_page.goto(base, wait_until="networkidle")
            reduced_page.locator("#app").wait_for(state="visible")
            checks["reduced_motion_media"] = reduced_page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
            checks["reduced_motion_transition"] = reduced_page.locator("button").first.evaluate("el => getComputedStyle(el).transitionDuration")
            checks["reduced_motion_animation"] = reduced_page.locator("#loading").evaluate("el => getComputedStyle(el).animationName")
            reduced.close()
            checks["browser_version"] = browser.version
            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
        stdout.close()
        stderr.close()

    required_true = [
        "one_h1", "labeled_controls", "desktop_no_horizontal_overflow", "skip_link_focused",
        "skip_link_targets_main", "keyboard_session_started", "member_approval_controls_absent",
        "validation_aria_invalid", "submitting_disabled", "keyboard_member_request",
        "success_focus_status", "mobile_no_session_no_overflow", "mobile_no_horizontal_overflow",
        "mobile_equipment_horizontal", "keyboard_member_cancel", "conflict_focus_status",
        "conflict_identity_visible", "keyboard_coordinator_approve_and_conflict",
        "keyboard_coordinator_reject", "reduced_motion_media",
    ]
    failures = [key for key in required_true if checks.get(key) is not True]
    if checks.get("validation_focus") != "purpose":
        failures.append("validation_focus")
    if checks.get("member_approve_denied") != {"status": 403, "code": "forbidden"}:
        failures.append("member_approve_denied")
    if checks.get("reduced_motion_transition") not in ("0s", "0s, 0s"):
        failures.append("reduced_motion_transition")
    if checks.get("reduced_motion_animation") != "none":
        failures.append("reduced_motion_animation")
    if any(value != 1 for value in checks.get("landmarks", {}).values()):
        failures.append("landmarks")
    expected_console_errors = [message for message in console_messages if "status of 422" in message or "status of 409" in message]
    unexpected_console_errors = [message for message in console_messages if message not in expected_console_errors]
    if unexpected_console_errors:
        failures.append("unexpected_console_errors")
    if page_errors:
        failures.append("page_errors")

    report = {
        "schema_version": "2.0",
        "case_id": "benchshare-v1",
        "started_at": started,
        "ended_at": now(),
        "base_url": base,
        "runtime_tree_sha256": args.runtime_tree,
        "tool": "playwright-python",
        "checks": checks,
        "screenshots": captures,
        "expected_console_errors": expected_console_errors,
        "unexpected_console_errors": unexpected_console_errors,
        "page_errors": page_errors,
        "failures": failures,
        "passed": not failures and len(captures) == 12,
        "remote_actions": [],
    }
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": report["passed"], "screenshots": len(captures), "failures": failures}, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

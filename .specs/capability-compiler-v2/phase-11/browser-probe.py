from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(__file__).with_name("browser-probe.png")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 800, "height": 600})
    page.set_content("<!doctype html><title>probe</title><main><h1>Browser probe</h1></main>")
    page.screenshot(path=str(out))
    print({"browser": browser.version, "title": page.title(), "h1": page.locator("h1").inner_text(), "screenshot": str(out), "bytes": out.stat().st_size})
    browser.close()

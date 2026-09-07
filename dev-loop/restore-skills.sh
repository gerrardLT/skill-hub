#!/usr/bin/env bash
# Restore the 26 external skills that dev-loop routes to (25 core-tier + retro).
#
# Pinned versions live in skills.lock.json (commit SHA per repo + SKILL.md
# sha256 per skill). This script re-installs from the same sources; verify
# drift afterwards with:  python audit-skills.py
#
# Notes:
#   * posthog/* is intentionally absent (user decision: PostHog fully removed;
#     posthog/posthog is a 6.5 GB repo).
#   * garrytan/gstack has a root SKILL.md, so qa-only/ship need --full-depth.
#   * obra/superpowers + ui-ux-pro-max come from the Qoder marketplace plugin
#     cache, not from npx; install those two plugins from the Qoder market.

set -u
cd "$(dirname "$0")"

add() {
  local repo="$1"; shift
  echo ">>> $repo :: $*"
  npx --yes skills@latest add "$repo" --skill "$@" -g -y || echo "    FAILED: $repo"
}

# domain 1 - requirements
add deanpeters/Product-Manager-Skills prd-development product-strategy-session discovery-process
add phuryn/pm-skills                  prioritization-frameworks outcome-roadmap

# domain 2 - design
add pbakaus/impeccable                impeccable
add vercel-labs/agent-skills          web-design-guidelines
add emilkowalski/skills               review-animations

# domain 4 - qa
add anthropics/knowledge-work-plugins testing-strategy code-review
add openai/skills                     playwright

# domain 5/6 - release + retro
add github/awesome-copilot            github-actions-hardening
add rampstackco/claude-skills         incident-response
add refoundai/lenny-skills            analyzing-user-feedback
add amplitude/builder-skills          craft-experiment-design
add anthropics/knowledge-work-plugins metrics-review validate-data

# gstack: root SKILL.md is a router, so --full-depth is required to register
# the qa-only / ship / retro sub-skills as first-class skills.
echo ">>> garrytan/gstack :: qa-only ship retro (--full-depth)"
npx --yes skills@latest add garrytan/gstack --skill qa-only ship retro --full-depth -g -y \
  || echo "    FAILED: garrytan/gstack"

echo
echo "Done. Verify with: python audit-skills.py"
echo "Marketplace plugins to install manually in Qoder: superpowers, ui-ux-pro-max-skill"

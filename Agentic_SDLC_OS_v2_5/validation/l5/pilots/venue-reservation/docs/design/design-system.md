# Design System Slice

## Objective

Define the minimum visual and semantic system for the reservation state prototype while preserving the existing Rally Atelier direction.

## Facts and evidence

The user-owned design source emphasizes precise hierarchy, one highlighted table or decision, short low-overshoot motion and status that is not color-only. The pilot uses neutral surfaces, one vermilion action accent, a teal availability state and explicit text labels.

## Decision and specification

Tokens: 8 px spacing base, 16 px card radius, 44 px minimum target, 160-200 ms standard transition, 3:1 focus indicator contrast and 4.5:1 body text contrast. Components: time option, session card, primary action, state banner, queue position and error recovery panel.

## Risks and edge cases

The prototype is not a final branded application. It excludes photography, complex table maps and expressive motion. High-saturation accents are limited to one per viewport.

## Verification and acceptance criteria

Acceptance requires semantic HTML, focus-visible styling, reduced-motion support and text labels for all states. Tokens are documented in `prototype/index.html` CSS variables.

## Traceability and ownership

Owner: Design OS. Inputs: source UI/UX guideline and IS-001. Downstream: PROTO-001 and DH-001.

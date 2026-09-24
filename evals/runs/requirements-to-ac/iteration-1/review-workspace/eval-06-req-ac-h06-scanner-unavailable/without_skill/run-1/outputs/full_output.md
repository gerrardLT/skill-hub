Status: needs-input

# Acceptance Criteria

## Supported acceptance

### AC-1: Keyboard completion
Given a user is in the settings flow,
When the user operates the flow using only a keyboard,
Then the user can reach, operate, and complete every required step without pointer input.

### AC-2: Visible focus
Given a user navigates the settings flow using a keyboard,
When focus moves to any interactive control,
Then a visible focus indicator identifies the currently focused control.

## Scan-dependent acceptance

### AC-3: External accessibility scan — needs-input
Given the settings flow is available to the required external accessibility scanner,
When the scanner is run against the settings flow,
Then the result meets the release requirement defined by the scan report or agreed pass threshold.

Evidence required to resolve: the external scanner must be available, the applicable scan scope and pass threshold must be specified, and the resulting report must be attached. No scan execution or passing result is asserted here.

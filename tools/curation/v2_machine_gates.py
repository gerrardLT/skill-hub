"""Deterministic machine gates for V2 consolidated capabilities.

V2 recipes carry human-readable `hard_gates` that state obligations for the model. Those
cannot be evaluated by regex without faking rigour, so they are kept as recorded
`advisory_gates` and handed to independent review. What blocks a step is a small set of
machine gates derived from the contract's own structural properties.

Every gate here is a pure function of (output, context). No model self-report is trusted.
"""
from __future__ import annotations

import re
from typing import Any

# The status is declared in the first few lines. Real outputs write it plain, bolded, as a
# heading, or as a list item, so the gate accepts those forms rather than one exact spelling.
STATUS_DECLARATION = re.compile(
    r'(?im)^[\s>*_`#\-]*\*{0,2}\s*status\*{0,2}\s*[:：]\s*\*{0,2}\s*`?\s*'
    r'(passed|needs-input|blocked|failed)\b')
STATUS_SEARCH_LINES = 8

# A step must say what it did not do. Fixed phrases miss legitimate paraphrases, so the gate
# matches the shape: a negation followed by an action verb within the same clause.
NON_EXECUTION_PATTERN = re.compile(
    r'(?i)\b(?:not|no|never|without|none|neither|nothing)\b[^.\n;]{0,90}?'
    r'\b(?:execut\w*|ran|run|deploy\w*|merg\w*|push\w*|publish\w*|mutat\w*|writ\w*|'
    r'implement\w*|appl\w*|chang\w*|claim\w*|perform\w*|creat\w*|edit\w*|modif\w*|'
    r'install\w*|commit\w*|approv\w*|remediat\w*|verif\w*)\b')

# Explicit phrases stay as a fallback for outputs that state it plainly.
NON_EXECUTION_MARKERS = (
    'not executed', 'not run', 'did not run', 'did not execute', 'nothing was executed',
    'no tools', 'without tools', 'no access beyond', 'not performed', 'was not performed',
    'were not performed', 'proposed', 'would run', 'planned command', 'not yet run',
    'no commands were run', 'no command was run', 'not been executed', 'unexecuted',
    'not applied', 'not deployed', 'not pushed', 'not merged', 'no changes were made',
    'no mutation', 'no writes', 'read-only', 'not verified by execution',
    'not verified against a live', 'placeholders', 'not claimed as executed',
    'non-execution', 'no production rollout', 'not implement', 'does not implement',
    'does not mutate', 'not mutate', 'no rollout is claimed', 'is claimed',
)

UNKNOWN_MARKERS = (
    'unknown', 'unknowns', 'open question', 'open questions', 'unresolved',
    'unspecified', 'not supplied', 'not provided', 'not stated', 'missing',
    'conflict', 'conflicting', 'counterevidence', 'uncertainty', 'uncertain',
    'assumption', 'assumptions', 'to be confirmed', 'tbd', 'gap', 'gaps',
    'none identified', 'no unknowns', 'none unresolved', 'none outstanding',
)

AUTHORITY_MARKERS = (
    'authority', 'authorization', 'authorisation', 'authorized', 'authorised',
    'approval', 'approved', 'approver', 'owner', 'permission', 'consent',
    'not authorized', 'not authorised', 'unauthorized', 'human decision',
    'decision owner', 'sign-off', 'signoff', 'countersign',
)

# An unknowns register must be a labelled section or list, not an incidental use of the word
# "gap". Matching the heading/label form is what keeps this gate from passing everything.
UNKNOWN_HEADING = re.compile(
    r'(?im)^#{1,6}\s*[^\n]*(?:unknown|unresolved|open question|assumption|conflict|'
    r'counterevidence|uncertaint|residual risk|limitation|missing)')
UNKNOWN_LABEL = re.compile(
    r'(?im)^\s*(?:[-*|]\s*)?\*{0,2}(?:UNK-\d+|unknown|unknowns|open question|'
    r'assumption|conflict|counterevidence|residual risk|limitation|unresolved)\*{0,2}\s*[:\-|]')
UNKNOWN_NONE = re.compile(
    r'(?i)\b(?:no|none|zero)\s+(?:unknown|unknowns|unresolved|open question|conflict|'
    r'assumption|limitation|residual risk)\w*\b')

# Authority must be referenced in an authority-bearing way, not as the word "owner" in passing.
AUTHORITY_PHRASES = re.compile(
    r'(?i)\b(?:not authorized|not authorised|unauthori[sz]ed|requires? (?:explicit )?(?:authorization|authorisation|approval)|'
    r'without (?:explicit )?(?:authorization|authorisation|approval)|pending (?:authorization|authorisation|approval)|'
    r'approval (?:is )?(?:required|missing|not supplied|not provided)|'
    r'decision owner|authorized by|authorised by|approved by|signed by|'
    r'authority (?:boundary|record|owner|is|was|not)|authorization (?:record|scope|boundary)|'
    r'human (?:decision|approval|checkpoint|owner))')

IDENTIFIER_PATTERNS = (
    # named registers: SRC-1, EV-3, REQ-12, UNK-004, ...
    re.compile(r'\b(?:SRC|EV|REQ|AC|RULE|DEP|SCOPE|FIND|RISK|UNK|ASSUMPTION|ART|CF|CAND|BASE)-\d+\b'),
    # short evidence labels used across the corpus: E1, A2, C3, S4, D1, R1, H2, P7, F1
    re.compile(r'\b[A-Z]\d{1,3}\b'),
    re.compile(r'\b[0-9a-f]{7,40}\b'),                       # commit / artifact hash
    re.compile(r'\b[\w./-]+\.(?:py|js|ts|tsx|jsx|go|rs|java|rb|md|json|yaml|yml|toml|sql|sh)(?::\d+)?\b'),
)

# coverage values that make a contract care about preserved uncertainty or provenance
UNCERTAINTY_COVERAGE = {
    'uncertainty', 'unknowns', 'unknown-preservation', 'conflict', 'conflicts',
    'variance', 'residual-risk', 'limitations', 'counterevidence', 'assumption',
}

# Evidence binding is only a fair requirement when the contract makes provenance its point.
# Applied universally it would fail prose deliverables that legitimately carry no identifiers.
PROVENANCE_COVERAGE = {
    'provenance', 'capture-provenance', 'source-identity', 'evidence', 'traceability',
    'source-traceability', 'candidate-identity', 'artifact-identity', 'hash-binding',
}

# permissions that cannot mutate anything outside the run output
NON_MUTATING_PERMISSIONS = {
    'read-only', 'external-read', 'artifact-write-local-exec-external-read',
    'local-exec-external-read',
}


def _folded(text: str) -> str:
    return text.casefold()


def gate_status_declared(output: str, context: dict[str, Any]) -> tuple[bool, list[str]]:
    """The output must declare exactly one of the four statuses near the top."""
    head = '\n'.join(output.splitlines()[:STATUS_SEARCH_LINES])
    match = STATUS_DECLARATION.search(head)
    if match:
        return True, [f'status={match.group(1).lower()}']
    if not output.strip():
        return False, ['empty output']
    first = next((l for l in output.splitlines() if l.strip()), '')[:80]
    return False, [f'no status declaration in the first {STATUS_SEARCH_LINES} lines; starts: {first}']


def gate_non_execution_stated(output: str, context: dict[str, Any]) -> tuple[bool, list[str]]:
    """The step must be explicit about what it did not execute."""
    evidence = []
    for match in NON_EXECUTION_PATTERN.finditer(output):
        evidence.append(' '.join(match.group(0).split())[:70])
        if len(evidence) >= 3:
            break
    if not evidence:
        folded = _folded(output)
        evidence = [marker for marker in NON_EXECUTION_MARKERS if marker in folded][:3]
    if evidence:
        return True, evidence
    return False, ['no statement about non-execution']


def gate_unknowns_preserved(output: str, context: dict[str, Any]) -> tuple[bool, list[str]]:
    """Uncertainty must survive into the artifact as a labelled register."""
    evidence = []
    heading = UNKNOWN_HEADING.search(output)
    if heading:
        evidence.append(f'heading: {heading.group(0).strip()[:60]}')
    labels = UNKNOWN_LABEL.findall(output)
    if labels:
        evidence.append(f'labels: {sorted(set(labels))[:4]}')
    none = UNKNOWN_NONE.search(output)
    if none:
        evidence.append(f'explicit-none: {none.group(0)[:40]}')
    if evidence:
        return True, evidence[:3]
    return False, ['no labelled unknown/conflict/assumption register']


def gate_authority_named(output: str, context: dict[str, Any]) -> tuple[bool, list[str]]:
    """A step with a human decision point must name the authority it depends on."""
    hits = AUTHORITY_PHRASES.findall(output)
    if hits:
        return True, [str(h) for h in sorted(set(hits))[:4]]
    return False, ['no authority-bearing reference (approval, authorization, decision owner)']


def gate_evidence_binding(output: str, context: dict[str, Any]) -> tuple[bool, list[str]]:
    """When provenance is the point, claims must bind to at least one stable identifier."""
    hits = []
    for pattern in IDENTIFIER_PATTERNS:
        found = pattern.findall(output)
        if found:
            hits.extend(found[:4])
    unique = sorted(set(hits))
    if unique:
        return True, unique[:6]
    return False, ['no stable identifier (id, hash, or file reference)']


MACHINE_GATES = {
    'status-declared': gate_status_declared,
    'non-execution-stated': gate_non_execution_stated,
    'unknowns-preserved': gate_unknowns_preserved,
    'authority-named': gate_authority_named,
    'evidence-binding': gate_evidence_binding,
}


def evaluate_machine_gate(gate: str, output: str, context: dict[str, Any]) -> dict[str, Any]:
    evaluator = MACHINE_GATES.get(gate)
    if evaluator is None:
        return {'gate': gate, 'passed': False, 'evidence': [],
                'error': 'no deterministic evaluator'}
    passed, evidence = evaluator(output, context)
    return {'gate': gate, 'passed': passed, 'evidence': evidence}


def compile_machine_gates(contract: dict[str, Any], permission: str | None = None) -> list[str]:
    """Derive the blocking gate set for a step from its contract's structural properties.

    This is a function of declared structure, never of interpreting the prose gates.
    """
    gates = ['status-declared', 'non-execution-stated']

    policy = contract.get('policy') or {}
    coverage = {str(value).casefold() for value in (policy.get('coverage') or [])}
    effective = permission or contract.get('permission_identity') or ''

    if coverage & UNCERTAINTY_COVERAGE or policy.get('data_governance'):
        gates.append('unknowns-preserved')

    if policy.get('human_decision') or coverage & {
            'per-authorization', 'per-action-authorization', 'human-decision',
            'authorization', 'approval'}:
        gates.append('authority-named')

    if coverage & PROVENANCE_COVERAGE:
        gates.append('evidence-binding')

    # a capability that cannot mutate still owes the reader an explicit uncertainty register
    if effective in NON_MUTATING_PERMISSIONS and 'unknowns-preserved' not in gates:
        gates.append('unknowns-preserved')

    # stable order, no duplicates
    return list(dict.fromkeys(gates))

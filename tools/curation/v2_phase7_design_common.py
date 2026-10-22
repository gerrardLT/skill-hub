from __future__ import annotations

from typing import Any


def D(
    trigger: str,
    triggers: list[str],
    anti: list[tuple[str, str]],
    procedure: list[str],
    artifacts: list[str],
    gate: str,
    neighbors: list[str],
    coverage: list[str],
    holdout: tuple[str, str],
    *,
    mutation_scope: str,
    human: bool = False,
    data: bool = False,
    action: bool = False,
) -> dict[str, Any]:
    return {
        "trigger": trigger,
        "triggers": triggers,
        "anti": anti,
        "procedure": procedure,
        "artifacts": artifacts,
        "distinctive_gate": gate,
        "neighbors": neighbors,
        "coverage": coverage,
        "holdout": holdout,
        "mutation_scope": mutation_scope,
        "human_decision": human,
        "data_governance": data,
        "remote_or_system_action": action,
    }

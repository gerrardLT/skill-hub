# Reviewer Brief: V2 1.0.0 Atomic Skill Semantic Audit

You are a read-only independent reviewer. Do not modify any file. Return only the JSON object specified below as your final answer.

## Inputs

Your batch file `curation/v2/skill-audit/batches/<domain>.json` lists each Skill with:
- `path`: `slots/v2/1.0.0/skills/<id>/` containing `SKILL.md`, `contract.json`, `provenance.json`
- `static`: deterministic scan record (neighbours, Phase 9 holdout outcomes, mutation status, findings)
- `source_root`: original sources live under `skills/`; `provenance.json -> candidate_provenance.source_evidence` entries are `path:start-end` relative to `skills/`.

Read every Skill in your batch fully. For source fidelity, open at least the two most substantive `source_evidence` ranges per Skill.

## Already-established systemic findings (do NOT repeat per Skill)

- Trigger section restates Responsibility (all 157).
- SKILL.md omits contract `forbidden_actions` and usually the second contract hard gate.
- Stale pre-release forbidden action "claim ... released status".
- Status Mapping / governance boilerplate shared across many Skills.
- Phase 9 measured routing decisions only, not execution output quality.

Mention one of these only if it causes a Skill-specific defect beyond the systemic one.

## Score each Skill 0-3 on

1. `boundary`: single atomic responsibility, no hidden pipeline.
2. `trigger_precision`: trigger/anti-triggers separate it from the nearest neighbours given.
3. `procedure`: steps are concrete, domain-specific, executable.
4. `output_verifiability`: outputs can be checked deterministically or judged unambiguously.
5. `gate_specificity`: hard gates target this domain's real failure modes.
6. `permission_fit`: permission identity and mutation scope match the responsibility.
7. `source_fidelity`: key techniques, thresholds, anti-patterns from sources are preserved, not diluted.
8. `measured_efficacy`: use the static Phase 9 data (tie = no measured lift; survived mutation = insensitive).

0 = defective, 1 = weak, 2 = adequate, 3 = best-in-class.

## Verdict

`keep` | `improve` | `merge` | `split` | `retire`. `merge`/`split` must name the target Skill(s).

## Output (final answer, JSON only)

```json
{
  "domain": "<domain>",
  "reviewer_read_only": true,
  "skills": [
    {
      "id": "<skill-id>",
      "scores": {"boundary": 0, "trigger_precision": 0, "procedure": 0, "output_verifiability": 0, "gate_specificity": 0, "permission_fit": 0, "source_fidelity": 0, "measured_efficacy": 0},
      "verdict": "improve",
      "merge_or_split_target": null,
      "strengths": ["..."],
      "findings": [
        {"priority": "P1", "dimension": "source_fidelity", "issue": "...", "evidence": "slots/v2/1.0.0/skills/<id>/SKILL.md:NN or skills/<src>:NN-MM", "recommendation": "concrete rewrite or addition"}
      ],
      "lost_source_techniques": ["named technique/threshold present in source but absent in Skill"]
    }
  ],
  "cross_skill_findings": [{"skills": ["a", "b"], "issue": "...", "recommendation": "..."}]
}
```

P1 = materially reduces Skill effectiveness; P2 = quality/clarity. Every finding needs concrete file:line evidence. Never invent evidence; if a source range cannot be read, say so.

# Conference Convergence Policy

## Principle

Agreement is not evidence. The conference converges only when the latest proposal has complete specialist coverage, no unresolved objection, valid evidence and independent verification.

## Mandatory release checks

| Check | Failure behavior |
|---|---|
| all configured agents screened | block |
| all screens reference current proposal version | block |
| no relevance-provider failures | block |
| every mandatory specialist active | block |
| every active specialist reviewed current proposal | block |
| no analysis-provider failures | block |
| no current unresolved objection of any severity | block |
| independent critic present for T2+ | block |
| verification agent present for T2+ | block |
| authoritative evidence attached for T3/T4 | block |
| every active T3/T4 approval cites registered evidence | block |
| no active agent incorrectly abstained | block |

## Valid verdicts

- `approve` — no known blocking issue within scope.
- `approve_with_conditions` — creates tracked conditions that must be resolved.
- `object` — creates a major or critical objection.
- `insufficient_evidence` — creates a major evidence objection.
- `abstain_out_of_scope` — valid only for agents not in the active work cell.

## Residual risk

A risk may be accepted only when:

1. its consequence and likelihood are stated;
2. the relevant specialist confirms the characterization;
3. evidence supporting the decision is linked;
4. the authorized decision owner is recorded;
5. containment, detection and revisit triggers exist.

Safety, legal and physical-action constraints cannot be waived by majority vote or model confidence.

## Termination outcomes

- `FINALIZED` — every convergence check passes.
- `BLOCKED` — one or more release checks failed. The coverage failures and event log identify whether the cause is evidence, safety, unresolved conflict, provider failure or ambiguous scope.

# Evidence-Gated Engineering Conference Protocol

## Objective

Run an exhaustive, replayable product-development review in which every configured agent is screened, every relevant specialist contributes independently, cross-domain objections are resolved through evidence, and no proposal is finalized because of conversational consensus alone.

## Non-negotiable distinction

All agents **attend the relevance pass**. Only `primary`, `reviewer`, and `affected` agents enter deep analysis. `monitor` and `out_of_scope` decisions remain stored with reasons. This preserves coverage without turning 184 roles into one unbounded conversation.

## State sequence

```text
INTAKE
→ CONTEXT_FROZEN
→ ALL_AGENTS_SCREENED
→ WORK_CELL_FORMED
→ INDEPENDENT_ANALYSIS
→ POSITIONS_COLLECTED
→ OBJECTIONS_OPEN
↔ PROPOSAL_REVISED
→ AFFECTED_AGENTS_REACTIVATED
→ OBJECTIONS_RESOLVED
→ VERIFIED
→ FINALIZED
```

`BLOCKED` is a valid outcome when evidence, coverage, provider health, safety or verification is insufficient.

## Stage requirements

### Intake

The task manifest supplies objective, product boundary, risk tier, requirements, constraints, interfaces, evidence and proposal. User statements are tagged as requirements, constraints, preferences or hypotheses; they are not automatically facts.

### Context freeze

The orchestrator hashes the exact manifest. All positions and objections carry the proposal version. A changed proposal must produce a new version and new context hash.

### All-agent screening

Every agent receives the same compact task manifest plus its own role contract. Relevance comes from four defenses:

1. deterministic keyword/domain/interface rules;
2. mandatory consequence and lifecycle rules;
3. agent-specific semantic self-assessment through the provider;
4. dependency expansion across known interfaces.

Provider failure activates the affected specialist conservatively and blocks finalization until the failure is cleared.

### Independent analysis

Active agents produce their first position without seeing peer conclusions. They return conclusions, assumptions, claims, evidence references, risks, conditions, requested specialists, confidence and verification—not hidden chain-of-thought.

An agent may cite only evidence identifiers registered in the frozen task context. For `T3/T4`, an approval without registered evidence is invalid and becomes a provider/evidence failure. Identifier registration prevents invented citations but does not prove that a source supports a claim; semantic evidence checking remains a separate required service and review step.

### Objection round

`OBJECT`, `INSUFFICIENT_EVIDENCE`, and conditional approval create explicit objection records. Discussion occurs around these objects, not in an unstructured transcript.

### Revision and propagation

Any proposal revision:

- increments `proposal_version`;
- records changed interfaces and evidence;
- marks old open objections as superseded pending review;
- re-runs all-agent screening;
- reactivates the latest active work cell;
- rejects stale approvals during convergence.

### Verification and finalization

Finalization requires the checks in [`CONVERGENCE_POLICY.md`](CONVERGENCE_POLICY.md). A unanimous but unverified answer remains blocked.

## Information supplied to agents

Agents receive only task-relevant context:

- authoritative mission and current requirements;
- exact proposal/configuration revision;
- relevant design and evidence artifacts;
- domain handbook and role contract;
- allowed tools and output schema;
- prior decisions that remain applicable.

Unrelated competitor dossiers, old revisions and other agents' initial opinions must not contaminate independent analysis.

## Output artifacts

Every run writes:

- `state.json` — complete current structured state;
- `events.ndjson` — append-ordered replay log;
- attendance decision for every agent;
- versioned positions and objections;
- coverage report;
- final decision only after convergence.

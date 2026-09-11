# Design Review Schema

Use this for electrical, mechanical, firmware, software, AI, manufacturing and system design reviews.

## 1. Header

```yaml
design_review_id:
artifact:
revision:
owner_agent:
review_agents: []
requirements_refs: []
interfaces_refs: []
risk_class:
review_type: concept|preliminary|critical|release|change
```

## 2. Review sequence

### A. Intent
- What problem is this design solving?
- What measurable requirements apply?
- What are the dominant constraints?
- What previous decision does this depend on?

### B. Architecture
- Is the partitioning coherent?
- Are interfaces explicit?
- Are hidden dependencies present?
- Is observability/debug access sufficient?
- Is there a simpler architecture with similar performance?

### C. Quantitative margins
For each relevant parameter record:

| Parameter | Requirement | Nominal | Worst case | Margin | Evidence/model |
|---|---:|---:|---:|---:|---|

Examples: voltage, current, noise, bandwidth, timing, memory, RF efficiency, temperature, stress, displacement, latency, inference cost, storage, yield, unit cost.

### D. Failure modes
Ask:

- How can this fail open/short/stuck/slow/intermittent?
- What single-point failures exist?
- What happens at min/max voltage, temperature, tolerance, load and aging?
- What happens during startup/shutdown/brownout/reset/reconnect/update?
- What happens when inputs are malformed or unavailable?
- Can the design fail silently?
- Can a failure damage adjacent systems?

### E. Cross-domain review

Relevant reviewers must address:

- electrical ↔ mechanical;
- PCB ↔ enclosure/antenna/thermal;
- firmware ↔ hardware startup/state;
- AI ↔ deterministic safety layer;
- camera ↔ optics/mechanics/lighting;
- design ↔ test observability;
- design ↔ manufacturing/process capability;
- product ↔ customer value;
- product ↔ security/privacy;
- architecture ↔ cost/schedule.

### F. Manufacturability / testability

- Can it be built repeatedly?
- Are tolerances compatible with process capability?
- Is inspection possible?
- Is rework possible where required?
- Are critical nodes/functions testable?
- Are production tests correlated with engineering tests?

### G. Verification

For every requirement:

```text
requirement → verification method → fixture/tool → data → acceptance criterion
```

Mark verification as analysis, inspection, simulation, test or demonstration.

## 3. Review findings classification

| Severity | Meaning |
|---|---|
| BLOCKER | Violates hard requirement/safety or invalidates architecture. |
| MAJOR | High likelihood of expensive rework or performance failure. |
| MODERATE | Material improvement/risk but not release-blocking yet. |
| MINOR | Cleanup, documentation or low-impact improvement. |
| QUESTION | Missing evidence; not yet a defect. |

Every finding has owner, evidence, proposed resolution and closure criterion.

## 4. Release decision

```yaml
status: approved|approved_with_actions|not_approved
blocking_findings: []
accepted_residual_risks: []
verification_remaining: []
revisit_triggers: []
```

A review is not "passed" because agents agree. It is passed because the design meets stated evidence thresholds and unresolved risks are explicitly accepted.

# Decision Record Template

Use for architecture, component, process, product, AI/model, business and company decisions that should survive beyond a chat/session.

```markdown
# DR-<NNNN> — <Decision title>

**Status:** proposed | accepted | superseded | rejected  
**Date:** YYYY-MM-DD  
**Owner agent:** <ID>  
**Review agents:** <IDs>  
**Risk class:** A | B | C | D

## 1. Decision question
State one precise question.

## 2. Context
What problem, requirement or dependency created the decision?

## 3. Hard constraints
- ...

## 4. Assumptions
- ...

## 5. Evidence
| Evidence ID | Claim / measurement | Source / artifact | Reliability |
|---|---|---|---|

## 6. Options considered
### Option A — ...
Mechanism / architecture:
Pros:
Cons:
Quantitative performance:
Risks:
Verification required:

### Option B — ...
...

### Option C — Status quo / do nothing
...

## 7. Trade matrix
| Criterion | Weight or priority | A | B | C | Notes |
|---|---:|---:|---:|---:|---|

Do not use weighted scoring to override hard constraints or hide incomparable uncertainty.

## 8. Adversarial review
Strongest argument against preferred option:
What would make the preferred option fail?
Which unknown dominates the decision?

## 9. Decision
Selected option:
Why:

## 10. Consequences
Positive:
Negative / debt introduced:
Interfaces affected:
Cost/schedule impact:

## 11. Verification
What evidence must be produced to prove the decision works?

## 12. Residual uncertainty
- ...

## 13. Revisit triggers
Examples: new measurement, vendor EOL, requirement change, failure rate, new model benchmark, customer evidence.

## 14. Linked artifacts
- requirement
- schematic/PCB/CAD/code commit
- simulation
- test data
- review record
```

## Rule

A decision record documents **why the decision was rational given the evidence available at the time**. It is not rewritten to make hindsight look clean. Superseding evidence creates a new record linked to the old one.

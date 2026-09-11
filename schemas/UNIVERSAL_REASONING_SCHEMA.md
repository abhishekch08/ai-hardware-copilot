# Universal Reasoning Schema

This is the common cognitive/execution scaffold for every agent. It is designed to make the virtual company falsifiable, evidence-driven and auditable rather than a collection of role-playing prompts.

## 0. Rule

Do not expose private chain-of-thought verbatim. Persist **decision-relevant reasoning artifacts**: assumptions, equations, evidence, alternatives, experiments, confidence and verification. The goal is reproducibility without relying on hidden internal monologue.

## 1. Task frame

```yaml
task_id: <stable-id>
objective: <single precise outcome>
requester: <user/agent/system>
domain_owner: <agent-id>
risk_class: A|B|C|D
success_criteria:
  - <measurable exit criterion>
constraints:
  hard:
    - <must not violate>
  soft:
    - <preference/tradeoff>
artifacts_in:
  - <path/ref/version>
artifacts_out:
  - <required deliverable>
reviewers:
  - <agent-id>
```

## 2. Problem decomposition

Every consequential task is decomposed into:

1. **What is observed?**
2. **What is expected?**
3. **What is the gap?**
4. **Which variables can causally produce the gap?**
5. **Which variables are controllable or measurable?**
6. **What constraints make some solutions impossible?**
7. **What minimum evidence would justify a decision?**

## 3. Evidence ledger

```markdown
| ID | Type | Claim / observation | Source | Version / condition | Reliability | Notes |
|---|---|---|---|---|---|---|
| E1 | FACT | ... | datasheet ... | rev ... | high | ... |
| E2 | MEASUREMENT | ... | scope capture ... | board rev ... | medium/high | loading ... |
| E3 | ASSUMPTION | ... | inherited | n/a | unknown | test required |
```

No material claim should be allowed to drift from "assumption" into "fact" without evidence.

## 4. First-principles model

Before proposing a solution, write the smallest model that explains the mechanism:

```markdown
Governing law / architecture:
Key state variables:
Dominant parameters:
Expected scaling / directionality:
Boundary conditions:
Units:
Simple sanity-check case:
```

Examples:

- electrical: KCL/KVL, transfer function, impedance, noise, energy/power;
- thermal: energy balance, thermal resistance/capacitance;
- mechanical: force/moment/stress/strain/contact;
- optics: geometry, radiometry, SNR;
- business: unit economics, customer value, conversion funnel;
- statistics: sampling model, uncertainty, causal assumptions.

## 5. Alternatives / competing hypotheses

Never stop at the first plausible answer.

```markdown
| Option/Hypothesis | Mechanism | Supporting evidence | Contradicting evidence | Key unknown | Risk if wrong |
|---|---|---|---|---|---|
```

Minimum expectations:

- design tasks: at least 2 credible alternatives when a real trade-off exists;
- debugging: all materially plausible root-cause families;
- strategic decisions: status quo must be an explicit alternative.

## 6. Quantification

Where applicable include:

- nominal calculation;
- min/max or corner calculation;
- uncertainty/tolerance;
- margin to requirement;
- sensitivity to dominant parameters;
- order-of-magnitude check.

If an answer depends strongly on an unknown parameter, expose that sensitivity instead of choosing a convenient nominal.

## 7. Disconfirmation test

Every recommendation should state:

> What observation would make this recommendation wrong?

Examples:

- measured phase margin below target;
- camera registration residual above allowed probe-position error;
- user study shows no reduction in debug time;
- inference cost destroys gross margin;
- manufacturing Cp/Cpk fails target.

## 8. Next-best-information action

When uncertainty prevents a decision, do not speculate indefinitely. Produce:

```yaml
next_experiment:
  question_resolved: <specific uncertainty>
  procedure: <minimal experiment>
  required_tools: [...]
  controlled_variables: [...]
  measurements: [...]
  predicted_results:
    hypothesis_A: ...
    hypothesis_B: ...
  safety_limits: [...]
  stop_conditions: [...]
  expected_information_gain: high|medium|low
```

## 9. Recommendation contract

A final recommendation contains:

```markdown
Recommendation:
Why this dominates alternatives:
Conditions under which it is valid:
Required implementation controls:
Expected benefit:
Main failure modes:
Verification:
Confidence: 0–1 or Low/Medium/High
Residual unknowns:
Revisit trigger:
```

## 10. Independent verification

Choose at least one:

- independent recalculation;
- simulation;
- unit/integration test;
- second model/agent review;
- direct measurement;
- golden-unit comparison;
- standards/source verification;
- prototype/user experiment.

High-risk decisions require multiple forms where practical.

## 11. Handoff schema

```yaml
handoff:
  from: <agent-id>
  to: <agent-id>
  decision_context: <one paragraph>
  accepted_facts: [...]
  unresolved_questions: [...]
  artifacts: [...]
  constraints: [...]
  requested_work: [...]
  acceptance_criteria: [...]
```

## 12. Completion checklist

- [ ] Objective answered directly.
- [ ] Material assumptions are explicit.
- [ ] Units and quantitative claims checked.
- [ ] Alternatives/hypotheses considered.
- [ ] Counterargument/disconfirmation condition included.
- [ ] Cross-domain interfaces reviewed.
- [ ] Safety/legal constraints addressed where applicable.
- [ ] Verification completed or defined.
- [ ] Confidence and unknowns stated.
- [ ] Artifact/version/source provenance retained.

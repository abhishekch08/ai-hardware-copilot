# Engineering Experiment Loop

This schema is the core of the product and the virtual engineering company.

## 1. State representation

Every debugging/characterization session maintains:

```yaml
system_under_test:
  product:
  board_revision:
  serial_or_unit_id:
  firmware_commit:
  software_version:
  mechanical_revision:
  configuration:
objective:
requirements:
available_tools:
observability:
known_good_reference:
active_hypotheses: []
evidence: []
experiments: []
root_cause_status: unproven|candidate|verified
```

## 2. Loop

```text
OBSERVE
  ↓
NORMALIZE EVIDENCE
  ↓
COMPARE TO EXPECTATION / GOLDEN
  ↓
UPDATE CAUSAL MODEL
  ↓
GENERATE + RANK HYPOTHESES
  ↓
CHOOSE DISCRIMINATING EXPERIMENT
  ↓
SAFETY CHECK
  ↓
EXECUTE / GUIDE HUMAN
  ↓
CAPTURE RAW EVIDENCE + METADATA
  ↓
INTERPRET
  ↓
UPDATE HYPOTHESES
  ↺ until root cause is proven
  ↓
APPLY FIX
  ↓
VERIFY FIX + REGRESSION
  ↓
PERSIST TRAJECTORY
```

## 3. Observation standard

An observation is not just a value. Capture:

- instrument/tool identity;
- calibration status if relevant;
- probe/connection location;
- board state and mode;
- firmware/software revision;
- instrument configuration;
- sampling rate/bandwidth/filtering;
- timestamp or synchronization;
- raw data reference;
- processed metric and processing code/version;
- uncertainty/loading caveats.

## 4. Hypothesis schema

```yaml
hypothesis_id: H<n>
statement: <causal explanation>
mechanism: <why it creates the symptom>
prior_confidence: <0..1 or qualitative>
predictions:
  - condition: ...
    expected_observation: ...
evidence_for: [...]
evidence_against: [...]
confounders: [...]
status: active|weakened|eliminated|verified
```

## 5. Experiment schema

```yaml
experiment_id: X<n>
question: <which uncertainty this resolves>
hypotheses_discriminated: [H1,H2]
procedure:
  - ...
controlled_variables: [...]
changed_variables: [...]
measurements: [...]
expected_results:
  H1: ...
  H2: ...
required_tools: [...]
safety:
  limits: [...]
  stop_conditions: [...]
  approval_required: true|false
cost:
  time:
  money:
  operator_effort:
result:
raw_evidence: [...]
interpretation:
```

## 6. Experiment ranking

Candidate experiments should be ranked using a utility function, conceptually:

\[
U(X)=w_I I(X)+w_C C(X)-w_R R(X)-w_T T(X)-w_M M(X)-w_O O(X)
\]

where:

- \(I\) = expected information gain / hypothesis separation;
- \(C\) = requirement or coverage value;
- \(R\) = risk of damage/hazard;
- \(T\) = time;
- \(M\) = monetary cost;
- \(O\) = operator burden.

Weights are task-dependent and must not hide hard safety limits. Unsafe experiments are rejected, not merely assigned a low score.

## 7. Root-cause proof standard

A candidate cause is **verified** only when evidence supports causality, not merely correlation. Prefer one or more of:

1. removing/correcting the cause removes the symptom;
2. deliberately reintroducing the cause reproduces the symptom when safe;
3. causal mechanism predicts quantitative observations that match measurement;
4. independent measurements eliminate credible alternatives;
5. golden/failing-unit comparison isolates the same mechanism.

## 8. Fix verification

After applying a fix:

- repeat the original failing test;
- repeat relevant neighboring/corner cases;
- check for new regressions;
- compare against requirement and golden data;
- record before/after evidence;
- update design/FMEA/knowledge graph if the failure can recur elsewhere.

## 9. Training/evaluation trajectory

Persist every useful trajectory, including failed paths:

```text
context → symptom → hypotheses → selected experiment → evidence → belief update → ... → root cause → fix → verification
```

Failed hypotheses are valuable: they teach the future system which experiments were wasteful and why.

## 10. Example: 4 mA regression

```text
Symptom: Rev B draws +4 mA vs Rev A in idle.

H1: firmware peripheral unintentionally active
H2: regulator quiescent-current change
H3: pull-up/pulldown population difference
H4: sensor not entering low-power mode
H5: leakage/assembly defect
H6: measurement configuration mismatch

First actions should not be random probing. Verify measurement comparability, diff design/BOM/firmware, then select measurements that partition these hypotheses—for example rail-by-rail current or controlled peripheral isolation—subject to available observability and safety.
```

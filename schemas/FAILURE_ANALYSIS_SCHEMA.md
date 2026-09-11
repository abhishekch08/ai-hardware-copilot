# Failure Analysis Schema

Use this schema for board, firmware, software, mechanical, manufacturing, AI-agent and system failures.

## 1. Failure definition

```yaml
failure_id:
system:
revision:
unit_id:
observed_symptom:
expected_behavior:
first_seen:
reproducibility: always|intermittent|unknown
severity:
containment_required:
```

Do not begin with a presumed cause. Define the symptom in measurable terms.

## 2. Reproduction control

Record:

- exact unit/build/firmware/software/model versions;
- environmental conditions;
- fixture/instrument configuration;
- input stimulus and timing;
- frequency of occurrence;
- golden/reference unit behavior;
- whether the failure survives reboot/power cycle/reassembly/reflash.

## 3. Immediate containment

Before root-cause work, determine whether to:

- stop testing to prevent damage;
- quarantine units/builds;
- freeze a software/model release;
- preserve failing evidence;
- capture volatile logs/registers/state;
- prohibit changes that could destroy the failure signature.

## 4. Fault-tree decomposition

Start from functional blocks rather than components.

Example electrical decomposition:

```text
SYSTEM FAILS TO BOOT
├── input power absent/invalid
├── power conversion invalid
├── sequencing/reset invalid
├── clock invalid
├── MCU silicon/electrical issue
├── boot configuration issue
├── firmware image/startup issue
├── peripheral holds bus/reset/rail
└── measurement/observation itself wrong
```

Only descend to components once evidence narrows the block.

## 5. Hypothesis table

| ID | Hypothesis | Causal mechanism | Prior basis | Evidence for | Evidence against | Predicted signature | Next discriminating test | Status |
|---|---|---|---|---|---|---|---|---|

## 6. Golden-vs-failing comparison

Where possible compare:

- BOM/population;
- schematic/PCB revision;
- firmware/software commits;
- configuration/nonvolatile state;
- current by rail/state;
- startup waveforms;
- clocks/resets;
- interface traffic;
- temperatures;
- mechanical assembly/tolerances;
- manufacturing lot/process data;
- agent/model/tool versions.

Change only one causal variable at a time unless intentionally running DOE.

## 7. Measurement validity gate

Before trusting surprising data ask:

- instrument accuracy/resolution/bandwidth sufficient?
- probe/loading changes circuit behavior?
- reference/ground correct?
- aliasing/filtering/averaging present?
- common-mode range respected?
- trigger/synchronization correct?
- calibration/zeroing required?
- processed value traceable to raw data?

TEST-04 Metrology Agent reviews measurements that drive major conclusions.

## 8. Root cause levels

Distinguish:

1. **Physical/technical cause** — e.g. insufficient pull-up current, via crack, firmware race.
2. **Design/process cause** — e.g. wrong constraint, missing tolerance analysis, uncontrolled dispense.
3. **Detection escape** — why validation/production test/review failed to catch it.
4. **Systemic cause** — what process/tool/agent memory should change to prevent recurrence.

A complete RCA should address all four where applicable.

## 9. Root-cause proof

Required fields:

```yaml
root_cause_candidate:
mechanism:
proof_evidence:
alternatives_eliminated:
fix:
fix_verification:
regression_results:
confidence:
```

Correlation alone is insufficient.

## 10. Corrective and preventive actions

Possible outputs:

- design change;
- firmware/software change;
- component/process change;
- test coverage update;
- fixture/calibration update;
- FMEA update;
- supplier corrective action;
- agent rule/tool guardrail;
- retrieval/knowledge update;
- requirement clarification;
- documentation/training update.

## 11. Final report template

```markdown
# Failure Analysis — <ID>

## Executive summary
## Failure signature
## Affected configurations
## Reproduction procedure
## Evidence timeline
## Hypotheses considered
## Experiments performed
## Root cause and causal proof
## Fix
## Verification / regression
## Why previous controls missed it
## Preventive actions
## Remaining risk
## Linked raw artifacts
```

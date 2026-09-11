# Bootstrap Plan — First 30 Days

## Objective

Stand up the minimum AI-native engineering organization and prove one closed-loop debugging workflow before expanding breadth.

The first month should produce evidence that the architecture can ingest a design, understand a board, control a limited lab stack, reason over measurements and produce a correct traceable root-cause report.

**Current checkpoint:** the software foundation spans parts of Weeks 1–3. All 184 roles compile; conference screening/iteration/fail-closed convergence, model routing/reference gateway, content-addressed evidence, narrow KiCad/BOM/firmware ingestion, typed instrument safety, a seeded closed-loop diagnostic simulation, durable job service, container packaging and CI are implemented and tested. These are alpha capabilities: real instruments, physical perception, live-model benchmarks and bench/customer proof remain unvalidated.

---

## Week 1 — Company runtime and design ingestion

### Deliverables
- [x] Convert all 184 synchronized registry entries into machine-readable configs.
- [x] Package constitution + schema + domain handbook + agent contract for the external model gateway.
- [x] Load the authoritative product-mission file for each active agent; keep optional industry intelligence task-routed.
- [x] Implement the first task router, consequence tiers, mandatory review rules and dependency expansion.
- [x] Implement immutable content/configuration-addressed evidence, derivation lineage, integrity verification and explicit claim assessment records.
- [x] Create a normalized project manifest and reference KiCad/firmware fixture.
- [x] Parse a narrow KiCad schematic/PCB subset and CSV BOM; preserve every source as evidence.
- [x] Index firmware symbols and verify an explicitly supplied Git revision.
- [ ] Complete schematic pin/net connectivity, requirements/datasheet links and component-pin-net-location-source graph queries.

### Exit criteria
An agent can answer, with provenance:

- What powers U7?
- Which components load 1V8_SYS?
- Where is TP17 on the board?
- Which MCU pin controls regulator enable?
- Which firmware symbol/configuration relates to that pin?

---

## Week 2 — Instrument layer and evidence capture

### Deliverables
- [x] Implement generic typed SCPI PSU, DMM and ASCII-waveform oscilloscope adapters behind test transports.
- [ ] Qualify one exact oscilloscope, PSU and DMM model on real hardware with conformance fixtures.
- Support serial logs.
- Support one JTAG/SWD flow.
- [x] Typed instrument abstraction with deterministic operating limits and exact-action approval.
- [x] Session/action/result metadata captured as content-addressed evidence.
- [x] Bounded ASCII waveform acquisition path; binary blocks and plotting remain.
- Golden-trace comparison prototype.
- Desktop UI skeleton for project, board revision, instruments, experiment timeline and evidence.

### Exit criteria
From software, the system can safely:

1. discover connected supported instruments;
2. configure a benign acquisition;
3. capture waveform/voltage/current evidence;
4. associate it with a named net/test condition;
5. store complete metadata;
6. replay the acquisition setup.

---

## Week 3 — Closed-loop debugging intelligence

### Deliverables
- [x] Hypothesis objects, Bayesian updates and ranking.
- Fault-tree generation from design graph.
- [x] Expected-information-gain/cost experiment planner for the seeded benchmark.
- Protocol/waveform interpretation.
- Golden-unit/revision comparison.
- [x] Independent critic/reviewer conference gates.
- [ ] Integrate diagnosis state, experiment execution and verified-fix report into one real bench loop.

### Build a seeded fault bench
Create known faults such as:

- wrong load resistor;
- missing capacitor;
- rail short/leakage;
- incorrect pull-up;
- regulator enable timing issue;
- firmware pin-state regression;
- I2C address/configuration error;
- SPI timing mismatch;
- excess sleep current;
- slow rail ramp.

### Exit criteria
For at least five seeded faults, the system must:

```text
observe symptom
 -> create multiple hypotheses
 -> choose next measurement
 -> collect/accept evidence
 -> update hypotheses
 -> identify root cause
 -> propose fix
 -> verify fix
```

Track time-to-root-cause and unnecessary experiments.

---

## Week 4 — Probe-aware perception + reliability benchmark

### Deliverables
- Camera calibration.
- Board identification/revision selection.
- PCB image to CAD registration.
- Component/test-point overlays.
- Probe-tip detection prototype.
- Spatial uncertainty estimate.
- Correct-node verification before capture.
- Agent benchmark harness.
- Security threat model for design data and physical tool control.

### Exit criteria
For a reference PCB under controlled bench conditions:

- locate board pose;
- overlay known components/test points;
- guide to at least a set of large/accessible test points;
- recognize when localization confidence is insufficient;
- associate measured evidence with the correct net.

Do not require 0201-level passive recognition for the first proof.

---

# Metrics for the first month

| Metric | Why it matters |
|---|---|
| Root-cause accuracy | Core product outcome |
| Median time-to-root-cause | Customer ROI |
| Experiments-to-root-cause | Quality of planning |
| Unnecessary experiment count | Agent efficiency |
| Unsafe tool proposals | Safety |
| Measurement metadata completeness | Reproducibility |
| Correct net/probe association | Physical intelligence |
| Engineer interventions | Autonomy |
| False-hypothesis persistence | Reasoning quality |
| Report traceability | Enterprise usefulness |
| Model cost per debug session | Economic viability |

---

# What not to build in the first month

- custom glasses;
- custom optics;
- robotic probe arms;
- support for every scope vendor;
- every EDA format;
- full PLM integration;
- broad mobile apps;
- manufacturing automation;
- custom foundation-model training.

All are legitimate later areas, but none is required to validate the core causal debugging loop.

---

# Founder operating cadence

Use the agent organization to run four repeated reviews:

### Product review
Is the work reducing a real debugging pain and is the metric improving?

### Architecture review
Are interfaces and data structures converging or accumulating one-off hacks?

### Evidence review
Which claims are measured versus merely plausible?

### Risk review
What can make the product unusable: accuracy, safety, latency, privacy, integration burden, or weak ROI?

---

# 30-day success definition

A convincing first milestone is not a polished UI. It is a recorded demonstration such as:

> "Board Rev B draws 4 mA more in sleep than Rev A. The agent ingests both revisions and firmware commits, proposes likely causes, controls/requests measurements, isolates the additional current to one subsystem/state, identifies the responsible change, verifies the fix, and produces a fully traceable report."

That demonstration would validate the central company thesis far more strongly than building custom wearable hardware early.

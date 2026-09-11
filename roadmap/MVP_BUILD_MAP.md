# MVP Build Map — AI Hardware Engineer / Lab Copilot

## Product wedge

> Reduce time-to-root-cause during first-board bring-up and power / communication debugging.

The MVP should prove the **intelligence + tool loop** before any custom wearable hardware.

## 1. User scenario

Engineer provides:

- schematic/PCB/BOM;
- firmware repository;
- board revision and symptom;
- connected supported instruments;
- optional golden-unit data;
- bench camera if visual guidance is enabled.

The system should:

1. ingest and normalize design context;
2. establish expected system behavior;
3. verify current test state;
4. generate competing hypotheses;
5. choose the most informative safe experiment;
6. configure instruments;
7. guide any manual probing;
8. capture raw evidence with metadata;
9. update hypothesis ranking;
10. repeat until root cause is sufficiently proven;
11. recommend/implement an approved fix where possible;
12. run verification/regression;
13. generate a complete RCA report.

## 2. MVP subsystems

### A. Engineering context ingestion

Support initially:

- one ECAD flow, preferably KiCad or Altium;
- PDF/datasheet ingestion;
- Git repositories;
- BOM CSV/XLSX;
- plain requirements/test documents.

Normalized objects:

```text
Board
Component
Pin
Net
Power rail
Interface
Test point
Requirement
Firmware symbol
Commit
Instrument
Measurement
Experiment
Hypothesis
Failure
Fix
```

### B. Engineering knowledge graph

Relationships include:

```text
component CONNECTED_TO net
component LOCATED_AT pcb_xy
component IMPLEMENTS function
component DOCUMENTED_BY datasheet
net POWERED_BY regulator
firmware_symbol CONTROLS pin
requirement VERIFIED_BY test
measurement OBSERVES net
experiment TESTS hypothesis
hypothesis EXPLAINS symptom
fix RESOLVES failure
```

### C. Instrument layer

Initial support should be intentionally narrow:

- 1–2 oscilloscope families;
- SCPI PSU;
- SCPI DMM;
- serial/UART;
- JTAG/SWD;
- optionally Saleae-class logic analyzer.

Every capability uses typed commands with deterministic limits.

### D. Agent core

Minimum runtime modules:

```text
Task Router
Context Builder
Domain Specialist
Hypothesis Engine
Experiment Planner
Safety Policy
Tool Executor
Evidence Interpreter
Critic
Report Generator
```

### E. Desktop engineering UI

Required surfaces:

- session objective/state;
- schematic/PCB cross-probe;
- current hypotheses and confidence;
- proposed next experiment and rationale;
- instrument status;
- waveform/evidence viewer;
- experiment timeline;
- approval prompt for risky actions;
- root-cause report;
- raw artifact access.

### F. Evaluation harness

Create physical or simulated fault cases covering at least:

- missing rail;
- wrong rail voltage;
- slow startup;
- excess idle current;
- reset held low;
- bad clock;
- I2C pull-up/configuration issue;
- I2C address conflict;
- SPI polarity/phase/timing issue;
- firmware peripheral not entering sleep;
- wrong component value;
- missing component;
- short/open/intermittent;
- bad solder joint;
- golden-vs-new-revision regression.

## 3. Suggested software architecture

```text
┌──────────────────────────────────────────────────────┐
│ Desktop / Web Engineering Workspace                 │
└───────────────┬──────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────┐
│ Session / Agent Orchestrator                        │
│ task state • permissions • evidence • audit         │
└──────┬──────────────┬───────────────┬────────────────┘
       │              │               │
       ▼              ▼               ▼
 Context Engine   Reasoning Core   Tool Gateway
       │              │               │
 EDA/Git/RAG     hypotheses/plan    typed actions
       │              │               │
       ▼              ▼               ▼
 Knowledge       Model Router      Instruments/JTAG
 Graph           + Specialists     /Serial/Camera
       │              │               │
       └──────────────┴───────────────┘
                      │
                      ▼
                Evidence Store
                      │
                      ▼
                  Evaluation
```

## 4. Milestone sequence

### M0 — Static engineering intelligence
Can ingest a design and answer exact, source-backed questions about components/nets/pins/firmware relationships.

### M1 — Instrument-aware assistant
Can discover/configure supported instruments and record structured measurements safely.

### M2 — Hypothesis-driven debugger
Can maintain explicit hypotheses and recommend information-efficient experiments.

### M3 — Closed-loop bench agent
Can execute approved instrument actions, incorporate evidence and iterate without the user manually re-prompting every step.

### M4 — Probe-aware camera MVP
Can register PCB view, identify target nodes and guide manual probing with quantified uncertainty.

### M5 — Customer proof-of-value
Can beat baseline debugging workflow on real customer/partner cases on time-to-diagnosis and evidence completeness.

## 5. Metrics

### Diagnosis quality
- correct root-cause rate;
- top-k hypothesis recall;
- false-root-cause rate;
- experiments-to-root-cause;
- time-to-root-cause.

### Autonomy
- tool calls requiring correction;
- human interventions/session;
- fraction of session executed automatically;
- rollback/recovery success.

### Safety
- unsafe command proposal rate;
- unsafe command execution rate (target effectively zero through guardrails);
- wrong-node probe guidance rate;
- policy violations.

### Perception
- board/revision identification accuracy;
- registration error;
- component/pad localization accuracy;
- probe-tip localization error.

### Product value
- senior engineer minutes saved;
- repeat-failure reduction;
- report creation time saved;
- avoided board spins/rework where demonstrable;
- weekly active engineering sessions;
- expansion of supported workflows.

## 6. What not to build first

Do not initially spend major effort on:

- custom smart glasses;
- custom optics/display;
- robot arm probing;
- broad support for every instrument vendor;
- every ECAD platform;
- autonomous hardware modifications;
- a generic company-wide AI assistant.

These are expansion paths, not proof of the core thesis.

## 7. Strongest falsification test for the company thesis

If experienced hardware engineers consistently complete representative bring-up/debug tasks faster and with equal-or-better evidence quality **without** the product after reasonable onboarding, the core value proposition is not yet proven. More features or a wearable UI should not be used to hide that failure.

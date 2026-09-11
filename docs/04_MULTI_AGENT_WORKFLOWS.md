# Multi-Agent Workflows

This document defines how the flat specialist network collaborates on real work. Agents are pulled in by dependency and failure risk, not by organizational ritual.

## Workflow 1 — Product requirement → system architecture

```text
Customer/market evidence
   ↓ PROD-03 + MKT-01 + APP-01
Problem statement / ROI hypothesis
   ↓ PROD-01 + PROD-02
Measurable requirements
   ↓ SYS-02
System alternatives
   ↓ SYS-01 + SYS-04
Domain feasibility reviews
   ↓ EE / EMB / AI / ME / TEST / SEC / MFG
Architecture decision record
   ↓ META-04 critic + META-05 evidence audit
Baselined system architecture
```

### Outputs
- customer problem evidence;
- product requirement document;
- system requirements and traceability;
- block architecture;
- interface definitions;
- technical trade study;
- risk register;
- verification strategy.

## Workflow 2 — Electrical board design

```text
SYS requirements
 ↓
EE-07 schematic owner
 ├─ EE-01 analog
 ├─ EE-02 power
 ├─ EE-04 digital
 ├─ EE-09/10 RF/antenna
 ├─ EE-11 sensors
 ├─ EE-15 components
 ├─ EMB-01 firmware interface
 └─ TEST-01/11 debug + production test access
 ↓
EE-14 simulation + corner analysis
 ↓
EE-08 PCB placement/routing
 ├─ EE-05 SI
 ├─ EE-06 PI
 ├─ TEST-08 EMC
 ├─ ME-01 mechanics
 ├─ ME-03 thermal
 └─ MFG-02 PCBA DFM
 ↓
Design review schema
 ↓
Fabrication package + bring-up plan
```

### Required AI-era addition
AI-22 EDA File Intelligence ingests the same native ECAD source so the future Lab Copilot can reason over components, nets, test points and geometry. Debug observability is designed in, not retrofitted.

## Workflow 3 — Firmware feature

```text
Requirement
 ↓ EMB-01 architecture
Interface review ↔ EE-04 / SYS-03
 ↓
EMB-02 implementation
 ↓
Static analysis + unit tests
 ↓
EMB-04 timing/concurrency review if real-time
 ↓
EMB-03 debug/trace instrumentation
 ↓
TEST-12 software verification
 ↓
Hardware-in-loop / real board
 ↓
Release artifact + telemetry hooks
```

Security-sensitive code additionally requires SEC-01/03 review.

## Workflow 4 — Instrument integration

```text
Instrument capability/source docs
 ↓ EMB-06
Typed vendor-neutral capability model
 ↓
Driver + simulator/mock
 ↓
Safety envelope / range validation
 ↓ TEST-04 + TEST-09
Integration tests on real instrument
 ↓ EMB-07
Session logging + metadata
 ↓ AI-16 backend + AI-17 desktop
Agent tool contract
 ↓ AI-01
Adversarial unsafe-command tests
 ↓ META-04 + SEC-04
```

The LLM never sends unrestricted raw SCPI directly to hardware. It requests typed actions enforced by deterministic limits.

## Workflow 5 — PCB scene understanding and probe guidance

```text
Native PCB/CAD
 ↓ AI-22 EDA parser
Normalized geometry/net graph
 ↓ AI-11 knowledge graph
Camera calibration
 ↓ AI-05 + ME-09
CAD ↔ image registration
 ↓ AI-06
Component/pad/testpoint localization
 ↓
Probe-tip tracking
 ↓ AI-07
Target net selection
 ↓ domain debug agent
Safety / electrical limits
 ↓ TEST-09 + EE relevant domain
Human guidance / future robotic motion
 ↓
Contact verification + instrument capture
 ↓ EMB-06
Evidence attached to exact net/state
```

### Critical metrics
- registration error in mm/pixels;
- target-node identification accuracy;
- probe-tip error;
- wrong-node guidance rate;
- occlusion/glare robustness;
- time-to-correct-node;
- unsafe guidance rate.

## Workflow 6 — Closed-loop board debugging

```text
Objective / symptom
 ↓ META-01 routes specialists
State verification
 ↓ TEST-01 + EMB-03 + EMB-06
Design context retrieval
 ↓ AI-22 + AI-11 + AI-12
Domain causal model
 ↓ relevant EE/EMB agent
Hypothesis set
 ↓ AI-08 + TEST-05
Candidate experiments
 ↓ AI-09
Measurement validity
 ↓ TEST-04
Safety gate
 ↓ TEST-09
Experiment execution
 ↓ EMB-06/07 + human probe/CV guidance
Raw evidence
 ↓ AI-10 + domain agent
Belief update
 ↺
Root cause candidate
 ↓ META-04 adversarial test
Fix
 ↓ design owner
Verification/regression
 ↓ TEST-02/03/12
RCA report
 ↓ DOC-01 + META-05
Knowledge graph update
```

## Workflow 7 — Customer wearable or other compact physical product

```text
Product + system requirements
 ↓ ME-01 mechanical architecture
Human interaction constraints
 ↓ ME-07 + ME-08
Form concepts
 ↓ ME-05 industrial design
Materials + appearance
 ↓ ME-04 + ME-06
Thermal/RF/camera/electrical interfaces
 ↓ ME-03 + EE-09/10 + ME-09 + EE-08
Tolerance stack
 ↓ ME-02
Manufacturing process
 ↓ MFG-03/04/05
Prototype
 ↓
Mechanical/environmental verification
 ↓ TEST-03/06
```

This workflow supports wearable customer programs, reference designs and other compact physical systems. Custom Lab Copilot glasses enter it only after an existing camera/glasses baseline is proven to be a product bottleneck.

## Workflow 8 — Optional XR / hands-free Lab Copilot interface

```text
Observed bench-workflow bottleneck + baseline metrics
 ↓ PROD-02 + APP-01 + ME-08
Commercial device/camera capability audit
 ↓ XR-01 + XR-08 + SEC-02/05
Go/no-go requirements and comparison protocol
 ↓ SYS-02 + XR-09
Spatial architecture and frame/error budget
 ↓ XR-03 + AI-06/07 + TEST-04
Interaction and failure-safe behavior
 ↓ XR-04 + TEST-09
Device/runtime/optics path as required
 ↓ XR-02/05/06/07
Bench trial against desktop/camera baseline
 ↓ XR-09 + AI-13 + PROD-02
Decision: use commercial hardware, defer XR, or justify custom interface
 ↓ SYS-04 + PROD-01 + FIN-02
```

The decision metric is engineering workflow value—correct-node rate, task time, interventions, comfort, latency, security and total deployment burden—not novelty or visual polish.

## Workflow 9 — AI capability development

```text
User task definition
 ↓ PROD-02
Benchmark/eval definition BEFORE optimization
 ↓ AI-13 + domain expert
Dataset/evidence
 ↓ AI-14
Baseline model/tool pipeline
 ↓ AI-01/02 + domain expert
Implementation
 ↓ AI/Software agents
Red-team failures
 ↓ META-04 + SEC-04
Benchmark
 ↓ AI-13
Error taxonomy
 ↓
Targeted model/tool/data changes
 ↺
Deployment
 ↓ AI-15
Production telemetry
 ↓ AI-25 + META-06
Routing/model update
```

A demo is not an eval. No AI capability is considered production-ready without an explicit benchmark and failure taxonomy.

## Workflow 10 — Manufacturing transition

```text
Released design
 ↓ SYS-05 config control
DFM/DFA
 ↓ MFG-01/02/03/04
Process windows
 ↓ MFG-05
Supplier qualification
 ↓ MFG-06/07
Production test
 ↓ TEST-11 + EMB-10
Pilot build
 ↓
Yield/process data
 ↓ MFG-10 + TEST-10
Failure analysis
 ↓ TEST-05
Corrective actions
 ↺
Production release
```

## Workflow 11 — Customer proof-of-value

```text
Target account workflow
 ↓ SALES-01 + APP-01
Baseline debugging task + time
 ↓ PROD-02 + AI-13
Integration plan
 ↓ APP-02 + SEC-02
Run customer cases
 ↓ Lab Copilot
Measure:
  time-to-root-cause
  experiments
  engineer interventions
  correct root cause
  unsafe proposals
  report completeness
 ↓ AI-25
ROI calculation
 ↓ FIN-02
Product gaps
 ↓ PROD-01 + engineering agents
```

## Workflow 12 — Patent / invention handling

```text
Potential novel technique
 ↓ domain engineering agent
Technical invention disclosure
 ↓ LEG-02
Prior-art landscape
 ↓ LEG-02/03 + SCI-01
Inventor/engineering validation
 ↓
External patent counsel where appropriate
 ↓
Filing decision
 ↓ BIZ-01 + FIN-01 + LEG-02
```

The agent can research and prepare technical material; formal legal opinions and filing representation should use qualified counsel as required.

## Workflow 13 — Critical release gate

Before a major customer/product release:

- SYS-02: requirements status;
- TEST-03/12: verification status;
- AI-13: AI benchmark regression;
- SEC-01/02/03/04: security status;
- GOV-01: unresolved risk;
- DOC-01: user/admin docs;
- PROD-01: product acceptance;
- META-05: evidence/provenance audit;
- META-04: adversarial final review.

The release is evidence-based, not consensus-based.

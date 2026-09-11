# Agent Deployment Sequence

The company contains many specialist agents, but the product should not start by running all of them continuously. Deploy agents in the order that reduces the largest product risk.

## Phase 0 — Company kernel

Deploy first:

- META-01 Task Decomposition & Agent Routing
- META-02 Model Router & Difficulty Controller
- META-04 Independent Critic
- META-05 Evidence & Provenance Auditor
- META-07 Repository / Artifact Librarian
- SYS-01 System Architecture
- SYS-02 Requirements Engineering
- PROD-01 Product Management
- PROD-02 Hardware Workflow Product

### Exit criteria

- every task has owner/reviewer/verifier roles;
- reasoning and decision schemas are enforced;
- repo artifacts are canonical/versioned;
- model routing is measurable rather than ad hoc.

## Phase 1 — Desktop hardware-debugging core

Deploy:

- EE-01 Analog/Mixed-Signal
- EE-02 Power Electronics/PMIC
- EE-04 Digital Electronics
- EE-07 Schematic
- EE-08 PCB Layout/ECAD
- EMB-01 Firmware Architecture
- EMB-03 Firmware Debug/JTAG
- EMB-06 Instrument Control/SCPI
- EMB-07 Lab Automation
- AI-01 Agent Architecture
- AI-08 Scientific Reasoning/Hypothesis
- AI-09 Active Experiment Planning
- AI-10 Waveform Intelligence
- AI-11 Engineering Knowledge Graph
- AI-12 Technical Retrieval
- AI-13 Evaluation/Benchmark
- AI-16 Backend Platform
- AI-17 Desktop Application
- AI-22 EDA File Intelligence
- TEST-01 Bring-Up
- TEST-04 Metrology
- TEST-05 Failure Analysis
- TEST-09 Safety
- DOC-01 Documentation
- SEC-01 Product Security

### Target capability

Given design files, firmware repo, instrument access and a stated symptom, the system can construct a structured investigation, control supported tools, capture evidence and narrow/verify root cause with human-guided probing.

### Exit criteria

- benchmark suite contains representative power/boot/interface faults;
- root-cause accuracy materially exceeds generic LLM checklist performance;
- all instrument writes pass deterministic safety policy;
- every experiment is replayable from captured metadata;
- user can finish a debug session with a defensible evidence report.

## Phase 2 — Physical-scene intelligence

Add:

- AI-04 Multimodal Intelligence
- AI-05 Computer Vision/Spatial Perception
- AI-06 CAD-to-Camera Registration
- AI-07 Probe Tracking & Guidance
- ME-09 Opto-Mechanical/Camera Hardware
- AI-23 Engineering Visualization
- ME-08 Human Factors

Keep **XR-01 XR/AR/VR Systems Engineering** callable in this phase to review hands-free workflow and commercial-device feasibility. It is an interface reviewer, not a custom-hardware workstream.

### Exit criteria

- camera is reliably registered to known board revision;
- component/test-point identification meets benchmark threshold;
- probe guidance has quantified spatial error and wrong-node rate;
- visual uncertainty gates measurements rather than faking certainty.

## Phase 3 — Broader engineering depth

Add as supported customer cases demand:

- SI/PI, RF/antenna, sensors, optics, haptics;
- FPGA/clocking;
- thermal/mechanical/materials;
- real-time/connectivity firmware;
- reliability, EMC, production test;
- manufacturing/NPI and supply-chain agents.

### Exit criteria

The product can move from bring-up debugging into characterization, validation and failure analysis without losing evidence traceability.

## Phase 4 — Enterprise deployment

Add:

- SEC-02 Enterprise Security/On-Prem
- SEC-03 Application Security
- SEC-04 AI Security/Prompt Injection
- SEC-05 Privacy
- INFRA-01 Cloud/DevOps/SRE
- INFRA-02 Local/Edge Compute
- APP-02 Solutions Architecture
- LEG/REG/GOV agents

### Exit criteria

- offline/on-prem deployment supported where required;
- SSO/RBAC/audit/data-retention controls exist;
- customer design IP boundaries are enforceable;
- deployment passes internal threat model and enterprise security review.

## Phase 5 — Manufacturing and lifecycle

Add MFG/TEST/quality/supplier agents to support:

- design-for-test feedback;
- automated production failure diagnosis;
- yield analytics;
- field-return RCA;
- process/supplier learning loops.

## Phase 6 — Custom physical interface only if evidence requires it

Only after proving a software/camera-based product bottleneck, deploy deeper custom-hardware agents for:

- custom wearable/glasses;
- XR-01 systems architecture and XR-02 optics/display;
- XR-03 spatial tracking/calibration and XR-04 spatial interaction;
- XR-05 head-worn sensing hardware and XR-06 runtime/platform integration;
- XR-07 ergonomics, XR-08 industrial workflow and XR-09 metrology/verification;
- low-power wearable electronics;
- custom camera/lighting;
- industrial design/CMF;
- battery/thermal/RF packaging;
- future robotic manipulation.

A custom wearable is justified only if it materially improves metrics such as task completion time, view quality, hands-free usability, latency, privacy or ergonomics enough to offset hardware complexity.

## Principle

Deploying an agent means more than writing its prompt. It requires:

1. a role contract;
2. scoped tools;
3. trusted context sources;
4. output schema;
5. benchmark/eval cases;
6. escalation rules;
7. artifact persistence;
8. known failure modes.

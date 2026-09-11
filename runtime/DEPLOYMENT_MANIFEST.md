# Deployment Manifest

## Purpose

This manifest defines the **initial active agent set** and the larger callable specialist pool. It is not an organization chart. All agents remain peers; the active set simply reflects the first product wedge.

---

## 1. Initial always-available core

These agents should be deployable from day one because most tasks will touch them.

| Agent | Default mode | Why active initially |
|---|---|---|
| SYS-01 System Architecture | deep reasoning | Cross-domain decomposition and interfaces |
| SYS-02 Requirements | standard/deep | Converts goals into measurable targets |
| SYS-03 Integration | deep | Prevents HW/FW/SW/mech interface drift |
| PROD-01 Product Management | deep | Keeps product tied to user value |
| PROD-02 Hardware Workflow Product | deep | Encodes real bench workflow |
| SYS-05 Configuration & Change Control | standard | Prevents revision confusion |
| EE-01 Analog/Mixed-Signal | deep | Core hardware design/debug |
| EE-02 Power/PMIC | deep | Bring-up/power faults are common |
| EE-04 Digital Electronics | deep | Reset/clock/interface/logic issues |
| EE-07 Schematic | standard/deep | Design understanding/review |
| EE-08 PCB/ECAD | deep | Layout, test point and physical context |
| EE-11 Sensors | deep | Broad sensor workflows |
| EE-14 Circuit Simulation | tool-heavy | Independent circuit evidence |
| EMB-01 Firmware Architecture | deep | HW/FW state understanding |
| EMB-03 Firmware Debug/JTAG | deep/tool-heavy | Root-cause workflows |
| EMB-06 Instrument Control/SCPI | deterministic/tool-heavy | Bench control layer |
| EMB-07 Lab Automation | standard/deep | Repeatable experiments |
| EMB-08 Protocol Analysis | deep/tool-heavy | I2C/SPI/UART/CAN diagnosis |
| AI-01 Agent Architecture | deep | Runtime and tool orchestration |
| AI-02 LLM/Foundation Model | deep | Model capability expertise |
| AI-03 Model Router | standard/deep | Compute/model selection |
| AI-04 Multimodal Intelligence | deep | Schematics/images/waveforms |
| AI-05 Computer Vision | deep | Physical scene understanding |
| AI-06 CAD-to-Camera Registration | deep | Core probe-aware differentiator |
| AI-07 Probe Tracking | deep | Core probe-aware differentiator |
| AI-08 Hypothesis Reasoning | deep | Causal debugging |
| AI-09 Experiment Planning | deep | Next-best-test selection |
| AI-10 Waveform/DSP | deep/tool-heavy | Instrument evidence interpretation |
| AI-11 Knowledge Graph | deep | Cross-file engineering context |
| AI-12 Technical Retrieval | standard/deep | Datasheets/design/source grounding |
| AI-13 AI Evaluation | deep | Reliability measurement |
| AI-16 Backend Platform | deep/code | Product runtime |
| AI-17 Desktop Application | deep/code | Primary bench application |
| AI-18 Web Frontend | standard/deep code | Engineering UI/admin/reporting |
| AI-21 Developer Tools/SDK | deep/code | Instrument/plugin ecosystem |
| AI-22 EDA File Intelligence | deep/code | Design graph/geometry parsing |
| Test/Validation core | deep/tool-heavy | Prove system behavior |
| Metrology core | deep | Avoid false measurement conclusions |
| Failure Analysis core | deep | Structured RCA |
| Security/AI Security core | deep | Enterprise/IP/tool safety |
| Technical Documentation | standard | Traceable artifacts |

---

## 2. On-demand engineering specialists

Activate when task tags require them:

- Battery/BMS/charging
- High-speed digital/SI
- Power integrity
- RF/wireless
- Antenna
- Optoelectronics/photonics
- Acoustics/haptics
- FPGA/RTL
- Clock/timing
- Protection/ESD
- CAD library
- Mechanical architecture
- Thermal
- Structural/FEA
- Tolerance/GD&T
- Industrial design
- CMF
- Human factors/ergonomics
- Wearable integration
- Optical/mechatronic integration
- Reliability/qualification
- EMC/EMI
- Regulatory/compliance
- Safety engineering
- Calibration
- Production test
- Quality/FMEA

### XR / AR / VR specialists available from day one

- **XR-01 XR/AR/VR Systems Engineering** is deployed as the default on-demand owner for hands-free bench-interface feasibility and cross-domain XR architecture.
- **XR-02 Display Optics**, **XR-03 Spatial Tracking**, **XR-04 Spatial Interaction**, **XR-05 Head-Worn Sensor Hardware**, **XR-06 XR Runtime**, **XR-07 Head-Worn Ergonomics**, **XR-08 Industrial AR Workflow**, and **XR-09 XR Verification** are activated by the specific interface or evidence risk.
- Their first responsibility is to evaluate commercial hardware and prove workflow value. They do not initiate a custom-glasses program without the Phase 6 evidence gate.

---

## 3. On-demand manufacturing and operations specialists

- DFM/DFA
- NPI
- PCB fabrication/PCBA process
- Plastics/molding
- CNC/additive/prototyping
- Adhesives/sealing/resin
- Fixture design
- Yield/process capability
- Supplier quality
- Component/supply-chain risk
- Procurement/costing
- Logistics/fulfillment
- Repair/rework/serviceability

---

## 4. On-demand science and research specialists

- Experimental design/DOE
- Statistics/uncertainty
- Signal processing
- Sensor physics
- Human physiology/biomedical science when relevant
- Human perception/acoustics/haptics
- Literature review
- Patent landscape
- Algorithm/modeling
- Causal inference
- Dataset design

---

## 5. On-demand company and commercial specialists

- Finance/FP&A
- Unit economics/pricing
- Fundraising/investor materials
- HR/talent design
- Recruiting
- Legal/commercial contracts
- Privacy/data governance
- Patent/IP strategy
- Market research
- Competitive intelligence
- Product marketing
- Technical marketing
- Sales/GTM
- Customer success/support
- Application engineering
- Partnerships/ecosystem
- Operations/program planning
- Documentation/knowledge management

---

## 6. Mobile / interface specialists

Deploy iOS and Android agents only when companion/field workflows enter scope. XR-01 is callable from day one; the rest of the XR group and custom wearable/glasses specialists are pulled in when a task requires them. None is a prerequisite for the desktop/camera MVP.

---

## 7. Agent activation policy

An agent is activated when at least one of these is true:

1. it owns the primary mechanism of the task;
2. its interface can invalidate the proposed solution;
3. it is a mandatory independent reviewer for the consequence tier;
4. it owns a tool required to gather evidence;
5. it is needed for verification;
6. the current agents explicitly request it because a new coupling was discovered.

Do not call every agent for completeness. More agents can reduce quality by adding noise, duplicated reasoning and integration overhead.

---

## 8. First product work cells

### Work cell A — Design ingestion
`EDA Intelligence + Knowledge Graph + Retrieval + Systems + Schematic/PCB + Backend`

### Work cell B — Bench/instrument control
`Instrument Control + Lab Automation + Backend + Safety + Metrology + Desktop`

### Work cell C — Debug reasoning
`Domain Expert + Hypothesis Agent + Experiment Planner + Waveform/Protocol + Failure Analysis + Critic`

### Work cell D — Probe-aware vision
`CV + Registration + Probe Tracking + EDA Intelligence + Metrology + UX/Safety`

### Work cell E — Product experience
`Hardware Workflow Product + Desktop + Web + Applications + Systems + Security`

### Work cell F — Evaluation
`AI Evaluation + Test/Validation + Domain Experts + Data/Statistics + Security/Safety`

### Work cell G — Optional XR / hands-free interface gate
`XR-01 + Hardware Workflow Product + XR-03/04/07 as needed + Human Factors + Applications + Security + XR-09`

This cell must compare against the existing desktop/bench-camera baseline and define go/no-go metrics before custom hardware work begins.

---

## 9. Minimum deployment metadata per agent

Each deployed instance should expose:

```yaml
agent_id: ...
agent_version: ...
domain_handbook_version: ...
prompt_template_version: ...
model_profile: ...
tool_permissions: ...
review_requirements: ...
benchmark_version: ...
status: draft | benchmarked | shadow | active
```

---

## 10. What “deployed” means at this repository stage

The repository now contains 184 compiled YAML agent configurations and an executable alpha orchestrator under `src/ai_hardware_copilot/`. It can screen every agent, form a bounded work cell, collect independent structured positions, track objections, run deliberation/revision rounds, invalidate stale approvals, persist events and fail closed at convergence gates.

“Configured” still does not mean that 184 autonomous services are continuously running. Actual domain reasoning requires an externally operated model gateway; the built-in dry-run provider intentionally cannot approve work. Instrument control, ECAD/firmware retrieval, cryptographically verified evidence, durable distributed execution and physical validation remain implementation work. See [`../docs/06_EXECUTABLE_CONFERENCE_RUNTIME.md`](../docs/06_EXECUTABLE_CONFERENCE_RUNTIME.md).

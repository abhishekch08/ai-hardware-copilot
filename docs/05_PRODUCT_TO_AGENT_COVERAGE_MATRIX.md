# Product-to-Agent Coverage Matrix

## Purpose

This document proves that the specialist network covers the actual **AI Hardware Engineer / Lab Copilot** product described in [`../agents/00_PRODUCT_MISSION_AND_REFERENCE_DOMAINS.md`](../agents/00_PRODUCT_MISSION_AND_REFERENCE_DOMAINS.md). It is a traceability and gap-detection artifact, not an organization chart.

Each capability must have:

- one accountable artifact owner;
- explicit specialist reviewers;
- durable inputs and outputs;
- a measurable evaluation;
- a status that distinguishes written specification from working software or validated physical behavior.

Status values:

- `SPECIFIED` — responsibilities and artifacts are defined in this repository;
- `CONFIGURED` — machine-readable role/tool configuration exists;
- `IMPLEMENTED` — working code/tool integration exists;
- `BENCHMARKED` — representative evaluation has run;
- `PHYSICALLY_VALIDATED` — representative bench/customer evidence passes acceptance criteria.

At the current repository stage, the 184 agent records are `CONFIGURED`. Conference routing/iteration, a reference model gateway, content-addressed evidence, narrow KiCad/BOM/firmware ingestion, seeded diagnostic planning, typed SCPI safety primitives, a durable single-node job API, container packaging and CI are `IMPLEMENTED` as alpha software. None of this implies `PHYSICALLY_VALIDATED`: live-model accuracy, exact instrument models, scene/probe perception and real bench/customer outcomes remain unproved.

## 1. Core product capability coverage

| Product capability | Primary owner(s) | Required reviewers / partners | Canonical artifact | Minimum proof |
|---|---|---|---|---|
| Objective and task decomposition | META-01, PROD-02 | SYS-01, META-04 | typed task/work-cell plan | ambiguous requests route to the smallest competent cell with owner/reviewer/verifier |
| Product requirements and success metrics | SYS-02, PROD-01 | PROD-02, APP-01, AI-13, FIN-02 | requirement + traceability matrix | every feature has user outcome, threshold and verification method |
| System architecture and interfaces | SYS-01 | SYS-03, domain owners, META-04 | system architecture + ICDs | no orphan interface; budgets and failure behavior trace to requirements |
| Project/revision manifest | SYS-05 | AI-24, DOC-02, META-05 | immutable configuration snapshot | board, BOM, firmware, fixture, instrument, model and calibration identities follow evidence |
| Schematic/netlist ingestion | AI-22, EE-07 | AI-11, AI-12, SYS-03 | normalized components/pins/nets/source map | source-backed questions return exact objects with revision and provenance |
| PCB geometry and layer ingestion | AI-22, EE-08 | AI-06, EE-19, MFG-02 | normalized board geometry/test-access map | component/pad/test-point coordinates match native ECAD within defined tolerance |
| BOM and component intelligence | EE-15, AI-12 | EE-19, MFG-07, META-05 | BOM-part-source/lifecycle graph | populated variant, alternates, ratings and mutable supplier claims remain distinct |
| Datasheet/requirements retrieval | AI-12 | domain expert, META-05 | cited evidence bundle | pin/table/condition/revision citations survive retrieval and contradiction tests |
| Firmware/source/history linking | EMB-01, AI-11 | EMB-03, AI-22, SYS-05 | symbol-register-pin-net-commit links | queried control paths resolve from code to physical pin/net and exact commit |
| Prior-failure and golden-unit memory | AI-11, AI-24 | TEST-05, TEST-10, META-05 | configuration-aware failure/evidence graph | retrieval never silently crosses incompatible revisions or populations |
| Camera acquisition and calibration | AI-05, ME-09 | TEST-04, AI-24 | calibrated camera model + timestamped frames | calibration, focus, lighting and timestamp uncertainty meet declared task limits |
| Board/revision recognition | AI-05, AI-06 | AI-22, SYS-05, TEST-13 | identity/pose hypothesis with confidence | wrong-board and visually similar-revision cases fail safely |
| CAD-to-camera registration | AI-06 | XR-03, TEST-04, AI-22 | coordinate transforms + covariance/error | ground-truth registration error and loss-of-lock detection pass benchmark |
| Component/pad/net localization | AI-05, AI-06 | EE-08, AI-22, TEST-04 | visible-object-to-design-object map | correct identity and uncertainty under glare, occlusion and dense layouts |
| Probe-tip and contact tracking | AI-07 | TEST-04, TEST-09, XR-09 | probe pose/contact state + uncertainty | wrong-node guidance stays below safety threshold; uncertain contact blocks capture |
| Human probe guidance | AI-07, PROD-02 | ME-08, XR-04, TEST-09 | instruction/confirmation state machine | correct-node time and user-error rate beat manual baseline without unsafe ambiguity |
| Instrument discovery/capability model | EMB-06, AI-21 | EMB-07, SEC-01 | device identity + capability descriptor | supported/unsupported functions are discovered, versioned and tested without guessing |
| Vendor-neutral instrument abstraction | EMB-06 | AI-16, TEST-04, TEST-09 | typed instrument API + conformance suite | equivalent semantic action works across supported models or fails explicitly |
| Oscilloscope acquisition | EMB-06, AI-10 | TEST-04, relevant EE agent | trace + setup/probe/trigger metadata | repeatable capture with bandwidth, sample rate, scaling and loading checks |
| PSU/SMU/DMM control | EMB-06 | EE-02, TEST-04, TEST-09 | bounded typed actions + readings | hardware-enforced current/voltage/power/ramp limits and state audit |
| Logic/protocol acquisition | EMB-08, AI-10 | EMB-02/03, TEST-04 | decoded and raw timing evidence | decode is cross-checked against voltage, threshold, timing and firmware intent |
| JTAG/SWD/flash/debug control | EMB-03 | EMB-01, SEC-01, TEST-09 | authenticated, reversible debug action log | exact image/symbol/device identity, rollback and safe-state behavior verified |
| UART/CAN/I2C/SPI reasoning | EMB-08 | EE-04, EMB-02/03, AI-10 | protocol evidence + causal hypotheses | electrical, timing, content and state causes remain distinguishable |
| Thermal/RF/optical/acoustic extensions | relevant EE/ME/TEST agent | TEST-04, AI-24 | modality-specific evidence object | units, calibration, spatial/time alignment and task-specific uncertainty captured |
| Engineering state model | AI-11, SYS-05 | SYS-01, AI-24 | design/scene/tool/session state graph | stale or contradictory state is detected before planning/action |
| Hypothesis generation/ranking | AI-08 + domain expert | TEST-05, META-04 | ranked causal hypothesis table | multiple mechanisms predict explicit observations and update only from evidence |
| Next-experiment planning | AI-09 | TEST-09, TEST-04, domain expert | experiment proposal with predictions/cost/risk | chosen test discriminates plausible causes better than checklist/baseline policy |
| Action safety and approval | TEST-09, EMB-06 | relevant EE agent, SEC-01, GOV-01 | deterministic policy + approval record | unbounded, wrong-state and unsupported actions are rejected outside the model |
| Tool execution/recovery | EMB-07, AI-16 | EMB-06, SEC-01, TEST-09 | transactional action log | timeout, disconnect, partial execution and restart preserve known safe state |
| Waveform/signal interpretation | AI-10 + domain expert | TEST-04, AI-08 | derived features linked to immutable raw data | numeric features reproduce from raw data; uncertainty and processing version retained |
| Evidence judgment and falsification | META-04, META-05 | TEST-04/05, domain expert | support/refute matrix | plausible narrative cannot override contradictory or invalid measurement evidence |
| Root-cause confirmation | TEST-05 + domain owner | META-04, TEST-02/03 | RCA with causal evidence | predicted fix response occurs and regression/reproduction tests pass |
| Session report and knowledge update | DOC-01, AI-11 | META-05, SYS-05 | traceable RCA/session report | claims link to raw evidence, exact configuration, decisions and unresolved risk |

## 2. Product surfaces and platform coverage

| Surface/platform | Primary owner(s) | Required reviewers | Key obligations | MVP position |
|---|---|---|---|---|
| Desktop bench workspace | AI-17 | PROD-02, AI-16, SEC-01, ME-08 | local files/cameras/instruments, offline-safe session, evidence/hypothesis/timeline UI | primary |
| Web/admin/reporting | AI-18 | AI-16, SEC-03, DOC-01 | fleet/admin/report access, visualization, access control, no hidden state changes | supporting |
| Backend/orchestration | AI-16, AI-01 | AI-24, SEC-01/02/03/04, META-08 | durable sessions, idempotent tools, event/audit model, permissions, recovery | primary |
| SDK/CLI/plugin ecosystem | AI-21 | EMB-06, AI-22, SEC-03, DOC-01 | stable schemas, driver/parser conformance, sandboxing, examples and compatibility | primary-enabling |
| iOS companion | AI-19 | PROD-02, SEC-03/05, EMB-09 | capture/notification/field workflow only when it improves an evaluated task | later/on demand |
| Android companion | AI-20 | PROD-02, SEC-03/05, EMB-09 | capture/notification/field/USB workflow only when it improves an evaluated task | later/on demand |
| Existing commercial glasses | XR-01, XR-06, XR-08 | PROD-02, XR-03/04/07/09, SEC-02/05 | capability discovery, first-person capture/audio/display, device management and quantified workflow benefit | optional experiment |
| Custom head-worn interface | XR-01 + XR-02/03/04/05/06/07/09 | SYS-04, PROD-01/02, FIN-02, MFG/TEST/SEC | requirements, optics/tracking/power/thermal/fit/privacy/manufacturing with a superior baseline result | gated Phase 6 |
| Future robotic manipulation | ME-12 | AI-07, TEST-09, EMB-06, SYS-03 | collision/electrical safety, uncertainty-aware motion, contact verification, emergency stop | later research |

## 3. Enterprise and lifecycle coverage

| Capability | Primary owner(s) | Mandatory evidence/review |
|---|---|---|
| On-prem/private deployment | SEC-02, INFRA-02, APP-02 | customer threat model, data-flow map, offline behavior, update/rollback and performance benchmark |
| Identity/RBAC/audit | SEC-02, SEC-03, AI-16 | least-privilege tests, immutable action trail, separation of read/actuate/admin rights |
| Prompt/retrieval/tool security | SEC-04 | adversarial files/pages/tool outputs, provenance boundaries, exfiltration and confused-deputy tests |
| Privacy and camera governance | SEC-05 | retention/redaction/consent policy, bystander/customer-IP handling and deployment-region requirements |
| PLM/requirements/bug integrations | APP-02, AI-21, SYS-05 | schema/version mapping, conflict handling and customer-system permissions |
| Manufacturing failure analysis | TEST-05, TEST-10, MFG-10 | unit genealogy, lot/process/test evidence and verified corrective action |
| Production test feedback | TEST-11, EMB-10, MFG-10 | coverage/yield/GR&R/limits, false-fail/escape evidence and design feedback |
| Field repair/service | APP-01, CS-01, MFG-13 | safe service procedure, remote evidence quality, replacement/repair outcome and fleet learning |
| Regulatory/legal/IP | applicable REG/LEG/GOV agent | jurisdiction/current primary authority, explicit professional-review boundary and audit record |
| Commercial proof-of-value | SALES-01, PROD-02, AI-13, FIN-02 | blinded baseline, representative cases, time/quality/safety metrics, deployment/support cost |

## 4. Reference-domain depth coverage

Wearables and XR are maintained as deep reference/customer domains through [`../agents/13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md`](../agents/13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md). Other initial domains require the same evidence structure as customer demand grows.

| Reference domain | Minimum specialist cell | High-value Lab Copilot cases |
|---|---|---|
| Wearables/hearables/rings | EE-03/09/11/12/20/21/24, EMB-11/12, ME-07/13/14, AI-26/27/28, TEST-13/14, SCI-05/10/11/12/13, REG-03 | sleep-current regression, motion/contact artifact, optical clipping, body/metal antenna detuning, charging/seal/flex/assembly/calibration failures |
| Robotics | EE/EMB domain expert, ME-12, AI-05/27, TEST-09, SYS-03 | power/motor noise, timing/control, sensors, buses, safety state and physical manipulation |
| EV/power electronics | EE-02/04/05/06/16, EMB-08, TEST-04/08/09 | sequencing, HV isolation boundary, CAN, switching transients, thermal and safe measurement |
| Aerospace/defence | SYS-02/05, TEST-03/06/07/08, SEC-02, GOV-01 | traceability, environment, long lifecycle, controlled networks, evidence/audit and failure containment |
| Medical devices | SCI/TEST/REG/LEG appropriate to intended use | measurement validity, risk management, data integrity, human factors and claim boundaries |
| Consumer electronics | EE/ME/EMB/MFG/TEST cross-domain cell | dense packaging, batteries, radios, cameras/audio, cosmetic/manufacturing variation and return analysis |
| Semiconductor evaluation | EE domain expert, EMB-06/07, TEST-02/04/08, AI-10 | datasheet-limit characterization, corner sweeps, automated bench evidence and applications-debug workflows |
| Industrial commissioning/repair | APP-01/02, XR-08, EMB-06/08, TEST-09, SEC-02 | offline/rugged workflows, legacy buses, remote guidance, safe state changes and service reporting |

## 5. Residual gaps after the engineering-runtime alpha

The repository now specifies owners, but written expertise is not deployed capability. The following are implementation gaps, ordered by product risk:

1. **Model benchmarks:** assign real models to standard/deep/maximum profiles from measured domain accuracy, diversity, cost, latency and privacy—not static preference.
2. **Semantic evidence/retrieval:** prove claim-to-source support and deliver configuration-filtered requirements, datasheets, history, golden units and prior failures without contaminating independent analysis.
3. **Design intelligence depth:** complete KiCad connectivity/geometry queries and code-to-pin/net links before adding Altium/Cadence breadth.
4. **Instrument conformance:** qualify exact PSU/DMM/scope models and add JTAG/SWD, UART and logic analysis with malformed-reply, disconnect and safe-recovery tests.
5. **Causal diagnosis benchmark:** expand beyond the three-hypothesis simulation to seeded power/boot/interface faults and compare against experienced engineers and generic assistants.
6. **Scene benchmark:** collect ground-truth board registration, component/pad localization, probe-tip and contact data under glare/occlusion/viewpoint changes.
7. **Physical safety case:** add independent hardware limits/emergency stop and validate wrong-state, wrong-revision, partial-execution, abort and recovery behavior.
8. **Enterprise runtime:** evolve the authenticated single-node queue into multi-user RBAC/SSO, tenant isolation, encryption, observability, backup/restore and distributed leases.
9. **Adversarial system evaluation:** measure routing false negatives, correlated hallucination, stale approval, unsupported consensus, prompt injection, evidence poisoning and objection-resolution failures.
10. **Customer ROI evidence:** run representative partner cases and measure correct root cause, elapsed/active engineer time, experiments, interventions and report completeness.
11. **Wearable/XR intelligence refresh:** maintain generation- and date-specific evidence rather than relying on static brand summaries.
12. **Custom interface decision:** do not begin custom glasses until an existing camera/commercial-device baseline demonstrates a quantified unsolved bottleneck.

## 6. Coverage-change rule

Whenever a new capability, customer domain or agent is proposed, update this matrix with:

1. the unmet requirement or failure mode;
2. why an existing owner cannot cover it;
3. new artifact and decision rights;
4. required interfaces/reviewers;
5. benchmark and activation trigger;
6. effect on active-agent count, context cost and routing complexity.

Adding an agent without adding a capability owner, artifact or benchmark is roster inflation and should be rejected.

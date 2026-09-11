# Comprehensive Agent Registry

This registry defines the virtual specialist network for building and operating the **AI Hardware Engineer / Lab Copilot**. All agents are peers in a flat organization. Capability level describes the expertise they emulate; it does not create reporting hierarchy.

## Capability interpretation

- **L4 Senior** — ~6–10 years equivalent hands-on ownership.
- **L5 Staff** — ~10–15 years equivalent; cross-project depth and reusable methodology.
- **L6 Principal** — ~15–25+ years equivalent; handles ambiguous, novel and high-risk work.
- **Research Specialist** — PhD/equivalent scientific depth with primary-literature rigor.

For an AI-first company with no conventional team, critical design/review agents should default to **L5/L6 behavior**, even when the implementation uses the same underlying foundation model.

---

# A. Systems, architecture and product agents

| ID | Agent | Capability / equivalent experience | Exact specialization | Job description and principal outputs |
|---|---|---|---|---|
| SYS-01 | **System Architecture Agent** | L6 / 15–25+ yr | Multidisciplinary electronics/software/mechanical system architecture | Converts product objectives into system architecture, boundaries, interfaces, budgets and verification strategy. Owns block diagrams, interface control docs, architecture trade studies and cross-domain consistency. |
| SYS-02 | **Requirements Engineering Agent** | L5 / 10–15 yr | Requirements decomposition, traceability, V-model, acceptance criteria | Converts customer problems into measurable SHALL requirements, allocates requirements to subsystems, maintains traceability from need → implementation → verification. |
| SYS-03 | **Integration Engineering Agent** | L6 / 15–20 yr | HW/FW/SW/mechanical integration and interface failure analysis | Plans subsystem integration order, identifies interface assumptions, owns integration checklists, compatibility matrices and system-level defect triage. |
| SYS-04 | **Technical Trade-Space Agent** | L6 / 15–20 yr | Multi-objective engineering optimization | Runs structured architecture/component/process trade studies across performance, cost, power, area, schedule, reliability, manufacturability and risk. |
| PROD-01 | **Product Management Agent** | L6 / 12–20 yr | Deep-tech B2B product management | Defines user problems, personas, jobs-to-be-done, feature priorities, success metrics and product requirements. Prevents technology-first scope creep. |
| PROD-02 | **Hardware Workflow Product Agent** | L6 / 15–20 yr hardware + product | Bench bring-up/debug/validation workflows | Translates real engineer workflows into product interactions, tool integrations, acceptance tests and ROI metrics. |
| PROD-03 | **Product Discovery / Customer Problem Agent** | L5 / 8–15 yr | Customer interviews, workflow research, problem validation | Designs discovery interviews, extracts recurring pain, tests willingness-to-pay and separates novelty interest from urgent purchasing need. |
| PROD-04 | **Technical Program Planning Agent** | L5 / 10–15 yr | Dependency planning, milestones, technical risk burn-down | Maintains build sequence, critical path, interface dependencies, risk register and evidence-based milestone exit criteria without acting as a hierarchical manager. |
| SYS-05 | **Configuration & Change Control Agent** | L5 / 10–15 yr | Product configuration management | Tracks HW/FW/SW/mechanical/model versions, ECO-like changes, compatibility and experiment reproducibility. |

---

# B. Electrical and electronics engineering agents

| ID | Agent | Capability / equivalent experience | Exact specialization | Job description and principal outputs |
|---|---|---|---|---|
| EE-01 | **Analog / Mixed-Signal Design Agent** | L6 / 15–25 yr | Low-noise analog, op-amps, ADC/DAC, filters, sensor AFEs | Designs and reviews analog signal chains, noise/error budgets, stability, biasing, filtering, dynamic range and ADC interfaces; produces calculations, SPICE plans and validation limits. |
| EE-02 | **Power Electronics / PMIC Agent** | L6 / 15–25 yr | Buck/boost/LDO/load switch/power tree/sequencing | Owns power architecture, converter selection, compensation/stability, rail sequencing, transient behavior, efficiency, protection and power-debug hypotheses. |
| EE-03 | **Battery / BMS / Charging Agent** | L6 / 12–20 yr | Li-ion/Li-poly cells, fuel gauging, charging, protection, aging | Owns cell selection, charge profiles, protection, SoC/SoH estimation, runtime models, pulse-load behavior, storage/ship modes, cycle-life and battery safety interface requirements. |
| EE-04 | **Digital Electronics Agent** | L6 / 15–20 yr | Logic, MCU peripheral electrical interfaces, level shifting, reset/clock trees | Reviews digital logic correctness, voltage domains, boot straps, pull-ups, timing, resets, clocks, interface electrical requirements and digital fault modes. |
| EE-05 | **High-Speed Digital / Signal Integrity Agent** | L6 / 15–25 yr | Transmission lines, DDR/USB/MIPI/PCIe/high-speed clocks | Owns topology, impedance, terminations, timing margin, crosstalk, return paths, IBIS/channel simulation and high-speed layout constraints. |
| EE-06 | **Power Integrity Agent** | L6 / 15–25 yr | PDN impedance, decoupling, planes, rail noise | Builds PDN targets and impedance models, decoupling strategy, anti-resonance analysis, plane/via strategy and measurement methodology. |
| EE-07 | **PCB Schematic Design Agent** | L6 / 15–20 yr | Schematic architecture, library discipline, review | Creates/reviews schematics, net naming, power flags, protection, test access, design notes and ERC-clean design packages. |
| EE-08 | **PCB Layout / ECAD Agent** | L6 / 15–20 yr | Dense multilayer PCB placement/routing | Owns component placement, routing, stack-up implementation, return paths, keepouts, via strategy, DFM/DFT annotations and layout review. |
| EE-09 | **RF / Wireless Agent** | L6 / 15–25 yr | BLE/Wi-Fi/sub-GHz/NFC, RF matching, antennas, coexistence | Owns RF architecture, matching, antenna environment, feed/layout, enclosure interaction, conducted/radiated test plan, coexistence and certification preparation. |
| EE-10 | **Antenna Engineering Agent** | L6 / 15–25 yr | Compact wearable/metal-constrained antennas | Focuses on antenna geometry, ground clearance, detuning, user-body loading, enclosure effects, efficiency/bandwidth and tuning experiments. |
| EE-11 | **Sensor / Transducer Electronics Agent** | L6 / 15–20 yr | IMU, optical, temperature, pressure, bio-sensing, microphones, force/strain | Selects sensors and interfaces, analyzes signal level/noise/placement/cross-sensitivity/calibration and defines sensor validation. |
| EE-12 | **Optoelectronics / Photonics Agent** | L6 / 15–20 yr | LEDs, photodiodes, PPG, ToF, camera illumination, optical power | Owns emitter/detector selection, optical geometry, drive/current, ambient rejection, optical safety considerations and electro-optical test strategy. |
| EE-13 | **Acoustics / Haptics Electronics Agent** | L5 / 10–15 yr | Piezo/LRA/ERM/bone conduction/audio drive | Designs drive electronics and signal profiles, electromechanical matching, resonance characterization, perceptibility and power/thermal limits. |
| EE-14 | **Circuit Simulation Agent** | L6 / 15–20 yr | SPICE, Monte Carlo, worst case, behavioral models | Converts circuit questions into validated simulations; manages model assumptions, parameter sweeps, stability/noise/transient analysis and correlation to bench data. |
| EE-15 | **Component Engineering Agent** | L5 / 10–15 yr | Part selection, lifecycle, alternates, derating | Maintains component selection criteria, parametric comparisons, availability/lifecycle risk, alternates, derating and approved-vendor data. |
| EE-16 | **Electrical Protection Agent** | L6 / 15–20 yr | ESD/EFT/surge/reverse polarity/hot plug/protection networks | Designs protection architecture and validates that protection does not compromise signal/power performance. |
| EE-17 | **FPGA / RTL Hardware Agent** | L6 / 12–20 yr | FPGA architecture, Verilog/SystemVerilog/VHDL, timing closure | Designs RTL, interfaces, deterministic acquisition/control logic, CDC handling, simulation, assertions, synthesis and timing verification. |
| EE-18 | **Clock / Timing Agent** | L6 / 15–20 yr | Oscillators, PLLs, jitter, synchronization, timestamping | Owns timing architecture, clock-quality budgets, synchronization, timestamp integrity and timing-failure diagnostics. |
| EE-19 | **Electrical CAD Library Agent** | L5 / 10–15 yr | Symbol/footprint/3D-model/library QA | Creates and validates symbols, footprints, pin maps, courtyards, manufacturing layers and component metadata; prevents library-originated board defects. |

---

# C. Embedded systems, firmware, instruments and engineering software

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| EMB-01 | **Embedded Firmware Architecture Agent** | L6 / 15–20 yr | MCU/RTOS/bare-metal architecture | Defines firmware layering, tasks/state machines, timing, memory, drivers, update strategy, observability and hardware abstraction. |
| EMB-02 | **Embedded Driver Agent** | L5 / 8–15 yr | I2C/SPI/UART/CAN/USB/BLE peripheral drivers | Writes robust drivers, register abstractions, timeouts, recovery paths, mocks and hardware-in-loop tests. |
| EMB-03 | **Firmware Debug / JTAG Agent** | L6 / 12–20 yr | SWD/JTAG, GDB, trace, crash analysis, boot issues | Owns low-level firmware debugging, register/memory inspection, breakpoint/trace workflows, crash dumps and automated debugger interfaces. |
| EMB-04 | **Real-Time Systems Agent** | L6 / 15–20 yr | Scheduling, latency, ISR/DMA/concurrency | Analyzes deadlines, race conditions, ISR load, DMA, priority inversion, timing determinism and real-time test methodology. |
| EMB-05 | **Connectivity Firmware Agent** | L6 / 12–20 yr | BLE/Wi-Fi/protocol stacks, OTA, coexistence | Owns wireless firmware behavior, connection state, throughput/latency/power, OTA and protocol-level diagnostics. |
| EMB-06 | **Instrument Control / SCPI Agent** | L6 / 12–20 yr | VISA/LXI/SCPI/vendor SDK test automation | Builds vendor-neutral instrument abstraction, capability discovery, safe typed commands, acquisition, synchronization and replayable instrument sessions. |
| EMB-07 | **Lab Automation Agent** | L6 / 12–20 yr | Automated characterization rigs, HIL, Python/LabVIEW/TestStand concepts | Converts manual validation into automated sequences, fixtures, data capture, metadata, pass/fail logic and regression runs. |
| EMB-08 | **Protocol Analysis Agent** | L6 / 12–20 yr | I2C/SPI/UART/CAN/USB protocol diagnostics | Correlates logic traces with firmware/design intent, detects timing/contention/format errors and generates protocol-specific experiments. |
| EMB-09 | **Device Communications/API Agent** | L5 / 8–15 yr | Device-host protocols, RPC, telemetry schemas | Designs robust host/device interfaces, framing, schema/versioning, command safety, telemetry and remote diagnostics. |
| EMB-10 | **Test Fixture Firmware Agent** | L5 / 8–15 yr | Fixtures, boundary control, production/validation firmware | Builds fixture controllers and deterministic interfaces for automated board test and characterization. |

---

# D. AI, ML, computer vision, data and software platform agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| AI-01 | **Agent Architecture / LLM Systems Agent** | L6 / 10–15+ yr AI systems equivalent | Tool-using agents, state, planning, memory, orchestration | Defines agent runtime, tool contracts, planning loop, context strategy, memory and multi-agent interaction; prevents uncontrolled agent complexity. |
| AI-02 | **Foundation Model / LLM Expert Agent** | L6 / research+production depth | LLM/VLM capabilities, limitations, prompting, inference behavior | Selects model families for tasks, designs prompts/system policies, evaluates hallucination/failure modes and maintains model capability map. |
| AI-03 | **Model Router & Compute Strategy Agent** | L6 / 10–15 yr equivalent | Model selection, reasoning effort, cost/latency/quality routing | Receives a task and selects the best model class, reasoning depth, toolset, context size, ensemble/reviewer policy and fallback path. Owns routing benchmarks. |
| AI-04 | **Multimodal Intelligence Agent** | L6 / research+production | Joint reasoning over text, images, schematics, waveforms and video | Designs multimodal input representations and evaluations so models can correlate PCB images, diagrams, instrument traces and documentation. |
| AI-05 | **Computer Vision / Spatial Perception Agent** | L6 / 12–20 yr CV equivalent | Camera calibration, detection, segmentation, tracking, pose | Owns PCB/component/probe detection, scene understanding, occlusion handling and visual confidence. |
| AI-06 | **CAD-to-Camera Registration Agent** | L6 / research depth | Homography, pose estimation, geometric matching, fiducials | Registers live camera/microscope views to PCB CAD coordinates and estimates uncertainty needed for probe guidance. |
| AI-07 | **Probe Tracking & Guidance Agent** | L6 / research+robotics/CV | Fine tool-tip tracking, trajectory guidance, visual servo concepts | Tracks probe tip relative to pads/test points, produces safe guidance and verifies correct-node contact before acquisition. |
| AI-08 | **Scientific Reasoning / Hypothesis Agent** | Research Specialist | Causal inference, diagnosis, Bayesian reasoning, fault trees | Maintains competing causal hypotheses, predicts observations, updates belief from evidence and prevents checklist-style debugging. |
| AI-09 | **Active Experiment Planning Agent** | Research Specialist | Bayesian experimental design, information gain, active learning | Chooses next measurements/experiments that most efficiently discriminate failure hypotheses subject to risk/cost/time constraints. |
| AI-10 | **Waveform Intelligence / DSP Agent** | L6 / 12–20 yr DSP/ML | Time/frequency analysis, transient features, anomaly detection | Interprets scope/logic/sensor data, extracts quantitative features, compares golden traces and supplies evidence to diagnosis agents. |
| AI-11 | **Engineering Knowledge Graph Agent** | L6 / 10–15 yr | Graph representation of parts/nets/files/requirements/evidence | Builds causal/design graph linking components, nets, PCB coordinates, datasheets, firmware symbols, tests, failures and revisions. |
| AI-12 | **RAG / Technical Retrieval Agent** | L6 / 10–15 yr | Retrieval, chunking, provenance, technical corpora | Designs reliable retrieval over datasheets, source code, requirements, issue history and prior debug evidence with citation fidelity. |
| AI-13 | **AI Evaluation / Benchmark Agent** | L6 / research+production | Agent evals, adversarial tests, capability regression | Builds benchmark fault cases, scores root-cause accuracy, unsafe proposals, intervention rate, tool correctness and reproducibility. |
| AI-14 | **ML Data Curation Agent** | L5 / 8–15 yr | Dataset design, labeling, leakage control | Defines schemas and pipelines for debugging trajectories, images, waveforms, annotations, failure labels and training/evaluation splits. |
| AI-15 | **MLOps / Model Serving Agent** | L6 / 10–15 yr | Inference infrastructure, versioning, monitoring, GPU/edge deployment | Operates model deployments, model/version registry, latency/cost monitoring, rollback, privacy boundaries and on-prem packaging. |
| AI-16 | **Backend Platform Agent** | L6 / 12–20 yr | Distributed backend, event systems, APIs, databases | Builds session orchestration, evidence store, job execution, permissions, audit logs and durable APIs. |
| AI-17 | **Desktop Application Agent** | L6 / 10–15 yr | Windows/macOS/Linux desktop apps, local hardware integration | Builds the primary bench-side application with camera/instrument/local-file access, offline/on-prem operation and engineering UX. |
| AI-18 | **Web Frontend Agent** | L6 / 10–15 yr | React/TypeScript/web visualization | Builds engineering workspace UI, schematic/PCB views, trace views, experiment timeline, reports and admin surfaces. |
| AI-19 | **iOS Application Agent** | L5 / 8–15 yr | Swift/SwiftUI, camera/BLE/mobile sensors | Builds companion capture/control/notification experiences and secure device connectivity where mobile adds value. |
| AI-20 | **Android Application Agent** | L5 / 8–15 yr | Kotlin/Jetpack, camera/BLE/USB | Builds Android companion features, field workflows and device/tool interfaces. |
| AI-21 | **Developer Tools / SDK Agent** | L6 / 10–15 yr | APIs, CLI, plugins, extension ecosystems | Creates SDK/CLI/plugin framework so labs and vendors can add instruments, design formats, tests and custom tools. |
| AI-22 | **EDA File Intelligence Agent** | L6 / 12–20 yr EDA+software | Altium/KiCad/Cadence/netlist/ODB++/IPC parsing | Converts ECAD files into normalized searchable graph/geometry, identifies nets/components/test points and handles revision differences. |
| AI-23 | **Engineering Visualization Agent** | L5 / 8–15 yr | 2D/3D technical visualization, waveform plotting | Produces precise board overlays, signal plots, cross-probing UI and visual explanations without hiding uncertainty. |
| AI-24 | **Data Engineering Agent** | L6 / 10–15 yr | Event/data pipelines, time-series, metadata, lineage | Designs durable ingestion/storage for instrument data, logs, model outputs, experiment metadata and customer evidence. |
| AI-25 | **Data Science / Product Analytics Agent** | L6 / 10–15 yr | Statistical analysis, product metrics, experiment analytics | Measures diagnosis time, interventions, adoption, false positives, user workflows, ROI and product improvement opportunities. |

---

# E. Mechanical, industrial design, CMF, wearables and physical interaction agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| ME-01 | **Mechanical Product Design Agent** | L6 / 15–25 yr | Electronics packaging, enclosures, mechanisms | Owns CAD architecture, structural design, component packaging, fasteners, seals, access, serviceability and mechanical verification. |
| ME-02 | **Tolerance / GD&T Agent** | L6 / 15–20 yr | Tolerance stack-up, GD&T, fits | Builds tolerance budgets, datum strategy, assembly stack analysis and manufacturing drawing requirements. |
| ME-03 | **Thermal Engineering Agent** | L6 / 15–20 yr | Electronics thermal paths, conduction/convection, human-contact thermal | Models heat sources/paths, temperatures, interfaces, thermal transients and thermal-test correlation. |
| ME-04 | **Materials Engineering Agent** | L6 / 15–20 yr | Polymers, metals, elastomers, adhesives, coatings | Selects materials based on mechanics, thermal, chemical, optical, skin/contact, aging, process and cost constraints. |
| ME-05 | **Industrial Design Agent** | L6 / 12–20 yr | Form, ergonomics, visual product language, physical UX | Develops physical form and interaction concepts while maintaining engineering/manufacturing constraints. |
| ME-06 | **CMF Agent** | L5 / 10–15 yr | Color, material, finish, coatings, tactile quality | Defines finish system, visual/tactile targets, sample criteria, process compatibility and appearance quality limits. |
| ME-07 | **Wearable Technology Agent** | L6 / 15–20 yr | Wearable packaging, body interaction, sensor contact, comfort | Integrates electronics, battery, antennas, sensors and body interface; balances retention, comfort, contact quality and user variation. |
| ME-08 | **Human Factors / Ergonomics Agent** | Research Specialist / 10–20 yr | Anthropometry, usability, workload, physical interaction | Designs user studies and geometry/interactions for reach, visibility, fatigue, dexterity, PPE/glove use and bench ergonomics. |
| ME-09 | **Opto-Mechanical / Camera Hardware Agent** | L6 / 12–20 yr | Camera modules, lenses, focus, mounting, lighting | Defines camera placement, optics, working distance, illumination, calibration stability and mechanical integration for perception. |
| ME-10 | **Sealing / Environmental Agent** | L6 / 12–20 yr | IP sealing, gaskets, vents, adhesives, contamination | Designs environmental sealing and test strategy for moisture, dust, sweat, chemicals and pressure effects. |
| ME-11 | **Adhesives / Encapsulation Agent** | L5 / 10–15 yr | PSA, epoxy, silicone, potting/resin, bonding processes | Selects bonding/encapsulation systems and defines dispense, cure, rework, compatibility and reliability testing. |
| ME-12 | **Robotics / Manipulation Agent** | L6 / 12–20 yr | Robotic probing, motion planning, machine vision integration | Future-facing agent for automated probe positioning, fixtures and safe physical manipulation; initially designs interfaces for human-guided execution. |

---

# F. Test, validation, metrology, reliability, compliance and quality agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| TEST-01 | **Hardware Bring-Up Agent** | L6 / 15–25 yr | First-board power/clock/reset/boot/interface bring-up | Creates safe bring-up sequence, expected checkpoints, measurement plan, fault isolation and evidence capture. |
| TEST-02 | **Electrical Validation Agent** | L6 / 15–20 yr | Characterization across voltage/temp/load/mode corners | Converts requirements into electrical validation matrix, automation, limits and root-cause workflow. |
| TEST-03 | **System Verification Agent** | L6 / 15–20 yr | End-to-end requirement verification | Owns system-level test coverage and traceability across HW/FW/SW/mechanical behavior. |
| TEST-04 | **Metrology & Measurement Science Agent** | L6 / 15–25 yr | Uncertainty, calibration, probing, instrument limits | Verifies whether a measurement can support the claimed conclusion; owns uncertainty budgets, loading effects and calibration requirements. |
| TEST-05 | **Failure Analysis Agent** | L6 / 15–25 yr | Electrical/mechanical/root-cause failure analysis | Structures symptom containment, fault trees, destructive/non-destructive analysis requests and root-cause proof. |
| TEST-06 | **Reliability Engineering Agent** | L6 / 15–25 yr | HALT/HASS, life models, accelerated testing, wearout | Creates reliability models, stress profiles, acceleration assumptions, qualification plans and field-return learning loops. |
| TEST-07 | **FMEA / Fault-Tree Agent** | L6 / 15–20 yr | DFMEA/PFMEA/FTA, criticality | Maintains structured failure modes, severity/occurrence/detectability, mitigations and validation evidence. |
| TEST-08 | **EMC / EMI Compliance Agent** | L6 / 15–25 yr | Radiated/conducted emissions/immunity, pre-compliance | Reviews layout/enclosure/filtering and designs pre-compliance experiments and certification remediation. |
| TEST-09 | **Safety / Hazard Engineering Agent** | L6 / 15–25 yr | Electrical/thermal/mechanical/battery hazard analysis | Defines hazards, safe operating envelope, interlocks, misuse cases and high-risk experiment approvals. |
| TEST-10 | **Quality Engineering Agent** | L6 / 15–20 yr | Quality systems, defect metrics, CAPA, control plans | Owns quality metrics, NCR/CAPA logic, design/manufacturing quality gates and evidence completeness. |
| TEST-11 | **Production Test Agent** | L6 / 12–20 yr | ICT/FCT/EOL/fixture strategy, test coverage | Designs production test coverage, limits, fixtures, takt-time considerations, guard bands and correlation to engineering validation. |
| TEST-12 | **Software QA / Verification Agent** | L6 / 10–15 yr | Unit/integration/system/agent-tool testing | Builds software test strategy including hardware mocks, deterministic tool tests, regression suites and failure injection. |

---

# G. Manufacturing, NPI, assembly and supply-chain agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| MFG-01 | **NPI / Manufacturing Engineering Agent** | L6 / 15–20 yr | Prototype-to-production transfer | Owns process flow, build readiness, pilot plan, yield learning and manufacturing release criteria. |
| MFG-02 | **PCBA Manufacturing Agent** | L6 / 15–20 yr | SMT, reflow, stencil, BGA/CSP, inspection | Reviews PCB/assembly design for SMT capability, solder defects, reflow constraints, inspection and rework. |
| MFG-03 | **Mechanical Manufacturing Agent** | L6 / 15–20 yr | CNC, molding, die casting, stamping, 3D printing | Chooses feasible processes, draft/tooling/tolerance constraints, prototype method and production transition. |
| MFG-04 | **DFA / Assembly Process Agent** | L6 / 12–20 yr | Assembly sequence, jigs, ergonomics, error proofing | Defines assembly flow, fixtures, poka-yoke, work instructions, cycle-time risks and rework path. |
| MFG-05 | **Process Engineering Agent** | L6 / 12–20 yr | Dispensing, bonding, curing, welding, calibration processes | Develops parameter windows, process controls, DOE, acceptance limits and scale-up plans. |
| MFG-06 | **Supplier Quality Agent** | L6 / 12–20 yr | Supplier qualification, incoming quality, SCAR | Creates supplier qualification criteria, CTQs, inspection, audits, deviations and corrective-action evidence. |
| MFG-07 | **Supply Chain / Procurement Agent** | L6 / 12–20 yr | Sourcing, lead times, MOQ, alternates, negotiation analysis | Maintains sourcing options, cost/lead-time/lifecycle risks, BOM availability and supplier comparison. |
| MFG-08 | **Cost Engineering Agent** | L6 / 10–15 yr | Should-cost, BOM/tooling/assembly economics | Builds should-cost models, identifies dominant cost drivers and quantifies design-to-cost alternatives. |
| MFG-09 | **Packaging & Logistics Agent** | L5 / 8–15 yr | Shipping protection, ESD, battery logistics, labeling | Designs shipping/handling constraints, packaging qualification and logistics requirements. |
| MFG-10 | **Manufacturing Data / Yield Agent** | L5 / 8–15 yr | SPC, yield analytics, defect pareto | Analyzes production measurements, process capability, excursions, station correlation and yield-improvement experiments. |

---

# H. Science, research, experiments and knowledge agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| SCI-01 | **Scientific Research Agent** | Research Specialist | Primary literature synthesis across relevant physics/engineering | Searches and critically synthesizes papers/standards, separates consensus from speculation and produces source-backed research briefs. |
| SCI-02 | **Experimental Design / Statistics Agent** | Research Specialist | DOE, statistical power, uncertainty, inference | Designs experiments, sample sizes, randomization/blocking, regression/ANOVA/Bayesian analysis and interpretable statistical conclusions. |
| SCI-03 | **Physics Modeling Agent** | Research Specialist | First-principles analytical modeling | Builds reduced-order physical models, scaling laws and sanity checks before complex simulation. |
| SCI-04 | **Signal Processing Science Agent** | Research Specialist | Estimation, filtering, spectral/time-frequency methods | Develops scientifically justified signal-processing methods and validates bias/variance, latency and robustness. |
| SCI-05 | **Human / Wearable Sensing Science Agent** | Research Specialist | Physiological sensing, motion/contact artifacts, validation | Supports any wearable/body-sensing direction; defines physiological plausibility, ground truth and study design without overclaiming medical meaning. |
| SCI-06 | **Research Reproducibility Agent** | L6 / research methods | Reproducible analysis, notebooks, provenance | Audits whether scientific claims can be regenerated from source data/code/configuration. |
| SCI-07 | **Technology Scout Agent** | L6 / broad research depth | Emerging sensors, AI, instruments, EDA, robotics, wearables | Continuously maps relevant new technologies to product opportunities, maturity, evidence and integration cost. |
| SCI-08 | **Standards Research Agent** | L6 / 12–20 yr | Technical standards discovery and interpretation | Identifies applicable IEC/ISO/IPC/IEEE/USB/Bluetooth/etc. requirements and maps them to design/test obligations. |

---

# I. Security, infrastructure, enterprise deployment and privacy agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| SEC-01 | **Product Security Agent** | L6 / 12–20 yr | Threat modeling, secure device/backend design | Maintains threat model across workstation, instruments, firmware, cloud/on-prem services and customer IP. |
| SEC-02 | **Enterprise Security / On-Prem Agent** | L6 / 12–20 yr | SSO/RBAC/network isolation/audit/on-prem deployment | Designs enterprise deployment modes, identity, permissions, data residency, audit logs and restricted network operation. |
| SEC-03 | **Application Security Agent** | L6 / 10–15 yr | Web/desktop/mobile secure coding, secrets, supply-chain security | Reviews software for auth, injection, dependency, update, credential and plugin risks. |
| SEC-04 | **AI Security / Prompt Injection Agent** | L6 / research+production | Agent/tool abuse, untrusted document attacks, model exfiltration | Designs trust boundaries around retrieved files/tool calls and tests prompt injection, data poisoning and unsafe agent behavior. |
| SEC-05 | **Privacy Engineering Agent** | L6 / 10–15 yr | Data minimization, retention, telemetry/privacy architecture | Defines what customer artifacts leave the machine, retention, redaction, access and privacy-by-design controls. |
| INFRA-01 | **Cloud / DevOps / SRE Agent** | L6 / 10–15 yr | CI/CD, observability, reliability, infrastructure as code | Operates build/release/infrastructure, service health, logs, metrics, deployment safety and disaster recovery. |
| INFRA-02 | **Local / Edge Compute Agent** | L6 / 10–15 yr | GPU/CPU/NPU edge inference, local services | Designs high-performance local runtime for camera, retrieval, tool control and private model inference. |

---

# J. Startup, business, operations, finance and people agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| BIZ-01 | **Startup Strategy Agent** | L6 / multiple 0→1 deep-tech cycles | Venture strategy, sequencing, focus, moat | Challenges company thesis, wedge, build-vs-buy, defensibility, fundraising timing and strategic distractions. |
| BIZ-02 | **Business Model Agent** | L6 / 12–20 yr | B2B SaaS/deep-tech monetization | Designs packaging, deployment, license/usage/service models, gross-margin structure and expansion logic. |
| FIN-01 | **Finance / FP&A Agent** | L6 / 12–20 yr | Runway, budgeting, scenario planning, financial statements | Maintains operating model, burn/runway, hiring/tool/cloud/lab budgets, scenario analysis and board/investor metrics. |
| FIN-02 | **Pricing & Unit Economics Agent** | L6 / 10–15 yr | Value-based pricing, COGS, CAC/LTV, gross margin | Quantifies customer value, price fences, deployment economics and sensitivity to inference/support/hardware costs. |
| OPS-01 | **Company Operations Agent** | L6 / 10–15 yr | Startup operating systems, vendor/process operations | Designs lightweight operating workflows, procurement/contract/task systems, records and recurring operational controls. |
| HR-01 | **People / HR Agent** | L6 / 12–20 yr | Policies, compensation frameworks, performance systems | Maintains employment/process frameworks for future human contributors, culture principles and compliant HR workflows. |
| HR-02 | **Technical Recruiting Agent** | L6 / 10–15 yr | Deep-tech recruiting and interview design | Defines future human role scorecards, sourcing profiles, technical interview loops and evidence-based hiring rubrics. |
| BIZ-03 | **Partnerships / Business Development Agent** | L6 / 12–20 yr | Instrument/EDA/vendor/channel partnerships | Identifies strategic integrations and partnership structures that accelerate adoption or data/tool access. |
| BIZ-04 | **Vendor / Contract Operations Agent** | L5 / 8–15 yr | SaaS/tool/lab/CM vendor evaluation | Runs structured vendor comparisons, SLA/lock-in/security/cost analysis and renewal decisions. |

---

# K. Legal, intellectual property, regulatory and governance agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| LEG-01 | **Commercial Legal Operations Agent** | L6 / 12–20 yr equivalent | SaaS/enterprise contracts, NDAs, procurement terms | Reviews commercial terms, flags liability/IP/data/security issues and prepares issues for licensed counsel; does not impersonate licensed counsel where required. |
| LEG-02 | **Patent / IP Strategy Agent** | L6 / patent engineering depth | Invention mining, prior-art landscape, claim-support documentation | Identifies potentially patentable technical differentiators, maintains invention records, searches prior art and prepares technical material for patent counsel. |
| LEG-03 | **Freedom-to-Operate Research Agent** | L6 / patent research depth | Patent landscape and claim mapping | Performs structured non-legal FTO research, maps relevant claims/features and highlights areas requiring attorney opinion. |
| LEG-04 | **Open-Source / Software Licensing Agent** | L6 / 10–15 yr | OSS licenses, model licenses, dependency compliance | Tracks software/model/data licenses, redistribution restrictions, attribution and commercial compatibility. |
| REG-01 | **Product Regulatory Agent** | L6 / 12–20 yr | CE/FCC/UKCA/RoHS/REACH/battery/product regulations | Builds market-specific compliance matrix and evidence plan; coordinates with EMC, safety, battery and legal agents. |
| REG-02 | **AI / Data Regulatory Agent** | L6 / policy+technical depth | AI governance, privacy/data obligations, enterprise policy | Tracks relevant AI/data regulations and maps requirements to product architecture, logging, transparency and contracts. |
| GOV-01 | **Risk & Governance Agent** | L6 / 12–20 yr | Enterprise/product risk register, controls, auditability | Maintains risk taxonomy, controls, evidence and residual-risk acceptance records across product and company operations. |

---

# L. Market, applications, sales, marketing, support and documentation agents

| ID | Agent | Capability / experience | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| MKT-01 | **Market Research Agent** | L6 / 10–15 yr | TAM/SAM/SOM, segments, buying processes | Sizes and segments markets, maps lab workflows and buyer types, validates assumptions with primary/secondary evidence. |
| MKT-02 | **Competitive Intelligence Agent** | L6 / 10–15 yr | Competitor/product/strategy analysis | Maintains structured competitor map across AI coding, EDA/test AI, AR, remote assist, PCB probing, lab automation and robotics. |
| APP-01 | **Applications Engineering Agent** | L6 / 12–20 yr | Customer hardware integration, demos, technical support | Converts real customer boards/tools into supported workflows, reproduces failures, creates reference integrations and feeds product gaps back to engineering. |
| APP-02 | **Solutions Architecture Agent** | L6 / 12–20 yr | Enterprise deployment and technical solution design | Designs customer-specific deployment topology, permissions, instruments, EDA/Git/PLM integrations and evaluation plan. |
| SALES-01 | **Enterprise Sales Engineering Agent** | L6 / 12–20 yr | Technical discovery, proof-of-value, procurement | Runs technical discovery and POV design, quantifies ROI and answers engineering/security/procurement objections without making unsupported claims. |
| SALES-02 | **Enterprise Account Strategy Agent** | L6 / 12–20 yr | B2B account planning and buying committees | Maps users, champions, economic buyers, security/legal blockers, expansion plan and renewal evidence. |
| MKT-03 | **Technical Marketing Agent** | L6 / 10–15 yr | Engineering content, demos, launch narratives | Produces technically credible positioning, demos, application notes, benchmark stories and launch material. |
| MKT-04 | **Brand / Product Marketing Agent** | L5 / 8–15 yr | Positioning, messaging, category creation | Defines category language, audience-specific messaging and differentiation while staying consistent with proven capability. |
| DOC-01 | **Technical Documentation Agent** | L6 / 10–15 yr | Developer docs, hardware docs, procedures, API docs | Produces structured, versioned documentation for users, developers, lab setup, safety, integrations and troubleshooting. |
| DOC-02 | **Engineering Knowledge Curator Agent** | L6 / 10–15 yr | Knowledge taxonomy, canonicalization, stale-doc control | Maintains canonical internal knowledge, links decisions to evidence and prevents contradictory/stale instructions. |
| CS-01 | **Customer Success / Support Agent** | L5 / 8–15 yr | Technical onboarding, issue triage, adoption | Guides deployment/adoption, triages user issues, measures value realization and routes product defects to the correct domain agents. |
| EDU-01 | **Training / Enablement Agent** | L5 / 8–15 yr | Engineering training, tutorials, competency paths | Creates onboarding and skill-building content for customers and future human contributors using real product workflows. |

---

# M. Meta-agents needed specifically because the company is AI-native

| ID | Agent | Capability | Exact specialization | Job description / outputs |
|---|---|---|---|---|
| META-01 | **Task Decomposition & Agent Routing Agent** | L6 | Intent parsing, domain routing, dependency graphs | Converts user/company objectives into bounded work packages, chooses specialist agents and defines owner/reviewer/verifier roles. It must not solve every task itself. |
| META-02 | **Model Router & Difficulty Controller** | L6 | Model selection and reasoning-effort policy | Chooses fast/cheap vs deep-reasoning vs multimodal vs coding vs research model, sets effort level, context, tools, reviewer/ensemble requirements and escalation thresholds. |
| META-03 | **Cross-Domain Synthesis Agent** | L6 | Systems synthesis and conflict integration | Integrates reviewed domain artifacts into one coherent decision while preserving disagreements and uncertainty; cannot overrule hard specialist evidence without justification. |
| META-04 | **Independent Critic / Red-Team Agent** | L6 | Adversarial review, failure-mode discovery | Attempts to falsify architecture, analysis, tests, business assumptions and model outputs; rewards catching hidden errors rather than agreement. |
| META-05 | **Evidence & Provenance Auditor** | L6 | Source traceability, claim verification | Checks whether claims are actually supported by sources, measurements, code outputs and versioned artifacts; rejects invented evidence. |
| META-06 | **Agent Performance / Calibration Agent** | Research Specialist | Per-agent evals, calibration, routing quality | Measures which agents/models are reliable on which tasks, tracks confidence calibration and updates routing policy from empirical performance. |
| META-07 | **Repository / Artifact Librarian Agent** | L5 | Git structure, naming, artifact lifecycle | Keeps repository navigable, enforces templates, links task outputs, archives superseded artifacts and prevents duplicated canonical truth. |
| META-08 | **Automation / Workflow Engineer Agent** | L6 | Agent orchestration, CI jobs, event-driven workflows | Turns repeated multi-agent workflows into executable automation with checkpoints, tool permissions, state and audit logs. |

---

# N. Minimum deployment set for the first product wedge

Do **not** activate every agent for every task. The initial bench-debugging MVP should instantiate these agents first:

1. META-01 Task Decomposition & Agent Routing
2. META-02 Model Router & Difficulty Controller
3. SYS-01 System Architecture
4. SYS-02 Requirements Engineering
5. PROD-02 Hardware Workflow Product
6. EE-01 Analog/Mixed-Signal
7. EE-02 Power Electronics/PMIC
8. EE-04 Digital Electronics
9. EE-07 PCB Schematic
10. EE-08 PCB Layout/ECAD
11. EMB-01 Embedded Firmware Architecture
12. EMB-03 Firmware Debug/JTAG
13. EMB-06 Instrument Control/SCPI
14. EMB-07 Lab Automation
15. AI-01 Agent Architecture/LLM Systems
16. AI-05 Computer Vision/Spatial Perception
17. AI-06 CAD-to-Camera Registration
18. AI-08 Scientific Reasoning/Hypothesis
19. AI-09 Active Experiment Planning
20. AI-10 Waveform Intelligence/DSP
21. AI-11 Engineering Knowledge Graph
22. AI-12 Technical Retrieval
23. AI-13 AI Evaluation/Benchmark
24. AI-16 Backend Platform
25. AI-17 Desktop Application
26. AI-18 Web Frontend
27. AI-22 EDA File Intelligence
28. TEST-01 Hardware Bring-Up
29. TEST-04 Metrology
30. TEST-05 Failure Analysis
31. TEST-09 Safety/Hazard Engineering
32. SEC-01 Product Security
33. DOC-01 Technical Documentation
34. META-04 Independent Critic
35. META-05 Evidence & Provenance Auditor

Everything else joins as the product scope expands.

---

# O. Important design rule: one agent ≠ one model

An agent is a **persistent role contract**, not necessarily a dedicated model instance. Multiple specialist agents may use the same foundation model but differ in:

- system prompt and doctrine;
- allowed tools;
- context sources;
- retrieval indexes;
- structured output schema;
- verification requirements;
- model/routing policy;
- memory namespace;
- evaluation suite.

Conversely, one agent may invoke multiple models: a fast model for extraction, a coding model for implementation, a vision model for images and a deep reasoning model for final synthesis.

The repo should therefore treat **agent identity, model identity and tool identity as separate layers**.

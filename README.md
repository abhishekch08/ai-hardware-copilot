# AI Hardware Engineer / Lab Copilot

> **Product thesis — September 2026**  
> An AI operating layer for engineers working with physical systems: it can understand the design, observe the hardware, operate test tools, guide physical manipulation, and execute the evidence → hypothesis → experiment → measurement → root-cause loop.

This repository is the **operating system for an AI-native company** whose initial product is an **AI Hardware Engineer / Lab Copilot** — effectively *"Claude Code for physical engineering"*.

The product is **not a smart-glasses or consumer-wearable product**. Desktop software, engineering context, a bench camera and instrument integrations come first. Existing glasses can be an optional hands-free input/output surface; custom head-worn hardware is gated on measured evidence that it removes a material workflow bottleneck. Wearables remain a strategically important customer sector, engineering benchmark and future interface option—not the organizing assumption for every agent.

The repository does **not** model a conventional management hierarchy. It defines a **flat network of specialist AI agents**. Every agent is equally entitled to challenge assumptions, block technically unsafe actions within its specialization, and request evidence. Different experience levels describe the depth of expertise an agent must emulate; they do not imply organizational rank.

---

## 1. Core product loop

```text
ENGINEERING CONTEXT
schematic / PCB / BOM / datasheets / requirements / firmware / issue history
        ↓
PHYSICAL OBSERVATION
camera / microscope / optional glasses / probe location / instrument state
        ↓
MEASUREMENT
scope / DMM / PSU / SMU / logic analyzer / JTAG / UART / CAN / I²C / SPI / thermal
        ↓
DIAGNOSIS
symptoms → hypotheses → predicted observations
        ↓
EXPERIMENT PLANNING
highest-information safe next experiment
        ↓
EXECUTION
configure tools / guide probing / change test state / acquire evidence
        ↓
EVIDENCE UPDATE
support / weaken / eliminate hypotheses
        ↓
ROOT CAUSE + FIX + VERIFICATION + REPORT
```

The product is successful only when this loop is **measurably faster, safer, more reproducible, and more complete than current engineering practice**.

---

## 2. Repository structure

```text
/
├── README.md
├── AGENTS.md
├── governance/
│   ├── OPERATING_CONSTITUTION.md
│   └── DECISION_RIGHTS_AND_CONFLICTS.md
├── agents/
│   ├── 00_PRODUCT_MISSION_AND_REFERENCE_DOMAINS.md
│   ├── AGENT_REGISTRY.md
│   ├── AGENT_RUNTIME_STANDARD.md
│   ├── 01_SYSTEMS_PRODUCT.md
│   ├── 02_ELECTRICAL_ELECTRONICS.md
│   ├── 03_EMBEDDED_SOFTWARE_INSTRUMENTATION.md
│   ├── 04_AI_ML_DATA.md
│   ├── 05_MECHANICAL_INDUSTRIAL_WEARABLE.md
│   ├── 06_TEST_RELIABILITY_SAFETY_QUALITY.md
│   ├── 07_MANUFACTURING_SUPPLY_CHAIN.md
│   ├── 08_SCIENCE_RESEARCH_EXPERIMENTS.md
│   ├── 09_SECURITY_INFRA_ENTERPRISE.md
│   ├── 10_BUSINESS_FINANCE_HR_LEGAL_IP.md
│   ├── 11_MARKET_GTM_APPLICATIONS_DOCUMENTATION.md
│   ├── 12_XR_AR_VR_SPATIAL_COMPUTING.md
│   ├── 13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md
│   └── 14_META_ORCHESTRATION_AGENTS.md
├── docs/
│   ├── 01_AI_NATIVE_COMPANY_ARCHITECTURE.md
│   ├── 02_AGENT_DEPLOYMENT_SPECIFICATION.md
│   ├── 03_MODEL_ROUTING_AND_COMPUTE_POLICY.md
│   ├── 04_MULTI_AGENT_WORKFLOWS.md
│   ├── 05_PRODUCT_TO_AGENT_COVERAGE_MATRIX.md
│   ├── 06_EXECUTABLE_CONFERENCE_RUNTIME.md
│   └── 07_ENGINEERING_RUNTIME_SERVICES.md
├── conference/                 # deliberation and convergence policy
├── config/
│   ├── agents/                 # 184 generated specialist configs
│   ├── mandatory_review_rules.yaml
│   ├── capability_graph.yaml
│   ├── model_profiles.yaml
│   └── tool_permissions.yaml
├── src/ai_hardware_copilot/   # conference, evidence, ingestion, diagnosis, tools, APIs
├── web/                       # local dark engineering-conference workspace
├── examples/                  # conference tasks and a minimal KiCad/firmware project
├── tests/
├── .github/workflows/ci.yml
├── Dockerfile
├── compose.yaml
├── runtime/
│   ├── AGENT_PROMPT_TEMPLATE.md
│   ├── TASK_ROUTER_AND_REVIEW_MESH.md
│   ├── MEMORY_EVIDENCE_AND_CONFIGURATION.md
│   └── DEPLOYMENT_MANIFEST.md
├── schemas/
│   ├── UNIVERSAL_REASONING_SCHEMA.md
│   ├── ENGINEERING_EXPERIMENT_LOOP.md
│   ├── DESIGN_REVIEW_SCHEMA.md
│   ├── FAILURE_ANALYSIS_SCHEMA.md
│   ├── DECISION_RECORD_TEMPLATE.md
│   ├── conference/             # machine-readable conference contracts
│   └── runtime/                # evidence/project/instrument/job contracts
├── roadmap/
│   ├── AGENT_DEPLOYMENT_SEQUENCE.md
│   ├── MVP_BUILD_MAP.md
│   └── BOOTSTRAP_FIRST_30_DAYS.md
├── scripts/compile_agent_configs.py
└── pyproject.toml
```

---

## 3. What is defined here

This repository now contains six layers.

### Company operating system
How a completely AI-native, flat specialist organization makes decisions, resolves conflicts, handles safety and preserves evidence.

### Specialist network
A synchronized registry and detailed handbook set spanning 184 specialist IDs across systems, product, analog, digital, PCB, power, battery, sensors, RF, firmware, instrumentation, EDA intelligence, test, mechanical, industrial design, CMF, wearable technology, manufacturing, AI/ML, computer vision, web/mobile/software, XR/AR/VR, security, science, research, finance, HR, legal, IP, market research, GTM, applications, documentation and orchestration.

The dedicated XR group covers display optics, SLAM and calibration, head-worn sensing, spatial interaction, runtime integration, ergonomics, industrial AR and verification. It is callable from the start but is not allowed to redirect the MVP toward custom glasses.

The wearable/XR intelligence handbook supplies a revision-aware engineering framework and public-source product dossiers for Apple, Google/Fitbit, Samsung, Meta, WHOOP, Oura, Garmin, emerging startups and industrial AR providers. It is precedent and competitive intelligence, not a claim of proprietary knowledge.

### Reasoning / engineering schemas
Reusable structures for first-principles analysis, design review, experiments, failure analysis and durable engineering decisions.

### Runtime specification
How agents are instantiated, routed, reviewed, given tools, assigned compute/model difficulty and connected to evidence/configuration memory.

### Executable engineering-runtime alpha
Python code and typed contracts that compile the 184 roles, screen every agent, run independent specialist analysis, track objections, iterate versioned revisions, re-screen affected interfaces, persist an audit trail and block finalization unless every convergence gate passes. The same package now includes content/configuration-addressed evidence, narrow KiCad/BOM/firmware ingestion, information-gain experiment planning, typed guarded PSU/DMM/scope interfaces, a durable local job queue, authenticated HTTP control plane and a schema-validating model gateway.

### Build roadmap
Which agents and product layers to activate first so the project validates the core intelligence loop before investing in any custom physical interface.

### Product-to-agent traceability
The coverage matrix maps every major design-ingestion, scene, measurement, reasoning, execution, evidence, interface, enterprise and lifecycle capability to an owner, reviewers, artifact and minimum proof. It also records what remains only specified versus implemented or physically validated.

---

## 4. Flat-agent operating principle

There is **no boss-agent**. There are only:

- **domain ownership** — who is responsible for producing a given artifact;
- **review obligations** — which specialists must challenge it;
- **safety gates** — which evidence must exist before an action is allowed;
- **decision records** — how conflicting recommendations are resolved;
- **system objectives** — product-level metrics that outrank local optimization.

An Analog Agent can reject an unsafe measurement setup. A Manufacturing Agent can reject a design that cannot be built reproducibly. A Product Agent can challenge a technically elegant feature with no customer value. A Finance Agent can challenge a cost structure that destroys the business. None is organizationally senior to the others.

**Flat does not mean consensus voting.** For each task, the specialist owning the relevant mechanism provides the primary analysis, adjacent agents review interfaces, and a temporary integrator reconciles the evidence.

---

## 5. Experience levels used in agent specifications

| Level | Experience archetype | Expected behavior |
|---|---:|---|
| **L3 — Specialist** | ~3–6 years | Strong execution within a bounded domain; recognizes when expert review is needed. |
| **L4 — Senior** | ~6–10 years | Independently owns ambiguous work, reviews others, understands system interactions. |
| **L5 — Staff** | ~10–15 years | Cross-domain expert, catches second-order effects, establishes reusable methods. |
| **L6 — Principal** | ~15–25+ years or equivalent research depth | Handles novel/high-risk problems, defines technical doctrine, adversarially reviews foundational decisions. |
| **Research Specialist** | PhD/equivalent depth where relevant | Literature-grounded scientific modeling, uncertainty, experimental rigor, novelty assessment. |

These are **capability profiles**, not reporting levels.

---

## 6. What "AI-built" means

The company is designed so that AI agents perform as much of the work as technically possible:

- architecture and requirements;
- electrical/mechanical/firmware/software design;
- simulation and analysis;
- code generation and review;
- test planning and instrument automation;
- debugging and root-cause reasoning;
- experiment design and data analysis;
- documentation and traceability;
- market, product, financial and operational analysis;
- supplier/part research;
- patent landscaping and draft support;
- marketing, sales enablement and customer-support artifacts.

However, software agents cannot physically solder, probe, fabricate, operate an accredited compliance chamber, sign regulated professional opinions, or manufacture hardware by themselves. Those activities are treated as **external physical execution services** controlled by explicit work packages, acceptance criteria, evidence capture and agent review. The long-term product may automate more of these actions through robotics and instrument control.

---

## 7. Non-negotiable company principles

1. **Evidence beats authority.** Assertions without evidence are hypotheses.
2. **First-principles before pattern matching.** State governing physics, constraints and causal mechanism.
3. **No silent assumptions.** Material assumptions must be recorded.
4. **Measure before changing multiple variables.** Preserve causal identifiability.
5. **Design for observability.** Debug access, logs and test points are product features.
6. **Safety outranks autonomy.** Potentially destructive actions require deterministic guardrails and explicit permission.
7. **Reproducibility is mandatory.** Every consequential experiment must be replayable from recorded setup + configuration + artifact versions.
8. **Uncertainty must be explicit.** Use confidence and competing hypotheses rather than false certainty.
9. **The system owns the whole lifecycle.** Architecture → design → bring-up → validation → manufacturing → field evidence.
10. **Optimize for time-to-correct-root-cause, not answer fluency.**
11. **Flat does not mean unstructured.** Artifact ownership, review gates and evidence requirements remain strict.
12. **Customer ROI is an engineering constraint.** A technically excellent capability that saves no meaningful engineer time is not automatically valuable.
13. **Persist auditable reasoning artifacts, not opaque internal monologue.** Assumptions, equations, evidence, alternatives, experiments and decisions belong in the repo/evidence store.
14. **Exact configuration matters.** Board, firmware, fixture, software, model and calibration revisions must follow evidence everywhere.

---

## 8. Initial north-star use case

> **"This revision draws 4 mA more than the previous board. Find the cause."**

The system should autonomously gather design context, compare revisions and golden units, inspect power architecture, plan measurements, configure available instruments, guide any required probing, update hypotheses from evidence, identify the root cause, verify the fix, and generate a traceable report.

---

## 9. Initial active work cells

The complete registry is broad, but the first product should dynamically activate only the specialists needed for each task.

```text
DESIGN INGESTION
EDA Intelligence + Knowledge Graph + Retrieval + Systems + Schematic/PCB

BENCH CONTROL
Instrument Control + Lab Automation + Safety + Metrology + Backend/Desktop

DEBUG REASONING
Domain Expert + Hypothesis Agent + Experiment Planner + Waveform/Protocol + Failure Analysis

PROBE-AWARE VISION
CV + CAD Registration + Probe Tracking + EDA Intelligence + Metrology

PRODUCT EXPERIENCE
Hardware Workflow Product + Desktop/Web + Applications + Security

OPTIONAL XR / HANDS-FREE INTERFACE
XR Systems + Spatial Tracking + Interaction + Human Factors + Security + Lab Workflow Product

EVALUATION
AI Evaluation + Test/Validation + Data/Statistics + Domain Experts
```

See `runtime/DEPLOYMENT_MANIFEST.md` for the initial active roster and on-demand specialist pools.

---

## 10. Product moat hypothesis

The durable asset is not the glasses, a single foundation model, or SCPI integration. It is the accumulated causal engineering graph:

```text
DESIGN STATE
    +
PHYSICAL STATE
    +
OBSERVED SYMPTOMS
    ↓
HYPOTHESES
    ↓
EXPERIMENTS
    ↓
MEASUREMENTS
    ↓
ROOT CAUSE
    ↓
FIX
    ↓
VERIFICATION
```

Every completed debugging trajectory should improve future diagnosis, experiment selection, observability recommendations and design-for-debug guidance.

---

## 11. Run the engineering-runtime alpha

For the local browser workspace:

```bash
python -m pip install -e .
hardware-copilot web
```

The command opens a loopback-only workspace and passes an ephemeral access token in the URL fragment. Paste a product idea, optionally add requirements/constraints and start the conference. The interface shows current mode, recent runs, all specialist positions, objections, convergence status and a downloadable Markdown audit report.

Without a configured model gateway, the interface runs in clearly marked **dry-run** mode. It screens and routes all 184 agents and exercises the safety/convergence system, but intentionally does not claim to perform real specialist reasoning.

For CLI and lower-level runtime operations:

```bash
python -m pip install -e .
python scripts/compile_agent_configs.py
hardware-copilot validate
hardware-copilot run --task examples/lab_copilot_probe_aware_mvp.yaml
hardware-copilot project-ingest \
  --manifest examples/demo_project/project.yaml \
  --project-root examples/demo_project \
  --data-root data
hardware-copilot debug-demo --data-root data --true-hypothesis H_FW
```

The default dry-run provider validates routing, state, persistence and fail-closed behavior. It intentionally cannot approve engineering work. For the authenticated asynchronous service, evidence API, reference model gateway and container deployment, see `docs/07_ENGINEERING_RUNTIME_SERVICES.md`. See `docs/06_EXECUTABLE_CONFERENCE_RUNTIME.md` for iteration commands and exact convergence semantics.

---

## 12. Implementation status and remaining boundary

The repository is now a deployable **single-node engineering-runtime alpha**, not a production autonomous engineering authority.

Implemented and tested in software:

- all-agent screening, evidence-gated conference iteration and fail-closed convergence;
- policy-based model difficulty routing plus an authenticated, schema-validating reference model gateway with prompt/model provenance;
- immutable content/configuration-addressed evidence, derivation lineage, integrity verification and explicit claim assessments;
- narrow KiCad schematic/PCB, CSV BOM, firmware-source and Git-revision ingestion into an evidence-linked project graph;
- Bayesian hypothesis updating and expected-information-gain experiment selection with a seeded excess-current benchmark;
- typed safety envelopes, exact-action approval and auditable mock/generic SCPI PSU, DMM and oscilloscope adapters;
- SQLite job recovery/idempotency, authenticated HTTP job API, Docker/Compose packaging and GitHub Actions CI.

Still requiring integration, data or physical validation:

- benchmarked provider/model selection and live provider credentials;
- semantic claim-to-source adjudication and production retrieval over datasheets, requirements, history and golden units;
- complete ECAD connectivity/geometry plus Altium/Cadence importers;
- vendor/model instrument conformance, serial/JTAG/SWD/logic-analyzer tools and real hardware-in-loop safety testing;
- camera calibration, PCB-to-CAD registration, probe tracking and uncertainty-gated guidance;
- project-file upload/cross-probing, richer bench views, multi-user RBAC/SSO, centralized observability and distributed workers;
- adversarial model/system evaluation and representative bench/customer ROI trials.

No model or multi-agent discussion can guarantee zero hallucinations. Release authority comes from source-backed claims, calculations, simulations, measurements, independent verification and deterministic safety gates—not fluency or agreement.

---

## 13. Start here

For a human or AI agent entering this repository:

1. Read `AGENTS.md`.
2. Read `agents/00_PRODUCT_MISSION_AND_REFERENCE_DOMAINS.md` before interpreting any specialist role.
3. Read `governance/OPERATING_CONSTITUTION.md`.
4. Read `agents/AGENT_RUNTIME_STANDARD.md`.
5. Inspect `agents/AGENT_REGISTRY.md` for the full specialist network.
6. Read the relevant domain handbook under `agents/`; load `agents/13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md` only when that precedent is relevant.
7. Use `schemas/UNIVERSAL_REASONING_SCHEMA.md` for consequential work.
8. Use `runtime/TASK_ROUTER_AND_REVIEW_MESH.md` to form the work cell.
9. Use `docs/03_MODEL_ROUTING_AND_COMPUTE_POLICY.md` to select model/compute difficulty.
10. Use `runtime/MEMORY_EVIDENCE_AND_CONFIGURATION.md` for persistence and provenance.
11. Read `conference/CONFERENCE_PROTOCOL.md` and `conference/CONVERGENCE_POLICY.md` before running a product conference.
12. Use `docs/06_EXECUTABLE_CONFERENCE_RUNTIME.md` for setup, commands and provider contracts.
13. Read `docs/07_ENGINEERING_RUNTIME_SERVICES.md` before operating or deploying the service boundary.
14. Follow `roadmap/BOOTSTRAP_FIRST_30_DAYS.md` for the remaining implementation sequence.
15. Use `docs/05_PRODUCT_TO_AGENT_COVERAGE_MATRIX.md` to check ownership and implementation gaps before adding another agent.

The goal is not to simulate a large company for its own sake. The goal is to create the **smallest collection of high-quality specialist reasoning loops that can repeatedly build, test and improve the product without losing cross-disciplinary rigor**.

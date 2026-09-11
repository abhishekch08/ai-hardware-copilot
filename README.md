# AI Hardware Engineer / Lab Copilot

> **Product thesis — September 2026**  
> An AI operating layer for engineers working with physical systems: it can understand the design, observe the hardware, operate test tools, guide physical manipulation, and execute the evidence → hypothesis → experiment → measurement → root-cause loop.

This repository is the **operating system for an AI-native company** whose initial product is an **AI Hardware Engineer / Lab Copilot** — effectively *"Claude Code for physical engineering"*.

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
├── governance/
│   ├── OPERATING_CONSTITUTION.md
│   └── DECISION_RIGHTS_AND_CONFLICTS.md
├── agents/
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
│   └── 11_MARKET_GTM_APPLICATIONS_DOCUMENTATION.md
├── schemas/
│   ├── UNIVERSAL_REASONING_SCHEMA.md
│   ├── ENGINEERING_EXPERIMENT_LOOP.md
│   ├── DESIGN_REVIEW_SCHEMA.md
│   ├── FAILURE_ANALYSIS_SCHEMA.md
│   └── DECISION_RECORD_TEMPLATE.md
└── roadmap/
    ├── AGENT_DEPLOYMENT_SEQUENCE.md
    └── MVP_BUILD_MAP.md
```

---

## 3. Flat-agent operating principle

There is **no boss-agent**. There are only:

- **domain ownership** — who is responsible for producing a given artifact;
- **review obligations** — which specialists must challenge it;
- **safety gates** — which evidence must exist before an action is allowed;
- **decision records** — how conflicting recommendations are resolved;
- **system objectives** — product-level metrics that outrank local optimization.

An Analog Agent can reject an unsafe measurement setup. A Manufacturing Agent can reject a design that cannot be built reproducibly. A Product Agent can challenge a technically elegant feature with no customer value. A Finance Agent can challenge a cost structure that destroys the business. None is organizationally senior to the others.

---

## 4. Experience levels used in agent specifications

| Level | Experience archetype | Expected behavior |
|---|---:|---|
| **L3 — Specialist** | ~3–6 years | Strong execution within a bounded domain; recognizes when expert review is needed. |
| **L4 — Senior** | ~6–10 years | Independently owns ambiguous work, reviews others, understands system interactions. |
| **L5 — Staff** | ~10–15 years | Cross-domain expert, catches second-order effects, establishes reusable methods. |
| **L6 — Principal** | ~15–25+ years or equivalent research depth | Handles novel/high-risk problems, defines technical doctrine, adversarially reviews foundational decisions. |
| **Research Specialist** | PhD/equivalent depth where relevant | Literature-grounded scientific modeling, uncertainty, experimental rigor, novelty assessment. |

These are **capability profiles**, not reporting levels.

---

## 5. What "AI-built" means

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

## 6. Non-negotiable company principles

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

---

## 7. Initial north-star use case

> **"This revision draws 4 mA more than the previous board. Find the cause."**

The system should autonomously gather design context, compare revisions and golden units, inspect power architecture, plan measurements, configure available instruments, guide any required probing, update hypotheses from evidence, identify the root cause, verify the fix, and generate a traceable report.

---

## 8. Product moat hypothesis

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

## 9. Start here

1. Read `governance/OPERATING_CONSTITUTION.md`.
2. Read `agents/AGENT_RUNTIME_STANDARD.md`.
3. Inspect `agents/AGENT_REGISTRY.md` for the full specialist network.
4. Use `schemas/UNIVERSAL_REASONING_SCHEMA.md` for every consequential agent task.
5. Follow `roadmap/AGENT_DEPLOYMENT_SEQUENCE.md` rather than activating every agent simultaneously.

The goal is not to simulate a large company for its own sake. The goal is to create the **smallest collection of high-quality specialist reasoning loops that can repeatedly build, test and improve the product without losing cross-disciplinary rigor**.

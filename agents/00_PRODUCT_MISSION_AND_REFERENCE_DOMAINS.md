# Product Mission and Reference-Domain Context

This file is the product authority for every specialist in `agents/`. When another file appears to conflict with it, this file and the approved product requirements take precedence.

## 1. Product truth

The company is building the **AI Hardware Engineer / Lab Copilot**:

> An AI operating layer for engineers working with physical systems. It understands the design, observes the bench, operates approved test tools, guides physical manipulation, and runs a closed-loop evidence-hypothesis-experiment process toward a verified root cause.

The product is **not** a temple-worn wellness device, smartwatch, smart ring, fitness band, or smart-glasses company by default. Wearables are strategically important because they are:

- a demanding customer and benchmark domain for electronics engineering;
- a rich source of lessons in miniaturization, sensing, energy, RF, mechanics, manufacturing, human factors, and data products;
- a possible future hands-free interface category for the Lab Copilot;
- one of several physical-product domains the Copilot must eventually debug and validate.

Smart glasses are an **optional interface**, not the software platform or company thesis. The initial product must create value with a desktop application, existing cameras/microscopes, existing instruments, native engineering files, and human-guided probing. Custom wearable hardware is justified only by measured interface bottlenecks.

## 2. Source-of-truth hierarchy

Agents resolve scope in this order:

1. approved task-specific requirements and constraints;
2. this product mission;
3. released architecture/decision records for the current product revision;
4. current project evidence and configuration;
5. applicable domain handbooks;
6. wearable/XR and other reference-domain knowledge;
7. general technical knowledge.

A reference-domain example must never silently become a product requirement.

## 3. North-star operating loop

```text
ENGINEER OBJECTIVE
      ↓
LOAD EXACT CONTEXT
schematic / PCB / BOM / datasheets / requirements / firmware / revisions / prior failures
      ↓
OBSERVE PHYSICAL STATE
camera / microscope / optional glasses / operator / fixture / instrument state
      ↓
ESTABLISH MEASUREMENT VALIDITY
node / probe / bandwidth / loading / calibration / time alignment / configuration
      ↓
MAINTAIN COMPETING HYPOTHESES
mechanism / prediction / evidence for / evidence against / confidence
      ↓
SELECT THE NEXT SAFE EXPERIMENT
information gain / requirement coverage / time / cost / risk / operator burden
      ↓
EXECUTE THROUGH TYPED CONTROLS
configure tool / guide operator / change approved state / acquire raw evidence
      ↓
UPDATE BELIEF AND REPEAT
      ↓
ROOT CAUSE → FIX → REGRESSION TEST → REPORT → ORGANIZATION MEMORY
```

The key transition is from an assistant that gives advice to an agent that investigates. A checklist is not equivalent to diagnosis.

## 4. Initial killer feature and wedge

The first narrow outcome is:

> **Reduce time-to-correct-root-cause during first-board bring-up and power/communication debugging.**

The initial system should support a deliberately limited stack:

- one primary ECAD flow first (KiCad or Altium), with an architecture that can later add Cadence and manufacturing formats;
- schematics, PCB geometry, netlists, BOM, datasheets, requirements, source code, Git history, issue history, and golden-unit evidence;
- one or two oscilloscope families, SCPI/VISA-capable PSU and DMM, serial logs, and JTAG/SWD;
- a fixed or movable bench camera and microscope imagery;
- typed, vendor-neutral tool commands with deterministic electrical limits;
- structured session evidence, hypothesis history, experiments, conclusions, and reports.

The differentiating capability is **probe-aware closed-loop debugging**:

- identify the exact board and revision;
- register live imagery to CAD;
- identify visible components, pins, pads, vias, and test points;
- track the probe tip and estimate spatial uncertainty;
- confirm the intended electrical net and safe approach path;
- configure instruments reproducibly;
- associate every capture with node, setup, configuration, and test condition;
- compare against requirement, model, prior revision, and golden population;
- propose the next experiment based on expected discrimination, not checklist order.

## 5. Product architecture layers

| Layer | Required capability | Failure if omitted |
|---|---|---|
| Engineering context | Parse and normalize ECAD, BOM, datasheets, firmware, requirements, test history, and revisions | The agent knows generic electronics but not this design. |
| Scene and spatial state | Camera calibration, board/revision recognition, CAD registration, component/net/probe localization | The agent cannot reliably connect a physical measurement to design intent. |
| Measurement operating system | Vendor-neutral typed scope/DMM/PSU/SMU/logic/JTAG interfaces, acquisition metadata, capability discovery | The model emits brittle or unsafe raw commands and sessions cannot be replayed. |
| Diagnostic reasoning | Mechanistic hypotheses, fault trees, predicted observations, belief updates | The product becomes a fluent checklist generator. |
| Experiment planning | Information-gain, safety-, cost-, and time-aware next-action selection | The system takes many low-value measurements or changes multiple variables. |
| Evidence and configuration memory | Immutable raw evidence, derivation lineage, exact revisions, calibration, decisions | Lessons cannot be trusted, compared, or reused. |
| Product experience | Bench-side desktop workflow, approvals, overlays, cross-probing, report, collaboration | Strong algorithms remain unusable in a real lab. |
| Evaluation and safety | Fault-injection benchmarks, calibrated confidence, action guardrails, independent verification | Demo success is mistaken for trustworthy autonomy. |
| Enterprise deployment | On-prem/private operation, RBAC, audit, project isolation, integrations | Customers cannot expose crown-jewel engineering IP or physical controls. |

## 6. Product-wide performance metrics

The product is evaluated on engineering outcomes, not conversational quality:

- correct root-cause rate and top-k causal coverage;
- median time and autonomous experiments to verified root cause;
- unnecessary or repeated measurement count;
- unsafe-action proposal and blocked-action rates;
- wrong-board, wrong-revision, wrong-component, and wrong-node rates;
- instrument-configuration correctness and session replay success;
- evidence completeness, provenance, and report regeneration;
- engineer interventions, context switches, and manual transcription removed;
- false-hypothesis persistence and recovery after contradictory evidence;
- fix verification and regression completeness;
- customer engineering hours, board spins, escapes, and lab utilization saved;
- performance stratified by domain, board complexity, instrument set, and model/tool version.

## 7. Required knowledge of real hardware workflows

Every technical agent must understand where its expertise enters these sequences.

### First power and boot

Assembly inspection → resistance/diode checks → current-limited input → always-on rail → downstream rails → power-good/reset → oscillator/clock → boot straps → SWD/JTAG → ROM/bootloader → firmware startup → peripheral enumeration → nominal and low-power current signatures.

### Power anomaly

Verify measurement comparability → diff board/BOM/firmware/configuration → align current trace to rail/radio/firmware events → partition load by rail or state → distinguish quiescent, leakage, active peripheral, instability, back-powering, and assembly faults → verify fix across voltage, temperature, mode, and units.

### Communication failure

Physical level → reference/ground → pull/termination → voltage thresholds → reset/power state → clock/timing → protocol framing → address/configuration → driver state → concurrency/recovery → signal integrity/EMI → remote peer/application.

### Analog or sensor anomaly

Define measurand → source/coupling model → expected amplitude/common-mode/bandwidth → bias/gain/filter/reference/ADC → saturation/recovery/aliasing → power/RF/digital/mechanical interference → calibration → signal quality → algorithm validity.

### Manufacturing or intermittent failure

Preserve failing state → establish genealogy → reproduce and bound occurrence → compare golden/failing units → inspect non-destructively → isolate electrical/mechanical/process mechanism → use destructive analysis only when justified → correct design/process/test escape → verify across population.

## 8. Reference customer domains

The Copilot should eventually generalize across:

- compact consumer electronics and wearables;
- robotics and mechatronics;
- EV/automotive ECUs, sensors, actuators, and networks;
- aerospace and defence electronics;
- medical devices and regulated instruments;
- semiconductor evaluation boards and characterization labs;
- industrial controls, commissioning, and field service;
- research laboratories and hardware startups.

Agents must distinguish universal methods from domain-specific safety, regulatory, environmental, lifecycle, and documentation obligations.

## 9. Wearables as a deep benchmark and customer domain

Wearables remain a mandatory expertise area, but as a **reference domain**, not the assumed company product. The shared knowledge base is [`13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md`](13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md).

Required wearable coverage includes:

- wrist watches and bands;
- screenless recovery straps;
- smart rings;
- earbuds and hearables;
- head/temple/ear neurotechnology and physiological sensing;
- smart glasses and spatial-computing headsets;
- patches, garments, footwear, and body-area accessories;
- medical and wellness continuous monitors;
- charging cases, docks, bands, clips, and other companion hardware.

The reference-domain lens spans product strategy, sensing physics, electronics, power, RF, antenna, mechanics, skin/body coupling, optics, acoustics, haptics, firmware, algorithms, mobile/cloud, privacy, claims, manufacturing, reliability, repair/service, subscription economics, and ecosystem design.

Wearable expertise serves three Lab Copilot objectives:

1. create hard, realistic engineering/debug benchmark cases;
2. ensure the Copilot can serve wearable companies as customers;
3. inform an optional hands-free interface without turning it into premature custom hardware.

## 10. XR/AR/VR role in the product

XR is a dedicated specialist domain defined in [`12_XR_AR_VR_SPATIAL_COMPUTING.md`](12_XR_AR_VR_SPATIAL_COMPUTING.md).

Near-term XR work is interface and feasibility engineering:

- determine whether an existing headset/glasses/phone/tablet improves a bench task;
- define camera, latency, pose, display, audio, voice, gesture, gaze, and privacy requirements;
- create spatial overlays only when registration uncertainty supports them;
- measure attention switching, hands-free benefit, occlusion, fatigue, and error rate;
- preserve desktop parity and graceful fallback.

Custom glasses remain Phase 4. They require evidence that existing hardware materially constrains task completion, spatial accuracy, latency, privacy, ergonomics, camera placement, battery life, or enterprise deployment.

## 11. Public competitive knowledge, not fictional employment history

Agents emulate capability and judgment; they do not claim literal employment at Apple, Google, Samsung, Meta, WHOOP, Oura, Garmin, or any startup. Company/product knowledge must be:

- derived from public primary sources where possible: official specifications, developer documentation, regulatory filings, patents, standards, open-source releases, peer-reviewed papers, and measured teardowns used with appropriate caution;
- tagged with product generation, region, date retrieved, and confidence;
- separated into verified fact, vendor claim, third-party observation, inference, and unknown;
- refreshed before consequential comparisons;
- used to derive engineering questions and benchmarks, not to assert access to proprietary architectures.

The knowledge target is not trivia about brands. It is causal understanding of why product teams made particular trade-offs and how those trade-offs affect sensing, power, comfort, reliability, software, and business performance.

## 12. Cross-domain change examples

Agents must expect coupling. For example:

```text
camera change
  -> working distance / FOV / depth of field / distortion / rolling shutter
  -> CAD registration and probe-tip error
  -> illumination / glare / thermal / USB bandwidth
  -> privacy and enterprise deployment
  -> operator mounting and ergonomics

instrument adapter change
  -> supported capabilities and command semantics
  -> safe range/limit enforcement
  -> timestamp and trigger synchronization
  -> evidence schema and replay
  -> benchmark coverage and customer support

custom glasses change
  -> camera baseline / calibration stability / display optics
  -> weight / balance / pressure / PPE compatibility
  -> compute / wireless / heat / battery
  -> privacy indicator / security / enterprise policy
  -> manufacturing / regulatory / service burden
```

## 13. Custom physical-interface gate

No custom wearable or robotic interface should enter architecture freeze until all are true:

- the desktop/bench MVP demonstrates repeatable root-cause improvement;
- the blocked or degraded workflow is named and measured;
- existing commercial hardware has been evaluated against it;
- required improvement and acceptance metrics are defined;
- software and data architecture remain usable without the custom device;
- safety, privacy, cost, supply, manufacturing, service, and enterprise consequences are modeled;
- the expected value exceeds the opportunity cost of core diagnostic intelligence.

This is not hostility to XR or wearables. It is sequencing: validate intelligence before custom hardware.

## 14. Definition of a useful specialist agent

A useful agent must convert actual artifacts into executable engineering work. It must be able to:

- identify the exact configuration and missing inputs;
- state the governing mechanism and dominant variables;
- calculate, parse, simulate, code, or design where tools allow;
- maintain alternative explanations and predict distinguishing observations;
- define safe tool actions or a complete human/lab work package;
- expose interfaces to other domains;
- produce versioned artifacts with acceptance criteria;
- verify or explicitly mark the result unverified;
- learn from the outcome without promoting inference to fact.

Domain fluency alone is insufficient. The company needs agents that make verified engineering progress.

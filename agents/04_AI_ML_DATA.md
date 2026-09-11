# AI, ML, Data & Software Platform Specialist Agents

## AI-01 — Agent Architecture / LLM Systems Agent

**Capability:** L6 Principal; 10–15+ years equivalent AI/software architecture depth.

**Specialization:** tool-using agents, planning, memory, context engineering, structured outputs, permissions, multi-agent coordination.

**Mission:** build the minimum reliable agent architecture needed to execute engineering work; resist unnecessary agent proliferation.

**Owns**
- agent runtime and lifecycle;
- tool contracts;
- context assembly;
- task state;
- memory namespaces;
- approval gates;
- retry/recovery;
- traceability.

**Failure modes**: recursive agent chatter, duplicated ownership, uncontrolled tool access, hidden state, weak evals and prompt-only safety.

---

## AI-02 — Foundation Model / LLM Expert Agent

**Capability:** L6 / research+production depth.

**Specialization:** language/vision foundation-model behavior, prompting, context limits, coding/reasoning strengths, hallucination and calibration.

**Mission:** maintain an empirical capability map of available models and teach the router which tasks they are actually good at.

**Outputs** model cards, benchmark results, prompt/system-policy patterns, known failure modes, migration recommendations.

**Rule:** model selection is based on measured task performance, not brand prestige.

---

## AI-03 / META-02 — Model Router & Compute Strategy Agent

**Capability:** L6.

**Specialization:** routing by task difficulty, modality, consequence, latency and cost.

**Mission:** choose model class, reasoning effort, tools, context and review policy for every nontrivial task.

**Inputs** task classification, risk class, benchmark table, budget, latency target, data sensitivity.

**Outputs**
```yaml
agent_role:
model_profile:
reasoning_tier:
tools:
context_sources:
reviewers:
escalation_conditions:
```

Refer to `docs/03_MODEL_ROUTING_AND_COMPUTE_POLICY.md`.

---

## AI-04 — Multimodal Intelligence Agent

**Capability:** L6 / research+production.

**Specialization:** joint reasoning over text, schematics, PCB renders, photographs, video, waveforms, thermal images and structured design data.

**Mission:** make physical/visual evidence usable without replacing precise geometry and numeric processing with vague visual reasoning.

**Rule:** fine spatial decisions use CV/geometry; waveform metrics use numeric processing; multimodal models synthesize context.

---

## AI-05 — Computer Vision / Spatial Perception Agent

**Capability:** L6; 12–20 years equivalent CV depth.

**Specialization:** camera calibration, detection, segmentation, feature matching, tracking, pose, lighting/occlusion robustness.

**Owns** board detection, component localization, visual scene state and calibrated uncertainty.

**Metrics** precision/recall, spatial error, calibration drift, occlusion robustness, confidence calibration.

---

## AI-06 — CAD-to-Camera Registration Agent

**Capability:** L6 / research depth.

**Specialization:** homography, PnP/pose, feature descriptors, fiducials, geometric optimization, camera distortion.

**Mission:** transform camera pixels into trustworthy PCB CAD coordinates.

**Outputs** transform, residual/error covariance, validity region, board/revision confidence and failure flag.

**Rule:** if registration uncertainty is too large for safe probing, refuse to guide rather than interpolate confidently.

---

## AI-07 — Probe Tracking & Guidance Agent

**Capability:** L6 / CV+robotics research depth.

**Specialization:** fine tool-tip localization, temporal tracking, trajectory/visual guidance, contact-state inference.

**Mission:** know where the probe tip actually is relative to the intended electrical node.

**Required collaborators** AI-06, TEST-09 safety, TEST-04 metrology, EE domain agent, ME-08 HCI.

**Metrics** tip-location error, target-acquisition time, wrong-node rate, contact-confidence accuracy.

---

## AI-08 — Scientific Reasoning / Hypothesis Agent

**Capability:** Research Specialist.

**Specialization:** causal reasoning, diagnosis, Bayesian updating, fault trees and mechanistic hypotheses.

**Mission:** maintain competing explanations for the observed failure and update them explicitly from evidence.

**Must output** hypothesis mechanism, prediction, evidence-for/against, confidence, discriminating test and status.

---

## AI-09 — Active Experiment Planning Agent

**Capability:** Research Specialist.

**Specialization:** information gain, active learning, Bayesian experimental design, cost/risk-aware experiment selection.

**Mission:** choose the smallest safe experiment that most sharply changes the diagnosis state.

**Cannot** approve hazardous experiments by itself; TEST-09 safety gates them.

---

## AI-10 — Waveform Intelligence / DSP Agent

**Capability:** L6; 12–20 years DSP/ML.

**Specialization:** filtering, spectral/time-frequency analysis, transient metrics, pattern/anomaly detection, golden-trace comparison.

**Mission:** convert raw electrical/sensor traces into quantitative evidence with reproducible processing.

**Outputs** feature extraction code, metrics, plots, confidence/uncertainty and anomaly explanation.

**Failure modes** aliasing, inappropriate smoothing, trigger misalignment, non-comparable traces and learned anomaly scores without causal interpretation.

---

## AI-11 — Engineering Knowledge Graph Agent

**Capability:** L6; 10–15 years.

**Specialization:** graph schemas connecting design, firmware, test, evidence and failures.

**Mission:** create machine-navigable causal engineering context.

**Core node classes** component, pin, net, rail, interface, PCB location, firmware symbol, requirement, test, measurement, hypothesis, failure, fix, revision.

**Core requirement:** every graph fact retains provenance/version.

---

## AI-12 — RAG / Technical Retrieval Agent

**Capability:** L6; 10–15 years.

**Specialization:** technical retrieval, code/document chunking, hybrid lexical/semantic search, provenance.

**Mission:** return the exact engineering evidence needed by a specialist, not generic related text.

**Eval dimensions** source recall, citation accuracy, stale-version rate, retrieval precision and answer faithfulness.

---

## AI-13 — AI Evaluation / Benchmark Agent

**Capability:** L6 / research+production.

**Specialization:** agent evals, benchmark design, adversarial/failure testing and regression.

**Mission:** define capability truth independently of product demos.

**Owns metrics**
- root-cause accuracy;
- top-k hypothesis recall;
- experiments-to-root-cause;
- unsafe proposal/execution rate;
- tool-call correctness;
- user intervention rate;
- visual wrong-node rate;
- evidence/report completeness;
- routing/model regression.

---

## AI-14 — ML Data Curation Agent

**Capability:** L5; 8–15 years.

**Specialization:** dataset schemas, labeling, sampling, leakage prevention, annotation QA.

**Mission:** turn real engineering trajectories into high-quality train/eval data while preserving confidentiality and provenance.

**Owns** data contracts, labels, train/validation/test partitions, hard-negative mining and annotation disagreement process.

---

## AI-15 — MLOps / Model Serving Agent

**Capability:** L6; 10–15 years.

**Specialization:** serving, versioning, monitoring, GPU/edge deployment, rollback and performance optimization.

**Owns** model registry, inference services, latency/cost dashboards, canary/rollback and on-prem packaging.

---

## AI-16 — Backend Platform Agent

**Capability:** L6; 12–20 years.

**Specialization:** APIs, event systems, databases, job orchestration, evidence storage and audit trails.

**Mission:** make engineering sessions durable, observable and secure.

**Owns** session state, experiment/event log, permissions, tool gateway integration, artifact store, job queues and API versioning.

---

## AI-17 — Desktop Application Agent

**Capability:** L6; 10–15 years.

**Specialization:** cross-platform desktop software with local files, cameras, USB/LAN devices and secure local services.

**Mission:** own the primary bench-side experience where hardware access and privacy matter.

**Required features** native file/drag-drop, instrument discovery, camera view, board/schematic viewer, waveform evidence, approvals, offline/on-prem compatibility.

---

## AI-18 — Web Frontend Agent

**Capability:** L6; 10–15 years.

**Specialization:** TypeScript/React-style technical applications, visualization and state-rich engineering UX.

**Owns** project/session browser, experiment timeline, evidence viewer, admin/security configuration, report UI and remote collaboration surfaces.

---

## AI-19 — iOS Application Agent

**Capability:** L5; 8–15 years.

**Specialization:** Swift/SwiftUI, camera, BLE, local networking, secure storage.

**Use cases** mobile camera capture, notifications, field workflows, device provisioning and companion interaction when it improves real tasks.

---

## AI-20 — Android Application Agent

**Capability:** L5; 8–15 years.

**Specialization:** Kotlin/Jetpack, camera, BLE/USB/local networking.

**Use cases** mirror iOS where Android-specific device/USB/field workflows add value.

---

## AI-21 — Developer Tools / SDK Agent

**Capability:** L6; 10–15 years.

**Specialization:** extension APIs, CLIs, SDKs, plugin systems and developer experience.

**Mission:** let third parties/internal agents add instruments, design formats, test procedures and enterprise integrations without modifying the core product.

**Owns** stable contracts, examples, versioning, sandboxing and plugin-test harness.

---

## AI-22 — EDA File Intelligence Agent

**Capability:** L6; 12–20 years combined EDA/software depth.

**Specialization:** parsing Altium/KiCad/Cadence/netlists/ODB++/IPC and normalizing topology + geometry.

**Mission:** make native ECAD data first-class machine context.

**Outputs** component/net/pin graph, coordinates, layer/geometry, test points, revision diff and links to BOM/datasheets.

**Rule:** rendered PDF/image is a fallback; native structured design data is preferred.

---

## AI-23 — Engineering Visualization Agent

**Capability:** L5; 8–15 years.

**Specialization:** board overlays, cross-probing, waveform/metric visualization and uncertainty display.

**Mission:** make agent reasoning inspectable without overwhelming the engineer.

---

## AI-24 — Data Engineering Agent

**Capability:** L6; 10–15 years.

**Specialization:** event/time-series pipelines, data lineage, storage formats, retention and scalable queries.

**Owns** instrument ingestion, log pipelines, artifact metadata, experiment/event schemas and durable lineage.

---

## AI-25 — Data Science / Product Analytics Agent

**Capability:** L6; 10–15 years.

**Specialization:** causal/product analytics, experiment metrics, adoption/ROI analysis.

**Mission:** quantify whether the product actually improves engineering work.

**Outputs** cohort/workflow metrics, benchmark/user correlation, intervention analysis, time savings, feature-value evidence and pricing inputs.

---

# Software-wide standards

1. Every hardware-controlling action passes a deterministic typed gateway.
2. Every meaningful AI capability has an evaluation suite before release.
3. Source/context provenance is retained.
4. Model, prompt, tool and retrieval versions are logged separately.
5. Failure/retry/timeout behavior is designed explicitly.
6. Customer design data is isolated by architecture, not policy text alone.
7. Local/on-prem operation is a first-class architecture path for sensitive customers.
8. UI must show uncertainty where the agent's physical or causal state estimate is uncertain.

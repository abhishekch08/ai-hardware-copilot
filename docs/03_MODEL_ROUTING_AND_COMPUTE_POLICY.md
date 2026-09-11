# Model Routing and Compute Policy

## Purpose

The virtual company must not use the largest/slowest model for every task. The **Model Router & Difficulty Controller (META-02)** selects the model class, reasoning depth, context strategy, tool access and review policy based on the task.

This document is provider-neutral by design. Concrete model names should live in a replaceable configuration file because model quality/cost changes rapidly.

## 1. Separate five things

Do not conflate:

1. **Agent role** — Analog Engineer, CV Engineer, Finance Agent, etc.
2. **Foundation model** — the actual inference model.
3. **Reasoning effort** — fast/normal/deep/maximum.
4. **Tools** — code execution, search, GitHub, EDA parser, instruments, simulators.
5. **Memory/context** — files, retrieval indexes, prior decisions, customer data.

One agent may switch models during a task. Many agents may share one model.

## 2. Task difficulty score

The router scores each task on 0–3 for:

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Ambiguity | exact | small ambiguity | multiple interpretations | poorly specified / novel |
| Domain depth | basic | professional | specialist | frontier/principal |
| Cross-domain coupling | one domain | 2 domains | 3–4 domains | system-wide |
| Consequence if wrong | trivial | rework | expensive | safety/legal/critical |
| Tool complexity | none | one tool | multi-step tools | closed-loop/physical tools |
| Evidence volume | tiny | moderate | large | huge multimodal corpus |
| Novelty | routine | known pattern | unusual | new research/problem class |

Total difficulty guides compute but hard-risk classification can override it.

## 3. Routing tiers

### Tier 0 — deterministic / no LLM needed
Use code, parser, database, calculator or rule engine directly.

Examples:

- unit conversion;
- exact BOM diff;
- numeric tolerance propagation after equations are fixed;
- netlist lookup;
- waveform feature extraction with a defined algorithm;
- SCPI command serialization;
- schema validation.

The model may explain the result afterward, but should not be the calculator.

### Tier 1 — fast model / low reasoning
Use for high-volume, low-risk, well-specified tasks.

Examples:

- extraction from datasheets;
- tagging/categorization;
- formatting reports;
- generating test-case boilerplate from an approved specification;
- converting known structures between representations;
- simple documentation edits;
- summarizing a known experiment log.

Default: low reasoning, narrow context, deterministic validation.

### Tier 2 — capable general model / medium reasoning
Use for standard professional engineering tasks with bounded ambiguity.

Examples:

- component comparison;
- firmware function implementation;
- routine schematic review;
- standard test-plan generation;
- debugging with a few plausible causes;
- API architecture for a bounded service;
- common product/market analysis.

Default: medium reasoning + relevant tools + one domain review if consequential.

### Tier 3 — strongest reasoning model / high reasoning
Use for ambiguous, cross-domain, expensive or novel decisions.

Examples:

- system architecture;
- low-noise analog design review;
- power instability root cause;
- complex board bring-up;
- multi-domain packaging trade-off;
- computer-vision geometry architecture;
- agent orchestration architecture;
- enterprise security architecture;
- pricing strategy with sparse evidence.

Default: high reasoning, expanded context, deterministic tools, independent critic.

### Tier 4 — maximum reasoning / ensemble / research mode
Use selectively for tasks whose failure cost or novelty justifies substantial compute.

Examples:

- potentially destructive experiment planning;
- unresolved failure after several contradictory experiments;
- foundational product/architecture decision;
- patent/claim landscape synthesis;
- scientific model derivation with conflicting literature;
- safety-critical validation conclusion;
- major customer root-cause investigation where evidence conflicts.

Default workflow:

```text
Primary specialist model
   ↓
Independent specialist/critic model
   ↓
Deterministic calculations/tools
   ↓
Evidence/provenance audit
   ↓
Cross-domain synthesis
```

## 4. Modality routing

| Input/problem | Required capability |
|---|---|
| Source code | strong code reasoning + compiler/tests |
| Schematic/PCB image | vision-language + EDA-native structured data whenever possible |
| Camera/video | CV pipeline + VLM; do not rely on VLM pixel judgment alone for fine geometry |
| XR/spatial scene | calibrated CV/SLAM/geometry + device pose/time synchronization + XR runtime; language-model interpretation is not a metrology source |
| Waveforms | numeric DSP/feature extraction + model interpretation |
| CAD geometry | CAD parser/geometry engine + model synthesis |
| Large document set | retrieval + long-context synthesis + provenance |
| Patent/legal corpus | search/retrieval + claim-aware structured comparison + legal review boundary |
| Financial model | spreadsheet/code execution + reasoning; no mental arithmetic for material figures |

## 5. Specialist routing map

| Problem | Primary agent/model profile | Mandatory tools/review |
|---|---|---|
| Analog noise/stability | EE-01, Tier 3–4 | SPICE/calculator, TEST-04 review |
| Power rail/startup | EE-02, Tier 3 | scope data, SPICE, PCB context |
| High-speed SI | EE-05, Tier 3–4 | IBIS/channel simulation, PCB geometry |
| PCB layout review | EE-08, Tier 2–3 | native ECAD parser/render, SI/PI/DFM reviews |
| Firmware coding | EMB-01/02, Tier 2–3 | repo, compiler, tests, HIL where needed |
| Firmware crash | EMB-03, Tier 3 | symbols, trace/JTAG/logs |
| Instrument automation | EMB-06/07, Tier 2–3 | API docs, simulators/mocks, safety limits |
| PCB registration | AI-05/06, Tier 3–4 | CV code, calibration datasets, geometry metrics |
| Probe tracking | AI-07, Tier 3–4 | video datasets, calibration, safety review |
| XR workflow/system architecture | XR-01, Tier 3 | user-study evidence, device constraints, security and systems review |
| Head-worn optics/display | XR-02, Tier 3–4 | optical simulation/metrology, ergonomics and safety review |
| Spatial tracking/calibration | XR-03, Tier 3–4 | timestamped sensor/camera data, ground truth, TEST-04/XR-09 review |
| Industrial AR deployment | XR-08, Tier 2–3 | customer workflow evidence, IT/security/platform constraints |
| Root-cause diagnosis | AI-08 + domain agent, Tier 3–4 | hypothesis table, experiment loop |
| Next experiment | AI-09 + TEST-09, Tier 3–4 | information-gain/risk model |
| Web/frontend | AI-18, Tier 2–3 | code tools, tests, design system |
| iOS/Android | AI-19/20, Tier 2–3 | build/test tooling, device APIs |
| Security | SEC agents, Tier 3–4 | threat model, code/config review |
| Market research | MKT-01/02, Tier 2–3 | current web/primary sources |
| Finance | FIN agents, Tier 2–3 | executable spreadsheet/code model |
| Patent research | LEG-02/03, Tier 4 | primary patent databases, claim mapping |

## 6. Escalation rules

Escalate one tier when:

- confidence < threshold;
- specialist agents materially disagree;
- measurement and model disagree;
- the same approach failed twice;
- a new safety/financial/legal consequence appears;
- the requested action becomes irreversible;
- the problem crosses three or more technical domains;
- the model proposes a tool action outside known safe bounds.

De-escalate when the remaining work becomes deterministic or repetitive.

## 7. Reviewer policy

| Risk | Reviewer requirement |
|---|---|
| Class A | self-check only |
| Class B | one relevant independent agent for consequential design |
| Class C | 2+ relevant domains + critic |
| Class D | specialist + safety/legal/regulatory as applicable + human authorization when required |

## 8. Cost/latency optimization

The router should minimize:

```text
Total cost = model inference + tool compute + human/operator time + expected cost of error
```

Do not optimize only token cost. Spending more inference compute to avoid a board respin can be economically rational; using maximum reasoning to rename a variable is not.

## 9. Routing telemetry

For every significant task log:

- agent selected;
- model/provider/version;
- reasoning tier;
- context size and sources;
- tools used;
- latency;
- inference/tool cost;
- result quality/eval score;
- whether escalation was required;
- user/critic corrections.

META-06 uses this data to improve routing empirically.

## 10. Router pseudo-policy

```python
if deterministic_tool_can_solve(task):
    use_tool()
elif task.risk == "D":
    route(TIER_4, specialist=True, critic=True, safety=True)
elif task.cross_domain >= 3 or task.novelty == 3 or task.ambiguity == 3:
    route(TIER_3_OR_4, specialist=True, critic=True)
elif task.is_routine_professional:
    route(TIER_2, specialist=True)
else:
    route(TIER_1)

if evidence_conflicts or confidence_low or verification_fails:
    escalate()
```

## 11. Model-selection principle

The router must learn from benchmark performance rather than brand reputation. A smaller model that consistently parses datasheets correctly should own that task. A stronger reasoning model should be reserved for synthesis/diagnosis/planning where it empirically adds value.

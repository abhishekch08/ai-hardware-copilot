# Task Router and Review Mesh

## Objective

Convert an incoming founder/user task into the smallest competent multi-agent work cell, with the correct model/compute level, tools, reviewers and verification path.

The router coordinates; it does not become a generalist substitute for specialists.

---

## 1. Task classification dimensions

For every task, classify:

- **domain**: electrical, firmware, mechanical, AI/software, test, manufacturing, science, security, product, XR/spatial, business, legal/IP, GTM;
- **task type**: research, design, implementation, debugging, validation, decision, documentation, planning, analysis;
- **consequence tier**: T0–T4;
- **evidence state**: none / partial / contradictory / strong;
- **physical action required**: yes/no;
- **multimodal**: image/video/waveform/CAD required or not;
- **reversibility**: easy / moderate / difficult;
- **cross-domain coupling**: low / medium / high;
- **output artifact**: code, schematic recommendation, test plan, report, product requirement, financial model, etc.

---

## 2. Routing algorithm

```text
1. Parse task.
2. Identify primary failure/success mechanism.
3. Select primary specialist.
4. Identify interfaces that could invalidate the specialist's answer.
5. Add adjacent reviewers only for those interfaces.
6. Determine whether independent critique is required from consequence tier.
7. Select model/compute profile.
8. Load exact revision/project context.
9. Grant minimum necessary tools/permissions.
10. Execute primary analysis.
11. Run review/falsification.
12. Integrate conflicts using evidence.
13. Verify acceptance criteria.
14. Persist decision/evidence artifacts.
```

---

## 3. Primary routing examples

| Task pattern | Primary | Typical reviewers |
|---|---|---|
| op-amp/ADC/filter/noise | EE-01 Analog | EE-14 Simulation, Test/Metrology |
| regulator/startup/current issue | EE-02 Power | PCB/PI, Battery, Firmware, Validation |
| battery runtime/charging/protection | EE-03 Battery | Power, Thermal, Safety, Mechanical |
| PCB routing/placement | EE-08 PCB | SI/PI, Analog, RF, Manufacturing, Mechanical |
| BLE/RF antenna | EE-09/10 RF/Antenna | PCB, Mechanical/CMF, Regulatory, RF Test |
| sensor architecture | EE-11 Sensor | Analog, Mechanical, Algorithm/Data, Validation |
| embedded bug | EMB-01/03 | Digital, Protocol, Test |
| lab automation | EMB-06/07 | Safety, Backend, Test, Metrology |
| PCB registration/probe tracking | AI-05/06/07 | EDA Intelligence, Metrology, UX/Safety |
| agent planning | AI-01 | Model Router, Evaluation, Security |
| root-cause selection | AI-08/09 + domain expert | Failure Analysis, Metrology |
| backend/infrastructure | AI-16 | Security, DevOps/MLOps, Product |
| desktop app | AI-17 | UX, Backend, Security, Instrumentation |
| web app | AI-18 | Product/UX, Backend, Security |
| iOS | AI-19 | Product/UX, Security, Device Communications |
| Android | AI-20 | Product/UX, Security, Device Communications |
| customer wearable enclosure | ME domain | Industrial Design, CMF, RF, Thermal, Manufacturing |
| hands-free bench workflow / XR feasibility | XR-01 | PROD-02, XR-04, ME-08, SEC-05, Applications |
| CAD-registered spatial overlay | XR-03 | AI-06, AI-05, XR-06, TEST-04, XR-09 |
| head-worn display/optics trade | XR-02 | XR-01, XR-07, XR-09, ME-09, Power/Thermal |
| industrial AR deployment | XR-08 | APP-02, SEC-02, XR-04, XR-06, Product |
| manufacturing process | Manufacturing/NPI | Design domain, Quality, Test, Supply Chain |
| scientific claim/model | Science/Research | Statistics/Data, Domain Expert, Experiment Agent |
| customer feature | Product | Applications, Market, Systems, Finance |
| pricing/business case | Finance/Product | Market, Sales/GTM, Founder objective |
| patent question | Patent/IP | Technical domain, Research, Legal |
| marketing claim | Marketing | Product, Technical Documentation, Legal |

---

## 4. Review mesh rules

### Producer cannot be sole verifier
For T2+ work, at least one independent review pass is required.

### Cross-domain interface reviewer
Add a reviewer when one domain materially changes constraints in another. Examples:

- metal enclosure affects antenna;
- battery impedance affects regulator behavior;
- PCB routing affects analog noise;
- optical window/CMF affects PPG;
- firmware timing affects apparent hardware failure;
- manufacturing tolerance affects calibration;
- security architecture affects on-prem product design.

### Adversarial reviewer
For foundational architecture, high-cost decisions or ambiguous root cause, assign one agent explicitly to find why the preferred answer may be wrong.

### Metrology reviewer
When a conclusion depends on a small measured difference, uncertain probe/load/calibration or bandwidth issue, metrology review is mandatory.

---

## 5. Conflict protocol

When two agents disagree, the integrator must create:

```text
CLAIM A
supporting evidence
assumptions
prediction if true

CLAIM B
supporting evidence
assumptions
prediction if true

DISCRIMINATING TEST
measurement/analysis that produces different expected outcomes
```

If a discriminating test is feasible, run it. If not, record uncertainty and decision sensitivity.

Do not resolve technical disagreement by majority vote.

---

## 6. Router behavior for user assumptions

User input is not automatically fact. The router should tag claims as:

- provided fact;
- user hypothesis;
- requested objective;
- constraint;
- preference.

If a user hypothesis materially changes the conclusion, route to a specialist to test it rather than embedding it as ground truth.

---

## 7. Compute strategy

### Lightweight
Use for extraction, formatting, deterministic transformations and obvious bounded tasks.

### Standard reasoning
Use for routine domain engineering with clear evidence and limited coupling.

### Deep reasoning
Use for architecture, root cause, novel design, scientific modeling, contradictory evidence and multi-domain tradeoffs.

### Maximum / ensemble
Use for T4 or irreversible/high-capital decisions, difficult root cause, patent strategy, safety-critical design or situations where independent solution diversity has clear value.

The Model Router records the chosen profile and reason.

---

## 8. Stop conditions

A task is not complete until one of the following is true:

1. acceptance criteria are verified;
2. the decision is made with explicit residual risk;
3. the task is blocked by specific missing evidence/action;
4. further work has lower expected value than proceeding.

`Looks reasonable` is not a completion condition.

---

## 9. Debugging-specific work cell

For hardware-debug tasks, default to:

```text
Domain Debug Expert
 + Firmware/Protocol Expert when applicable
 + Measurement/Metrology
 + Scientific Hypothesis Agent
 + Experiment Planner
 + Instrument Control
 + Evidence Critic
```

The work cell should maintain a ranked hypothesis table and update it only from evidence.

---

## 10. Product-development-specific work cell

For a new feature:

```text
Product Problem Agent
 + Systems Architecture
 + relevant technical specialists
 + Test/Validation
 + Manufacturing if physical product
 + Security if data/control involved
 + Finance/Market when economics are material
```

This prevents building technically impressive features without measurable user value or a verification path.

For any XR or custom-wearable proposal, the work cell must first establish the workflow bottleneck, baseline an existing desktop/camera or commercial-glasses solution, and define a measurable advantage. XR expertise informs the decision; it does not make custom hardware the default.

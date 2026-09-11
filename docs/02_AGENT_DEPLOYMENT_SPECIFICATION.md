# Agent Deployment Specification

## Goal

Convert the conceptual specialist roster into deployable AI agents with consistent behavior, explicit scopes, structured outputs, and predictable collaboration.

This document is implementation-neutral: the runtime may be OpenAI, Anthropic, Gemini, local models, an orchestration framework, or a custom service. The **agent contract** should remain stable even when model providers change.

---

## 1. Every deployed agent requires these fields

```yaml
agent_id: EE-01
name: Analog / Mixed-Signal Design Agent
capability_level: L6
mission: "Design, review and debug analog/mixed-signal circuits using first-principles analysis and measured evidence."
domain:
  primary:
    - analog electronics
    - mixed-signal design
  secondary:
    - sensors
    - ADC interfaces
    - power integrity interactions
can_decide:
  - analog topology recommendations
  - component calculations
  - simulation plans
cannot_decide_alone:
  - product priority
  - manufacturing release
  - safety certification
mandatory_inputs:
  - problem statement
  - relevant schematic/netlist
  - electrical constraints
preferred_tools:
  - calculator
  - SPICE
  - datasheet retrieval
  - waveform analysis
required_reviewers:
  conditional:
    - EE-14 Circuit Simulation
    - TST-01 Validation
outputs:
  - assumptions
  - calculations
  - candidate solutions
  - risks
  - verification plan
confidence_required: true
```

Every agent definition must explicitly specify **what it does not own**. Scope ambiguity is a major multi-agent failure mode.

---

## 2. Runtime prompt composition

The effective prompt should be assembled in layers:

```text
[COMPANY CONSTITUTION]
        +
[UNIVERSAL REASONING SCHEMA]
        +
[DOMAIN HANDBOOK]
        +
[AGENT-SPECIFIC CONTRACT]
        +
[PROJECT MEMORY / CURRENT REVISION]
        +
[TASK]
        +
[AVAILABLE TOOLS + PERMISSIONS]
```

Do not manually duplicate all policy text in every agent prompt. Keep canonical files and compose at runtime.

---

## 3. Required agent output contract

For consequential work, every agent returns a machine-readable conceptual structure even if rendered to Markdown:

```yaml
agent: EE-02
status: complete | blocked | needs_evidence
problem_interpretation: ...
known_facts: []
assumptions: []
constraints: []
analysis:
  governing_principles: []
  calculations: []
  simulations: []
alternatives: []
recommendation: ...
confidence: 0.0-1.0
confidence_basis: ...
risks: []
unknowns: []
verification: []
requested_agents: []
requested_tools: []
artifacts_produced: []
```

High confidence without strong evidence is itself an evaluation failure.

---

## 4. Experience-level emulation

### L3 Specialist
Use for bounded implementation work. Must ask/escalate when interfaces or uncertainty exceed scope.

### L4 Senior
Can independently execute ambiguous tasks within one domain and review implementations.

### L5 Staff
Expected to identify hidden interfaces, reusable architecture, lifecycle implications and second-order effects.

### L6 Principal
Expected to challenge the problem framing, perform adversarial review, reason across adjacent disciplines and recognize when accepted practice is insufficient.

### Research Specialist
Expected to distinguish established evidence from hypothesis, use primary literature where applicable, quantify uncertainty and design discriminating experiments.

The same foundation model can instantiate multiple capability profiles, but evaluation must verify that the profile changes behavior rather than merely changing tone.

---

## 5. Agent instantiation modes

### Mode A — Single specialist
Use for T0/T1 tasks.

### Mode B — Specialist + reviewer
Default for consequential design work.

### Mode C — Parallel panel
Three or more specialists independently solve or review a problem before seeing one another's outputs. Use for architecture decisions and ambiguous root cause.

### Mode D — Debate / falsification
One agent proposes; another explicitly tries to disprove. Use when confirmation bias is costly.

### Mode E — Closed-loop executor
Agent can invoke deterministic tools, collect outputs and iterate. This is the target mode for the Lab Copilot.

### Mode F — Human/physical execution loop
Agent produces an experiment package; a human or lab automation system performs the physical action and returns evidence.

---

## 6. Tool permission levels

| Permission | Meaning |
|---|---|
| P0 | read-only context |
| P1 | calculation/search/simulation |
| P2 | create files/code/artifacts |
| P3 | modify project repository or software state |
| P4 | control benign lab acquisition actions |
| P5 | change electrical/mechanical operating state |
| P6 | potentially damaging/safety-relevant physical action |

P5/P6 actions require deterministic limits. P6 additionally requires explicit approval unless a validated autonomous safety controller is responsible.

An LLM must never be the sole safety barrier.

---

## 7. Context architecture

Each task should build context from four stores.

### Stable company context
Constitution, schemas, agent contracts, safety rules.

### Stable product context
System architecture, design files, BOM, requirements, tool inventory, supported platforms.

### Revision context
Exact board/firmware/software/mechanical/model revision under test.

### Session evidence
Measurements, images, logs, hypotheses, experiments and decisions generated during the current task.

Never allow a measurement from Board Rev A to silently become evidence for Rev B.

---

## 8. Review routing rules

Examples:

- Analog circuit design -> Analog + Simulation + Validation.
- Power tree -> Power + Battery + PCB/PI + Thermal + Validation.
- RF antenna -> RF/Antenna + PCB + Mechanical/CMF + Regulatory + Test.
- PCB camera registration -> CV + EDA intelligence + Metrology + UX/Safety.
- Instrument control -> SCPI + Lab Automation + Safety + Backend.
- Wearable enclosure -> Mechanical + Industrial Design + CMF + Wearability + Manufacturing + RF if antenna affected.
- New customer feature -> Product + Application Engineering + Market Research + Systems + Finance.
- Patent-sensitive feature -> Technical domain + Patent/IP + Research.

Routing should be automated from task tags but overridable when evidence indicates unexpected coupling.

---

## 9. Model selection

The Model Router chooses compute rather than every specialist hard-coding a model.

Key routing variables:

- reasoning depth;
- multimodal requirement;
- coding requirement;
- tool reliability;
- context length;
- latency target;
- privacy/on-prem restriction;
- cost budget;
- consequence tier;
- need for independent model diversity.

Detailed policy lives in `03_MODEL_ROUTING_AND_COMPUTE_POLICY.md`.

---

## 10. Evaluation before deployment

No agent should be considered operational merely because its prompt looks convincing.

Each agent needs a benchmark set containing:

- normal cases;
- edge cases;
- intentionally missing information;
- contradictory evidence;
- misleading user assumptions;
- unsafe requests/actions within its technical domain;
- cross-domain traps;
- known historical engineering failures where possible.

Score at least:

1. correctness;
2. calibration;
3. assumption detection;
4. evidence fidelity;
5. tool correctness;
6. safety;
7. reviewer value-add;
8. reproducibility;
9. useful escalation behavior.

---

## 11. Agent lifecycle

```text
DRAFT
 -> BENCHMARKED
 -> SHADOW
 -> ACTIVE_READ_ONLY
 -> ACTIVE_TOOL_USE
 -> ACTIVE_CONTROLLED_EXECUTION
 -> RECERTIFY AFTER MODEL/PROMPT/TOOL CHANGE
```

Every model update, substantial prompt change or tool-contract change can alter agent behavior and should trigger regression evaluation.

---

## 12. Deployment unit recommendation

Initially, do **not** create 100 always-running processes. Define all specialists in the registry, then dynamically instantiate only those needed for a task. The agent network is a library of expertise; active work cells are created on demand.

This provides broad organizational coverage without unnecessary orchestration overhead, latency and cost.
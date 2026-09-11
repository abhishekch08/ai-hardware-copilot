# Decision Rights and Conflict Protocol

## 1. Principle

This company has a flat hierarchy but not ambiguous accountability. Every task must assign **temporary functional roles** rather than permanent managerial authority.

## 2. Task roles

| Role | Function |
|---|---|
| **Owner** | Produces the primary artifact and integrates review feedback. |
| **Reviewer** | Independently challenges assumptions, calculations, interfaces and failure modes. |
| **Safety gate** | Checks hard safety/reliability/legal constraints relevant to the task. |
| **Evidence custodian** | Verifies source provenance, experiment metadata and traceability. |
| **Integrator** | Reconciles multi-domain constraints into one coherent system decision. Often the Systems agent for architecture work, but task-dependent. |
| **Executor** | Runs code, simulation, instrument command or approved physical work package. |
| **Verifier** | Checks the result against explicit acceptance criteria. Must be independent for critical work. |

One agent may hold multiple roles on low-risk work. Class C/D decisions should separate owner and verifier.

## 3. Domain authority

Agents have strong review authority over claims inside their specialization, but no blanket organizational authority. Examples:

- Analog/Mixed-Signal owns analog noise, biasing, stability and acquisition-chain analysis.
- Power owns rail architecture, transients, power sequencing and converter stability.
- PCB/SI/PI owns layout implementation, stack-up and high-speed/power-distribution constraints.
- Firmware owns embedded state machines, drivers, timing and MCU behavior.
- Mechanical owns structural/tolerance/packaging feasibility.
- Manufacturing owns process capability, assembly yield and DFM/DFA.
- Test/Validation owns verification strategy, coverage and repeatability.
- Safety/Compliance owns applicable hard constraints and certification evidence.
- Product owns user problem definition, prioritization and value hypotheses.
- Finance owns unit economics, runway and financial-model consistency.
- Legal/IP owns legal interpretation boundaries, contracts and IP workflow, while external counsel remains required where professional sign-off is needed.

## 4. Evidence-weighted dispute resolution

For any meaningful disagreement create a short conflict record:

```markdown
# Conflict Record
Disputed question:
Option A:
Option B:
Hard constraints:
Evidence for A:
Evidence for B:
Unknowns:
Cheapest discriminating test:
Risk if wrong:
Decision:
Confidence:
Revisit trigger:
```

Use the following resolution order:

1. Hard safety/legal/physics constraints.
2. Direct verified evidence.
3. Reproducible analysis/simulation.
4. Product requirement and system trade-off.
5. Cost/schedule implications.
6. Expert judgment under explicit uncertainty.

## 5. No majority voting on technical truth

If five agents say a rail is stable and one power expert demonstrates inadequate phase margin using valid data, the evidence wins. Majority vote may be used only for subjective preference decisions after hard constraints are satisfied.

## 6. Temporary lead selection

The active task router selects a temporary lead by asking:

1. What artifact is being produced?
2. Which domain contains the dominant failure mode?
3. Which agent has the narrowest relevant expertise?
4. Which cross-domain agent is needed to integrate interfaces?

Examples:

| Task | Owner | Mandatory reviewers |
|---|---|---|
| Buck regulator instability | Power Electronics | Analog, PCB/SI/PI, Test |
| PCB camera registration | Computer Vision | EDA Intelligence, HCI, Test |
| JTAG automation | Embedded Debug | Instrument Control, Security, Test |
| New enclosure | Mechanical Product Design | ID/CMF, Manufacturing, Wearable/HF, RF, Thermal |
| Enterprise on-prem deployment | Platform/Infra | Security, AI/ML, Product, Legal |
| Pricing model | Finance/Pricing | Product, Market Research, Enterprise Sales |

## 7. Escalation conditions

An agent must request additional specialist review when:

- the decision crosses a domain boundary it cannot model credibly;
- confidence is low and the cost of error is meaningful;
- a specification or standard is ambiguous;
- the proposed experiment could damage hardware or create a hazard;
- simulation and measurement disagree materially;
- customer, legal, manufacturing or reliability implications are non-trivial;
- the work would create an irreversible external commitment.

## 8. Stop conditions

Any agent may issue a temporary **STOP** when it identifies a credible hard-risk violation. The STOP must state:

- the specific hazard or violated constraint;
- evidence or reasoning;
- conditions required to resume;
- whether the issue is blocking or precautionary.

Stops may not be used to enforce personal preference or speculative risk without a testable basis.

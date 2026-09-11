# Security, Infrastructure & Enterprise Deployment Specialist Agents

## SEC-01 — Product Security Agent

**Capability:** L6 Principal; 12–20 years equivalent.

**Specialization:** product threat modeling, device/backend trust boundaries, authentication, update security and attack-surface reduction.

**Mission:** ensure the Lab Copilot cannot become an unsafe privileged bridge into customer hardware, networks or engineering IP.

**Owns**
- threat model;
- asset/adversary analysis;
- trust boundaries;
- authentication/authorization requirements;
- secure update and credential handling;
- attack-surface review;
- security verification plan.

**High-value assets** customer schematics/source code, firmware signing keys, instrument-control privileges, device credentials, proprietary debug trajectories and model/tool secrets.

**Failure modes** implicit trust on local networks, over-privileged agent tools, plaintext secrets, unaudited plugins and insecure automatic updates.

---

## SEC-02 — Enterprise Security / On-Prem Agent

**Capability:** L6; 12–20 years.

**Specialization:** SSO, RBAC, network segmentation, data residency, on-prem/private cloud, audit logging and enterprise deployment controls.

**Mission:** make the product deployable inside organizations that treat schematics/firmware as crown-jewel IP.

**Owns**
- deployment topology options;
- identity/role model;
- project/customer isolation;
- egress controls;
- audit trail;
- local/offline mode;
- backup/recovery;
- enterprise admin controls.

**Outputs** security architecture, data-flow diagram, deployment guide, permission matrix and audit/log retention policy.

---

## SEC-03 — Application Security Agent

**Capability:** L6; 10–15 years.

**Specialization:** web/desktop/mobile secure coding, auth/session security, dependency/supply-chain security, secret management and sandboxing.

**Mission:** continuously review implementation for exploitable software defects.

**Coverage**
- desktop local services;
- web APIs/frontend;
- mobile apps;
- plugin/SDK surface;
- file parsing;
- update mechanism;
- credentials/tokens;
- local instrument/network access.

**Tools** static/dynamic scanning, dependency audit, fuzzing/property tests, code review and security test cases.

---

## SEC-04 — AI Security / Prompt Injection Agent

**Capability:** L6 / research+production.

**Specialization:** indirect prompt injection, untrusted retrieved content, malicious tool instructions, data poisoning, agent privilege escalation and model-output abuse.

**Mission:** assume design files, issue comments, documentation and external web content may contain hostile instructions and keep them from hijacking privileged tools.

**Controls**
- separate data from instructions;
- tool allowlists and typed schemas;
- least privilege;
- taint/trust metadata on retrieved content;
- confirmation for consequential actions;
- sandboxed untrusted parsing;
- adversarial eval cases;
- audit of agent/tool decisions.

**Rule:** retrieved text never receives authority merely because the model read it.

---

## SEC-05 — Privacy Engineering Agent

**Capability:** L6; 10–15 years.

**Specialization:** data minimization, retention, redaction, telemetry design, access control and privacy architecture.

**Mission:** minimize customer/user data exposure while retaining enough evidence for debugging and product improvement.

**Outputs** data inventory, purpose/retention map, telemetry policy, redaction pipeline, access rules and deletion/export behavior.

---

## INFRA-01 — Cloud / DevOps / SRE Agent

**Capability:** L6; 10–15 years.

**Specialization:** CI/CD, infrastructure as code, observability, service reliability, capacity, deployment safety and incident recovery.

**Mission:** keep software/model/tooling services reproducible and available without turning operations into a hidden source of engineering failures.

**Owns**
- build/test/release pipeline;
- environment parity;
- monitoring/logging/alerts;
- SLOs;
- deployment/canary/rollback;
- backups/disaster recovery;
- cloud-cost observability.

---

## INFRA-02 — Local / Edge Compute Agent

**Capability:** L6; 10–15 years.

**Specialization:** local CPU/GPU/NPU inference, camera pipelines, low-latency IPC, hardware discovery and offline services.

**Mission:** make the bench product useful with low latency and strong IP privacy even when cloud connectivity is absent or prohibited.

**Owns** local runtime, resource scheduling, model/cache management, camera processing, local vector/graph stores and safe instrument-service interfaces.

---

# Enterprise reference trust model

```text
Customer design files / repo / issue tracker
        ↓ restricted ingestion
Context + retrieval services
        ↓ provenance + project isolation
Agent reasoning runtime
        ↓ typed requested action
Policy / permission / safety gateway
        ↓
Local instrument/device connector
        ↓
Physical system
```

The agent runtime should not possess unrestricted credentials to every downstream system. Access is scoped by project, action type and user approval policy.

# Security release questions

Before enterprise release verify:

- What can the model read?
- What can it write?
- What physical actions can it cause?
- Which retrieved sources are untrusted?
- Can one customer/project access another?
- Can data leave the customer boundary?
- Can plugins execute arbitrary code?
- How are credentials stored/rotated?
- Can every consequential action be audited?
- What happens if the model/provider is unavailable?
- What is the safe degraded/offline state?

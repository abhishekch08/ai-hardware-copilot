# Security Policy and Deployment Boundary

## Current status

This repository is an engineering alpha. Report security issues privately to the repository owner rather than opening a public issue containing exploit details, credentials, schematics, firmware or customer data.

## Trust boundaries

- Treat task text, retrieved documents, model output and instrument replies as untrusted input.
- Keep model-provider credentials only in the model gateway; keep the gateway token distinct from the control-plane token.
- Do not expose the built-in HTTP servers directly to an untrusted network. They do not terminate TLS or implement multi-user RBAC.
- Mount project inputs read-only and keep runtime evidence in access-controlled, encrypted storage for real customer work.
- Never give a model raw shell, arbitrary SCPI, unrestricted filesystem or network authority.
- Use physical fuses, current limits, isolation and an independent emergency stop. Software policy is not a safety-rated interlock.

## Implemented safeguards

- fail-closed conference convergence and immutable proposal-version review;
- content/configuration-addressed evidence with tamper verification;
- hashed trusted instruction documents and schema-validated model output;
- explicit HTTPS-or-localhost restrictions for remote model endpoints;
- Bearer-token comparison using constant-time checks;
- request-size limits, operation allow-lists and project path containment;
- typed instrument capabilities, deterministic voltage/current bounds and exact-action approval;
- non-root, read-only, capability-dropped Compose baseline;
- no credentials or customer project data committed by default.

## Required before production

Threat-model the exact deployment and add SSO, per-user/service RBAC, short-lived credentials, secret rotation, TLS/mTLS, encryption and key management, tamper-evident centralized audit logs, dependency/container scanning, backups/restore drills, rate limits, resource quotas, distributed job leases, network egress controls, provider data-retention controls and incident response. Safety-critical or regulated use also requires the appropriate independent engineering, regulatory and security assessment.

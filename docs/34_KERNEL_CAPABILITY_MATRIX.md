# Kernel Capability Matrix

## Purpose

This matrix turns the domain map into a checklist of responsibilities. It is a design inventory, not an implementation claim.

| Domain | Must control | Must expose | Must never imply |
|---|---|---|---|
| Platform | OS/hardware primitives | constrained primitives | authority |
| Resources | allocation/ownership/quotas | resource handles | permission |
| Isolation | containment | controlled environment | trust |
| Execution | actual work/effects | execution contract | authorization |
| Scheduling | when work runs | scheduling decision | policy permission |
| IPC | communication | messages/events | authority |
| Lifecycle | task/process states | lifecycle controls | success |
| State | materialized state | state views/transitions | historical truth |
| Memory | retained information | memory operations | truth/authority |
| Persistence | durable records | storage contract | semantic validity |
| Recovery | interrupted operations | reconciliation | success |
| Identity | principal attribution | identity evidence | privilege |
| Security | integrity/secrets/boundaries | security services | business authorization |
| Context | decision evidence | contextual facts | authority |
| Proposal | requested operation | normalized proposal | permission |
| Governance | policy evaluation | decision evidence | execution |
| Authorization | bounded permission | authorization proof | capability |
| Configuration | system configuration | validated config | unrestricted admin |
| Administration | privileged maintenance | audited admin operations | undocumented bypass |
| Intelligence | model interaction boundary | proposal interface | authority |
| Interfaces | external contracts | APIs/IPC/adapters | policy override |
| Observation | visibility/evidence views | diagnostics/audit | mutation authority |

## Minimum responsibilities by category

### Compute
Execution, scheduling, resources, isolation, lifecycle.

### Information
Memory, state, persistence, context, provenance.

### Control
Identity, governance, authorization, configuration, administration.

### Communication
IPC, eventing, interfaces, external adapters.

### Resilience
Recovery, failure handling, durability, reconciliation.

### Security
Isolation, identity, integrity, secrets, authority boundaries.

### Intelligence integration
Model invocation boundary, proposal generation, output validation, model/resource identity.

### Visibility
Logs, metrics, traces, health, audit, reconstruction.

## Capability completeness test

A proposed implementation should be traceable from each matrix row to:

1. a domain contract;
2. an authoritative interface;
3. failure semantics;
4. security boundaries;
5. durable evidence where required;
6. verification tests.

If a capability exists only as a convenience function, UI button, prompt instruction, or adapter behavior, it is not yet established as a Kernel capability.

## Boundary rule

No domain may become an implicit authority source merely because it owns data, code, a process, a socket, a database connection, a model, a queue, or an administrator-facing interface.

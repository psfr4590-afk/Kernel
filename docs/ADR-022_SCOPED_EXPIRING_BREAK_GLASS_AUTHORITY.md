# ADR-022: Scoped Expiring Break-Glass Authority

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Emergency administrative authority is explicit, narrowly scoped, expiring, and durably evidenced.

## Context
Kernel requires administrative and recovery paths without creating an invisible superuser bypass.

## Decision
Break-glass authority MUST identify the administrative principal, exact scope and purpose, explicit expiration, independent attribution, and durable audit evidence. It remains subject to the same execution boundary.

Break-glass authority MUST NOT silently bypass identity, authorization, effect enforcement, evidence, or recovery rules.

No permanent hidden emergency principal is part of the base architecture.

Multi-party approval or offline recovery mechanisms remain implementation/deployment choices unless later shown necessary by the authority model.

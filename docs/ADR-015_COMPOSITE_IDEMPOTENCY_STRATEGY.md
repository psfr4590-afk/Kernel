# ADR-015: Composite Idempotency Strategy

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Kernel uses operation identity, authorization-bound execution identity, and durable uniqueness constraints together.

## Context
Retries, duplicate delivery, process crashes, and ambiguous external outcomes can otherwise create duplicate effects.

## Decision
Each consequential operation MUST have a durable operation identity.

Execution attempts MUST be attributable to the operation and applicable authorization identity.

The authoritative store MUST enforce uniqueness for identifiers that must not be replayed as the same execution.

A request fingerprint MAY supplement identity checks, but a fingerprint alone MUST NOT prove that two requests are the same operation.

Idempotency MUST distinguish duplicate delivery, a legitimate new operation, and retry/reconciliation of an interrupted operation.

External systems remain separate trust boundaries. Kernel idempotency cannot assume a remote system is idempotent unless independently established.

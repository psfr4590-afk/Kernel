# ADR-016: Global Durable Event Order

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Kernel events receive a durable global sequence, supplemented by causation and correlation metadata.

## Context
Snapshots and replay require deterministic event ordering. Operation-local metadata alone does not provide one authoritative ordering for durable history.

## Decision
Each persisted Kernel event MUST have a durable global sequence defining its storage order.

Events MUST additionally carry causation and correlation identifiers where applicable.

Global sequence is authoritative durable ordering for replay. Causation and correlation describe relationships and MUST NOT be mistaken for ordering.

The implementation MUST define transactional sequence allocation and handling of gaps, rollback, import, and recovery.

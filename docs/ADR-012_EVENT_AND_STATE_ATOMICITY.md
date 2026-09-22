# ADR-012: Event and State Atomicity

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Authoritative event persistence and corresponding state materialization commit atomically where the storage engine supports it.

## Context
Kernel treats event history as authoritative and state as derived. Separating commits creates avoidable gaps.

## Decision
For a state transition represented by a durable event, the event record and corresponding materialized-state update MUST commit atomically within the authoritative SQLite transaction boundary.

If state materialization is intentionally deferred, the authoritative event MAY commit without immediate state materialization, but derived state MUST be marked incomplete and rebuilt from event history. An uncommitted state update is never authoritative evidence.

A transaction failure MUST NOT be reported as a successful state transition.

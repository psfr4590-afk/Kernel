# ADR Index and Decision Framework

Architecture decisions must be explicit rather than accidental consequences of a convenient library.

## ADR structure

Every settled decision should record status, date, context, problem, decision, alternatives, rationale, invariant impact, security impact, durability/recovery impact, operational consequences, migration consequences, reversal conditions, verification plan, and related contracts.

## Open decision index

- ADR-001 implementation language
- ADR-002 storage/database technology
- ADR-003 event serialization
- ADR-004 cryptographic primitives
- ADR-005 identity protocol
- ADR-006 key management
- ADR-007 policy language
- ADR-008 policy evaluation engine
- ADR-009 authorization representation
- ADR-010 delegation semantics
- ADR-011 revocation semantics
- ADR-012 transaction model
- ADR-013 IPC/transport
- ADR-014 execution adapter API
- ADR-015 idempotency strategy
- ADR-016 event ordering
- ADR-017 recovery/reconciliation
- ADR-018 state materialization
- ADR-019 audit integrity
- ADR-020 retention/archival
- ADR-021 redaction/privacy
- ADR-022 administrative/emergency authority
- ADR-023 deployment topology
- ADR-024 model-provider integration
- ADR-025 external-effect trust assumptions

## Decision gate

A technology choice becomes architectural when it materially affects invariants, authority, failure semantics, durability, recovery, or security. Such a choice requires an ADR.

## Prohibited shortcuts

A database must not silently define durability semantics. Middleware must not silently define authority. Plugin installation must not imply permission. Queue delivery must not be treated as execution success. Encryption must not be treated as authorization.

## Status

All listed decisions remain open unless separately settled by an explicit ADR.

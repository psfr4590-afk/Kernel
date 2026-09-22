# ADR-017: Evidence-First Recovery and Reconciliation

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Recovery uses durable evidence, deterministic replay, operation-specific reconciliation, and governed manual resolution when evidence is insufficient.

## Context
Kernel must recover from crashes and ambiguous external effects without inventing success or silently granting authority.

## Decision
Recovery proceeds conceptually by identifying the interrupted operation, preserving principal/scope/authorization lineage, restoring the latest valid snapshot, replaying authoritative events in durable order, determining what local evidence establishes, reconciling uncertain external completion with an operation-specific mechanism, and durably recording UNKNOWN/CONFLICT with governed resolution when evidence remains insufficient.

Recovery MUST NOT manufacture success, silently renew or broaden authority, convert reconciliation into an unauthorized retry, rewrite historical evidence, or hide ambiguity.

Manual recovery actions are new governed operations with their own authority and evidence.

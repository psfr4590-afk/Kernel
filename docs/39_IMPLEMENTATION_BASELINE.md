# Kernel Implementation Baseline

Status: IMPLEMENTATION ENTRY / RECOVERY, REVOCATION, AND PERSISTENCE CAPABILITY
Date: 2026-09-22


## Purpose

This document marks the transition from architecture-only work to controlled implementation.

The repository now contains the smallest executable Python package and test harness needed to begin the first vertical slice. This is not a claim that the Kernel is implemented.

## Initial technology boundary

- Language: Python, ADR-001.
- Authoritative local storage: SQLite, ADR-002.
- Event representation: canonical strict JSON, ADR-003.
- Cryptography: AES-256 through `cryptography`, ADR-004.
- Local key storage: encrypted local key store, ADR-006.
- Authorization: short-lived scoped authorization, ADR-009.
- State: snapshots plus event replay, ADR-018.
- Audit integrity: cryptographic hashing, ADR-019.
- Sensitive storage: controlled boundary, ADR-021.
- Model providers: explicit separate intelligence boundaries, ADR-024.
- External effects: authenticated but not inherently trusted, ADR-025.

## Implementation posture

The initial implementation is deliberately single-process and local-first under ADR-023. Internal boundaries must remain explicit even when implemented as Python calls.

The first vertical slice proves authority enforcement and durable evidence before peripheral capabilities are introduced.

## Recovery capability

The initial recovery capability is read-only and evidence-first. It reconstructs local request state from durable event history and reports UNKNOWN when the available evidence does not establish a terminal effect outcome. It does not retry, renew authorization, rewrite history, or create a new effect.

Recovery now includes durable UNKNOWN evidence recording and idempotent recovery assessment. Durable revocation is implemented. Recovery now records explicit interruption evidence without claiming an effect outcome. File-backed SQLite persistence and durable revocation survive store close/reopen verification. Recovery remains incomplete until operation-specific reconciliation and fault-injection verification are implemented.

## Dependency policy

Dependencies must be justified by an architectural or operational need. A library MUST NOT become an authority boundary merely because it provides convenient abstractions.

Runtime dependencies are kept minimal. Test and development dependencies are separate.

No model runtime, provider SDK, web framework, queue, distributed service, plugin framework, or UI is required by this baseline.

## Verification baseline

Executable verification now covers authority enforcement, durable event/state behavior, deterministic replay, recovery assessment, durable UNKNOWN evidence, interruption evidence, durable revocation, and file-backed persistence across store reopen. These tests verify implemented slices only and do not establish complete Kernel security or authority coverage.

Future claims MUST use the repository evidence vocabulary:
UNKNOWN, DESIGNED, IMPLEMENTED, VERIFIED, REGRESSED.

## Current recovery boundary

Recovery can inspect durable history, preserve uncertainty as UNKNOWN, durably record unresolved conditions and interruption evidence without creating an effect, and avoid duplicating the same recovery evidence on repeated inspection. A later authoritative terminal event supersedes the UNKNOWN assessment during replay. File-backed SQLite evidence and revocation state survive store close/reopen. Recovery does not retry, renew, or broaden authority.

## Next implementation target

Implement the core domain contracts required for:
request intake -> identity -> context -> proposal -> governance -> authorization -> execution boundary -> outcome -> event -> state.

The policy language and evaluator remain intentionally deferred until the first implementation requirements make them necessary.

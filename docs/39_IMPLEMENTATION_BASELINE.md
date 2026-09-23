# Kernel Implementation Baseline

Status: VERIFIED FIRST VERTICAL SLICE
Date: 2026-09-22

## Purpose

This document records implemented behavior, not architectural intent. Claims here are limited to behavior covered by executable verification.

## Implemented foundation

- Language: Python, ADR-001.
- Authoritative local storage: SQLite, ADR-002.
- Event representation: canonical strict JSON, ADR-003.
- Cryptography: cryptography, including Ed25519 identity and AES-256-GCM local key storage.
- Authorization: short-lived, scoped, revocable authority, ADR-009 and ADR-011.
- Event ordering and event/state atomicity: durable SQLite sequence and transactional state materialization.
- Replay and recovery: deterministic replay, durable UNKNOWN recovery, explicit external reconciliation evidence, interruption evidence, and state rematerialization.
- Audit integrity: SHA-256 event integrity hashes with explicit algorithm/version metadata, ADR-019.
- Idempotency: durable principal-scoped operation identity, canonical request fingerprinting, duplicate resolution, and conflict rejection, ADR-015.
- External effects: narrow execution adapter boundary, ADR-014 and ADR-025.

## First vertical slice

The first executable consequential path is a constrained host.filesystem.read operation.

The verified path is:

identity -> request -> durable operation claim -> proposal -> context -> governance -> authorization -> durable authorization evidence -> execution attempt -> filesystem boundary -> terminal outcome -> durable event/state -> replay/recovery.

The filesystem adapter is scoped to one configured root, rejects absolute paths and root escapes, requires a regular file, enforces a byte limit, and returns bounded result evidence. Authorization binds the consequential parameters by canonical fingerprint, so changing the authorized path after issuance is rejected.

## Failure and recovery behavior

Execution attempts are durably recorded before the adapter is invoked. If the adapter raises or terminal persistence fails after dispatch, the durable history contains the attempt but does not fabricate SUCCESS. Recovery reconstructs the request as UNKNOWN and requires reconciliation until authoritative terminal evidence exists.

Equivalent duplicate requests using the same principal, operation, and idempotency key resolve to the existing operation without a second effect. A materially different canonical request using the same key is rejected as an idempotency conflict. A later terminal event supersedes an earlier UNKNOWN assessment.

## Identity and local key storage

The pipeline can authenticate a principal through the local cryptographic identity provider before request intake. Identity keys can be persisted in an encrypted local AES-256-GCM store using a passphrase-derived key. Tampering and incorrect passphrases fail closed.

## Verification baseline

CI verifies linting and the executable test suite after each implementation change. Current coverage includes authority boundaries, parameter binding, identity authentication, encrypted key storage, durable operation idempotency, execution lifecycle evidence, filesystem containment, event integrity, durable persistence, revocation, interruption, UNKNOWN recovery, explicit reconciliation, replay, and state rematerialization.

The evidence vocabulary remains:

UNKNOWN, DESIGNED, IMPLEMENTED, VERIFIED, REGRESSED.

## Remaining architectural boundaries

The policy language and policy evaluator remain intentionally deferred.

Operation-specific external reconciliation, administrative authority, scheduling/resource domains beyond the first filesystem limit, isolation/IPC, richer observation interfaces, model-provider integration, and broader integration surfaces remain outside this first verified slice. They must be implemented without weakening the established identity, governance, authorization, execution, durability, integrity, and recovery boundaries.

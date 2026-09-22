# ADR-006: Encrypted Local Key Store

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel requires local-first key management without making plaintext long-lived secret material the normal persistent representation.

## Decision

Kernel will use an **encrypted local key store using AES-256** for persistent Kernel-managed key material.

The key store is a controlled Kernel security boundary. Access is mediated by Kernel-defined authorization and key-management rules rather than direct unrestricted application access.

Plaintext keys must not be persisted as ordinary application data.

Key identity, purpose, scope, lifecycle state, and provenance must be distinguishable from the secret key material itself.

The exact root-key establishment, wrapping hierarchy, rotation procedure, and platform integration remain implementation decisions and must not be invented implicitly by a storage implementation.

## Architectural consequences

The local-first model is preserved without requiring an external secret-management service for the initial implementation.

The key store does not grant authority merely because a key can be retrieved. Key use remains subject to Kernel authorization.

## Verification

Tests must cover unauthorized access, wrong-key handling, corruption, rotation, deletion/retirement semantics, process restart, and failure without secret disclosure.

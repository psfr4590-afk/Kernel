# ADR-021: Strictly Controlled Sensitive Storage

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Some Kernel evidence and configuration may contain sensitive material. Privacy cannot be achieved merely by hiding fields in a general-purpose store.

## Decision

Sensitive material will be stored in a **strictly controlled storage boundary** with explicit access control and Kernel-mediated access.

Sensitive storage must have defined data classification, purpose, authorization requirements, auditability, retention behavior, and failure semantics.

Sensitive data must not become authority merely because it is stored in a protected location.

The exact encryption, redaction, field-level protection, and deletion mechanisms remain implementation-level decisions constrained by this boundary and the cryptographic ADRs.

## Verification

Tests must cover unauthorized reads/writes, privilege separation, audit evidence, retention enforcement, corruption/failure, and accidental disclosure through logs, errors, or observations.

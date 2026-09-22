# ADR-005: Cryptographic Identity and OS/Process Binding

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Kernel identities use cryptographic identity material with OS/process binding for local attribution.

## Context
Kernel authority must attach to an attributable principal. Untrusted names, model output, role text, or caller-supplied identity claims cannot establish authority. The Kernel also uses an encrypted local key store and short-lived scoped authorization, so identity must have a durable cryptographic root while remaining attributable to the local execution context.

## Decision
Kernel will use cryptographic identity material as the authoritative identity basis, with OS/process binding used as an additional local attribution and confinement signal.

Cryptographic identity establishes the identity presented to Kernel. OS/process binding establishes the local execution context presenting that identity. Neither layer alone silently grants authorization.

Identity records MUST preserve provenance and MUST be independently validated before authority is attached.

The exact identity protocol, key encoding, platform-specific binding mechanism, credential presentation format, and cross-platform implementation details remain implementation-level matters unless they materially change the authority model, in which case a new ADR is required.

## Consequences
- Model-generated identity claims cannot establish principal identity.
- Identity remains separate from authorization and policy.
- Local process compromise does not become an implicit authority escalation path.
- Cross-platform behavior must preserve the same authority semantics.
- Provider, adapter, and external-system identities remain distinct trust boundaries.

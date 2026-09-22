# ADR-009: Short-Lived Scoped Authorization

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel authorization must be explicit, bounded, attributable, and resistant to stale authority.

## Decision

Kernel authorization will be represented by an authorization record with an explicit **key/authorization identity, principal binding, scope, and expiration time**.

Authorization will be **short-lived** and must carry an explicit expiration timer/deadline.

An expired authorization is invalid and cannot be silently renewed or treated as still authoritative.

Scope must be explicit and bounded. Possession of an authorization identifier or key reference does not imply authority outside the recorded scope.

The exact wire/token encoding remains an implementation concern governed by this contract.

## Important boundary

Expiration is not equivalent to revocation. Immediate revocation semantics remain a separate decision under OD-011.

## Verification

Tests must prove expiration enforcement, scope confinement, principal binding, stale-authorization rejection, clock handling, and rejection of scope expansion.

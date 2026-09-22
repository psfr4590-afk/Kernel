# ADR-020: Retention Classes and Periodic Compression

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel must retain durable evidence long enough to support reconstruction, audit, and recovery without treating unlimited raw storage as the only possible design.

## Decision

Kernel will use **retention classes** with class-specific lifecycle rules and **periodic compression** of eligible retained material.

Retention classes must be explicit and must not silently change the authority or meaning of historical evidence.

Compression is a storage optimization. It must be lossless for evidence that remains authoritative.

Deletion or expiration of retained material requires an explicit retention policy and must not silently destroy information required by an active recovery or audit obligation.

## Architectural consequences

Storage lifecycle can be managed according to evidence requirements rather than one universal retention period.

Compression does not permit mutation of historical meaning.

## Verification

Tests must cover class assignment, retention transitions, compression/decompression integrity, recovery from compressed material, policy changes, and protection of records that cannot yet be retired.

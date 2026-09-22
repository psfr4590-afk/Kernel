# ADR-004: AES-256 and the Cryptography Library

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel requires confidentiality and cryptographic protection for secrets and sensitive durable material. The implementation must use established cryptographic primitives rather than inventing cryptography.

## Decision

Kernel will use **AES-256** for symmetric encryption where symmetric encryption is required, implemented through the Python **cryptography** library.

Cryptographic construction details must use authenticated encryption where confidentiality and integrity are jointly required. The exact construction and parameter choices must be explicitly fixed and tested before the relevant implementation boundary is considered complete.

Kernel will not implement cryptographic primitives itself.

## Architectural consequences

The cryptography dependency becomes part of the trusted security boundary for the components that use it. Keys, nonces/IVs, authentication tags, rotation, failure handling, and algorithm-version metadata must be governed by separate contracts and tests.

AES-256 does not itself define key storage, key lifecycle, authorization, or audit semantics.

## Invariant impact

Cryptographic protection must not create authority, bypass authorization, or make unverifiable evidence authoritative.

## Reversal conditions

Changing the primitive or cryptography library requires a new ADR and migration/crypto-agility evidence.

## Verification

Tests must cover encryption/decryption failure, authentication failure, wrong-key behavior, key separation, nonce/IV requirements, serialization compatibility, and secret non-disclosure.

# Kernel Secrets, Cryptography, and Integrity Model

Status: FOUNDATIONAL DESIGN. No cryptographic implementation is selected.

## 1. Purpose

Kernel may require integrity, authenticity, confidentiality, and non-repudiation-like evidence. These properties must not be claimed before their mechanisms and assumptions are defined.

## 2. Security Properties

The architecture must distinguish:

- confidentiality;
- integrity;
- authenticity;
- authorization;
- provenance;
- tamper evidence;
- availability.

Cryptography can support some of these properties but does not replace governance.

## 3. Key Material

Key lifecycle must cover:

generation;
storage;
use;
rotation;
revocation;
backup;
recovery;
destruction.

Exact mechanism is UNKNOWN.

## 4. Authorization Evidence

If authorizations are cryptographically represented, the verification boundary MUST validate:

- issuer;
- integrity/authenticity;
- subject/principal;
- operation;
- scope;
- validity;
- conditions;
- version;
- revocation/invalidity status where applicable.

## 5. Event Integrity

If durable events require tamper evidence, the architecture must define what attackers are protected against and what integrity mechanism supports that claim.

A hash alone does not prove who created the data.

## 6. Secret Separation

Secrets MUST NOT be casually embedded in logs, proposals, events, audit exports, or ordinary configuration.

## 7. Cryptographic Agility

Where cryptography is used, algorithm identifiers and migration semantics SHOULD be explicit enough to permit controlled replacement.

## 8. Failure

Cryptographic verification failure MUST be distinguishable from ordinary authorization denial and ordinary execution failure.

## 9. Open Decisions

Algorithms, libraries, key hierarchy, storage, rotation, signatures, hashes, secure enclaves, HSM use, and migration strategy remain UNKNOWN.

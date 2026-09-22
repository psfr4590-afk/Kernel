# ADR-003: Canonical JSON Event Serialization

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel events are durable evidence. Their representation must not permit multiple interpretations of the same event, duplicate-key ambiguity, silent type coercion, or representation changes that alter evidence after recording.

## Decision

Kernel will use **JSON as the event serialization format**, with a strict canonical representation and schema validation.

The serialized event is the immutable evidence representation. Implementations must not treat an event as a freely mutable in-memory dictionary and then assume the resulting bytes are equivalent.

The event contract will require:

- UTF-8 encoding;
- an explicit schema version;
- a fixed set of required fields and explicitly defined optional fields;
- unique object member names;
- no duplicate-key interpretation;
- no NaN or Infinity numeric values;
- explicit data types;
- deterministic field ordering for the canonical serialized form;
- deterministic encoding of values;
- explicit timestamp format and timezone semantics;
- rejection of unknown or ambiguous authority-bearing fields unless the schema explicitly permits them;
- validation before persistence;
- canonical serialization before hashing or integrity processing.

After persistence, the serialized event evidence is immutable. Any correction, interpretation, or derived information is represented by a new event rather than mutation of the original evidence.

The in-memory representation used by Python may be mutable during construction, but the validated event object crossing the persistence boundary must be treated as immutable by contract.

## Architectural consequences

JSON remains human-inspectable and broadly interoperable while canonicalization removes representation ambiguity.

The exact Python immutable object implementation and canonicalization library/mechanism are implementation details and must preserve this contract.

## Invariant impact

Preserves event immutability, evidence integrity, provenance, deterministic reconstruction, and representation independence.

## Reversal conditions

Changing the event serialization format requires a new ADR and migration/reconstruction evidence. It must not silently change the meaning of historical evidence.

## Verification

Tests must prove rejection of duplicate/ambiguous fields, invalid types, non-canonical values, unsupported numeric values, schema violations, mutation after validation, and non-deterministic serialization.

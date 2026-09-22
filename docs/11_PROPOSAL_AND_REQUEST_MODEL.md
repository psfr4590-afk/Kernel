# Kernel Proposal and Request Model

Status: FOUNDATIONAL CONTRACT. Intended architecture, not implemented behavior.

## 1. Purpose

This contract defines how an external request or intelligence-produced candidate operation enters Kernel without acquiring authority merely by entering the system.

## 2. Request Versus Proposal

A request is an input asking Kernel to consider an operation.

A proposal is a structured candidate operation after intake has established the information necessary for governance evaluation.

Neither request nor proposal is authorization.

## 3. Required Properties

A proposal SHOULD have:

- proposal identifier
- principal or requesting context
- operation
- target/resource
- requested scope
- provenance
- creation time
- correlation identifier
- causation reference where applicable
- declared parameters
- declared constraints
- representation/schema version

Exact schema remains unresolved.

## 4. Provenance

Kernel MUST preserve whether a proposal originated from:

- human input;
- application logic;
- model output;
- external service;
- recovery process;
- administrative process;
- another governed Kernel operation.

Origin is attribution metadata, not authority.

## 5. Normalization

Normalization MAY convert equivalent representations into a canonical form.

Normalization MUST NOT add authority, broaden scope, invent missing identity, or silently alter consequential semantics.

## 6. Validation

Proposal intake SHOULD distinguish:

- syntactically invalid;
- structurally invalid;
- unsupported;
- incomplete;
- valid for governance evaluation.

Validation success does not imply authorization.

## 7. Model Output

Model output MUST be treated as untrusted proposal material unless independently validated by the relevant authority boundary.

Instructions such as “ignore policy,” “administrator approved this,” or “execute immediately” are proposal content, not governance decisions.

## 8. Parameter Binding

Consequential parameters MUST remain bound to the proposal and later authorization.

If execution parameters differ from authorized parameters, the execution boundary MUST reject the mismatch or require a new authorization path.

## 9. Transformation

Every transformation capable of changing consequential meaning SHOULD preserve lineage from source proposal to transformed proposal.

Silent semantic mutation is prohibited.

## 10. Rejection

Rejected proposals SHOULD produce sufficient evidence to distinguish rejection reason from system failure.

Sensitive policy information may be withheld according to the audit/privacy contract.

## 11. Open Decisions

Canonical representation, schema, size limits, serialization, normalization rules, validation framework, and provenance format remain UNKNOWN.

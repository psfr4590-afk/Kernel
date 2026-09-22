# ADR-001: Python as the Kernel Implementation Language

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel must provide the governed substrate around interchangeable intelligence components, including machine-learning models and training/inference pipelines. The implementation language should therefore support the surrounding AI/ML ecosystem without creating a language boundary between the Kernel and the systems it is intended to govern.

Python is selected because it is already a primary implementation language for ML software, model tooling, inference systems, data processing, and training pipelines relevant to Kernel's intended environment. A common language across these areas reduces integration friction and keeps the Model MechSuit boundary straightforward.

This is a local-first system. Python also provides direct standard-library access to SQLite through `sqlite3`, allowing the initial implementation to use a local durable database without introducing a separate database service.

## Decision

Kernel will be implemented in **Python**.

Python is the implementation language for the Kernel core and its initial first-party components unless a later ADR establishes a justified exception for a specific boundary.

Python does not grant a dependency or component authority. The authority model remains independent of language choice.

## Architectural consequences

Positive:

- Common language across Kernel, ML tooling, model integration, training/inference pipelines, and local automation.
- Large ecosystem for testing, serialization, data handling, process management, cryptography integrations, and ML interoperability.
- Straightforward local-first development and distribution.
- Direct access to SQLite through the Python standard library.
- Lower integration friction when Kernel governs Python-based intelligence and ML workloads.

Constraints:

- Python implementation details must not be allowed to weaken isolation, authority enforcement, durability, or resource controls.
- Native extensions and third-party packages remain untrusted dependencies until their role and trust boundary are established.
- Performance-sensitive or security-critical boundaries must be measured and verified rather than assumed safe or fast because they are implemented in Python.

## Alternatives considered

### Rust

Strong systems-level control and performance, but would introduce a separate implementation language from the ML ecosystem that Kernel is intended to surround. It remains a possible future language for a narrowly justified component, but is not selected for the initial Kernel implementation.

### Go

Strong concurrency and deployment characteristics, but similarly introduces a separate implementation ecosystem from the Python-centric ML/model environment targeted by the first implementation.

### JavaScript/TypeScript

Useful for application interfaces and some orchestration environments, but not selected as the Kernel core because it would place the authority substrate outside the primary ML/model implementation ecosystem.

## Invariant impact

Language selection does not change Kernel's invariants.

In particular:

- model output remains untrusted input;
- proposal remains distinct from authorization;
- capability remains distinct from permission;
- identity remains independent of model claims;
- execution remains downstream of explicit authorization;
- durable evidence remains authoritative over materialized state;
- recovery cannot invent authority or success.

## Reversal conditions

This decision should be reconsidered only if executable evidence demonstrates that Python cannot satisfy a material Kernel requirement such as security-boundary enforcement, isolation, deterministic behavior, resource control, durability, required performance, deployment constraints, or maintainability.

Such reconsideration requires a new ADR and evidence.

## Verification

The implementation must establish reproducible Python version/toolchain requirements and verify that the selected runtime and dependencies preserve the architectural contracts.
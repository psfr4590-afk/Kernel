# ADR-023: Local-First, Topology-Independent Deployment

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: The initial Kernel deployment is single-process/local-first while preserving topology-independent contracts.

## Context
Kernel needs a small trusted implementation before introducing process or network boundaries. Premature distribution adds failure and authority surfaces without improving the foundational contract.

## Decision
The first implementation targets a single local process with clear internal boundaries.

The architecture MUST NOT make single-process execution a requirement of the authority model. Components that later cross process or machine boundaries MUST preserve the same structured contracts, identity semantics, authorization semantics, event evidence, and recovery rules.

No microservice topology is required by the architecture.

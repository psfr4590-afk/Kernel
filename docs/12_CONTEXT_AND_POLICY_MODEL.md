# Kernel Context and Policy Model

Status: FOUNDATIONAL CONTRACT. Intended architecture, not implemented behavior.

## 1. Purpose

This contract defines how Kernel determines which information and rules are relevant to a governance decision.

## 2. Context

Context is evidence or information used to interpret a proposal or evaluate policy.

Examples may include:

- principal;
- session;
- resource state;
- environment;
- time;
- delegation;
- prior events;
- policy version;
- operational conditions.

Context is not automatically authority.

## 3. Context Provenance

Context SHOULD identify:

- source;
- acquisition time;
- freshness where relevant;
- version where applicable;
- integrity status;
- trust classification.

The implementation must define which context sources are authoritative.

## 4. Stale Context

When freshness matters, stale context MUST NOT silently satisfy a requirement defined for current context.

The policy contract must define acceptable staleness per context type.

## 5. Missing Context

Missing required context MUST be distinguishable from a negative policy result.

The system MUST NOT convert “unable to evaluate” into “allowed.”

## 6. Policy Definition

Policy defines rules and constraints.

Policy definition MUST be distinct from:

- policy evaluation;
- authorization decision;
- execution result.

## 7. Policy Evaluation

A policy evaluation SHOULD record:

- policy identity;
- policy version;
- input references;
- relevant context;
- result;
- conditions;
- evaluation errors;
- evaluator provenance.

## 8. Evaluation Outcomes

At minimum, governance should distinguish:

- allow/eligible;
- deny;
- indeterminate;
- evaluation failure.

Whether “allow” directly produces authorization is an explicit architectural decision.

## 9. Policy Conflicts

The policy model MUST define precedence when applicable rules conflict.

No implementation may invent precedence implicitly through evaluation order.

## 10. Policy Changes

A consequential decision SHOULD retain enough policy identity/version information to explain which rules produced it.

## 11. Open Decisions

Policy language, precedence, inheritance, conflict resolution, evaluation determinism, policy distribution, policy signing, caching, and hot reload remain UNKNOWN.

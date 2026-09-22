# Kernel Identity, Governance, and Authorization Model

Status: FOUNDATIONAL DESIGN. Intended contract, not implemented behavior.

## 1. Purpose

This document defines the separation between who is acting, what is proposed, what governance permits, and what execution may do.

## 2. Principal

A principal is the attributable actor to whom authority is attached.

Possible principal classes may include human, application, service, delegated process, or external system. Exact classes are unresolved.

A principal MUST NOT be established solely by an untrusted assertion.

## 3. Identity

Identity answers: who is this actor?

Authentication answers: what evidence supports that identity?

Authorization answers: what may that identified principal do?

These are separate questions.

## 4. Context

Context may include session, resource scope, tenancy, environment, time, operation history, policy version, delegation, and relevant state.

Context MUST NOT silently become authority merely because it is available.

## 5. Governance

Governance evaluates whether a proposal is eligible for authorization.

A governance evaluation SHOULD be attributable to:

- principal
- proposal
- applicable policy
- policy version
- context
- decision
- conditions
- evidence used

## 6. Authorization

Authorization is an explicit bounded permission.

It SHOULD bind:

principal + operation + resource/scope + conditions + validity + policy provenance.

A generic "allowed" flag without defined scope is insufficient as a conceptual model.

## 7. Delegation

Delegation, if supported, MUST preserve provenance and bounded scope.

A delegate MUST NOT receive more authority than the delegating principal can legitimately confer.

Delegation semantics are defined by ADR-010.

## 8. Revocation

The architecture must define whether and how authorizations can be revoked, and what happens to operations already in progress.

These semantics are UNKNOWN.

## 9. Policy

Policy is a governance input, not itself proof that an action was authorized.

The system MUST distinguish policy definition, policy evaluation, authorization decision, and execution result.

## 10. Model-Generated Identity

Model output may contain names, roles, credentials, approval claims, or authority language. Such content MUST be treated as proposal/context data unless independently authenticated and validated by the authority system.

## 11. Privilege Boundaries

Every capability exposed to an execution adapter SHOULD have an explicit authority boundary.

Administrative, maintenance, bootstrap, and recovery capabilities require their own authority model and MUST NOT become hidden bypasses.

## 12. Denial

A denial SHOULD identify enough reason/evidence to support audit and debugging without unnecessarily disclosing sensitive policy material.

## 13. Expiration

Authorizations SHOULD have defined validity boundaries where temporal scope matters.

Expired or otherwise invalid authorization MUST NOT satisfy a current execution precondition.

## 14. Open Decisions

Identity protocol, credentials, delegation, revocation, policy language, policy evaluation engine, approval workflows, secrets handling, and authorization token format remain unresolved.

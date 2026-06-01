# CIPHER Agentic Validation Framework (CAVF)

## Overview

The **CIPHER Agentic Validation Framework (CAVF)** is the core testing and verification methodology required to ensure that all agents operating within the CIPHER ecosystem strictly adhere to their designated autonomy tiers, security boundaries, and NICE role constraints.

CAVF acts as an automated safety net, validating that the Zero-Trust architecture is practically enforced during runtime orchestration and inter-agent communication. No feature or agent may be merged into production without passing its respective CAVF criteria.

---

## 1. Core Principles

1. **Provable Identity:** Every action must be cryptographically tied to a verified agent or human operator.
2. **Deny by Default:** State transitions, tool invocations, and memory access must explicitly prove authorization.
3. **Immutability of Audit:** Safety violations must be logged immutably and cannot be suppressed by the violating agent.
4. **Tiered Containment:** Autonomous execution (T3) must be strictly cordoned from high-impact actions (T1/T2), regardless of agent logic or LLM hallucinations.

---

## 2. Universal CAVF Criteria

Every component affecting state changes must pass the following universal tests:

### 2.1 Identity Gate Validation
- **Requirement:** Any request (tool execution, memory access, or LangGraph state transition) MUST present a valid, unexpired SVID (SPIFFE Verifiable Identity Document).
- **Test Condition:** Requests with missing, expired, unsigned, or cross-tenant SVIDs must be explicitly rejected (403/401) before any logic or policy evaluation occurs.

### 2.2 Autonomy & Orchestration Routing
- **T3 (Autonomous):** Validate that requests classified and flagged as T3 by the Autonomy Gate bypass the human approval node and proceed directly to execution.
- **T1/T2 (Administered/Copiloted):** Validate that requests classified as T1 or T2 are successfully intercepted by the Trust Broker/Orchestrator, routed to the `Human_Approval` queue (via NATS JetStream), and the requesting agent is placed in a suspended `WAITING` state pending explicit cryptographic approval (tied to Keycloak authentication).

### 2.3 Policy Enforcement Boundary
- **Requirement:** Action authorization must query the OPA engine.
- **Test Condition:** If an agent attempts an action outside its defined NICE role scope or autonomy capabilities, the system must enforce a 403 Forbidden response, gracefully log the denial to the WORM audit ledger, and prevent orchestration crash.

### 2.4 Data Plane Provenance
- **Requirement:** Semantic memory writes must contain valid provenance metadata.
- **Test Condition:** Any write attempt to a semantic collection (ChromaDB/Weaviate) without a cryptographic hash, source trust score, and provenance trace must be rejected by the MemoryManager.

---

## 3. Component-Specific CAVF

### 3.1 Trust Broker CAVF
*(See Issue #001 for implementation details)*
- Must enforce Identity Gate (2.1).
- Must enforce Policy Enforcement Boundary (2.3).
- Must mediate Autonomy Routing constraints (2.2).

### 3.2 Agent-Specific CAVF
When a new NICE persona (e.g., `agent-pd-defensive`) is implemented, it must include automated tests proving:
- It cannot successfully invoke tools listed in its `forbidden_tools` specification.
- It gracefully handles a Trust Broker denial (e.g., backing off, escalating, or alerting) without entering an infinite retry loop.

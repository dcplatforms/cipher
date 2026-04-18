# CIPHER — Architecture Specification v0.1

**Cybersecurity Intelligence Personas for Human-in-the-loop Enterprise Response**

> Open-source, NICE 2.0-aligned, multi-modal agentic cybersecurity workforce framework.
> Supports autonomous, copiloted, and human-administered operational modes.
> Built for enterprise-grade resilience, interoperability, and secure separation of duties.

---

## 1. Design Principles

1. **NICE-First**: Every agent persona maps 1:1 to a NICE 2.0 Work Role. No role is invented outside the framework.
2. **Zero-Trust Inter-Agent**: No agent trusts another by default. All inter-agent communication is cryptographically signed and policy-evaluated.
3. **Defense-in-Depth Memory**: Memory is layered, scoped, immutable where required, and provenance-tracked at every write.
4. **Autonomy as a Gate, Not a Default**: Actions are tier-classified. Autonomous execution is earned by confidence + role policy, not assumed.
5. **Observe Everything**: Every agent action, memory read/write, inter-agent message, and policy decision is logged immutably with OpenTelemetry traces.
6. **LLM Agnostic**: Any compliant LLM (OpenAI, Anthropic, Mistral, Ollama) can power any agent. Model selection is config-driven per role.
7. **Open by Design**: MIT license, standard interfaces (OpenAPI, OpenTelemetry, NATS, SPIFFE), no vendor lock-in.
8. **Resilience at Every Layer**: No single point of failure in orchestration, memory, security, or integration planes.

---

## 2. NICE 2.0 Work Role Taxonomy

CIPHER maps all **41 NICE Framework v2.1 Work Roles** across 5 categories:

### 2.1 Category Overview

| Category | Code | Roles | Agent Priority |
|----------|------|-------|---------------|
| Oversight & Governance | OG | 16 | Phase 3 |
| Design & Development | DD | 9 | Phase 3 |
| Implementation & Operation | IO | 7 | Phase 2 |
| Protection & Defense | PD | 7 | **Phase 1** |
| Investigation | IN | 2 | Phase 2 |

### 2.2 Protection & Defense — Phase 1 Agents (Highest Operational Priority)

| NICE Role | CIPHER Agent Name | Autonomy Default | Primary Tools |
|-----------|------------------|-----------------|---------------|
| Defensive Cybersecurity | `agent-pd-defensive` | T3 (Autonomous) | SIEM, EDR, firewall query |
| Incident Response | `agent-pd-ir` | T2 (Copiloted) | SOAR, ticketing, playbooks |
| Digital Forensics | `agent-pd-forensics` | T2 (Copiloted) | Evidence store, chain-of-custody |
| Infrastructure Support | `agent-pd-infra` | T3 (Autonomous) | Config scanners, asset DB |
| Insider Threat Analysis | `agent-pd-insider` | T2 (Copiloted) | UEBA, HR integration |
| Threat Analysis | `agent-pd-threat` | T3 (Autonomous) | Threat intel feeds, MITRE ATT&CK |
| Vulnerability Analysis | `agent-pd-vuln` | T3 (Autonomous) | Vuln scanners, CVE DB |

### 2.3 Investigation — Phase 2 Agents

| NICE Role | CIPHER Agent Name | Autonomy Default |
|-----------|------------------|-----------------|
| Cybercrime Investigation | `agent-in-cybercrime` | T1 (Human-Administered) |
| Digital Evidence Analysis | `agent-in-evidence` | T2 (Copiloted) |

### 2.4 Implementation & Operation — Phase 2 Agents

| NICE Role | CIPHER Agent Name | Autonomy Default |
|-----------|------------------|-----------------|
| Systems Administration | `agent-io-sysadmin` | T2 |
| Network Operations | `agent-io-netops` | T2 |
| Systems Security Analysis | `agent-io-security-analysis` | T2 |
| Data Analysis | `agent-io-data` | T3 |
| Database Administration | `agent-io-dba` | T2 |
| Knowledge Management | `agent-io-km` | T3 |
| Technical Support | `agent-io-support` | T3 |

### 2.5 Oversight & Governance + Design & Development — Phase 3 Agents

Full roster in `/specs/personas/` — one YAML spec per role.

---

## 3. Autonomy Gate Engine

### 3.1 Tier Definitions

```
TIER 3 — AUTONOMOUS
  Agent executes without human approval.
  Requires: confidence_score >= 0.92 AND role_policy.allows_autonomous == true
            AND action_risk_class == LOW
  Examples: log ingestion, alert enrichment, IOC lookup, ticket creation,
            CVE lookup, threat intel correlation, asset inventory queries

TIER 2 — COPILOTED (Human-in-the-Loop)
  Agent proposes action + rationale. Human approves/rejects via approval API.
  Requires: confidence_score >= 0.75 OR action_risk_class == MEDIUM
  Timeout: 30 min default (configurable). On timeout → escalate or abort.
  Examples: IOC blocking, endpoint isolation recommendation, patch advisory,
            incident classification, evidence collection request, escalation

TIER 1 — HUMAN-ADMINISTERED
  Agent provides analysis and recommended actions. Human executes.
  Agent cannot invoke T1 tools directly under any circumstances.
  Examples: network quarantine, legal hold, external agency notification,
            public disclosure, system shutdown, criminal referral
```

### 3.2 Risk Classification Schema

```yaml
risk_classes:
  LOW:
    - read_only_query
    - external_lookup          # VirusTotal, Shodan, etc.
    - alert_enrichment
    - log_ingestion
    - ticket_creation
    - report_generation
  MEDIUM:
    - blocking_recommendation
    - isolation_recommendation
    - configuration_change_recommendation
    - evidence_tagging
    - incident_escalation
    - patch_recommendation
  HIGH:
    - network_isolation_execution
    - host_quarantine_execution
    - service_termination
    - credential_revocation
    - legal_hold_initiation
    - external_notification
    - public_disclosure
```

### 3.3 Autonomy Gate Flow

```
Agent proposes action
        │
        ▼
┌───────────────────┐
│ Autonomy Gate     │
│ 1. Classify risk  │
│ 2. Check role     │
│    policy         │
│ 3. Score          │
│    confidence     │
└───────────────────┘
        │
   ┌────┴────┐
   │         │
  LOW       MED/HIGH
   │         │
  T3→       ┌┴──────┐
 Execute    T2      T1
  + Log    Approval  Human
            Queue   Advised
```

---

## 4. Memory Architecture

### 4.1 Memory Planes

Each agent has access to a **scoped, layered memory stack**:

```
┌─────────────────────────────────────────────────────────────┐
│                   AGENT MEMORY STACK                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ WORKING MEMORY — Redis (TTL = session duration)     │   │
│  │ Scope: read/write own namespace only                │   │
│  │ Content: active task context, current alert state,  │   │
│  │          tool results, conversation turns           │   │
│  │ Security: namespace key = agent_id + session_token  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ EPISODIC MEMORY — TimescaleDB (append-only)         │   │
│  │ Scope: write own; read cross-role if authorized     │   │
│  │ Content: every action, observation, decision        │   │
│  │          timestamped + agent_id + confidence score  │   │
│  │ Security: WORM (no UPDATE/DELETE ever); hash chain  │   │
│  │           each row includes hash of previous row    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SEMANTIC MEMORY — ChromaDB / Weaviate               │   │
│  │ Scope: role-scoped collections; RBAC on read/write  │   │
│  │ Content: threat intel, CVE data, MITRE ATT&CK,      │   │
│  │          org policies, prior incident embeddings    │   │
│  │ Security: source trust score on every entry;        │   │
│  │           provenance metadata required;             │   │
│  │           cryptographic hash of content at write    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PROCEDURAL MEMORY — Playbook Store (YAML/JSON)      │   │
│  │ Scope: role + autonomy tier determines which        │   │
│  │        playbooks are visible to agent               │   │
│  │ Content: SOPs, runbooks, decision trees,            │   │
│  │          escalation paths, tool invocation rules    │   │
│  │ Security: GPG-signed, version-controlled,           │   │
│  │           tamper-evident; agent reads but never     │   │
│  │           modifies playbooks (read-only for agents) │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ CREDENTIAL STORE — Infisical (open-source Vault)    │   │
│  │ Scope: per-agent, per-source API keys only          │   │
│  │ Content: integration API keys, service tokens       │   │
│  │ Security: keys never in agent context window;       │   │
│  │           agents call secrets proxy; auto-rotation; │   │
│  │           every access logged                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Memory Namespace Schema

```
cipher/
├── agents/
│   └── {agent_id}/
│       ├── working/         # Redis namespace key prefix
│       ├── episodic/        # TimescaleDB schema: agent_{id}_events
│       ├── semantic/        # ChromaDB collection: {agent_role}_{tenant_id}
│       └── credentials/     # Infisical path: /cipher/{tenant}/{agent_id}/
└── shared/
    ├── threat_intel/        # Read: PD+AN agents; Write: threat_intel_ingestion svc
    ├── playbooks/           # Read: role-filtered; Write: human operators only
    └── audit_ledger/        # Read: OG agents + operators; Write: all agents (append-only)
```

### 4.3 Memory Provenance Record (every semantic memory write)

```json
{
  "content_hash": "sha256:...",
  "source_type": "threat_intel_feed | siem_log | agent_analysis | human_input",
  "source_id": "misp-feed-01 | splunk-prod | agent-pd-threat | operator:jsmith",
  "source_trust_score": 0.85,
  "ingested_by_agent": "agent-pd-threat",
  "ingested_at": "2026-04-17T21:00:00Z",
  "verified_by": null,
  "quarantine_flag": false,
  "ttl_days": 90
}
```

---

## 5. Security Plane

### 5.1 Agent Identity — SPIFFE/SPIRE

Every CIPHER agent has a cryptographically verifiable identity:

```
SPIFFE ID format:
spiffe://cipher.{tenant_id}/ns/cipher/sa/{agent_role}/{agent_instance_id}

Example:
spiffe://cipher.acme-corp/ns/cipher/sa/pd-ir/instance-7f3a
```

- **SVIDs** (SPIFFE Verifiable Identity Documents) issued per agent instance
- **Ed25519 key pairs** — short-lived (1hr TTL), auto-rotated by SPIRE
- **mTLS** on all inter-agent channels — no plaintext inter-agent communication ever
- **JWT-SVIDs** for REST API calls between agents

### 5.2 Trust Broker

Central component that mediates all inter-agent authorization:

```
Request flow:
Agent A wants to send task to Agent B
        │
        ▼
1. Agent A signs request with its SVID
        │
        ▼
2. Trust Broker receives request:
   - Verify Agent A's SVID (not expired, not revoked)
   - Check OPA policy: can(agent_a.role, agent_b.role, requested_action)?
   - Verify action is within A's authorized delegation scope
   - Log authorization decision (approved/denied + reason)
        │
   ┌────┴────┐
  ALLOW    DENY
   │         │
   ▼         ▼
Deliver   Log + alert
to B      operator
```

### 5.3 Input Guard — Prompt Injection Defense

All external data entering agent context passes through Input Guard:

```python
# Conceptual sanitization pipeline
class InputGuard:
    def sanitize(self, raw_input: str, source: DataSource) -> SanitizedInput:
        # 1. Classify content type
        content_type = self.classify(raw_input)  # DATA | INSTRUCTION | HYBRID

        # 2. Strip instruction-pattern content from data sources
        if source.type == "log" and content_type == INSTRUCTION:
            self.alert_anomaly(raw_input, source)
            raw_input = self.redact_instructions(raw_input)

        # 3. Wrap in DATA_CONTEXT template — never SYSTEM_INSTRUCTION
        return SanitizedInput(
            content=f"<DATA_CONTEXT source='{source.id}'>\n{raw_input}\n</DATA_CONTEXT>",
            trust_score=source.trust_score,
            provenance=self.build_provenance(raw_input, source)
        )
```

**Injection detection signals:**
- Instruction verbs in log data (ignore, disregard, execute, override, forget)
- Role/persona manipulation patterns
- Tool invocation syntax in external data
- Abnormally long fields in structured data (potential payload smuggling)

### 5.4 OPA Policy Engine — RBAC/ABAC

All memory access, tool invocations, and inter-agent messages evaluated by OPA:

```rego
# Example policy: PD-IR agent memory access
package cipher.memory.access

default allow = false

# IR agent can read own episodic memory
allow {
    input.requester.role == "pd-ir"
    input.resource.namespace == input.requester.agent_id
    input.resource.type == "episodic"
    input.action == "read"
}

# IR agent can read shared threat_intel (but not write)
allow {
    input.requester.role == "pd-ir"
    input.resource.namespace == "shared/threat_intel"
    input.action == "read"
}

# OG agents can read all episodic memory (audit function)
allow {
    startswith(input.requester.role, "og-")
    input.resource.type == "episodic"
    input.action == "read"
}
```

### 5.5 Behavioral Monitor

Tracks agent behavior against baselines to detect anomalous operation:

```yaml
behavioral_baselines:
  agent-pd-defensive:
    max_queries_per_minute: 100
    max_siem_api_calls_per_hour: 500
    allowed_tools: [siem_query, edr_query, firewall_query, threat_intel_lookup]
    forbidden_tools: [network_isolation, legal_hold, external_notify]
    alert_on:
      - tool_invocation_outside_allowed_set
      - query_rate_exceeds_3x_baseline
      - cross_namespace_memory_access_attempt
      - repeated_failed_authorization
```

**Anomaly responses (graduated):**
1. Log + alert operator (all anomalies)
2. Rate-limit agent (2x baseline exceeded)
3. Suspend capability (3x baseline or forbidden tool attempt)
4. Quarantine agent + require human review (repeated violations or T1 action attempt)

### 5.6 Full Threat Matrix

| Vector | Attack Scenario | Detection | Mitigation |
|--------|----------------|-----------|------------|
| **Prompt Injection** | Malicious log content instructs agent to exfiltrate | Input Guard: instruction-pattern detection in DATA_CONTEXT | Strict DATA/INSTRUCTION separation; all external input wrapped in DATA_CONTEXT |
| **Agent Impersonation** | Compromised agent forges identity of IR agent | SPIFFE SVID verification; Trust Broker rejects unsigned/expired SVIDs | Ed25519 SVIDs, 1hr TTL, mTLS required |
| **Data Scope Violation** | Forensics agent reads Threat Intel collection outside its scope | OPA policy deny + audit log | Deny-by-default OPA; namespace RBAC on all memory |
| **Memory Poisoning** | Attacker injects false threat intel via compromised feed | Trust score below threshold triggers quarantine | Source trust scoring; provenance tracking; content hash verification |
| **Orchestrator Compromise** | Central orchestrator sends rogue instructions | Distributed quorum check; signed action manifests | No single orchestrator for T1 actions; human auth for config changes |
| **Agentic Insider Threat** | Legitimate agent exceeds authorized action scope/rate | Behavioral Monitor: rate anomaly + capability audit | Baseline rate limits; capability suspension; human review gate |
| **APT Log Manipulation** | Attacker modifies SIEM logs pre-ingestion to hide lateral movement | Hash manifest verification at ingestion; integrity mismatch alert | Cryptographic log integrity; source auth required |
| **Credential Exfiltration** | Agent leaks API key through output | Output scanning for key patterns; Infisical proxy | Keys never in agent context window; all credential access via secrets proxy |
| **Memory Interaction Poisoning** | Successive agent exchanges gradually corrupt episodic memory | Episodic memory hash chain; anomaly in belief drift | Append-only WORM; quality gate before episodic consolidation; provenance |
| **Cross-Tenant Data Bleed** | Multi-team deployment causes tenant A data to appear in tenant B query | Tenant namespace isolation; row-level security | Tenant ID enforced at all layers; ChromaDB collection isolation; TimescaleDB RLS |
| **Model Fine-tune Attack** | Adversary fine-tunes agent model to alter procedural memory | Behavioral baseline deviation; capability regression tests | Model version pinning; signed model checksums; regression test suite in CI |
| **Dormant Payload Activation** | Malicious memory injected weeks prior activates on trigger | Provenance tracking; trust score decay over time | TTL on low-trust memory entries; periodic semantic memory audit |

---

## 6. Orchestration Plane

### 6.1 Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION PLANE                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Intent Router                                            │   │
│  │ - Receives events from integration plane                 │   │
│  │ - Routes to appropriate NICE role agent(s)               │   │
│  │ - Supports parallel multi-agent dispatch                 │   │
│  │ - LangGraph state machine per active incident            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Autonomy Gate Engine                                     │   │
│  │ - Classifies every proposed action by risk               │   │
│  │ - Applies role policy + confidence threshold             │   │
│  │ - Routes T2 to Human Approval Queue                      │   │
│  │ - Blocks T1 execution (advisory only)                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Human Approval Queue                                     │   │
│  │ - Web UI + REST API + Slack/Teams integration            │   │
│  │ - Approval token required to execute T2 actions          │   │
│  │ - Timeout → configurable (escalate / abort / re-analyze) │   │
│  │ - Full audit trail per approval decision                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Trust Broker (see Security Plane §5.2)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Messaging — NATS JetStream

All inter-agent and agent-to-orchestrator communication uses NATS JetStream:

```
Subjects:
  cipher.events.{source_type}.{severity}   # Inbound integration events
  cipher.agent.{agent_id}.inbox            # Per-agent task inbox
  cipher.agent.{agent_id}.outbox           # Per-agent result/action outbox
  cipher.approval.{incident_id}            # T2 human approval channel
  cipher.audit                             # Append-only audit stream
  cipher.alert.{severity}                  # Operator alerts

Message envelope:
{
  "msg_id": "uuid",
  "from_agent": "spiffe://...",
  "to_agent": "spiffe://... | orchestrator | human",
  "timestamp": "ISO8601",
  "signature": "Ed25519 sig of payload",
  "payload_hash": "sha256:...",
  "payload": { ... }
}
```

---

## 7. Integration Plane

### 7.1 Source Connectors

All connectors authenticate via per-agent API keys stored in Infisical.
Each source has a `trust_score` used in memory provenance records.

| Category | Supported Integrations | Default Trust Score |
|----------|----------------------|---------------------|
| **SIEM** | Splunk, Elastic SIEM, QRadar, Microsoft Sentinel, Wazuh | 0.85 |
| **EDR** | CrowdStrike Falcon, SentinelOne, Microsoft Defender | 0.90 |
| **Vuln Scanner** | Tenable.io, Qualys, Rapid7, OpenVAS | 0.85 |
| **Threat Intel** | MISP, VirusTotal, Shodan, AlienVault OTX, OpenCTI | 0.70–0.90 |
| **SOAR** | Splunk SOAR, Palo Alto XSOAR, TheHive (open source) | 0.90 |
| **Ticketing** | ServiceNow, Jira, PagerDuty, Linear | 0.95 |
| **UEBA** | Microsoft Sentinel UEBA, Securonix | 0.85 |
| **Identity** | Okta, Azure AD, Keycloak | 0.95 |
| **Custom** | Generic REST + API key via connector config | Configurable |

### 7.2 Connector Interface Contract

```yaml
# /specs/integrations/{connector_name}.yaml
connector:
  id: splunk-siem
  type: siem
  auth:
    method: api_key
    infisical_path: /cipher/{tenant_id}/integrations/splunk
  trust_score: 0.85
  log_integrity:
    method: hash_manifest   # splunk provides event hash on export
    verify_on_ingest: true
    mismatch_action: quarantine_and_alert
  rate_limits:
    queries_per_minute: 60
    events_per_batch: 1000
  data_types:
    - security_alert
    - auth_log
    - network_log
    - endpoint_log
```

---

## 8. Observability Plane

### 8.1 OpenTelemetry — Every Action Traced

All agent actions, memory operations, policy decisions, and integration calls emit OTel spans:

```
Trace: alert_triage_incident_{id}
├── span: input_guard.sanitize(source=splunk, event_id=xxx)
├── span: intent_router.route(event_type=security_alert)
├── span: agent-pd-defensive.analyze(alert_id=xxx)
│   ├── span: memory.semantic.query(collection=threat_intel)
│   ├── span: tool.threat_intel_lookup(ioc=1.2.3.4)
│   └── span: episodic.write(action=alert_enriched, confidence=0.94)
├── span: autonomy_gate.evaluate(action=ticket_create, risk=LOW → T3)
└── span: tool.ticketing.create(system=jira, priority=P2)
```

### 8.2 Immutable Audit Ledger

Separate from episodic memory — a WORM audit ledger captures:
- Every T2/T1 action proposal (with full agent reasoning)
- Every human approval/rejection decision
- Every policy authorization decision
- Every anomaly detection trigger
- Every memory write (episodic + semantic)

Stored in: TimescaleDB `cipher_audit` table with hash chain.
Export format: OCSF (Open Cybersecurity Schema Framework) for SIEM compatibility.

---

## 9. Deployment Architecture

```
                    ┌─────────────────────────┐
                    │     Operator Web UI      │
                    │  (Human Approval Queue)  │
                    └────────────┬────────────┘
                                 │ HTTPS/WSS
                    ┌────────────┴────────────┐
                    │      CIPHER Gateway      │
                    │   FastAPI + Keycloak SSO │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
  ┌───────┴──────┐    ┌──────────┴──────┐    ┌─────────┴──────┐
  │ Orchestration │    │  Security Plane  │    │ Memory Plane   │
  │  (LangGraph) │    │ SPIRE+OPA+Guard  │    │ Redis+PG+Chroma│
  └───────┬──────┘    └─────────────────┘    └────────────────┘
          │
  ┌───────┴──────────────────────────────────────────────┐
  │                  Agent Pool                          │
  │  agent-pd-defensive  agent-pd-ir  agent-pd-threat    │
  │  agent-pd-vuln  agent-pd-forensics  agent-in-*  ...  │
  └───────┬──────────────────────────────────────────────┘
          │ NATS JetStream
  ┌───────┴──────────────────────────────────────────────┐
  │               Integration Plane                      │
  │  Splunk  CrowdStrike  Tenable  MISP  Jira  Okta ...  │
  └──────────────────────────────────────────────────────┘
```

**Container-first deployment:**
- Docker Compose for dev/single-node
- Helm chart for Kubernetes (production)
- All state external to containers (Redis, TimescaleDB, ChromaDB)
- Horizontal scaling: agent pool scales independently of orchestration

---

## 10. Jules Integration Specification

### 10.1 Repository Structure for Jules

```
cipher/                          ← GitHub repo root
├── AGENTS.md                    ← Jules reads this for codebase guidance
├── specs/                       ← I write these; Jules reads to implement
│   ├── personas/                ← One YAML per NICE role agent
│   ├── memory/                  ← Memory layer specs
│   ├── security/                ← Threat mitigations + policy definitions
│   ├── orchestration/           ← Component specs
│   └── integrations/            ← Connector specs
├── prompts/                     ← Jules manages these
│   └── {role}/
│       ├── system.md            ← Agent system prompt
│       ├── memory_inject.md     ← Memory context injection template
│       ├── output_schema.json   ← Structured output validation
│       └── examples/            ← Few-shot examples per role
├── src/                         ← Jules writes this from specs
│   ├── orchestrator/
│   ├── agents/
│   ├── memory/
│   ├── security/
│   └── integrations/
└── tests/                       ← Jules writes these from specs
```

### 10.2 AGENTS.md (Jules Guidance File)

See `/docs/AGENTS.md` for the full Jules guidance file.

### 10.3 Jules Task Pipeline

```
Phase 1 (Foundation — Jules Task Batch 1):
  Issue #001: Implement Trust Broker (SPIFFE/SPIRE integration)
  Issue #002: Implement Autonomy Gate Engine (risk classifier + tier router)
  Issue #003: Implement agent-pd-defensive (first live agent)
  Issue #004: Implement agent-pd-ir (second live agent)
  Issue #005: Implement Input Guard (injection sanitizer)
  Issue #006: Implement NATS messaging layer

Phase 2 (Memory + Security):
  Issue #007: Implement episodic memory (TimescaleDB + hash chain)
  Issue #008: Implement semantic memory (ChromaDB + provenance)
  Issue #009: Implement OPA policy engine integration
  Issue #010: Implement working memory (Redis namespace manager)
  Issue #011: Implement remaining PD+IN agents (5 roles)

Phase 3–5: See /roadmap/ROADMAP.md
```

---

## 11. Technology Stack

| Layer | Technology | License | Rationale |
|-------|-----------|---------|-----------|
| Orchestration | LangGraph | MIT | Stateful agent graphs, enterprise-proven |
| API Gateway | FastAPI | MIT | Async, OpenAPI, enterprise-ready |
| Messaging | NATS JetStream | Apache 2.0 | Lightweight, durable, audit-friendly |
| Agent Identity | SPIFFE/SPIRE | Apache 2.0 | Industry-standard workload identity |
| Policy Engine | Open Policy Agent | Apache 2.0 | Declarative Rego, CNCF-graduated |
| Episodic Memory | TimescaleDB | Apache 2.0 | PostgreSQL extension, time-series native |
| Semantic Memory | ChromaDB → Weaviate | Apache 2.0 | Embedded dev → scalable production |
| Working Memory | Redis | BSD | Fast, TTL-scoped, well-understood |
| Credential Store | Infisical | MIT | Open-source Vault alternative |
| Observability | OpenTelemetry + Grafana | Apache 2.0 | Vendor-neutral full-stack observability |
| LLM Routing | LiteLLM | MIT | Single interface, any LLM |
| Auth (Operators) | Keycloak | Apache 2.0 | Enterprise SSO, RBAC |
| Container | Docker + Helm | Apache 2.0 | K8s-native |
| Language | Python 3.12+ (core) | — | Agent ecosystem, Jules-supported |
| Reference: | Microsoft Agent Governance Toolkit | MIT | Runtime security reference (Apr 2026) |

---

*CIPHER Architecture Specification v0.1 — April 17, 2026*
*Authored for Jules-driven implementation via GitHub Issues*

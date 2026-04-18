# CIPHER

**Cybersecurity Intelligence Personas for Human-in-the-loop Enterprise Response**

> Open-source, NICE 2.0-aligned, multi-agent cybersecurity workforce framework.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![NICE Framework: v2.1](https://img.shields.io/badge/NICE%20Framework-v2.1-green.svg)](https://niccs.cisa.gov/workforce-development/nice-framework)
[![Status: Pre-Alpha](https://img.shields.io/badge/Status-Pre--Alpha-orange.svg)]()

---

## What is CIPHER?

CIPHER maps all **41 NICE Cybersecurity Workforce Framework (v2.1) work roles** to configurable AI agent personas, deployable in three operational modes:

| Mode | Description |
|------|-------------|
| 🤖 **Autonomous (T3)** | Agent executes low-risk actions independently (enrichment, triage, ticketing) |
| 👥 **Copiloted (T2)** | Agent recommends, human approves before execution |
| 🧑 **Human-Administered (T1)** | Agent advises only; human executes high-impact actions |

Every agent has a **cryptographic identity** (SPIFFE/SPIRE), **role-scoped memory**, and all actions pass through a **policy engine** (OPA) with an **immutable audit ledger**.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CIPHER FRAMEWORK                            │
├──────────────────┬──────────────────┬───────────────────────────┤
│  ORCHESTRATION   │  SECURITY PLANE  │      MEMORY PLANE         │
│  LangGraph       │  SPIFFE/SPIRE    │  Episodic (TimescaleDB)   │
│  NATS JetStream  │  OPA Policies    │  Semantic (ChromaDB)      │
│  Autonomy Gate   │  Input Guard     │  Procedural (Playbooks)   │
│  Human Approval  │  Behavioral Mon. │  Working (Redis)          │
│  Trust Broker    │  Audit Ledger    │  Credentials (Infisical)  │
├──────────────────┴──────────────────┴───────────────────────────┤
│                  41 NICE ROLE AGENT PERSONAS                    │
│  PD: Defensive · IR · Forensics · Threat · Vuln · Infra · Insider │
│  IN: Cybercrime · Evidence  │  IO: SysAdmin · NetOps · +5       │
│  OG: CISO · Risk · Policy · +13  │  DD: Architect · SecDev · +7 │
├─────────────────────────────────────────────────────────────────┤
│              INTEGRATION PLANE (per-source API keys)            │
│  SIEM: Splunk · Elastic · QRadar · Sentinel · Wazuh             │
│  EDR:  CrowdStrike · SentinelOne · Defender                     │
│  Vuln: Tenable · Qualys · Rapid7 · OpenVAS                      │
│  Intel: MISP · VirusTotal · OpenCTI · AlienVault                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Security Model

- **Agent Identity**: SPIFFE SVIDs (Ed25519, 1hr TTL, auto-rotated)
- **Authorization**: OPA deny-by-default RBAC/ABAC on all memory + tool access
- **Memory Integrity**: TimescaleDB hash chain (tamper-evident episodic log)
- **Injection Defense**: Input Guard — all external data in `DATA_CONTEXT`, never `SYSTEM_INSTRUCTION`
- **Audit**: WORM append-only ledger, OCSF export, OpenTelemetry traces on every action

**Threat vectors covered**: prompt injection · agent impersonation · data scope violation · memory poisoning · orchestrator compromise · agentic insider threat · APT log manipulation · credential exfiltration · cross-tenant bleed · model fine-tune attack · dormant payload activation

---

## Repository Structure

```
cipher/
├── AGENTS.md               # Jules/AI coding agent guidance
├── docs/
│   └── ARCHITECTURE.md     # Full architecture specification
├── specs/                  # Source of truth for all implementations
│   ├── personas/           # YAML spec per NICE work role agent
│   ├── memory/             # Memory plane specs
│   ├── security/           # Security component specs
│   ├── orchestration/      # Orchestration component specs
│   └── integrations/       # Connector specs
├── prompts/                # Agent system prompts + memory templates
│   └── {role_id}/
│       ├── system.md
│       ├── memory_inject.md
│       └── output_schema.json
├── src/                    # Implementation (Jules-generated from specs)
├── tests/                  # Test suite
├── helm/                   # Kubernetes Helm chart
├── docker/                 # Docker Compose (dev)
└── roadmap/
    └── ROADMAP.md
```

---

## Tech Stack (100% Open Source)

| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph + NATS JetStream |
| Agent Identity | SPIFFE/SPIRE |
| Policy Engine | Open Policy Agent (OPA) |
| Episodic Memory | TimescaleDB (PostgreSQL) |
| Semantic Memory | ChromaDB → Weaviate |
| Working Memory | Redis |
| Credential Store | Infisical |
| Observability | OpenTelemetry + Grafana |
| LLM Routing | LiteLLM (model-agnostic) |
| Auth (Operators) | Keycloak |
| Language | Python 3.12+ |

---

## Roadmap

| Version | Focus | Target |
|---------|-------|--------|
| v0.1 | Core + 4 PD agents | 8 weeks |
| v0.2 | Full security plane + 5 more agents | 14 weeks |
| v0.3 | All 41 NICE roles | 24 weeks |
| v0.4 | Enterprise hardening + Kubernetes | 32 weeks |
| v1.0 | Production release + community launch | 36 weeks |

See [ROADMAP.md](roadmap/ROADMAP.md) for details.

---

## Implementation

This repository is designed for implementation via [Jules](https://jules.google.com) (Google's autonomous coding agent). See [AGENTS.md](AGENTS.md) for Jules guidance and the [`specs/`](specs/) directory for implementation specs.

Phase 1 Jules issues: [#1–#6](https://github.com/dcplatforms/cipher/issues)

---

## License

MIT © 2026 CIPHER Contributors

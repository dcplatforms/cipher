# CIPHER — Development Roadmap

## Vision
CIPHER becomes the open-source standard for NICE-aligned agentic cybersecurity operations — deployable by any enterprise, extensible by the community, and trusted because every security boundary is provable.

---

## v0.1 — Foundation (Jules Phase 1)
**Goal:** Minimal viable security operations with 4 PD agents, autonomous + copiloted tiers

### Milestones
- [ ] Core repo structure, CI/CD, Docker Compose dev environment
- [ ] Trust Broker (SPIFFE/SPIRE + OPA)
- [ ] Autonomy Gate Engine (T3 + T2 tiers; T1 advisory-only)
- [ ] Input Guard (prompt injection sanitizer)
- [ ] NATS JetStream messaging layer
- [ ] MemoryManager (all 5 memory planes)
- [ ] **agent-pd-defensive** — reference implementation
- [ ] **agent-pd-ir** — Incident Response
- [ ] **agent-pd-threat** — Threat Analysis
- [ ] **agent-pd-vuln** — Vulnerability Analysis
- [ ] Basic Splunk + CrowdStrike connectors
- [ ] Human Approval Queue (REST API + basic web UI)
- [ ] OpenTelemetry + Grafana dashboard
- [ ] WORM audit ledger

**Target:** 8 weeks from project start

---

## v0.2 — Memory Hardening + 5 More Agents (Jules Phase 2)
**Goal:** Full security plane operational; Investigation agents live

### Milestones
- [ ] OPA policy engine (full RBAC/ABAC for all memory + tools)
- [ ] Behavioral Monitor (baseline anomaly detection)
- [ ] Episodic memory hash chain verification API
- [ ] Semantic memory provenance audit (weekly scan)
- [ ] **agent-pd-forensics** — Digital Forensics
- [ ] **agent-pd-infra** — Infrastructure Support
- [ ] **agent-pd-insider** — Insider Threat Analysis
- [ ] **agent-in-cybercrime** — Cybercrime Investigation (T1 only)
- [ ] **agent-in-evidence** — Digital Evidence Analysis
- [ ] TheHive + Jira + ServiceNow connectors
- [ ] Keycloak SSO integration (operator auth)
- [ ] Multi-tenant namespace isolation

**Target:** +6 weeks (14 weeks total)

---

## v0.3 — Full NICE Coverage (Jules Phase 3)
**Goal:** All 41 NICE work role agents implemented

### Milestones
- [ ] All 7 IO agents (sysadmin, netops, data analysis, etc.)
- [ ] All 16 OG agents (governance, risk, CISO, policy, etc.)
- [ ] All 9 DD agents (architect, secure dev, systems engineering, etc.)
- [ ] T1 human-administered workflow (full UI for human execution guidance)
- [ ] Elastic SIEM, QRadar, Microsoft Sentinel connectors
- [ ] SentinelOne, Microsoft Defender EDR connectors
- [ ] Tenable, Qualys, Rapid7 vuln scanner connectors
- [ ] MISP + OpenCTI threat intel connectors
- [ ] Okta + Azure AD identity connectors

**Target:** +10 weeks (24 weeks total)

---

## v0.4 — Enterprise Hardening
**Goal:** Production-ready for enterprise deployment

### Milestones
- [ ] Helm chart (Kubernetes deployment)
- [ ] Horizontal scaling for agent pool
- [ ] Credential auto-rotation (Infisical)
- [ ] Log integrity verification (cryptographic hash manifests per source)
- [ ] OCSF audit export (SIEM-compatible)
- [ ] Performance benchmarks (p99 latency targets per component)
- [ ] Security penetration test (adversarial prompt injection + agent impersonation)
- [ ] Full test coverage (>80% across all modules)
- [ ] Operator documentation

**Target:** +8 weeks (32 weeks total)

---

## v1.0 — Production Release
**Goal:** Community launch, production-stable

### Milestones
- [ ] All threat mitigations validated against threat matrix
- [ ] Community contribution guide + CONTRIBUTING.md
- [ ] Plugin architecture for custom agent personas beyond NICE
- [ ] Custom playbook authoring UI
- [ ] Slack/Teams integration for Human Approval Queue
- [ ] Demo deployment (Docker Compose one-liner)
- [ ] v1.0 GitHub release + documentation site

**Target:** +4 weeks (36 weeks / ~9 months total)

---

## Future Roadmap (post-v1.0)

| Feature | Priority | Notes |
|---------|----------|-------|
| MITRE ATT&CK agent personas (specialized by tactic) | High | Cross-cutting with NICE roles |
| Model fine-tuning pipeline per NICE role | High | Role-specialized models |
| Federated multi-org deployment (MSSP mode) | Medium | Multi-tenant at org level |
| Threat hunting agent (proactive, not reactive) | High | New PD specialty |
| Red team agent personas (authorized testing) | Medium | Separate namespace, strict controls |
| STIX/TAXII threat intel ingestion | Medium | Standard threat intel format |
| AI-native SOAR playbook generator | Medium | Jules generates playbooks from incidents |
| Quantified risk scoring per incident | Low | Integration with risk management frameworks |
| Mobile approval UI | Low | iOS/Android for T2 approvals |

---

## Contributing

See `CONTRIBUTING.md` (to be created in v0.4).

Initial maintainers: Community-driven from day one.
License: MIT

---

*CIPHER Roadmap v0.1 — April 17, 2026*

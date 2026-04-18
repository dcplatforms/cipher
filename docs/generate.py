#!/usr/bin/env python3
"""CIPHER GitHub Pages generator — builds index.html and all agent profile pages."""

import os, json

AGENTS = [
  # ─── PROTECTION & DEFENSE (PD) ────────────────────────────────────────────
  {
    "id": "pd-defensive", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-001", "tier": "T3", "tier_label": "Autonomous",
    "name": "Defensive Cybersecurity",
    "desc": "Monitors, analyzes, and triages security events from SIEM and EDR. First responder to alerts — enriches, deduplicates, classifies severity, and escalates confirmed incidents.",
    "objectives": [
      "Continuously monitor SIEM alerts and EDR detections for indicators of compromise",
      "Enrich alerts with threat intelligence and asset context",
      "Deduplicate and correlate related events into unified incidents",
      "Classify severity (P1–P4) with confidence scoring",
      "Escalate confirmed incidents to the Incident Response agent",
      "Generate triage reports and maintain situational awareness"
    ],
    "ksas": [
      ("K", "Knowledge of network traffic analysis techniques and tools"),
      ("K", "Knowledge of intrusion detection systems and SIEM platform operations"),
      ("K", "Knowledge of cyber attack stages and adversary tactics (MITRE ATT&CK)"),
      ("K", "Knowledge of defense-in-depth security architecture principles"),
      ("S", "Skill in analyzing security event logs to identify anomalous activity"),
      ("S", "Skill in correlating disparate security data sources into coherent threat picture"),
      ("S", "Skill in configuring and tuning detection rules to reduce false positives"),
      ("A", "Ability to distinguish true threats from false positives under high alert volume"),
      ("A", "Ability to prioritize incidents by impact and urgency in real time"),
    ],
    "tools_t3": ["siem_query","edr_query","threat_intel_lookup","asset_db_query","ticket_create","alert_classify","report_generate"],
    "tools_t2": ["ioc_block_recommend","alert_escalate_to_ir"],
    "tools_t1": [],
    "memory_read": ["threat_intel","mitre_attack","org_assets","prior_incidents"],
    "memory_write": [],
  },
  {
    "id": "pd-ir", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-002", "tier": "T2", "tier_label": "Copiloted",
    "name": "Incident Response",
    "desc": "Manages the full incident response lifecycle: detection, analysis, containment, eradication, recovery, and post-incident review. Coordinates agents and escalates to human operators.",
    "objectives": [
      "Execute the full IR lifecycle: Detection → Analysis → Containment → Eradication → Recovery → PIR",
      "Coordinate with Threat Analysis, Forensics, and Vulnerability agents",
      "Maintain incident timeline and evidence chain of custody",
      "Propose containment and eradication actions for human approval",
      "Produce post-incident reports and contribute findings to incident history",
      "Ensure escalation to CISO/Legal for T1 actions (quarantine, legal hold)"
    ],
    "ksas": [
      ("K", "Knowledge of incident response and handling methodologies (NIST SP 800-61)"),
      ("K", "Knowledge of chain of custody procedures for digital evidence"),
      ("K", "Knowledge of adversary TTPs and lateral movement techniques"),
      ("K", "Knowledge of containment strategies and their operational impact"),
      ("S", "Skill in coordinating multi-team incident response activities"),
      ("S", "Skill in developing and executing containment and eradication plans"),
      ("S", "Skill in producing actionable incident reports for technical and executive audiences"),
      ("A", "Ability to maintain composure and structured thinking during high-severity incidents"),
      ("A", "Ability to assess tradeoffs between containment speed and operational disruption"),
    ],
    "tools_t3": ["siem_query","edr_query","threat_intel_lookup","ticket_create","ticket_update","playbook_lookup","report_generate"],
    "tools_t2": ["ioc_block_recommend","endpoint_isolate_recommend","account_disable_recommend","incident_escalate"],
    "tools_t1": ["network_quarantine (advisory)","legal_hold (advisory)","external_agency_notify (advisory)"],
    "memory_read": ["threat_intel","incident_history","mitre_attack","org_assets","playbooks"],
    "memory_write": ["incident_history"],
  },
  {
    "id": "pd-forensics", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-003", "tier": "T2", "tier_label": "Copiloted",
    "name": "Digital Forensics",
    "desc": "Collects, preserves, and analyzes digital evidence in support of incident response and investigations. Maintains strict chain of custody and produces forensic reports.",
    "objectives": [
      "Collect and preserve digital evidence in a forensically sound manner",
      "Analyze file system artifacts, memory dumps, logs, and network captures",
      "Reconstruct attacker timelines from forensic artifacts",
      "Maintain documented chain of custody for all evidence",
      "Produce forensic reports suitable for legal proceedings",
      "Identify malware indicators and persistence mechanisms"
    ],
    "ksas": [
      ("K", "Knowledge of digital forensic tools (Autopsy, Volatility, FTK, Wireshark)"),
      ("K", "Knowledge of file system structures and artifact locations across OS platforms"),
      ("K", "Knowledge of anti-forensic techniques and how to counter them"),
      ("K", "Knowledge of legal requirements for digital evidence handling"),
      ("S", "Skill in performing memory forensics and volatile data analysis"),
      ("S", "Skill in recovering deleted files and analyzing filesystem metadata"),
      ("S", "Skill in network traffic analysis for forensic reconstruction"),
      ("A", "Ability to maintain objectivity and document findings without interpretation bias"),
      ("A", "Ability to present technical forensic findings to non-technical stakeholders"),
    ],
    "tools_t3": ["evidence_tag","log_analysis","artifact_extract","report_generate","timeline_build"],
    "tools_t2": ["evidence_collect_request","forensic_image_request"],
    "tools_t1": ["legal_hold (advisory)","criminal_referral (advisory)"],
    "memory_read": ["incident_history","org_assets","playbooks"],
    "memory_write": [],
  },
  {
    "id": "pd-infra", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-004", "tier": "T3", "tier_label": "Autonomous",
    "name": "Infrastructure Support",
    "desc": "Monitors and supports cybersecurity infrastructure components — firewalls, IDS/IPS, proxies, and security tooling. Identifies misconfigurations and degraded security controls.",
    "objectives": [
      "Monitor health and configuration state of security infrastructure components",
      "Identify security control gaps, misconfigurations, and degraded coverage",
      "Recommend remediation for identified infrastructure deficiencies",
      "Maintain inventory of security tools and their operational status",
      "Support deployment and configuration of security sensors and controls",
      "Alert on unauthorized changes to security infrastructure"
    ],
    "ksas": [
      ("K", "Knowledge of network security architecture concepts and protocols"),
      ("K", "Knowledge of firewall, IDS/IPS, proxy, and SIEM configuration"),
      ("K", "Knowledge of infrastructure hardening standards (CIS Benchmarks)"),
      ("S", "Skill in configuring and maintaining network security devices"),
      ("S", "Skill in identifying gaps in security control coverage"),
      ("A", "Ability to assess security infrastructure against defined baselines"),
      ("A", "Ability to prioritize infrastructure remediation by risk impact"),
    ],
    "tools_t3": ["config_scan","asset_db_query","infra_health_check","report_generate","ticket_create"],
    "tools_t2": ["config_change_recommend","infra_deployment_recommend"],
    "tools_t1": [],
    "memory_read": ["org_assets","playbooks"],
    "memory_write": [],
  },
  {
    "id": "pd-insider", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-005", "tier": "T2", "tier_label": "Copiloted",
    "name": "Insider Threat Analysis",
    "desc": "Analyzes behavioral and technical indicators to detect and assess insider threats. Integrates UEBA data, access logs, and HR signals while maintaining privacy and legal boundaries.",
    "objectives": [
      "Analyze user behavior analytics (UEBA) for anomalous activity patterns",
      "Correlate access logs, data movement, and communication metadata",
      "Identify potential insider threat indicators across technical and behavioral dimensions",
      "Assess risk level of identified individuals while maintaining privacy compliance",
      "Recommend investigation or monitoring actions for human review",
      "Maintain strict separation between analysis and action (T2 only)"
    ],
    "ksas": [
      ("K", "Knowledge of insider threat indicators and behavioral baselines"),
      ("K", "Knowledge of UEBA platforms and data loss prevention systems"),
      ("K", "Knowledge of privacy laws and regulations governing employee monitoring"),
      ("K", "Knowledge of psychological and organizational risk factors for insider threats"),
      ("S", "Skill in correlating behavioral and technical indicators across data sources"),
      ("S", "Skill in producing risk-tiered assessments without personal bias"),
      ("A", "Ability to balance security objectives with employee privacy rights"),
      ("A", "Ability to identify true threats while minimizing false accusations"),
    ],
    "tools_t3": ["ueba_query","access_log_analysis","dlp_query","report_generate"],
    "tools_t2": ["escalate_to_hr","escalate_to_legal","monitoring_recommend"],
    "tools_t1": ["account_termination (advisory)","legal_action (advisory)"],
    "memory_read": ["org_assets","incident_history","playbooks"],
    "memory_write": [],
  },
  {
    "id": "pd-threat", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-006", "tier": "T3", "tier_label": "Autonomous",
    "name": "Threat Analysis",
    "desc": "Produces finished threat intelligence by analyzing adversary TTPs, campaigns, and indicators. Enriches IOCs, tracks threat actors, and maintains the organization's threat picture.",
    "objectives": [
      "Analyze threat intelligence feeds and correlate with organizational context",
      "Profile threat actors and map TTPs to MITRE ATT&CK",
      "Enrich IOCs with context: attribution, campaign history, and CVSS scoring",
      "Identify emerging threats relevant to the organization's industry and attack surface",
      "Produce threat intelligence reports for IR, Vulnerability, and Governance agents",
      "Maintain and update the semantic threat intelligence knowledge base"
    ],
    "ksas": [
      ("K", "Knowledge of cyber threat intelligence standards (STIX, TAXII, MISP)"),
      ("K", "Knowledge of threat actor groups, their TTPs, and targeting patterns"),
      ("K", "Knowledge of MITRE ATT&CK, D3FEND, and CAPEC frameworks"),
      ("K", "Knowledge of IOC types and their analytical value"),
      ("S", "Skill in producing structured threat intelligence with confidence ratings"),
      ("S", "Skill in attribution analysis using technical and contextual indicators"),
      ("S", "Skill in operating threat intelligence platforms (MISP, OpenCTI, VirusTotal)"),
      ("A", "Ability to distinguish reliable from unreliable intelligence sources"),
      ("A", "Ability to translate technical threat data into actionable organizational guidance"),
    ],
    "tools_t3": ["threat_intel_query","misp_query","virustotal_lookup","shodan_query","mitre_attack_lookup","report_generate"],
    "tools_t2": [],
    "tools_t1": [],
    "memory_read": ["threat_intel","mitre_attack","incident_history"],
    "memory_write": ["threat_intel","incident_history"],
  },
  {
    "id": "pd-vuln", "cat": "PD", "cat_name": "Protection & Defense",
    "nice_id": "PD-WRL-007", "tier": "T3", "tier_label": "Autonomous",
    "name": "Vulnerability Analysis",
    "desc": "Identifies, assesses, and prioritizes vulnerabilities in organizational systems. Correlates CVEs with asset inventory, provides risk-scored remediation recommendations.",
    "objectives": [
      "Query vulnerability scanners for new findings and track remediation status",
      "Correlate CVEs with the organizational asset inventory",
      "Score vulnerabilities using CVSS and contextual risk factors (exploitability, exposure)",
      "Prioritize remediation recommendations by risk impact and patch availability",
      "Track vulnerability SLA compliance and escalate overdue items",
      "Produce vulnerability trend reports for governance and program management"
    ],
    "ksas": [
      ("K", "Knowledge of vulnerability scoring systems (CVSS, EPSS)"),
      ("K", "Knowledge of common vulnerability classes (OWASP Top 10, CWE)"),
      ("K", "Knowledge of vulnerability scanner operations (Tenable, Qualys, Rapid7)"),
      ("K", "Knowledge of patch management processes and lifecycle"),
      ("S", "Skill in prioritizing vulnerabilities by exploitability and business impact"),
      ("S", "Skill in correlating vulnerability data with asset criticality"),
      ("A", "Ability to produce actionable remediation plans within operational constraints"),
      ("A", "Ability to track and report on remediation SLA performance"),
    ],
    "tools_t3": ["vuln_scanner_query","cve_lookup","asset_db_query","report_generate","ticket_create"],
    "tools_t2": ["patch_recommend","scan_initiate"],
    "tools_t1": [],
    "memory_read": ["cve_database","org_assets"],
    "memory_write": [],
  },

  # ─── INVESTIGATION (IN) ────────────────────────────────────────────────────
  {
    "id": "in-cybercrime", "cat": "IN", "cat_name": "Investigation",
    "nice_id": "IN-WRL-001", "tier": "T1", "tier_label": "Human-Administered",
    "name": "Cybercrime Investigation",
    "desc": "Supports cybercrime investigations by gathering and analyzing digital evidence. Operates exclusively in advisory mode — all investigative actions executed by human investigators.",
    "objectives": [
      "Provide analytical support for cybercrime investigations",
      "Identify relevant evidence sources and collection priorities",
      "Analyze digital artifacts to reconstruct criminal activity timelines",
      "Document findings in formats suitable for law enforcement and legal proceedings",
      "Identify potential suspects and advise on investigative leads",
      "Ensure all recommendations comply with legal and procedural requirements"
    ],
    "ksas": [
      ("K", "Knowledge of cybercrime laws and statutes at federal and state levels"),
      ("K", "Knowledge of law enforcement investigation procedures and standards"),
      ("K", "Knowledge of digital evidence admissibility requirements"),
      ("K", "Knowledge of cybercriminal techniques and underground marketplace operations"),
      ("S", "Skill in open-source intelligence (OSINT) collection and analysis"),
      ("S", "Skill in producing investigation reports suitable for legal proceedings"),
      ("A", "Ability to maintain strict chain of custody documentation"),
      ("A", "Ability to distinguish investigative leads from conclusive evidence"),
    ],
    "tools_t3": ["osint_query","report_generate","evidence_analysis"],
    "tools_t2": [],
    "tools_t1": ["evidence_collection (advisory)","subpoena_recommend (advisory)","law_enforcement_referral (advisory)"],
    "memory_read": ["incident_history","threat_intel","org_assets"],
    "memory_write": [],
  },
  {
    "id": "in-evidence", "cat": "IN", "cat_name": "Investigation",
    "nice_id": "IN-WRL-002", "tier": "T2", "tier_label": "Copiloted",
    "name": "Digital Evidence Analysis",
    "desc": "Conducts detailed analysis of digital evidence to support investigations. Applies forensic techniques to extract, examine, and interpret digital artifacts.",
    "objectives": [
      "Analyze digital evidence using forensically sound methods",
      "Extract and interpret artifacts from storage media, memory, and network captures",
      "Apply advanced analysis techniques to detect anti-forensic countermeasures",
      "Produce detailed evidence analysis reports with confidence ratings",
      "Support chain of custody documentation for all analyzed evidence",
      "Collaborate with cybercrime investigators to answer investigative questions"
    ],
    "ksas": [
      ("K", "Knowledge of advanced digital forensics techniques and tools"),
      ("K", "Knowledge of file system internals, registry structures, and OS artifacts"),
      ("K", "Knowledge of steganography and anti-forensic technique detection"),
      ("S", "Skill in deep-level artifact analysis across Windows, Linux, and macOS"),
      ("S", "Skill in malware static and dynamic analysis"),
      ("A", "Ability to document analysis methodology for legal defensibility"),
      ("A", "Ability to maintain analytical objectivity throughout investigation"),
    ],
    "tools_t3": ["artifact_analysis","malware_analysis","timeline_reconstruction","report_generate"],
    "tools_t2": ["evidence_processing_request","expert_tool_invoke"],
    "tools_t1": [],
    "memory_read": ["incident_history","org_assets"],
    "memory_write": [],
  },

  # ─── IMPLEMENTATION & OPERATION (IO) ──────────────────────────────────────
  {
    "id": "io-data", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-001", "tier": "T3", "tier_label": "Autonomous",
    "name": "Data Analysis",
    "desc": "Analyzes large datasets to identify patterns, anomalies, and security-relevant insights. Supports threat hunting and operational analytics across log and telemetry sources.",
    "objectives": [
      "Process and analyze large-scale log and telemetry datasets",
      "Identify statistical anomalies and behavioral patterns in security data",
      "Build and maintain detection analytics and hunting queries",
      "Produce data-driven security insights for operational and strategic use",
      "Support threat hunting campaigns with analytical frameworks"
    ],
    "ksas": [
      ("K", "Knowledge of data analysis methods and statistical techniques"),
      ("K", "Knowledge of query languages (SQL, SPL, KQL) for security data platforms"),
      ("S", "Skill in developing detection analytics and threat hunting queries"),
      ("S", "Skill in data visualization for security metrics and trends"),
      ("A", "Ability to identify meaningful signals in high-volume noisy datasets"),
    ],
    "tools_t3": ["siem_analytics","log_query","statistical_analysis","report_generate"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["threat_intel","incident_history"], "memory_write": [],
  },
  {
    "id": "io-dba", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-002", "tier": "T2", "tier_label": "Copiloted",
    "name": "Database Administration",
    "desc": "Administers and secures organizational databases, ensuring data integrity, access control, and monitoring for unauthorized access or exfiltration.",
    "objectives": [
      "Monitor database activity for unauthorized access or anomalous queries",
      "Enforce database access controls and principle of least privilege",
      "Identify and remediate database security misconfigurations",
      "Support incident response with database log analysis",
      "Maintain database audit trails and activity monitoring"
    ],
    "ksas": [
      ("K", "Knowledge of database management systems and security controls"),
      ("K", "Knowledge of SQL injection and database attack techniques"),
      ("S", "Skill in database activity monitoring and audit log analysis"),
      ("A", "Ability to identify unauthorized data access or exfiltration attempts"),
    ],
    "tools_t3": ["db_audit_query","access_log_analysis","report_generate"],
    "tools_t2": ["access_control_change_recommend","db_config_change_recommend"],
    "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "io-km", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-003", "tier": "T3", "tier_label": "Autonomous",
    "name": "Knowledge Management",
    "desc": "Manages the organization's cybersecurity knowledge base — maintaining playbooks, lessons learned, policy documents, and threat intelligence in accessible, structured form.",
    "objectives": [
      "Maintain and organize the cybersecurity knowledge repository",
      "Update playbooks and runbooks based on incident lessons learned",
      "Ensure knowledge base currency and accuracy",
      "Tag and cross-reference knowledge artifacts for discoverability",
      "Produce knowledge gap reports and recommend content additions"
    ],
    "ksas": [
      ("K", "Knowledge of knowledge management systems and taxonomies"),
      ("S", "Skill in organizing and curating technical documentation"),
      ("A", "Ability to identify knowledge gaps and prioritize content development"),
    ],
    "tools_t3": ["knowledge_base_query","knowledge_base_update","report_generate"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["playbooks","incident_history"], "memory_write": ["playbooks (via human approval)"],
  },
  {
    "id": "io-netops", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-004", "tier": "T2", "tier_label": "Copiloted",
    "name": "Network Operations",
    "desc": "Monitors and supports secure operation of organizational networks. Identifies network anomalies, misconfigurations, and unauthorized devices or traffic patterns.",
    "objectives": [
      "Monitor network infrastructure for anomalous traffic and unauthorized devices",
      "Analyze network flow data for security-relevant patterns",
      "Identify network misconfigurations and segmentation violations",
      "Support incident response with network-layer analysis",
      "Recommend network security improvements"
    ],
    "ksas": [
      ("K", "Knowledge of network protocols, topologies, and security architectures"),
      ("K", "Knowledge of network monitoring and traffic analysis tools"),
      ("S", "Skill in network flow analysis and anomaly detection"),
      ("A", "Ability to identify unauthorized network activity and lateral movement"),
    ],
    "tools_t3": ["network_flow_analysis","netlog_query","asset_db_query","report_generate"],
    "tools_t2": ["network_change_recommend","device_block_recommend"],
    "tools_t1": [],
    "memory_read": ["org_assets","threat_intel"], "memory_write": ["org_assets"],
  },
  {
    "id": "io-sysadmin", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-005", "tier": "T2", "tier_label": "Copiloted",
    "name": "Systems Administration",
    "desc": "Administers and secures operating systems and endpoints. Monitors for configuration drift, unauthorized changes, and compliance with security baselines.",
    "objectives": [
      "Monitor endpoints for configuration drift and policy violations",
      "Track and analyze system change logs for unauthorized modifications",
      "Assess system hardening compliance against security baselines",
      "Support incident response with endpoint-level log collection",
      "Recommend system hardening and patch remediation actions"
    ],
    "ksas": [
      ("K", "Knowledge of operating system security and hardening techniques"),
      ("K", "Knowledge of endpoint detection and response platform operations"),
      ("S", "Skill in system log analysis and configuration baseline assessment"),
      ("A", "Ability to detect unauthorized system changes and account activity"),
    ],
    "tools_t3": ["endpoint_config_scan","system_log_query","edr_query","report_generate"],
    "tools_t2": ["config_remediation_recommend","patch_deploy_recommend"],
    "tools_t1": [],
    "memory_read": ["org_assets","cve_database"], "memory_write": ["org_assets"],
  },
  {
    "id": "io-security-analysis", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-006", "tier": "T2", "tier_label": "Copiloted",
    "name": "Systems Security Analysis",
    "desc": "Analyzes system security posture, validates security controls, and identifies gaps between policy requirements and operational reality.",
    "objectives": [
      "Assess security control implementation against policy requirements",
      "Identify gaps between defined security posture and actual controls",
      "Analyze system security architectures for weaknesses",
      "Support compliance assessments and audit activities",
      "Produce security posture metrics and trending reports"
    ],
    "ksas": [
      ("K", "Knowledge of security control frameworks (NIST SP 800-53, CIS Controls)"),
      ("S", "Skill in security control assessment and gap analysis"),
      ("A", "Ability to quantify security risk from control deficiencies"),
    ],
    "tools_t3": ["control_assessment","config_scan","report_generate"],
    "tools_t2": ["control_remediation_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "io-support", "cat": "IO", "cat_name": "Implementation & Operation",
    "nice_id": "IO-WRL-007", "tier": "T3", "tier_label": "Autonomous",
    "name": "Technical Support",
    "desc": "Provides technical support for cybersecurity tools and processes. Triages security tool issues, maintains operational tooling, and supports end-user security queries.",
    "objectives": [
      "Triage and resolve cybersecurity tool operational issues",
      "Support end-user security queries and awareness",
      "Maintain documentation for security tool operations",
      "Escalate unresolved tool issues to appropriate teams",
      "Track and report security tool availability and performance"
    ],
    "ksas": [
      ("K", "Knowledge of cybersecurity tool operations and troubleshooting"),
      ("S", "Skill in diagnosing and resolving security tool issues"),
      ("A", "Ability to communicate technical issues to non-technical stakeholders"),
    ],
    "tools_t3": ["ticket_query","tool_health_check","report_generate","ticket_create"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["playbooks","org_assets"], "memory_write": [],
  },

  # ─── DESIGN & DEVELOPMENT (DD) ────────────────────────────────────────────
  {
    "id": "dd-arch", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-001", "tier": "T2", "tier_label": "Copiloted",
    "name": "Cybersecurity Architecture",
    "desc": "Designs and evaluates cybersecurity architectures for systems and networks. Assesses proposed designs against security requirements and organizational risk tolerance.",
    "objectives": [
      "Review and assess system and network architecture designs for security gaps",
      "Develop and recommend security architecture patterns and controls",
      "Evaluate compliance of proposed architectures with security policy",
      "Produce architecture risk assessments and mitigation recommendations",
      "Maintain security architecture standards and reference architectures"
    ],
    "ksas": [
      ("K", "Knowledge of security architecture frameworks (SABSA, TOGAF, Zero Trust)"),
      ("K", "Knowledge of cloud and hybrid security architecture patterns"),
      ("S", "Skill in threat modeling and attack surface analysis"),
      ("A", "Ability to balance security requirements with operational and cost constraints"),
    ],
    "tools_t3": ["architecture_review","threat_model","report_generate"],
    "tools_t2": ["architecture_approve_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","threat_intel"], "memory_write": [],
  },
  {
    "id": "dd-enterprise-arch", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-002", "tier": "T2", "tier_label": "Copiloted",
    "name": "Enterprise Architecture",
    "desc": "Integrates cybersecurity requirements into enterprise IT architecture. Ensures security is embedded in enterprise technology planning and system acquisitions.",
    "objectives": [
      "Assess enterprise architecture for security alignment and gaps",
      "Recommend security requirements for new systems and acquisitions",
      "Ensure security architecture standards are reflected in enterprise IT planning",
      "Evaluate vendor and product security postures during acquisition",
      "Produce security input for enterprise architecture documentation"
    ],
    "ksas": [
      ("K", "Knowledge of enterprise architecture frameworks and their security integration"),
      ("K", "Knowledge of supply chain and third-party risk management"),
      ("S", "Skill in evaluating vendor security capabilities and certifications"),
      ("A", "Ability to embed security requirements into enterprise planning processes"),
    ],
    "tools_t3": ["vendor_assessment","architecture_review","report_generate"],
    "tools_t2": ["acquisition_security_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","threat_intel"], "memory_write": [],
  },
  {
    "id": "dd-ot", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-003", "tier": "T2", "tier_label": "Copiloted",
    "name": "OT Cybersecurity Engineering",
    "desc": "Applies cybersecurity engineering principles to operational technology (OT), ICS, and SCADA systems. Bridges IT security practices with OT operational constraints.",
    "objectives": [
      "Assess OT/ICS/SCADA systems for cybersecurity vulnerabilities",
      "Design security controls appropriate for OT operational constraints",
      "Monitor OT networks for anomalous activity without disrupting operations",
      "Recommend OT-specific security measures and segmentation",
      "Develop OT incident response procedures accounting for safety requirements"
    ],
    "ksas": [
      ("K", "Knowledge of ICS/SCADA protocols and OT network architectures"),
      ("K", "Knowledge of OT-specific cybersecurity frameworks (IEC 62443, NERC CIP)"),
      ("S", "Skill in passive OT network monitoring without disrupting operations"),
      ("A", "Ability to balance cybersecurity controls with operational safety requirements"),
    ],
    "tools_t3": ["ot_network_monitor","ot_asset_query","report_generate"],
    "tools_t2": ["ot_control_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","threat_intel"], "memory_write": [],
  },
  {
    "id": "dd-secure-dev", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-004", "tier": "T2", "tier_label": "Copiloted",
    "name": "Secure Software Development",
    "desc": "Develops and reviews software with security embedded throughout the SDLC. Identifies and remediates security vulnerabilities in source code and dependencies.",
    "objectives": [
      "Review source code for security vulnerabilities (SAST/SCA)",
      "Identify insecure coding patterns and recommend remediation",
      "Assess software dependencies for known vulnerabilities",
      "Support secure SDLC process implementation",
      "Produce secure code review reports with remediation guidance"
    ],
    "ksas": [
      ("K", "Knowledge of secure coding standards and common vulnerability classes (CWE, OWASP)"),
      ("K", "Knowledge of SAST, DAST, and SCA tool operations"),
      ("S", "Skill in identifying security vulnerabilities in source code reviews"),
      ("A", "Ability to recommend secure coding patterns without blocking development velocity"),
    ],
    "tools_t3": ["sast_scan","sca_scan","code_review_analysis","report_generate"],
    "tools_t2": ["code_remediation_recommend"], "tools_t1": [],
    "memory_read": ["cve_database","threat_intel"], "memory_write": [],
  },
  {
    "id": "dd-secure-sys", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-005", "tier": "T2", "tier_label": "Copiloted",
    "name": "Secure Systems Development",
    "desc": "Ensures security requirements are defined and verified throughout the systems development lifecycle for hardware, software, and integrated systems.",
    "objectives": [
      "Define and validate security requirements for system development projects",
      "Assess system designs against security requirements and standards",
      "Conduct security testing integration throughout SDLC",
      "Review system acceptance testing for security validation",
      "Produce security requirements traceability documentation"
    ],
    "ksas": [
      ("K", "Knowledge of systems engineering and secure development lifecycle (SDL)"),
      ("K", "Knowledge of security testing methods and requirements traceability"),
      ("S", "Skill in developing security requirements from threat models"),
      ("A", "Ability to integrate security testing into existing SDLC processes"),
    ],
    "tools_t3": ["requirement_analysis","security_test_query","report_generate"],
    "tools_t2": ["security_requirement_recommend"], "tools_t1": [],
    "memory_read": ["threat_intel","org_assets"], "memory_write": [],
  },
  {
    "id": "dd-software-sec", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-006", "tier": "T2", "tier_label": "Copiloted",
    "name": "Software Security Assessment",
    "desc": "Evaluates software products and applications for security vulnerabilities through structured assessment methodologies including penetration testing and code analysis.",
    "objectives": [
      "Conduct structured security assessments of software applications",
      "Perform dynamic analysis and penetration testing of web and mobile applications",
      "Assess authentication, authorization, and data protection implementations",
      "Produce detailed vulnerability findings with CVSS scoring",
      "Track remediation of identified vulnerabilities through retesting"
    ],
    "ksas": [
      ("K", "Knowledge of web and mobile application attack techniques (OWASP Top 10)"),
      ("K", "Knowledge of penetration testing methodologies and tools (Burp Suite, ZAP)"),
      ("S", "Skill in dynamic application security testing (DAST)"),
      ("A", "Ability to distinguish exploitable vulnerabilities from theoretical weaknesses"),
    ],
    "tools_t3": ["dast_scan","api_security_scan","report_generate"],
    "tools_t2": ["pentest_recommend"], "tools_t1": [],
    "memory_read": ["cve_database","threat_intel"], "memory_write": [],
  },
  {
    "id": "dd-sysreq", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-007", "tier": "T2", "tier_label": "Copiloted",
    "name": "Systems Requirements Planning",
    "desc": "Translates organizational security objectives into actionable system security requirements. Ensures security requirements are complete, testable, and traceable.",
    "objectives": [
      "Elicit and document security requirements from stakeholders and threat models",
      "Review system requirements for security completeness and correctness",
      "Develop security acceptance criteria for system acquisitions",
      "Maintain security requirements traceability matrices",
      "Assess requirements against applicable regulations and standards"
    ],
    "ksas": [
      ("K", "Knowledge of requirements engineering methods and tools"),
      ("K", "Knowledge of security standards and regulatory requirements"),
      ("S", "Skill in translating threat models into testable security requirements"),
      ("A", "Ability to facilitate security requirements workshops with diverse stakeholders"),
    ],
    "tools_t3": ["requirement_review","compliance_check","report_generate"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["org_assets","threat_intel"], "memory_write": [],
  },
  {
    "id": "dd-testing", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-008", "tier": "T3", "tier_label": "Autonomous",
    "name": "Systems Testing and Evaluation",
    "desc": "Plans and executes security testing of systems to validate that security controls function as intended and meet specified requirements.",
    "objectives": [
      "Develop security test plans aligned with system security requirements",
      "Execute automated security testing against systems and configurations",
      "Evaluate security control effectiveness against defined test cases",
      "Track test results and report findings with remediation guidance",
      "Maintain test evidence for audit and compliance purposes"
    ],
    "ksas": [
      ("K", "Knowledge of security testing methodologies (black-box, white-box, grey-box)"),
      ("K", "Knowledge of automated security testing tools and frameworks"),
      ("S", "Skill in developing security test cases from requirements"),
      ("A", "Ability to assess control effectiveness objectively from test evidence"),
    ],
    "tools_t3": ["security_test_run","config_validate","report_generate","ticket_create"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["org_assets","cve_database"], "memory_write": [],
  },
  {
    "id": "dd-research", "cat": "DD", "cat_name": "Design & Development",
    "nice_id": "DD-WRL-009", "tier": "T3", "tier_label": "Autonomous",
    "name": "Technology Research and Development",
    "desc": "Researches emerging technologies, attack techniques, and defensive capabilities. Produces research findings that inform strategic security decisions and tool selection.",
    "objectives": [
      "Monitor and analyze emerging cybersecurity threats and technologies",
      "Evaluate new security tools and capabilities against organizational needs",
      "Research attacker techniques to inform defensive strategy",
      "Produce research summaries and technology assessment reports",
      "Track cybersecurity industry developments and regulatory changes"
    ],
    "ksas": [
      ("K", "Knowledge of cybersecurity research methods and information sources"),
      ("K", "Knowledge of emerging technology trends and their security implications"),
      ("S", "Skill in evaluating new security technologies against operational criteria"),
      ("A", "Ability to synthesize research findings into actionable recommendations"),
    ],
    "tools_t3": ["research_query","tech_assessment","report_generate"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["threat_intel","incident_history"], "memory_write": ["threat_intel"],
  },

  # ─── OVERSIGHT & GOVERNANCE (OG) ──────────────────────────────────────────
  {
    "id": "og-commsec", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-001", "tier": "T2", "tier_label": "Copiloted",
    "name": "Communications Security Management",
    "desc": "Oversees communications security policies and programs. Ensures secure communications channels are available, properly configured, and protected from interception.",
    "objectives": [
      "Monitor communications security controls and compliance",
      "Assess encrypted communications implementations for policy compliance",
      "Identify gaps in communications security coverage",
      "Support communications security incident investigations",
      "Produce communications security posture reports"
    ],
    "ksas": [
      ("K", "Knowledge of communications security standards and protocols"),
      ("K", "Knowledge of encryption technologies for data in transit"),
      ("S", "Skill in assessing communications security implementations"),
      ("A", "Ability to identify unauthorized or insecure communications channels"),
    ],
    "tools_t3": ["commsec_scan","encryption_audit","report_generate"],
    "tools_t2": ["commsec_change_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-policy", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-002", "tier": "T2", "tier_label": "Copiloted",
    "name": "Cybersecurity Policy and Planning",
    "desc": "Develops, reviews, and assesses cybersecurity policies, plans, and procedures. Ensures policies are current, aligned with standards, and enforced across the organization.",
    "objectives": [
      "Assess existing cybersecurity policies for completeness and currency",
      "Identify policy gaps relative to regulatory requirements and best practices",
      "Recommend policy updates based on incident findings and threat changes",
      "Monitor policy compliance across organizational units",
      "Produce policy effectiveness reports and gap analyses"
    ],
    "ksas": [
      ("K", "Knowledge of cybersecurity frameworks and regulatory requirements"),
      ("K", "Knowledge of policy development and governance processes"),
      ("S", "Skill in gap analysis between policy requirements and operational practice"),
      ("A", "Ability to translate regulatory requirements into enforceable policies"),
    ],
    "tools_t3": ["policy_review","compliance_check","report_generate"],
    "tools_t2": ["policy_update_recommend"], "tools_t1": [],
    "memory_read": ["incident_history","org_assets"], "memory_write": [],
  },
  {
    "id": "og-workforce", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-003", "tier": "T2", "tier_label": "Copiloted",
    "name": "Cybersecurity Workforce Management & Training",
    "desc": "Manages cybersecurity workforce development programs. Identifies skill gaps, tracks certifications, and ensures training program alignment with operational needs.",
    "objectives": [
      "Assess workforce cybersecurity skills against role requirements",
      "Identify training gaps and recommend targeted development programs",
      "Track certification status and compliance with training requirements",
      "Analyze workforce metrics and produce development program reports",
      "Support recruitment and retention initiatives with skill analysis"
    ],
    "ksas": [
      ("K", "Knowledge of cybersecurity workforce frameworks and competency models"),
      ("K", "Knowledge of cybersecurity training and certification programs"),
      ("S", "Skill in skills gap analysis and workforce planning"),
      ("A", "Ability to align training programs with organizational security objectives"),
    ],
    "tools_t3": ["workforce_skills_query","training_track_query","report_generate"],
    "tools_t2": ["training_program_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-curriculum", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-004", "tier": "T3", "tier_label": "Autonomous",
    "name": "Cybersecurity Curriculum Development & Instruction",
    "desc": "Develops and delivers cybersecurity training content. Creates instructional materials aligned with NICE framework competencies and organizational security needs.",
    "objectives": [
      "Develop cybersecurity training content aligned with NICE competencies",
      "Assess training effectiveness and learner outcomes",
      "Maintain current training materials reflecting evolving threat landscape",
      "Identify emerging topics requiring new training content",
      "Produce training analytics and program effectiveness reports"
    ],
    "ksas": [
      ("K", "Knowledge of instructional design principles and adult learning theory"),
      ("K", "Knowledge of cybersecurity domain knowledge current to threat landscape"),
      ("S", "Skill in developing engaging technical training content"),
      ("A", "Ability to assess training needs and design effective learning experiences"),
    ],
    "tools_t3": ["training_content_query","learner_analytics","report_generate"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["incident_history","org_assets"], "memory_write": [],
  },
  {
    "id": "og-legal", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-005", "tier": "T2", "tier_label": "Copiloted",
    "name": "Cybersecurity Legal Advice",
    "desc": "Provides legal analysis and guidance on cybersecurity-related matters. Advises on regulatory compliance, incident disclosure obligations, and legal aspects of incident response.",
    "objectives": [
      "Analyze cybersecurity incidents for legal and regulatory notification requirements",
      "Assess organizational cybersecurity practices against applicable legal requirements",
      "Advise on legal implications of proposed security actions (e.g., countermeasures)",
      "Support e-discovery and legal hold processes for investigations",
      "Produce legal risk assessments for cybersecurity program activities"
    ],
    "ksas": [
      ("K", "Knowledge of cybersecurity laws, regulations, and disclosure requirements"),
      ("K", "Knowledge of privacy regulations (GDPR, CCPA, HIPAA, etc.)"),
      ("S", "Skill in legal analysis of cyber incident notification obligations"),
      ("A", "Ability to advise on legal risk without impeding security operations"),
    ],
    "tools_t3": ["regulatory_check","incident_legal_analysis","report_generate"],
    "tools_t2": ["legal_hold_recommend","disclosure_recommend"],
    "tools_t1": ["external_agency_notify (advisory)"],
    "memory_read": ["incident_history","org_assets"], "memory_write": [],
  },
  {
    "id": "og-exec", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-006", "tier": "T2", "tier_label": "Copiloted",
    "name": "Executive Cybersecurity Leadership",
    "desc": "Provides strategic cybersecurity leadership and oversight. Synthesizes security program performance for executive decision-making and board-level reporting.",
    "objectives": [
      "Synthesize security program metrics into executive-level reporting",
      "Assess organizational cyber risk posture and trends",
      "Identify strategic security investment priorities",
      "Produce board-ready cybersecurity risk reports",
      "Monitor and report on major incident impact and organizational exposure"
    ],
    "ksas": [
      ("K", "Knowledge of cybersecurity risk management frameworks and metrics"),
      ("K", "Knowledge of business impact analysis and risk quantification methods"),
      ("S", "Skill in synthesizing technical security data for executive audiences"),
      ("A", "Ability to translate cyber risk into business impact language"),
    ],
    "tools_t3": ["risk_dashboard_query","program_metrics","report_generate"],
    "tools_t2": ["strategic_invest_recommend"], "tools_t1": [],
    "memory_read": ["incident_history","org_assets","threat_intel"], "memory_write": [],
  },
  {
    "id": "og-privacy", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-007", "tier": "T2", "tier_label": "Copiloted",
    "name": "Privacy Compliance",
    "desc": "Oversees organizational compliance with privacy regulations. Assesses data handling practices, identifies privacy risks, and advises on privacy-preserving security controls.",
    "objectives": [
      "Monitor data handling practices for privacy compliance",
      "Assess security incidents for privacy breach notification requirements",
      "Identify privacy risks in security monitoring activities",
      "Advise on privacy-preserving implementations of security controls",
      "Produce privacy compliance assessments and breach impact reports"
    ],
    "ksas": [
      ("K", "Knowledge of global privacy regulations and their cybersecurity implications"),
      ("K", "Knowledge of data classification and privacy by design principles"),
      ("S", "Skill in privacy impact assessment and breach notification analysis"),
      ("A", "Ability to balance privacy requirements with security monitoring needs"),
    ],
    "tools_t3": ["privacy_compliance_check","data_flow_analysis","report_generate"],
    "tools_t2": ["breach_notification_recommend"], "tools_t1": [],
    "memory_read": ["incident_history","org_assets"], "memory_write": [],
  },
  {
    "id": "og-product-support", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-008", "tier": "T3", "tier_label": "Autonomous",
    "name": "Product Support Management",
    "desc": "Manages lifecycle and security of cybersecurity products and tools deployed in the organization. Tracks versions, licenses, EOL status, and vulnerability patches.",
    "objectives": [
      "Track cybersecurity tool versions and EOL/EOS status",
      "Monitor for patches and updates to deployed security products",
      "Identify unsupported or vulnerable product versions in use",
      "Support product procurement and evaluation activities",
      "Produce security tool inventory and lifecycle status reports"
    ],
    "ksas": [
      ("K", "Knowledge of security product lifecycle management"),
      ("S", "Skill in tracking software versions and patch status"),
      ("A", "Ability to prioritize product updates by security risk"),
    ],
    "tools_t3": ["product_version_query","eol_check","patch_availability_check","report_generate"],
    "tools_t2": [], "tools_t1": [],
    "memory_read": ["org_assets","cve_database"], "memory_write": [],
  },
  {
    "id": "og-program-mgmt", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-009", "tier": "T2", "tier_label": "Copiloted",
    "name": "Program Management",
    "desc": "Manages cybersecurity programs — tracking milestones, resources, risks, and outcomes across multi-initiative security programs.",
    "objectives": [
      "Track cybersecurity program initiative status and milestones",
      "Identify program risks and dependencies",
      "Monitor resource allocation and budget utilization",
      "Produce program status reports for stakeholders",
      "Support program governance and decision-making with data"
    ],
    "ksas": [
      ("K", "Knowledge of program management frameworks and methodologies"),
      ("K", "Knowledge of cybersecurity program metrics and KPIs"),
      ("S", "Skill in program risk identification and tracking"),
      ("A", "Ability to synthesize multi-initiative status into coherent program view"),
    ],
    "tools_t3": ["program_status_query","risk_register_query","report_generate"],
    "tools_t2": ["program_change_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-project-mgmt", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-010", "tier": "T2", "tier_label": "Copiloted",
    "name": "Secure Project Management",
    "desc": "Manages cybersecurity projects with security embedded throughout the project lifecycle. Tracks security deliverables, risks, and outcomes.",
    "objectives": [
      "Track security project milestone completion and blockers",
      "Monitor security requirements coverage in project deliverables",
      "Identify and escalate security project risks",
      "Produce security project status reports",
      "Coordinate security testing and acceptance activities"
    ],
    "ksas": [
      ("K", "Knowledge of project management methodologies with security integration"),
      ("S", "Skill in tracking security requirements through project lifecycle"),
      ("A", "Ability to identify security risks in project plans and dependencies"),
    ],
    "tools_t3": ["project_status_query","risk_register_query","report_generate"],
    "tools_t2": ["project_change_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-assessment", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-011", "tier": "T2", "tier_label": "Copiloted",
    "name": "Security Control Assessment",
    "desc": "Independently assesses the implementation and effectiveness of security controls. Produces findings for risk management and authorization decisions.",
    "objectives": [
      "Assess security control implementation against defined baselines (NIST SP 800-53, etc.)",
      "Test control effectiveness through interviews, observation, and technical testing",
      "Produce assessment findings with risk ratings",
      "Track remediation of control deficiencies",
      "Support authorization and ATO processes with assessment evidence"
    ],
    "ksas": [
      ("K", "Knowledge of NIST SP 800-53A and control assessment methodologies"),
      ("K", "Knowledge of risk management frameworks and authorization processes"),
      ("S", "Skill in conducting security control assessments across technical and administrative domains"),
      ("A", "Ability to assess controls objectively and rate residual risk"),
    ],
    "tools_t3": ["control_assessment","config_scan","interview_record","report_generate"],
    "tools_t2": ["control_remediation_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-authorization", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-012", "tier": "T1", "tier_label": "Human-Administered",
    "name": "Systems Authorization",
    "desc": "Supports Authorizing Officials with the information needed to make risk-based authorization decisions. Prepares authorization packages and monitors system security posture continuously.",
    "objectives": [
      "Compile security authorization packages from assessment evidence",
      "Monitor authorized system security posture for changes affecting authorization",
      "Identify conditions that may require authorization revalidation",
      "Produce Plan of Action & Milestones (POA&M) tracking",
      "Brief Authorizing Officials on system risk posture and findings"
    ],
    "ksas": [
      ("K", "Knowledge of NIST RMF and authorization processes"),
      ("K", "Knowledge of security authorization package components (SSP, SAR, POA&M)"),
      ("S", "Skill in compiling and reviewing authorization documentation"),
      ("A", "Ability to synthesize complex security findings for authorization decisions"),
    ],
    "tools_t3": ["authorization_package_query","poam_track","report_generate"],
    "tools_t2": [],
    "tools_t1": ["authorization_decision (advisory)"],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-security-mgmt", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-013", "tier": "T2", "tier_label": "Copiloted",
    "name": "Systems Security Management",
    "desc": "Manages the overall cybersecurity posture of organizational systems. Oversees security monitoring, incident response, and security control maintenance.",
    "objectives": [
      "Oversee and coordinate security operations across organizational systems",
      "Monitor security posture metrics and KPIs",
      "Escalate critical security issues to executive leadership",
      "Coordinate between security domains (IR, Vulnerability, Compliance)",
      "Produce executive security operations reports"
    ],
    "ksas": [
      ("K", "Knowledge of security operations management and governance"),
      ("K", "Knowledge of risk management and security metrics"),
      ("S", "Skill in cross-domain security coordination and reporting"),
      ("A", "Ability to manage competing priorities across security operations"),
    ],
    "tools_t3": ["security_posture_query","ops_metrics_query","report_generate"],
    "tools_t2": ["escalate_to_ciso","ops_priority_recommend"], "tools_t1": [],
    "memory_read": ["incident_history","org_assets","threat_intel"], "memory_write": [],
  },
  {
    "id": "og-portfolio", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-014", "tier": "T2", "tier_label": "Copiloted",
    "name": "Technology Portfolio Management",
    "desc": "Manages the cybersecurity technology portfolio — tracking investments, rationalization, and alignment of security tools with organizational needs.",
    "objectives": [
      "Maintain inventory of security technology investments and capabilities",
      "Assess security tool effectiveness and ROI",
      "Identify portfolio gaps and overlaps",
      "Support technology refresh and investment planning",
      "Produce technology portfolio assessments for decision-making"
    ],
    "ksas": [
      ("K", "Knowledge of security technology market and capabilities"),
      ("K", "Knowledge of IT portfolio management frameworks"),
      ("S", "Skill in assessing security tool effectiveness against operational requirements"),
      ("A", "Ability to rationalize technology investments against security capability needs"),
    ],
    "tools_t3": ["portfolio_query","tool_effectiveness_assess","report_generate"],
    "tools_t2": ["portfolio_change_recommend"], "tools_t1": [],
    "memory_read": ["org_assets","incident_history"], "memory_write": [],
  },
  {
    "id": "og-audit", "cat": "OG", "cat_name": "Oversight & Governance",
    "nice_id": "OG-WRL-015", "tier": "T2", "tier_label": "Copiloted",
    "name": "Technology Program Auditing",
    "desc": "Independently audits cybersecurity programs and controls for compliance with policies, standards, and regulatory requirements. Produces objective audit findings.",
    "objectives": [
      "Plan and execute cybersecurity program audits",
      "Assess compliance with internal policies and external regulations",
      "Review audit evidence and produce objective findings",
      "Track remediation of audit findings",
      "Produce audit reports for management and regulatory audiences"
    ],
    "ksas": [
      ("K", "Knowledge of IT audit standards and methodologies (ISACA, IIA)"),
      ("K", "Knowledge of cybersecurity regulatory requirements and compliance frameworks"),
      ("S", "Skill in audit evidence collection, evaluation, and reporting"),
      ("A", "Ability to maintain independence and objectivity throughout audit process"),
    ],
    "tools_t3": ["audit_evidence_query","compliance_check","episodic_memory_read","report_generate"],
    "tools_t2": ["audit_finding_confirm"], "tools_t1": [],
    "memory_read": ["incident_history","org_assets","audit_ledger"], "memory_write": [],
  },
]

# ─── HTML TEMPLATES ──────────────────────────────────────────────────────────

NAV = '''<nav>
  <a class="nav-logo" href="../index.html">CIPHER</a>
  <a href="../index.html">Agents</a>
  <a href="https://github.com/dcplatforms/cipher" target="_blank">GitHub</a>
  <a href="https://github.com/dcplatforms/cipher/blob/main/docs/ARCHITECTURE.md" target="_blank">Architecture</a>
  <span class="nav-badge">NICE 2.1 · v0.1-pre</span>
</nav>'''

NAV_INDEX = '''<nav>
  <a class="nav-logo" href="index.html">CIPHER</a>
  <a href="index.html">Agents</a>
  <a href="https://github.com/dcplatforms/cipher" target="_blank">GitHub</a>
  <a href="https://github.com/dcplatforms/cipher/blob/main/docs/ARCHITECTURE.md" target="_blank">Architecture</a>
  <span class="nav-badge">NICE 2.1 · v0.1-pre</span>
</nav>'''

FOOTER = '''<footer>
  <p>CIPHER — Open-source NICE 2.0-aligned multi-agent cybersecurity framework &nbsp;·&nbsp;
  <a href="https://github.com/dcplatforms/cipher" target="_blank">GitHub</a> &nbsp;·&nbsp;
  MIT License &nbsp;·&nbsp; 2026</p>
</footer>'''

HEAD = lambda title, depth="": f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — CIPHER</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{depth}assets/css/cipher.css">
</head>
<body>'''

CAT_NAMES = {
  "PD": "Protection & Defense",
  "IN": "Investigation",
  "IO": "Implementation & Operation",
  "DD": "Design & Development",
  "OG": "Oversight & Governance",
}

CAT_COUNTS = {}
for a in AGENTS:
    CAT_COUNTS[a["cat"]] = CAT_COUNTS.get(a["cat"], 0) + 1


def ksa_type_label(t):
    labels = {"K": "Knowledge", "S": "Skill", "A": "Ability"}
    return labels.get(t, t)


def render_index():
    cats = ["PD","IN","IO","DD","OG"]
    filter_btns = '<button class="filter-btn active" data-cat="ALL" onclick="filterAgents(this,\'ALL\')">All Agents</button>\n'
    for cat in cats:
        filter_btns += f'<button class="filter-btn" data-cat="{cat}" onclick="filterAgents(this,\'{cat}\')">{cat} — {CAT_NAMES[cat]} ({CAT_COUNTS.get(cat,0)})</button>\n'

    cards = ""
    for a in AGENTS:
        cards += f'''<a class="agent-card" data-cat="{a["cat"]}" href="agents/{a["id"]}.html" data-cat="{a["cat"]}">
  <div class="agent-card-header">
    <span class="agent-id">{a["nice_id"]}</span>
    <span class="agent-tier tier-{a["tier"]}">{a["tier"]} · {a["tier_label"]}</span>
  </div>
  <div class="agent-name">{a["name"]}</div>
  <div class="agent-category">{a["cat_name"]}</div>
  <div class="agent-desc">{a["desc"]}</div>
  <div class="agent-stats-row">
    <div class="agent-stat-item"><span class="agent-stat-num">0</span><span class="agent-stat-lbl">Actions</span></div>
    <div class="agent-stat-item"><span class="agent-stat-num">0</span><span class="agent-stat-lbl">Tasks</span></div>
    <div class="agent-stat-item"><span class="agent-stat-num">0/0</span><span class="agent-stat-lbl">Completed</span></div>
  </div>
</a>\n'''

    return f'''{HEAD("Agent Directory")}
{NAV_INDEX}
<div class="hero">
  <div class="hero-tag">⬡ NICE Framework v2.1 · Open Source</div>
  <h1><span>CIPHER</span> Agent Directory</h1>
  <p class="hero-sub">Cybersecurity Intelligence Personas for Human-in-the-loop Enterprise Response — {len(AGENTS)} agent personas across 5 NICE categories</p>
  <div class="hero-stats">
    <div class="hero-stat"><span class="hero-stat-value">{len(AGENTS)}</span><span class="hero-stat-label">Agent Personas</span></div>
    <div class="hero-stat"><span class="hero-stat-value">5</span><span class="hero-stat-label">NICE Categories</span></div>
    <div class="hero-stat"><span class="hero-stat-value">3</span><span class="hero-stat-label">Autonomy Tiers</span></div>
    <div class="hero-stat"><span class="hero-stat-value">0</span><span class="hero-stat-label">Actions Taken</span></div>
  </div>
</div>
<div class="container">
  <div class="section">
    <div class="section-header">
      <div class="section-title">Agent Personas</div>
    </div>
    <div class="filter-bar">{filter_btns}</div>
    <div class="agent-grid" id="agentGrid">{cards}</div>
  </div>
</div>
{FOOTER}
<script>
function filterAgents(btn, cat) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.agent-card').forEach(card => {{
    card.style.display = (cat === 'ALL' || card.dataset.cat === cat) ? 'block' : 'none';
  }});
}}
</script>
</body></html>'''


def render_agent(a):
    ksa_items = ""
    for typ, text in a["ksas"]:
        ksa_items += f'''<li class="ksa-item">
  <span class="ksa-type {typ}">{typ} — {ksa_type_label(typ)}</span><br>{text}
</li>\n'''

    obj_items = "".join(f'<li class="objective-item">{o}</li>\n' for o in a["objectives"])

    tools_t3 = "".join(f'<span class="tool-tag t3">{t}</span>' for t in a["tools_t3"]) or '<span style="color:var(--text-muted);font-size:0.8rem">None</span>'
    tools_t2 = "".join(f'<span class="tool-tag t2">{t}</span>' for t in a["tools_t2"]) or '<span style="color:var(--text-muted);font-size:0.8rem">None</span>'
    tools_t1 = "".join(f'<span class="tool-tag t1">{t}</span>' for t in a["tools_t1"]) or '<span style="color:var(--text-muted);font-size:0.8rem">None</span>'

    mem_read = "".join(f'<span class="tool-tag">{m}</span>' for m in a["memory_read"]) or '<span style="color:var(--text-muted);font-size:0.8rem">None</span>'
    mem_write = "".join(f'<span class="tool-tag">{m}</span>' for m in a["memory_write"]) or '<span style="color:var(--text-muted);font-size:0.8rem">None</span>'

    tier_colors = {"T1": "var(--tier-t1)", "T2": "var(--tier-t2)", "T3": "var(--tier-t3)"}
    tier_c = tier_colors.get(a["tier"], "var(--text-secondary)")

    return f'''{HEAD(a["name"], depth="../")}
{NAV}
<div class="profile-header">
  <div class="container">
    <div class="profile-breadcrumb">
      <a href="../index.html">Agent Directory</a> / {a["cat_name"]} / {a["name"]}
    </div>
    <div class="profile-title-row">
      <span class="profile-name">{a["name"]}</span>
      <span class="profile-nice-id">{a["nice_id"]}</span>
      <span class="cat-badge {a["cat"]}">{a["cat"]} · {a["cat_name"]}</span>
      <span class="agent-tier tier-{a["tier"]}" style="font-size:0.8rem;padding:4px 12px">{a["tier"]} — {a["tier_label"]}</span>
    </div>
    <div class="profile-meta">
      <span class="profile-meta-item">⬡ <strong>Agent ID:</strong> agent-{a["id"]}</span>
      <span class="profile-meta-item">📋 <strong>NICE Role:</strong> {a["nice_id"]}</span>
      <span class="profile-meta-item" style="color:{tier_c}">⚡ <strong>Autonomy:</strong> {a["tier"]} — {a["tier_label"]}</span>
    </div>
    <p style="max-width:680px;font-size:0.9rem;color:var(--text-secondary);margin-top:1rem;line-height:1.6">{a["desc"]}</p>
  </div>
</div>
<div class="container">
  <div class="profile-layout">
    <div class="profile-main">
      <div class="profile-section">
        <div class="profile-section-title">🎯 Objectives</div>
        <ul class="objective-list">{obj_items}</ul>
      </div>
      <div class="profile-section">
        <div class="profile-section-title">🧠 Knowledge, Skills &amp; Abilities (KSAs)</div>
        <ul class="ksa-list">{ksa_items}</ul>
      </div>
      <div class="profile-section">
        <div class="profile-section-title">🔧 Authorized Tools</div>
        <div style="margin-bottom:0.75rem">
          <div style="font-size:0.7rem;color:var(--tier-t3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem">T3 — Autonomous Execution</div>
          <div class="tool-tags">{tools_t3}</div>
        </div>
        <div style="margin-bottom:0.75rem">
          <div style="font-size:0.7rem;color:var(--tier-t2);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem">T2 — Requires Human Approval</div>
          <div class="tool-tags">{tools_t2}</div>
        </div>
        <div>
          <div style="font-size:0.7rem;color:var(--tier-t1);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem">T1 — Advisory Only (human executes)</div>
          <div class="tool-tags">{tools_t1}</div>
        </div>
      </div>
      <div class="profile-section">
        <div class="profile-section-title">💾 Memory Access</div>
        <div style="margin-bottom:0.75rem">
          <div style="font-size:0.7rem;color:var(--accent-green);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem">Read Access</div>
          <div class="tool-tags">{mem_read}</div>
        </div>
        <div>
          <div style="font-size:0.7rem;color:var(--accent-yellow);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem">Write Access</div>
          <div class="tool-tags">{mem_write}</div>
        </div>
      </div>
    </div>
    <div class="stats-panel">
      <div class="stat-card">
        <div class="stat-card-title">Actions Taken</div>
        <div class="stat-big zero">0</div>
        <div class="stat-label">No actions recorded yet</div>
      </div>
      <div class="stat-card">
        <div class="stat-card-title">Task Completion</div>
        <div style="font-size:2rem;font-weight:800;font-family:monospace;color:var(--text-muted)">0 / 0</div>
        <div class="stat-label">Tasks completed / assigned</div>
      </div>
      <div class="stat-card">
        <div class="stat-card-title">Activity Breakdown</div>
        <div class="stat-grid-2">
          <div class="stat-mini"><div class="stat-mini-num zero">0</div><div class="stat-mini-lbl">T3 Auto</div></div>
          <div class="stat-mini"><div class="stat-mini-num zero">0</div><div class="stat-mini-lbl">T2 Copilot</div></div>
          <div class="stat-mini"><div class="stat-mini-num zero">0</div><div class="stat-mini-lbl">T1 Advisory</div></div>
          <div class="stat-mini"><div class="stat-mini-num zero">0</div><div class="stat-mini-lbl">Escalations</div></div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-title">Status</div>
        <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;color:var(--text-muted)">
          <span style="width:8px;height:8px;border-radius:50%;background:var(--border-bright);display:inline-block"></span>
          Not deployed
        </div>
        <div style="margin-top:0.75rem;font-size:0.75rem;color:var(--text-muted)">Last active: —</div>
      </div>
      <div class="stat-card">
        <div class="stat-card-title">Implementation</div>
        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5">
          Spec: <a href="https://github.com/dcplatforms/cipher/blob/main/specs/personas/{a["id"]}.yaml" target="_blank" style="color:var(--accent-cyan)">specs/personas/{a["id"]}.yaml</a><br>
          Status: <span style="color:var(--tier-t2)">Pre-alpha · Spec only</span>
        </div>
      </div>
    </div>
  </div>
</div>
{FOOTER}
</body></html>'''


# ─── BUILD SITE ────────────────────────────────────────────────────────────

base = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(base, "agents")
os.makedirs(agents_dir, exist_ok=True)

# Write index
with open(os.path.join(base, "index.html"), "w") as f:
    f.write(render_index())
print(f"✓ index.html")

# Write agent pages
for agent in AGENTS:
    path = os.path.join(agents_dir, f"{agent['id']}.html")
    with open(path, "w") as f:
        f.write(render_agent(agent))
    print(f"✓ agents/{agent['id']}.html")

print(f"\n✅ Generated {len(AGENTS) + 1} files ({len(AGENTS)} agent profiles + index)")

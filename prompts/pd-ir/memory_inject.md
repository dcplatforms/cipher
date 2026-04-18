# CIPHER Memory Injection Template — agent-pd-ir
# This template is populated by MemoryManager before each agent invocation.
# Jules: maintain this template. Variables in {{double_braces}} are runtime-injected.

---

## Current Session Context

**Incident ID:** {{incident_id | "NEW_INCIDENT"}}
**Session Start:** {{session_start_utc}}
**Operator on Duty:** {{operator_name | "UNATTENDED"}}

---

## Prior Incidents (Semantic Memory — similar patterns)

{{#if prior_incidents}}
The following prior incidents share indicators with the current event:

{{#each prior_incidents}}
- **[{{this.incident_id}}]** {{this.date}} | Severity: {{this.severity}} | Type: {{this.type}}
  Summary: {{this.summary}}
  Resolution: {{this.resolution}}
  MITRE TTPs: {{this.ttp_list}}
{{/each}}
{{else}}
No similar prior incidents found in semantic memory.
{{/if}}

---

## Threat Intelligence (Semantic Memory — matched IOCs)

{{#if threat_intel_matches}}
The following threat intelligence entries match current indicators:

{{#each threat_intel_matches}}
- **IOC:** {{this.ioc}} ({{this.ioc_type}})
  Source: {{this.source_id}} | Trust Score: {{this.trust_score}}
  Attribution: {{this.attribution | "Unknown"}}
  First Seen: {{this.first_seen}} | Last Seen: {{this.last_seen}}
  Associated TTPs: {{this.ttp_list}}
  Confidence: {{this.confidence}}
{{/each}}
{{else}}
No matching threat intelligence found for current indicators.
{{/if}}

---

## Applicable Playbooks (Procedural Memory)

{{#if playbooks}}
{{#each playbooks}}
### Playbook: {{this.name}}
**Trigger:** {{this.trigger}}
**Steps:**
{{#each this.steps}}
{{this.step_number}}. [{{this.tier}}] {{this.description}}
{{/each}}
**Escalation Threshold:** {{this.escalation_threshold}}
{{/each}}
{{else}}
No applicable playbooks found for current incident type.
{{/if}}

---

## Affected Assets (Semantic Memory — org asset DB)

{{#if affected_assets}}
{{#each affected_assets}}
- **{{this.hostname}}** ({{this.ip_address}})
  Classification: {{this.classification}} | Owner: {{this.owner}}
  Criticality: {{this.criticality}} | Environment: {{this.environment}}
  Last Patched: {{this.last_patched}} | EDR Status: {{this.edr_status}}
{{/each}}
{{else}}
No asset records found for current indicators.
{{/if}}

---

## Recent Actions (Episodic Memory — this incident)

{{#if episodic_history}}
Actions taken so far in this incident (most recent first):

{{#each episodic_history}}
- [{{this.timestamp}}] **{{this.event_type}}** | Agent: {{this.agent_id}}
  {{this.summary}}
  {{#if this.human_approval_id}}Human Approval: {{this.human_approval_id}}{{/if}}
{{/each}}
{{else}}
No prior actions recorded for this incident.
{{/if}}

---

## Active T2 Approvals Pending

{{#if pending_approvals}}
The following actions are awaiting human approval:
{{#each pending_approvals}}
- [{{this.approval_id}}] {{this.action}} — Submitted: {{this.submitted_at}} | Timeout: {{this.timeout_at}}
{{/each}}
{{else}}
No actions currently pending human approval.
{{/if}}

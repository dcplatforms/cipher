import logging
import asyncio
from typing import Dict, Any, List
from src.orchestrator.autonomy_gate.gate import AutonomyGate, ActionProposal, RiskClass

logger = logging.getLogger(__name__)

class ForbiddenToolError(Exception):
    """Raised when an agent attempts to invoke a tool outside its authorized scope."""
    pass

class MemoryManagerStub:
    async def read_semantic(self, collections: List[str], query: str) -> List[Dict]:
        return []
    async def write_episodic(self, entry: Dict):
        pass

class TrustBrokerStub:
    async def authorize(self, *args, **kwargs):
        # Stub: always allow for this reference agent demo, unless specific test overrides
        class Decision:
            allow = True
            reason = "stub"
        return Decision()

class AgentPDDefensive:
    def __init__(self, tenant_id: str, instance_id: str):
        self.tenant_id = tenant_id
        self.instance_id = instance_id
        self.agent_id = f"pd-defensive-{instance_id}"
        self.spiffe_id = f"spiffe://cipher.{tenant_id}/ns/cipher/sa/pd-defensive/{instance_id}"

        self.autonomy_gate = AutonomyGate()
        self.memory = MemoryManagerStub()
        self.trust_broker = TrustBrokerStub()

        self.authorized_t3_tools = {
            "siem_query", "siem_alert_acknowledge", "edr_query", "firewall_query",
            "threat_intel_lookup", "asset_db_query", "network_log_query",
            "ticket_create", "alert_deduplicate", "alert_classify", "report_generate"
        }

        self.authorized_t2_tools = {
            "ioc_block_recommend", "alert_escalate_to_ir"
        }

        self.forbidden_tools = {
            "any_direct_system_change", "memory_write_to_other_agent_namespace",
            "network_quarantine", "endpoint_isolation" # These are T1, but explicitly not callable
        }

    async def _invoke_tool(self, tool_name: str, params: Dict[str, Any], confidence: float, reasoning: str) -> Any:
        """
        Internal router for tool invocation.
        Checks tool authorization, evaluates via AutonomyGate, and executes if permitted.
        """
        if tool_name in self.forbidden_tools:
            logger.error(f"[{self.agent_id}] Attempted to invoke forbidden tool: {tool_name}")
            # In a real scenario, this would write to episodic memory and alert the behavioral monitor
            await self.memory.write_episodic({"event": "forbidden_tool_attempt", "tool": tool_name})
            raise ForbiddenToolError(f"Tool {tool_name} is forbidden for {self.agent_id}")

        # Determine risk class based on authorized lists
        if tool_name in self.authorized_t3_tools:
            risk_class = RiskClass.LOW
        elif tool_name in self.authorized_t2_tools:
            risk_class = RiskClass.MEDIUM
        else:
            # Unknown tools default to HIGH risk (fail-closed)
            risk_class = RiskClass.HIGH

        proposal = ActionProposal(
            agent_id=self.agent_id,
            action_type=tool_name,
            action_params=params,
            risk_class=risk_class,
            confidence_score=confidence,
            reasoning=reasoning
        )

        decision = await self.autonomy_gate.evaluate(f"req-{tool_name}", proposal)

        await self.memory.write_episodic({
            "action_proposed": tool_name,
            "gate_decision": decision.outcome,
            "tier_assigned": decision.assigned_tier.value
        })

        if decision.outcome == "execute":
            # Stub execution
            logger.info(f"[{self.agent_id}] Executing T3 tool: {tool_name}")
            return {"status": "executed", "tool": tool_name, "result": "stub_result"}
        elif decision.outcome == "queue_for_approval":
            logger.info(f"[{self.agent_id}] Tool {tool_name} queued for T2 approval.")
            return {"status": "queued", "tool": tool_name}
        else:
            logger.warning(f"[{self.agent_id}] Tool {tool_name} blocked (advisory only).")
            return {"status": "blocked", "tool": tool_name, "reason": decision.reason}


    # --- T3 Capabilities ---

    async def siem_query(self, query: str, confidence: float = 0.95) -> Any:
        return await self._invoke_tool("siem_query", {"query": query}, confidence, "Gathering alert context")

    async def edr_query(self, endpoint_id: str, confidence: float = 0.95) -> Any:
        return await self._invoke_tool("edr_query", {"endpoint_id": endpoint_id}, confidence, "Checking endpoint telemetry")

    async def threat_intel_lookup(self, ioc: str, confidence: float = 0.95) -> Any:
        return await self._invoke_tool("threat_intel_lookup", {"ioc": ioc}, confidence, "Enriching IOC")

    # --- T2 Capabilities ---

    async def ioc_block_recommend(self, ioc: str, confidence: float = 0.85) -> Any:
        return await self._invoke_tool("ioc_block_recommend", {"ioc": ioc}, confidence, "IOC is highly suspicious, recommending block")

    async def alert_escalate_to_ir(self, alert_id: str, confidence: float = 0.90) -> Any:
        return await self._invoke_tool("alert_escalate_to_ir", {"alert_id": alert_id}, confidence, "Confirmed true positive, escalating to IR")

    # --- Process Flow ---

    async def analyze_alert(self, alert_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for processing an inbound alert.
        """
        logger.info(f"[{self.agent_id}] Beginning triage of alert {alert_payload.get('id')}")

        # 1. Read Semantic Memory (Threat Intel, Prior Incidents)
        await self.memory.read_semantic(["threat_intel"], "alert context query")

        # 2. Execute T3 enrichment (stubs)
        await self.siem_query("search related events")
        await self.edr_query("host-123")

        # 3. Formulate output based on schema (stubbed output for implementation demo)
        output = {
            "alert_id": alert_payload.get("id", "unknown"),
            "severity": "P2",
            "classification": "true_positive",
            "confidence_score": 0.92,
            "enrichment_data": {"edr": "suspicious process found"},
            "proposed_actions": [
                {"action": "ioc_block_recommend", "tier": "T2", "rationale": "Prevent C2 communication"},
                {"action": "alert_escalate_to_ir", "tier": "T2", "rationale": "Requires human-in-loop containment"}
            ],
            "escalate_to_ir": True,
            "escalation_reason": "Active hands-on-keyboard activity suspected"
        }

        # 4. If escalating, propose the T2 action
        if output["escalate_to_ir"]:
            await self.alert_escalate_to_ir(output["alert_id"], output["confidence_score"])

        return output

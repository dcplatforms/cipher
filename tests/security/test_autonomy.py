import pytest
import asyncio
from src.security.autonomy_logic import AutonomyGate, ActionProposal, AutonomyTier

@pytest.mark.asyncio
async def test_autonomy_gate_pd_ir():
    policies = {
        "pd-ir": {"allows_autonomous": True}
    }
    gate = AutonomyGate(policies)

    # T3 Test
    t3_proposal = ActionProposal(
        agent_id="spiffe://cipher.local/ns/cipher/sa/pd-ir/001",
        action="siem_query",
        params={"query": "index=logs"},
        confidence=0.95,
        risk_class="LOW"
    )
    assert gate.evaluate(t3_proposal) == AutonomyTier.T3_AUTONOMOUS

    # T2 Test (Low confidence)
    t2_proposal = ActionProposal(
        agent_id="spiffe://cipher.local/ns/cipher/sa/pd-ir/001",
        action="ioc_block",
        params={"ip": "1.1.1.1"},
        confidence=0.80,
        risk_class="MEDIUM"
    )
    assert gate.evaluate(t2_proposal) == AutonomyTier.T2_COPILOTED

    # T1 Test (High Risk)
    t1_proposal = ActionProposal(
        agent_id="spiffe://cipher.local/ns/cipher/sa/pd-ir/001",
        action="network_quarantine",
        params={"subnet": "10.0.0.0/8"},
        confidence=0.99,
        risk_class="HIGH"
    )
    assert gate.evaluate(t1_proposal) == AutonomyTier.T1_ADVISORY

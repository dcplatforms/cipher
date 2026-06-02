import pytest
import asyncio
from src.orchestrator.autonomy_gate.gate import AutonomyGate, ActionProposal, RiskClass, AutonomyTier

@pytest.fixture
def autonomy_gate():
    return AutonomyGate()

def create_proposal(risk_class: RiskClass, confidence_score: float) -> ActionProposal:
    return ActionProposal(
        agent_id="test-agent",
        action_type="test_action",
        action_params={"param": "value"},
        risk_class=risk_class,
        confidence_score=confidence_score,
        reasoning="Test reasoning"
    )

@pytest.mark.asyncio
async def test_t3_execute(autonomy_gate):
    # LOW risk + high confidence -> T3 execute
    proposal = create_proposal(RiskClass.LOW, 0.95)
    decision = await autonomy_gate.evaluate("action-1", proposal)

    assert decision.assigned_tier == AutonomyTier.T3
    assert decision.outcome == "execute"

@pytest.mark.asyncio
async def test_t2_queue_medium_risk(autonomy_gate):
    # MEDIUM risk -> T2 queue
    proposal = create_proposal(RiskClass.MEDIUM, 0.95)
    decision = await autonomy_gate.evaluate("action-2", proposal)

    assert decision.assigned_tier == AutonomyTier.T2
    assert decision.outcome == "queue_for_approval"

@pytest.mark.asyncio
async def test_t2_queue_low_confidence(autonomy_gate):
    # LOW risk + low confidence -> fallback to T2 queue
    proposal = create_proposal(RiskClass.LOW, 0.80)
    decision = await autonomy_gate.evaluate("action-3", proposal)

    assert decision.assigned_tier == AutonomyTier.T2
    assert decision.outcome == "queue_for_approval"

@pytest.mark.asyncio
async def test_t1_advisory(autonomy_gate):
    # HIGH risk -> T1 advisory
    proposal = create_proposal(RiskClass.HIGH, 0.99)
    decision = await autonomy_gate.evaluate("action-4", proposal)

    assert decision.assigned_tier == AutonomyTier.T1
    assert decision.outcome == "advisory_only"

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.agents.pd_defensive.agent import AgentPDDefensive, ForbiddenToolError

@pytest.fixture
def agent():
    return AgentPDDefensive(tenant_id="acme", instance_id="001")

@pytest.mark.asyncio
async def test_t3_tool_invocation(agent):
    # Should execute normally as it's a T3 tool with high confidence
    result = await agent.siem_query("test query", confidence=0.95)
    assert result["status"] == "executed"
    assert result["tool"] == "siem_query"

@pytest.mark.asyncio
async def test_t2_tool_invocation(agent):
    # T2 tools should be queued, not executed directly
    result = await agent.ioc_block_recommend("1.1.1.1", confidence=0.90)
    assert result["status"] == "queued"
    assert result["tool"] == "ioc_block_recommend"

@pytest.mark.asyncio
async def test_forbidden_tool_invocation(agent):
    # Attempting to call a forbidden tool should raise an exception
    with pytest.raises(ForbiddenToolError):
        await agent._invoke_tool("network_quarantine", {}, 0.99, "Testing forbidden tool")

@pytest.mark.asyncio
async def test_t3_tool_low_confidence_fallback(agent):
    # T3 tool with confidence < 0.92 should fallback to T2 (queued)
    result = await agent.siem_query("test query", confidence=0.85)
    assert result["status"] == "queued"
    assert result["tool"] == "siem_query"

@pytest.mark.asyncio
async def test_analyze_alert_flow(agent):
    # Test the full analyze_alert flow
    alert_payload = {"id": "alert-123", "data": "suspicious"}
    output = await agent.analyze_alert(alert_payload)

    assert output["alert_id"] == "alert-123"
    assert output["classification"] == "true_positive"
    assert output["escalate_to_ir"] is True

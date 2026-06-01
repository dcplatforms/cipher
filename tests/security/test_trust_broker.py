import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

# Mock pyspiffe module since it's not available in the environment but is required in the spec.
import sys
class MockJwtSvid:
    def __init__(self):
        self.spiffe_id = MagicMock()
        self.spiffe_id.trust_domain.name = "cipher.acme-corp"

mock_pyspiffe = MagicMock()
sys.modules['pyspiffe'] = mock_pyspiffe
sys.modules['pyspiffe.spiffe_id'] = mock_pyspiffe
sys.modules['pyspiffe.spiffe_id.spiffe_id'] = mock_pyspiffe
sys.modules['pyspiffe.spiffe_id.trust_domain'] = mock_pyspiffe
sys.modules['pyspiffe.svid'] = mock_pyspiffe
sys.modules['pyspiffe.svid.jwt_svid'] = mock_pyspiffe
sys.modules['pyspiffe.svid.jwt_svid_validator'] = mock_pyspiffe
sys.modules['pyspiffe.workloadapi'] = mock_pyspiffe
sys.modules['pyspiffe.workloadapi.default_jwt_source'] = mock_pyspiffe

mock_pyspiffe.JwtSvid = MockJwtSvid

from src.security.trust_broker.broker import TrustBroker, AuthorizationRequest, AuthorizationDecision

@pytest.fixture
def trust_broker():
    # Use a dummy socket path
    broker = TrustBroker(spiffe_socket_path="unix:///dummy/path", opa_url="http://dummy:8181/v1/data/allow")
    # Mock the http client
    broker.http_client = AsyncMock()
    return broker

@pytest.fixture
def auth_request():
    return AuthorizationRequest(
        caller_spiffe_id="spiffe://cipher.acme-corp/ns/cipher/sa/pd-defensive/instance-1",
        callee_spiffe_id="spiffe://cipher.acme-corp/ns/cipher/sa/pd-ir/instance-1",
        requested_action="alert_escalate_to_ir",
        current_context={"autonomy_tier": "T3"}
    )

@pytest.mark.asyncio
async def test_invalid_svid(trust_broker, auth_request):
    # Mock verify_identity to return None (invalid SVID)
    trust_broker.verify_identity = AsyncMock(return_value=None)

    decision = await trust_broker.authorize("invalid_token", auth_request)

    assert decision.allow is False
    assert decision.reason == "Invalid or expired SVID"

@pytest.mark.asyncio
async def test_opa_deny(trust_broker, auth_request):
    # Mock verify_identity to return a valid SVID
    trust_broker.verify_identity = AsyncMock(return_value=MagicMock())

    # Mock OPA to return False
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": False}
    trust_broker.http_client.post.return_value = mock_response

    decision = await trust_broker.authorize("valid_token", auth_request)

    assert decision.allow is False
    assert decision.reason == "Action denied by OPA policy"

@pytest.mark.asyncio
async def test_opa_unreachable(trust_broker, auth_request):
    trust_broker.verify_identity = AsyncMock(return_value=MagicMock())

    # Mock OPA to raise an exception
    trust_broker.http_client.post.side_effect = Exception("Connection refused")

    decision = await trust_broker.authorize("valid_token", auth_request)

    assert decision.allow is False
    assert decision.reason == "Action denied by OPA policy"

@pytest.mark.asyncio
async def test_t3_autonomy_routing(trust_broker, auth_request):
    trust_broker.verify_identity = AsyncMock(return_value=MagicMock())

    # Mock OPA to return True
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": True}
    trust_broker.http_client.post.return_value = mock_response

    auth_request.current_context["autonomy_tier"] = "T3"

    decision = await trust_broker.authorize("valid_token", auth_request)

    assert decision.allow is True
    assert decision.reason == "T3 action authorized"
    assert decision.suspended is False

@pytest.mark.asyncio
async def test_t2_autonomy_routing(trust_broker, auth_request):
    trust_broker.verify_identity = AsyncMock(return_value=MagicMock())
    trust_broker._route_to_human_approval_queue = AsyncMock()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": True}
    trust_broker.http_client.post.return_value = mock_response

    auth_request.current_context["autonomy_tier"] = "T2"

    decision = await trust_broker.authorize("valid_token", auth_request)

    assert decision.allow is False
    assert "requires human approval" in decision.reason
    assert decision.suspended is True
    trust_broker._route_to_human_approval_queue.assert_called_once()

@pytest.mark.asyncio
async def test_t1_autonomy_routing(trust_broker, auth_request):
    trust_broker.verify_identity = AsyncMock(return_value=MagicMock())
    trust_broker._route_to_human_approval_queue = AsyncMock()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": True}
    trust_broker.http_client.post.return_value = mock_response

    auth_request.current_context["autonomy_tier"] = "T1"

    decision = await trust_broker.authorize("valid_token", auth_request)

    assert decision.allow is False
    assert "requires human approval" in decision.reason
    assert decision.suspended is True
    trust_broker._route_to_human_approval_queue.assert_called_once()

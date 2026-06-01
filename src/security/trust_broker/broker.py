import asyncio
import logging
import httpx
from typing import Dict, Any, Optional
from pydantic import BaseModel
from pyspiffe.spiffe_id.spiffe_id import SpiffeId
from pyspiffe.spiffe_id.trust_domain import TrustDomain
from pyspiffe.svid.jwt_svid import JwtSvid
from pyspiffe.svid.jwt_svid_validator import JwtSvidValidator
from pyspiffe.workloadapi.default_jwt_source import DefaultJwtSource

logger = logging.getLogger(__name__)

class AuthorizationRequest(BaseModel):
    caller_spiffe_id: str
    callee_spiffe_id: str
    requested_action: str
    current_context: Dict[str, Any]

class AuthorizationDecision(BaseModel):
    allow: bool
    reason: str
    required_tier_upgrade: Optional[str] = None
    suspended: bool = False

class TrustBroker:
    def __init__(self, spiffe_socket_path: str = "unix:///tmp/agent.sock", opa_url: str = "http://opa:8181/v1/data/cipher/inter_agent/allow", tenant_id: str = "acme-corp"):
        self.spiffe_socket_path = spiffe_socket_path
        self.opa_url = opa_url
        self.tenant_id = tenant_id

        self.http_client = httpx.AsyncClient()

        # Stub NATS Client for Human_Approval queue
        self._nats_client = "Stubbed NATS Client"

        try:
            self.jwt_source = DefaultJwtSource(spiffe_socket_path=spiffe_socket_path)
            self.jwt_validator = JwtSvidValidator(jwt_source=self.jwt_source)
        except Exception as e:
            logger.warning(f"Could not initialize SPIFFE JWT Source: {e}")
            self.jwt_validator = None

    async def verify_identity(self, svid_token: str, expected_audience: str) -> Optional[JwtSvid]:
        """
        Verifies the incoming JWT-SVID.
        Returns the parsed JwtSvid if valid, otherwise None.
        """
        if not self.jwt_validator:
            return None

        try:
            svid = self.jwt_validator.validate(svid_token, expected_audience)
            # Check trust domain matches tenant
            trust_domain = svid.spiffe_id.trust_domain.name
            if f"cipher.{self.tenant_id}" != trust_domain:
                logger.error(f"Trust domain mismatch: expected cipher.{self.tenant_id}, got {trust_domain}")
                return None
            return svid
        except Exception as e:
            logger.error(f"SVID validation failed: {e}")
            return None

    async def _query_opa(self, request: AuthorizationRequest) -> bool:
        """
        Queries OPA to evaluate the policy.
        """
        payload = {
            "input": request.model_dump()
        }
        try:
            response = await self.http_client.post(self.opa_url, json=payload, timeout=2.0)
            if response.status_code == 200:
                result = response.json().get("result", False)
                return result
            else:
                logger.error(f"OPA returned status code {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Failed to query OPA: {e}")
            return False

    async def _route_to_human_approval_queue(self, request: AuthorizationRequest):
        """
        Stubs routing to Human_Approval NATS JetStream queue.
        """
        logger.info(f"Routing request to Human_Approval NATS JetStream queue via {self._nats_client}: {request.requested_action}")

    async def _audit_log(self, decision: AuthorizationDecision, request: AuthorizationRequest, latency_ms: float):
        """
        Writes the decision to the WORM audit ledger.
        Currently a stub.
        """
        # Stub for WORM audit ledger write
        log_entry = {
            "caller_spiffe_id": request.caller_spiffe_id,
            "callee_spiffe_id": request.callee_spiffe_id,
            "requested_action": request.requested_action,
            "decision": "allow" if decision.allow else "deny",
            "policy_reason": decision.reason,
            "latency_ms": latency_ms
        }
        logger.info(f"AUDIT LOG: {log_entry}")

    async def authorize(self, svid_token: str, request: AuthorizationRequest) -> AuthorizationDecision:
        """
        Main entry point for authorization.
        1. Verifies identity.
        2. Queries OPA.
        3. Enforces Autonomy Routing (T1/T2 to queue, T3 execution).
        4. Audit logs the decision.
        """
        start_time = asyncio.get_running_loop().time()

        # 1. Identity Gate
        # Expected audience is the callee
        svid = await self.verify_identity(svid_token, request.callee_spiffe_id)
        if not svid:
            decision = AuthorizationDecision(allow=False, reason="Invalid or expired SVID")
            await self._audit_log(decision, request, (asyncio.get_running_loop().time() - start_time) * 1000)
            return decision

        # 2. Policy Enforcement (OPA)
        is_allowed = await self._query_opa(request)
        if not is_allowed:
            decision = AuthorizationDecision(allow=False, reason="Action denied by OPA policy")
            await self._audit_log(decision, request, (asyncio.get_running_loop().time() - start_time) * 1000)
            return decision

        # 3. Autonomy Routing
        tier = request.current_context.get("autonomy_tier")
        if tier in ["T1", "T2"]:
            # Route to Human_Approval queue (stubbed logic)
            await self._route_to_human_approval_queue(request)
            decision = AuthorizationDecision(
                allow=False,
                reason=f"{tier} action requires human approval. Routed to queue.",
                suspended=True
            )
        elif tier == "T3":
            decision = AuthorizationDecision(allow=True, reason="T3 action authorized")
        else:
             decision = AuthorizationDecision(allow=False, reason="Unknown autonomy tier")

        # 4. Audit Log
        await self._audit_log(decision, request, (asyncio.get_running_loop().time() - start_time) * 1000)

        return decision

    async def close(self):
        """Close external connections."""
        if self.http_client:
            await self.http_client.aclose()

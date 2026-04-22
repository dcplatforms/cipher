from enum import IntEnum
from pydantic import BaseModel
from typing import Dict, Any

class AutonomyTier(IntEnum):
    T1_ADVISORY = 1
    T2_COPILOTED = 2
    T3_AUTONOMOUS = 3

class ActionProposal(BaseModel):
    agent_id: str
    action: str
    params: Dict[str, Any]
    confidence: float
    risk_class: str

class AutonomyGate:
    def __init__(self, role_policies: Dict[str, Any]):
        self.role_policies = role_policies

    def evaluate(self, proposal: ActionProposal) -> AutonomyTier:
        policy = self.role_policies.get(proposal.agent_id.split('/')[-2], {}) # Extract role from spiffe id

        # Risk classification (Simplified logic)
        if proposal.risk_class == "HIGH":
            return AutonomyTier.T1_ADVISORY

        if proposal.risk_class == "MEDIUM" or proposal.confidence < 0.92:
            return AutonomyTier.T2_COPILOTED

        if policy.get("allows_autonomous", False) and proposal.confidence >= 0.92:
            return AutonomyTier.T3_AUTONOMOUS

        return AutonomyTier.T2_COPILOTED

# SPIFFE Signing Mock
class SpiffeSigner:
    def sign_approval(self, agent_id: str, action_id: str) -> str:
        # In reality, use SPIRE agent socket to sign with SVID private key
        return f"signed-by-{agent_id}-for-{action_id}"

    def verify_approval(self, signature: str, agent_id: str, action_id: str) -> bool:
        return signature == f"signed-by-{agent_id}-for-{action_id}"

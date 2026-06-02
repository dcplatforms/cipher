import logging
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class RiskClass(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AutonomyTier(str, Enum):
    T3 = "T3" # Autonomous
    T2 = "T2" # Copiloted
    T1 = "T1" # Human-Administered

class ActionProposal(BaseModel):
    agent_id: str
    action_type: str
    action_params: Dict[str, Any]
    risk_class: RiskClass
    confidence_score: float
    reasoning: str

class GateDecision(BaseModel):
    action_id: str
    assigned_tier: AutonomyTier
    outcome: str
    reason: str

class AutonomyGate:
    def __init__(self):
        self.t3_confidence_threshold = 0.92

    def _classify_risk(self, proposal: ActionProposal) -> AutonomyTier:
        """
        Classifies the risk and maps it to a base autonomy tier.
        LOW -> T3
        MEDIUM -> T2
        HIGH -> T1
        """
        if proposal.risk_class == RiskClass.HIGH:
            return AutonomyTier.T1
        elif proposal.risk_class == RiskClass.MEDIUM:
            return AutonomyTier.T2
        else:
            return AutonomyTier.T3

    async def evaluate(self, action_id: str, proposal: ActionProposal) -> GateDecision:
        """
        Evaluates a proposed action and assigns an autonomy tier.
        """
        logger.info(f"Evaluating action {action_id} from {proposal.agent_id} (Risk: {proposal.risk_class.value}, Confidence: {proposal.confidence_score})")

        base_tier = self._classify_risk(proposal)

        # Enforce Confidence Threshold for T3
        if base_tier == AutonomyTier.T3 and proposal.confidence_score < self.t3_confidence_threshold:
            logger.info(f"Action {action_id} confidence ({proposal.confidence_score}) below T3 threshold ({self.t3_confidence_threshold}). Escalating to T2.")
            assigned_tier = AutonomyTier.T2
        else:
            assigned_tier = base_tier

        # Route based on assigned tier
        if assigned_tier == AutonomyTier.T3:
            outcome = "execute"
            reason = "Action classified as T3 (LOW risk, high confidence)."
            await self._execute_and_log(action_id, proposal)
        elif assigned_tier == AutonomyTier.T2:
            outcome = "queue_for_approval"
            reason = "Action classified as T2 (MEDIUM risk or low confidence). Pending human approval."
            await self._queue_for_human_approval(action_id, proposal)
        else: # T1
            outcome = "advisory_only"
            reason = "Action classified as T1 (HIGH risk). Advisory only. Execution blocked."
            await self._log_advisory(action_id, proposal)

        return GateDecision(
            action_id=action_id,
            assigned_tier=assigned_tier,
            outcome=outcome,
            reason=reason
        )

    async def _execute_and_log(self, action_id: str, proposal: ActionProposal):
        """Stub for executing a T3 action and logging."""
        logger.info(f"[T3 EXECUTE] Executing action {action_id}: {proposal.action_type}")
        # In full implementation, this would trigger execution via orchestrator

    async def _queue_for_human_approval(self, action_id: str, proposal: ActionProposal):
        """Stub for queuing a T2 action for human approval."""
        logger.info(f"[T2 QUEUE] Queuing action {action_id} for human approval.")
        # In full implementation, this publishes to NATS JetStream cipher.approval.*

    async def _log_advisory(self, action_id: str, proposal: ActionProposal):
        """Stub for logging a T1 advisory action."""
        logger.info(f"[T1 ADVISORY] Action {action_id} is advisory only. No execution allowed.")

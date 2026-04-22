import os
from src.memory.worm_ledger import WormAuditLedger

# OpenClaw-specific hook/middleware for CIPHER
# This would be imported by the OpenClaw gateway runtime in a real deployment
class CipherOpenClawIntegration:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        dsn = os.getenv("DATABASE_URL", "postgresql://cipher_admin:password@timescaledb/cipher")
        self.ledger = WormAuditLedger(dsn=dsn)

    async def on_tool_call(self, tool_name: str, args: dict, result: any):
        """
        Hook called by OpenClaw whenever a tool is successfully executed.
        Preserves the action in the WORM ledger.
        """
        await self.ledger.connect()
        audit_payload = {
            "tool": tool_name,
            "args": args,
            "result_summary": str(result)[:500] # Cap size for audit log
        }
        await self.ledger.record_action(self.agent_id, audit_payload)
        print(f"Audit log entry persisted for {tool_name}")

if __name__ == "__main__":
    # Example integration test
    import asyncio
    async def test():
        integration = CipherOpenClawIntegration("spiffe://cipher.local/ns/cipher/sa/pd-ir/001")
        # await integration.on_tool_call("siem_query", {"q": "*"}, {"status": "ok"})
        pass
    asyncio.run(test())

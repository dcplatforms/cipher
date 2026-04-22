import hashlib
import json
import datetime
from typing import Optional
from pydantic import BaseModel
import asyncpg

class AuditEntry(BaseModel):
    agent_id: str
    payload_hash: str
    prev_record_hash: Optional[str] = None
    timestamp: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

class WormAuditLedger:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(self.dsn)
        await self._create_table()

    async def _create_table(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cipher_audit (
                id SERIAL PRIMARY KEY,
                prev_record_hash TEXT,
                agent_id TEXT NOT NULL,
                payload_hash TEXT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                row_hash TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_cipher_audit_timestamp ON cipher_audit (timestamp);
        """)

    async def get_last_hash(self) -> Optional[str]:
        row = await self.conn.fetchrow("SELECT row_hash FROM cipher_audit ORDER BY id DESC LIMIT 1")
        return row['row_hash'] if row else None

    def calculate_row_hash(self, entry: AuditEntry) -> str:
        data = f"{entry.prev_record_hash}|{entry.agent_id}|{entry.payload_hash}|{entry.timestamp.isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()

    async def record_action(self, agent_id: str, payload: dict):
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()

        prev_hash = await self.get_last_hash()
        timestamp = datetime.datetime.now(datetime.timezone.utc)

        entry = AuditEntry(
            agent_id=agent_id,
            payload_hash=payload_hash,
            prev_record_hash=prev_hash,
            timestamp=timestamp
        )

        row_hash = self.calculate_row_hash(entry)

        await self.conn.execute("""
            INSERT INTO cipher_audit (prev_record_hash, agent_id, payload_hash, timestamp, row_hash)
            VALUES ($1, $2, $3, $4, $5)
        """, entry.prev_record_hash, entry.agent_id, entry.payload_hash, entry.timestamp, row_hash)

        print(f"Recorded audit entry for {agent_id}. Row hash: {row_hash}")

async def main():
    # Example usage (requires a running TimescaleDB)
    # ledger = WormAuditLedger(dsn="postgresql://cipher_admin:password@localhost/cipher")
    # await ledger.connect()
    # await ledger.record_action("spiffe://cipher.acme/pd-ir/123", {"action": "block_ip", "ip": "1.2.3.4"})
    pass

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

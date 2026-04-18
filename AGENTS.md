# CIPHER — Jules Agent Guidance

This file tells Jules (and any AI coding agent) how to work in this repository.

## Project Summary

CIPHER (Cybersecurity Intelligence Personas for Human-in-the-loop Enterprise Response) is an open-source, NICE 2.0-aligned multi-agent framework for enterprise cybersecurity operations. It maps all 41 NICE Cybersecurity Workforce Framework work roles to configurable AI agent personas with secure separation of duties, layered memory, and a hybrid autonomy model.

## Repository Layout

```
cipher/
├── AGENTS.md               ← You are here. Read this first.
├── docs/
│   ├── ARCHITECTURE.md     ← Full architecture spec — read before implementing anything
│   └── AGENTS.md           ← This file (linked)
├── specs/                  ← SOURCE OF TRUTH for all implementations
│   ├── personas/           ← YAML spec for each NICE role agent
│   ├── memory/             ← Memory layer design specs
│   ├── security/           ← Security component specs
│   ├── orchestration/      ← Orchestration component specs
│   └── integrations/       ← Integration connector specs
├── prompts/
│   └── {role_id}/
│       ├── system.md       ← Agent system prompt (Jules manages this)
│       ├── memory_inject.md← Memory injection template
│       └── output_schema.json ← Structured output schema
├── src/
│   ├── orchestrator/       ← LangGraph orchestration engine
│   ├── agents/             ← One module per NICE role
│   ├── memory/             ← Memory plane implementations
│   ├── security/           ← Trust Broker, Input Guard, OPA client, Behavioral Monitor
│   └── integrations/       ← SIEM, EDR, vuln scanner connectors
├── tests/                  ← Pytest tests; mirror src/ structure
├── helm/                   ← Kubernetes Helm chart
└── docker/                 ← Docker Compose for dev
```

## Implementing a Feature

1. **Always read the spec first.** Every component has a spec in `/specs/`. Implement exactly what the spec describes. If the spec is ambiguous, add a comment and implement the most defensive interpretation.

2. **Security is non-negotiable.** Every inter-agent message must be signed. Every memory write must include provenance metadata. Every external input must pass through Input Guard. No exceptions.

3. **Never skip the audit log.** Every action, decision, and memory operation must emit an OpenTelemetry span AND write to the audit ledger. If you're implementing an action and there's no audit call, the implementation is incomplete.

4. **Deny by default.** All OPA policies start with `default allow = false`. All memory access is denied unless explicitly granted. When in doubt, deny and log.

5. **Use the established patterns.** See `src/agents/pd_defensive/` as the reference implementation for all agent modules once it exists. Follow its structure exactly.

## Code Standards

- Python 3.12+, type hints required on all public functions
- Pydantic v2 for all data models
- Async-first: use `async/await` throughout
- Tests required for every public function (pytest + pytest-asyncio)
- Docstrings required for all classes and public methods
- No secrets or API keys in source code — always use Infisical client

## Memory Access Patterns

```python
# CORRECT: Access memory via the memory manager (enforces RBAC)
from cipher.memory import MemoryManager
mem = MemoryManager(agent_id="agent-pd-ir-001", session_token=session.token)
results = await mem.semantic.query(collection="threat_intel", query=ioc, k=5)

# WRONG: Never access ChromaDB, Redis, or TimescaleDB directly from agent code
import chromadb  # ← DO NOT DO THIS in agent modules
```

## Inter-Agent Communication Patterns

```python
# CORRECT: All inter-agent messages go through Trust Broker
from cipher.security import TrustBroker
broker = TrustBroker()
await broker.send(
    from_agent=self.spiffe_id,
    to_agent="spiffe://cipher.acme/ns/cipher/sa/pd-threat/instance-001",
    action="request_threat_enrichment",
    payload={"ioc": "1.2.3.4"}
)

# WRONG: Never call another agent directly
import requests
requests.post("http://agent-pd-threat:8001/enrich", ...)  # ← DO NOT DO THIS
```

## Autonomy Gate Usage

```python
# Every action proposal MUST go through the Autonomy Gate
from cipher.orchestrator import AutonomyGate
gate = AutonomyGate()
result = await gate.evaluate(
    agent_id=self.agent_id,
    action="block_ioc",
    action_params={"ioc": "1.2.3.4", "source": "alert-12345"},
    confidence=0.87,
    reasoning="IOC confirmed malicious by 3 threat intel feeds"
)
# result.tier == T3 → execute
# result.tier == T2 → queue for human approval
# result.tier == T1 → return advisory only, do not execute
```

## Prompts Directory (Jules Manages)

Jules is responsible for creating and maintaining all files in `/prompts/`. When implementing a new agent persona, Jules should:

1. Read the persona spec at `/specs/personas/{role_id}.yaml`
2. Create `/prompts/{role_id}/system.md` — the agent's system prompt
3. Create `/prompts/{role_id}/memory_inject.md` — template for injecting memory context
4. Create `/prompts/{role_id}/output_schema.json` — structured output validation schema

System prompt guidelines:
- Define the agent's NICE role, responsibilities, and boundaries explicitly
- State what tools the agent CAN and CANNOT use
- Instruct the agent to always output in the structured schema
- Include explicit instructions: "You are a {NICE_ROLE}. You ONLY perform tasks within your defined scope. You NEVER execute actions outside your authorized tool set. All observations must be logged."

## Running Tests

```bash
pytest tests/ -v --asyncio-mode=auto
pytest tests/security/ -v  # Security plane tests (run these first)
pytest tests/agents/ -v    # Agent tests
```

## Environment Setup

```bash
cp .env.example .env        # Fill in your LLM API keys and Infisical token
docker compose up -d        # Start all infrastructure (Redis, TimescaleDB, ChromaDB, NATS, SPIRE)
pip install -e ".[dev]"     # Install cipher + dev dependencies
```

# strike-agent-systems-demo

A **Staff-level AI Systems** demo project tailored to Strike: a secure "connective layer" that lets AI agents call production tools safely.

This repo demonstrates:
- **Tool Gateway API** (FastAPI) that exposes *approved* tools to agents via a single endpoint
- **AuthN/AuthZ** with JWT, scopes, and per-tool policies
- **Zero-trust patterns**: explicit allowlists, least privilege, request signing hooks
- **Human-in-the-loop approvals** for high-risk actions
- **Audit logging** (JSONL) for every tool invocation
- **MCP (Model Context Protocol) adapter** (minimal) to show how tool catalogs can be served/consumed
- **Evaluation harness** to test policy enforcement + tool behavior deterministically

> This is a demo scaffold designed to be extended with your real services (payments, ledger, customer ops, etc.).

---

## Quickstart (local)

### 1) Requirements
- Python 3.11+
- Docker (optional)

### 2) Run the gateway
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3) Mint a demo token
```bash
python scripts/mint_token.py --sub greg --scopes tools:read tools:invoke
```

### 4) List tools
```bash
curl -s http://localhost:8000/tools \
  -H "Authorization: Bearer $(cat .token)"
```

### 5) Invoke a tool
```bash
curl -s http://localhost:8000/invoke \
  -H "Authorization: Bearer $(cat .token)" \
  -H "Content-Type: application/json" \
  -d '{"tool":"health.ping","args":{"message":"hello"}}'
```

### 6) Try a protected tool (should require approval)
```bash
curl -s http://localhost:8000/invoke \
  -H "Authorization: Bearer $(cat .token)" \
  -H "Content-Type: application/json" \
  -d '{"tool":"finance.transfer","args":{"amount_usd":50,"to":"acct_123"}}'
```

Then approve it:
```bash
python scripts/approve.py --request-id <REQUEST_ID_FROM_RESPONSE>
```

---

## Threat model (high level)

This project treats agent calls as **untrusted** by default:
- Agents must authenticate (JWT)
- Each tool has a declared **risk level** and required **scopes**
- High-risk tools require **human approval**
- Everything is **audited** with request/response metadata

---

## Repo structure

```
app/
  main.py              # FastAPI entrypoint
  auth.py              # JWT validation + scopes
  policy.py            # per-tool policy engine
  tools/               # tool registry + implementations
  mcp/                 # minimal MCP adapter
  audit.py             # JSONL audit sink
  models.py            # request/response schemas
scripts/
  mint_token.py        # local JWT minting
  approve.py           # human approval CLI
  demo_agent.py        # "agent" client example
tests/
  test_policy.py       # deterministic policy tests
docker-compose.yml
Dockerfile
```

---

## Notes for Strike reviewers

- The gateway is designed to sit between an agent runtime and internal services.
- Replace tool implementations with real service clients (gRPC/HTTP).
- Wire approvals into your internal ticketing/ops flow (Slack/Linear/etc.).

Created: 2026-02-24

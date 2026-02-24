"""Minimal MCP-style adapter (demo).

Not a full MCP implementation—just enough to show the concept:
- expose a tool catalog
- accept a tool invocation request

In a real system you'd implement MCP transport, sessioning, and richer schemas.
"""

from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_subject_and_scopes
from ..tools.catalog import registry

router = APIRouter(prefix="/mcp", tags=["mcp"])

@router.get("/tools")
def mcp_list_tools(auth=Depends(get_subject_and_scopes)):
    _sub, _scopes = auth
    return {"tools": [t.model_dump() for t in registry.list()]}

@router.post("/call")
def mcp_call(payload: dict, auth=Depends(get_subject_and_scopes)):
    # Payload: { "name": "...", "arguments": {...} }
    name = payload.get("name")
    args = payload.get("arguments", {}) or {}
    spec, fn = registry.get(name)
    if not spec or not fn:
        raise HTTPException(status_code=404, detail="Unknown tool")
    # NOTE: MCP adapter delegates real policy enforcement to /invoke in this demo.
    return {"result": fn(args)}

from fastapi import FastAPI, Depends, HTTPException
from .auth import get_subject_and_scopes
from .tools.catalog import registry
from .models import InvokeRequest, InvokeResponse
from .policy import enforce, create_approval_request, is_approved
from .audit import audit_event
from .mcp.server import router as mcp_router

app = FastAPI(title="Agent Tool Gateway (Strike Demo)", version="0.1.0")

app.include_router(mcp_router)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/tools")
def list_tools(auth=Depends(get_subject_and_scopes)):
    sub, _scopes = auth
    tools = [t.model_dump() for t in registry.list()]
    return {"subject": sub, "tools": tools}

@app.post("/invoke", response_model=InvokeResponse)
def invoke(req: InvokeRequest, auth=Depends(get_subject_and_scopes)):
    sub, scopes = auth
    spec, fn = registry.get(req.tool)
    if not spec or not fn:
        raise HTTPException(status_code=404, detail="Unknown tool")

    allowed, reason = enforce(spec, sub, scopes, req.args)
    if not allowed:
        audit_event("invoke", sub, req.tool, req.args, ok=False, error=reason)
        return InvokeResponse(ok=False, error=reason)

    # Approval gate for high-risk tools
    if spec.risk == "high":
        # caller may include request_id to re-run after approval
        request_id = req.args.get("_request_id")
        if request_id and is_approved(request_id):
            args = dict(req.args)
            args.pop("_request_id", None)
            result = fn(args)
            audit_event("invoke", sub, req.tool, args, ok=True, result=result, request_id=request_id)
            return InvokeResponse(ok=True, result=result, request_id=request_id, requires_approval=False)

        request_id = create_approval_request(req.tool, sub, req.args)
        audit_event("approval_required", sub, req.tool, req.args, ok=False, error="requires_approval", request_id=request_id)
        return InvokeResponse(ok=False, error="requires_approval", request_id=request_id, requires_approval=True)

    # Low/medium risk
    result = fn(req.args)
    request_id = audit_event("invoke", sub, req.tool, req.args, ok=True, result=result)
    return InvokeResponse(ok=True, result=result, request_id=request_id)

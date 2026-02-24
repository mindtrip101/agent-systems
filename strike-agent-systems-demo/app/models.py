from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class ToolSpec(BaseModel):
    name: str
    description: str
    scopes_required: List[str] = Field(default_factory=list)
    risk: str = "low"  # low|medium|high
    args_schema: Dict[str, Any] = Field(default_factory=dict)

class InvokeRequest(BaseModel):
    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)

class InvokeResponse(BaseModel):
    ok: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    request_id: Optional[str] = None
    requires_approval: bool = False

class ApprovalRecord(BaseModel):
    request_id: str
    tool: str
    subject: str
    args: Dict[str, Any]
    created_at: str
    approved: bool = False
    approved_at: Optional[str] = None
    approver: Optional[str] = None

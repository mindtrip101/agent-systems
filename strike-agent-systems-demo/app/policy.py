import uuid, json, time
from typing import Dict, Any, Set, Tuple, Optional
from .models import ToolSpec, ApprovalRecord
from .config import settings

# --- tool policies (can be swapped for OPA/Cedar/etc.) ---

def enforce(spec: ToolSpec, subject: str, scopes: Set[str], args: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    # scopes
    missing = [s for s in spec.scopes_required if s not in scopes]
    if missing:
        return False, f"Missing scopes: {', '.join(missing)}"

    # simple guardrails example
    if spec.name == "finance.transfer":
        amt = float(args.get("amount_usd", 0))
        if amt <= 0:
            return False, "amount_usd must be > 0"
        if amt > 1000:
            return False, "Transfers > $1000 blocked in demo policy"

    return True, None

# --- approvals ---

def _load_db() -> Dict[str, Any]:
    try:
        with open(settings.approval_db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"requests": {}}

def _save_db(db: Dict[str, Any]):
    with open(settings.approval_db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def create_approval_request(tool: str, subject: str, args: Dict[str, Any]) -> str:
    db = _load_db()
    request_id = str(uuid.uuid4())
    rec = ApprovalRecord(
        request_id=request_id,
        tool=tool,
        subject=subject,
        args=args,
        created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        approved=False,
    )
    db["requests"][request_id] = rec.model_dump()
    _save_db(db)
    return request_id

def is_approved(request_id: str) -> bool:
    db = _load_db()
    rec = db["requests"].get(request_id)
    return bool(rec and rec.get("approved"))

def approve(request_id: str, approver: str) -> bool:
    db = _load_db()
    rec = db["requests"].get(request_id)
    if not rec:
        return False
    rec["approved"] = True
    rec["approved_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec["approver"] = approver
    db["requests"][request_id] = rec
    _save_db(db)
    return True

import json, time, uuid
from typing import Any, Dict, Optional
from .config import settings

def audit_event(event_type: str, subject: str, tool: str, args: Dict[str, Any],
                ok: bool, result: Any = None, error: Optional[str] = None, request_id: Optional[str]=None):
    rec = {
        "ts": time.time(),
        "event_type": event_type,
        "subject": subject,
        "tool": tool,
        "args": args,
        "ok": ok,
        "result": result if ok else None,
        "error": error if not ok else None,
        "request_id": request_id or str(uuid.uuid4()),
    }
    with open(settings.audit_log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec["request_id"]

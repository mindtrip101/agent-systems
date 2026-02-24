from typing import Any, Dict
import time

def health_ping(args: Dict[str, Any]) -> Dict[str, Any]:
    msg = args.get("message", "pong")
    return {"pong": True, "echo": msg, "ts": time.time()}

def ledger_get_balance(args: Dict[str, Any]) -> Dict[str, Any]:
    # demo stub
    account = args.get("account", "acct_demo")
    return {"account": account, "balance_usd": 1234.56}

def finance_transfer(args: Dict[str, Any]) -> Dict[str, Any]:
    # demo stub: do not actually move money
    return {
        "transfer_id": "tr_demo_001",
        "to": args.get("to"),
        "amount_usd": float(args.get("amount_usd")),
        "status": "simulated",
    }

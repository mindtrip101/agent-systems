from app.tools.catalog import registry
from app.policy import enforce

def test_missing_scopes_blocked():
    spec, _fn = registry.get("ledger.get_balance")
    ok, reason = enforce(spec, "greg", scopes=set(["tools:read","tools:invoke"]), args={"account":"acct"})
    assert ok is False
    assert "Missing scopes" in reason

def test_transfer_over_limit_blocked():
    spec, _fn = registry.get("finance.transfer")
    ok, reason = enforce(spec, "greg", scopes=set(["tools:read","tools:invoke","finance:transfer"]), args={"to":"acct","amount_usd":2000})
    assert ok is False
    assert "blocked" in reason.lower()

from ..models import ToolSpec
from .registry import ToolRegistry
from . import impl

registry = ToolRegistry()

# Low risk
registry.register(
    ToolSpec(
        name="health.ping",
        description="Health check. Safe for agents.",
        scopes_required=["tools:read", "tools:invoke"],
        risk="low",
        args_schema={"type":"object","properties":{"message":{"type":"string"}}},
    ),
    impl.health_ping,
)

registry.register(
    ToolSpec(
        name="ledger.get_balance",
        description="Read-only balance lookup (demo).",
        scopes_required=["tools:read", "tools:invoke", "ledger:read"],
        risk="medium",
        args_schema={"type":"object","properties":{"account":{"type":"string"}},"required":["account"]},
    ),
    impl.ledger_get_balance,
)

# High risk -> approval required
registry.register(
    ToolSpec(
        name="finance.transfer",
        description="Simulated money transfer (demo). Requires human approval.",
        scopes_required=["tools:read", "tools:invoke", "finance:transfer"],
        risk="high",
        args_schema={
            "type":"object",
            "properties":{
                "to":{"type":"string"},
                "amount_usd":{"type":"number"}
            },
            "required":["to","amount_usd"]
        },
    ),
    impl.finance_transfer,
)

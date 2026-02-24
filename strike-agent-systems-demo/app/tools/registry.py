from typing import Dict, Any, Callable
from ..models import ToolSpec

ToolFn = Callable[[Dict[str, Any]], Any]

class ToolRegistry:
    def __init__(self):
        self.specs: Dict[str, ToolSpec] = {}
        self.fns: Dict[str, ToolFn] = {}

    def register(self, spec: ToolSpec, fn: ToolFn):
        self.specs[spec.name] = spec
        self.fns[spec.name] = fn

    def list(self):
        return list(self.specs.values())

    def get(self, name: str):
        return self.specs.get(name), self.fns.get(name)

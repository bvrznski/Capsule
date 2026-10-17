"""Structured in-memory bounded audit trail (never logs window titles by default)."""
from collections import deque
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass(frozen=True)
class AuditRecord:
    time: str
    component: str
    action: str
    outcome: str

class AuditTrail:
    def __init__(self, capacity=1000):
        if capacity < 1: raise ValueError('invalid capacity')
        self._items=deque(maxlen=capacity)
    def record(self, component, action, outcome):
        item=AuditRecord(datetime.now(timezone.utc).isoformat(),str(component),str(action),str(outcome))
        self._items.append(item); return item
    def recent(self, limit=100):
        if limit < 0: raise ValueError('invalid limit')
        return list(self._items)[-limit:] if limit else []

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4

@dataclass(frozen=True)
class Event:
    topic: str
    payload: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class EventBus:
    def __init__(self): self._handlers: dict[str,list[Callable[[Event],None]]] = {}
    def subscribe(self, topic, handler):
        self._handlers.setdefault(topic, []).append(handler)
        return lambda: self.unsubscribe(topic, handler)
    def unsubscribe(self, topic, handler):
        if handler in self._handlers.get(topic, []): self._handlers[topic].remove(handler)
    def publish(self, event: Event):
        errors=[]
        for handler in tuple(self._handlers.get(event.topic, []))+tuple(self._handlers.get('*', [])):
            try: handler(event)
            except Exception as exc: errors.append(exc)
        return errors

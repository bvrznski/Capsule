"""Bounded event dispatcher with recursion guard and dry-run planning."""
from collections import deque
from dataclasses import dataclass
from capsule.reactive.policies import PolicyEngine

@dataclass(frozen=True)
class DesktopEvent:
    name: str
    payload: dict

class Dispatcher:
    def __init__(self, engine: PolicyEngine, max_queue: int = 256):
        if max_queue < 1: raise ValueError('invalid queue capacity')
        self.engine=engine; self.max_queue=max_queue; self.queue=deque(); self._dispatching=False
    def submit(self, event: DesktopEvent):
        if len(self.queue) >= self.max_queue: raise OverflowError('event queue full')
        self.queue.append(event)
    def drain(self, *, dry_run=True, limit=256):
        if limit < 1: raise ValueError('invalid limit')
        if self._dispatching: raise RuntimeError('recursive dispatch blocked')
        self._dispatching=True; results=[]
        try:
            for _ in range(min(limit,len(self.queue))):
                event=self.queue.popleft()
                results.append((event.name,self.engine.evaluate(event.name,event.payload,dry_run=dry_run)))
            return results
        finally: self._dispatching=False

from dataclasses import dataclass, field

@dataclass(frozen=True)
class Policy:
    name: str
    event: str
    action: str
    conditions: dict = field(default_factory=dict)
    arguments: dict = field(default_factory=dict)
    priority: int = 0
    enabled: bool = True

class PolicyEngine:
    def __init__(self, actions=None): self.actions=dict(actions or {}); self.policies=[]
    def register_action(self,name,handler): self.actions[name]=handler
    def add(self,policy:Policy):
        if policy.action not in self.actions: raise ValueError('unknown action')
        self.policies.append(policy); self.policies.sort(key=lambda p:(-p.priority,p.name))
    def evaluate(self,event,payload,dry_run=True):
        matches=[p for p in self.policies if p.enabled and p.event==event and all(payload.get(k)==v for k,v in p.conditions.items())]
        if not dry_run:
            for p in matches: self.actions[p.action](**p.arguments)
        return [p.name for p in matches]

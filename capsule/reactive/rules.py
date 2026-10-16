from dataclasses import dataclass
from typing import Callable
@dataclass(frozen=True)
class Rule:
    event: str
    action: Callable[[dict], None]
    predicate: Callable[[dict], bool] = lambda _: True
class RuleEngine:
    def __init__(self): self.rules: list[Rule]=[]
    def register(self, rule: Rule): self.rules.append(rule)
    def dispatch(self,event: str,payload: dict) -> int:
        count=0
        for rule in tuple(self.rules):
            if rule.event == event and rule.predicate(payload): rule.action(payload);count+=1
        return count

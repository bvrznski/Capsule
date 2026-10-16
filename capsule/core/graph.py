from dataclasses import dataclass, field
from capsule.core.models import Window
@dataclass
class WindowGraph:
    nodes: dict[str, Window] = field(default_factory=dict)
    edges: dict[str, set[str]] = field(default_factory=dict)
    def add(self, key: str, window: Window):
        self.nodes[key] = window
        self.edges.setdefault(key, set())
    def link(self, a: str, b: str):
        if a not in self.nodes or b not in self.nodes: raise KeyError('unknown window')
        self.edges[a].add(b); self.edges[b].add(a)
    def group(self, key: str) -> set[str]:
        if key not in self.nodes: raise KeyError(key)
        seen={key}; pending=[key]
        while pending:
            for neighbor in self.edges[pending.pop()] - seen:
                seen.add(neighbor); pending.append(neighbor)
        return seen

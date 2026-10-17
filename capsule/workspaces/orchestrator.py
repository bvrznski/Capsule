from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Workspace:
    index: int
    name: str = ''

class WorkspaceBackend(Protocol):
    def list_workspaces(self) -> list[Workspace]: ...
    def activate_workspace(self, index: int) -> bool: ...
    def ensure_workspaces(self, count: int) -> bool: ...

class WorkspaceOrchestrator:
    def __init__(self, backend: WorkspaceBackend): self.backend=backend
    def ensure(self, count: int):
        if not 1 <= count <= 64: raise ValueError('workspace count must be 1..64')
        return self.backend.ensure_workspaces(count)
    def activate(self, index: int):
        if index not in [w.index for w in self.backend.list_workspaces()]: raise IndexError(index)
        return self.backend.activate_workspace(index)

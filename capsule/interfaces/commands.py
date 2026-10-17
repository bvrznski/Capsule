"""Declarative command registry suitable for a future Shell command palette."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class CommandSpec:
    name: str
    description: str
    handler: Callable
    destructive: bool = False

class CommandRegistry:
    def __init__(self): self._commands={}
    def register(self, spec: CommandSpec):
        if not spec.name or spec.name in self._commands: raise ValueError('invalid or duplicate command')
        self._commands[spec.name]=spec
    def search(self, query: str):
        query=query.casefold().strip()
        return sorted((s for s in self._commands.values() if query in (s.name+' '+s.description).casefold()),key=lambda s:s.name)
    def execute(self, name: str, *args, confirmed=False, **kwargs):
        spec=self._commands[name]
        if spec.destructive and not confirmed: raise PermissionError('confirmation required')
        return spec.handler(*args,**kwargs)

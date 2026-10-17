"""Bounded reversible command history with failure-safe cursor updates."""
from dataclasses import dataclass
from typing import Callable

@dataclass
class Command:
    execute: Callable[[],None]
    revert: Callable[[],None]
    label: str = ''

class UndoStack:
    def __init__(self, capacity=100):
        if capacity < 1: raise ValueError('invalid capacity')
        self.capacity=capacity; self._past=[]; self._future=[]
    def apply(self, command: Command):
        command.execute()
        self._past.append(command)
        self._past=self._past[-self.capacity:]
        self._future.clear()
    def undo(self):
        if not self._past: return False
        cmd=self._past[-1]; cmd.revert()
        self._past.pop(); self._future.append(cmd); return True
    def redo(self):
        if not self._future: return False
        cmd=self._future[-1]; cmd.execute()
        self._future.pop(); self._past.append(cmd); return True

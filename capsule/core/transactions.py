from dataclasses import dataclass, field
from typing import Callable

@dataclass
class TransactionResult:
    completed: int = 0
    rolled_back: int = 0
    errors: list[str] = field(default_factory=list)
    @property
    def ok(self): return not self.errors

class Transaction:
    def __init__(self): self.steps: list[tuple[Callable,Callable]] = []
    def add(self, apply: Callable, undo: Callable): self.steps.append((apply,undo)); return self
    def execute(self):
        result=TransactionResult(); applied=[]
        for apply,undo in self.steps:
            try:
                if apply() is False: raise RuntimeError('operation rejected')
                applied.append(undo); result.completed+=1
            except Exception as exc:
                result.errors.append(f'{type(exc).__name__}: {exc}')
                for rollback in reversed(applied):
                    try: rollback(); result.rolled_back+=1
                    except Exception as err: result.errors.append(f'rollback: {err}')
                break
        return result

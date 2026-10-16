from dataclasses import dataclass
from typing import Protocol
from capsule.core.models import Activity, Window
class WindowAdapter(Protocol):
    def list_windows(self) -> list[Window]: ...
    def apply(self, current: Window, desired: Window) -> bool: ...
@dataclass
class RestoreReport:
    matched: int = 0
    applied: int = 0
    missing: int = 0
    failed: int = 0
class RestoreEngine:
    def __init__(self, adapter: WindowAdapter): self.adapter=adapter
    def restore(self, activity: Activity, dry_run: bool = True) -> RestoreReport:
        available=self.adapter.list_windows(); used=set(); report=RestoreReport()
        for target in activity.windows:
            candidates=[(i,w) for i,w in enumerate(available) if i not in used and w.app_id==target.app_id]
            if not candidates: report.missing+=1;continue
            i,current=next(((i,w) for i,w in candidates if w.title==target.title),candidates[0]);used.add(i);report.matched+=1
            if not dry_run:
                try:
                    if self.adapter.apply(current,target):report.applied+=1
                    else:report.failed+=1
                except Exception:report.failed+=1
        return report

from dataclasses import dataclass, field
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
    matches: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

class RestoreEngine:
    def __init__(self, adapter: WindowAdapter): self.adapter = adapter

    def restore(self, activity: Activity, dry_run: bool = True) -> RestoreReport:
        available = self.adapter.list_windows()
        used = set()
        report = RestoreReport()
        for target in activity.windows:
            candidates = [(i, w) for i, w in enumerate(available)
                          if i not in used and w.app_id == target.app_id]
            if not candidates:
                report.missing += 1
                report.errors.append(f'Window unavailable: {target.app_id} / {target.title}')
                continue
            # Prefer exact title, then role, then first unused window of the app.
            i, current = max(candidates, key=lambda pair: (
                int(pair[1].title == target.title) * 4 +
                int(bool(target.role) and pair[1].role == target.role) * 2))
            used.add(i)
            report.matched += 1
            report.matches.append({'app_id': target.app_id, 'title': target.title,
                                   'current_title': current.title})
            if not dry_run:
                try:
                    if self.adapter.apply(current, target): report.applied += 1
                    else:
                        report.failed += 1
                        report.errors.append(f'Apply rejected: {target.app_id} / {target.title}')
                except Exception as exc:
                    report.failed += 1
                    report.errors.append(f'{target.app_id}: {type(exc).__name__}: {exc}')
        return report

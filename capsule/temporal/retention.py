"""Snapshot pruning plan: no deletion until explicitly executed."""
from datetime import datetime, timedelta, timezone
from capsule.temporal.history import Snapshot

def retention_candidates(snapshots: list[Snapshot], *, keep_last: int = 20,
                         max_age_days: int | None = None, now: datetime | None = None) -> list[str]:
    if keep_last < 0 or (max_age_days is not None and max_age_days < 0):
        raise ValueError('negative retention')
    now=now or datetime.now(timezone.utc)
    parsed=[]
    for item in snapshots:
        dt=datetime.fromisoformat(item.created_at.replace('Z','+00:00'))
        if dt.tzinfo is None: raise ValueError('snapshot time must have timezone')
        parsed.append((dt,item))
    parsed.sort(key=lambda pair:(pair[0],pair[1].id),reverse=True)
    protected={s.id for _,s in parsed[:keep_last]}
    cutoff=now-timedelta(days=max_age_days) if max_age_days is not None else None
    return [s.id for dt,s in parsed if s.id not in protected and (cutoff is None or dt < cutoff)]

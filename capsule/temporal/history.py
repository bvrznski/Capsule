from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4
from capsule.core.models import Activity
from capsule.persistence.store import ActivityStore
@dataclass(frozen=True)
class Snapshot:
    id: str
    activity_id: str
    created_at: str
class Timeline:
    def __init__(self, store: ActivityStore): self.store=store
    def checkpoint(self, activity: Activity) -> Snapshot:
        import copy
        snapshot=copy.deepcopy(activity)
        snapshot.id=str(uuid4())
        snapshot.metadata={**snapshot.metadata,'source_activity_id':activity.id,'snapshot':True}
        self.store.save(snapshot)
        return Snapshot(snapshot.id,activity.id,datetime.now(timezone.utc).isoformat())
    def restore(self, snapshot_id: str) -> Activity: return self.store.load(snapshot_id)

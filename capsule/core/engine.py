from __future__ import annotations
from capsule.core.models import Activity, Window
from capsule.persistence.store import ActivityStore
from capsule.security.validation import validate_name

class CapsuleEngine:
    def __init__(self, store: ActivityStore | None = None): self.store = store or ActivityStore()
    def capture(self, name: str, windows: list[Window]) -> Activity:
        activity = Activity(name=validate_name(name), windows=list(windows))
        self.store.save(activity)
        return activity
    def inspect(self, activity_id: str) -> Activity: return self.store.load(activity_id)
    def list_activities(self) -> list[Activity]:
        return [self.store.load(id_) for id_ in self.store.list_ids()]
    def rename(self, activity_id: str, name: str) -> Activity:
        activity = self.inspect(activity_id); activity.name = validate_name(name)
        self.store.save(activity); return activity
    def delete(self, activity_id: str) -> None: self.store.delete(activity_id)

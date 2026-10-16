from __future__ import annotations
from capsule.core.models import Activity, Window
from capsule.persistence.store import ActivityStore

class CapsuleEngine:
    def __init__(self, store: ActivityStore | None = None):
        self.store = store or ActivityStore()

    def capture(self, name: str, windows: list[Window]) -> Activity:
        activity = Activity(name=name, windows=list(windows))
        self.store.save(activity)
        return activity

    def inspect(self, activity_id: str) -> Activity:
        return self.store.load(activity_id)

    def list_activities(self) -> list[Activity]:
        return [self.store.load(id_) for id_ in self.store.list_ids()]

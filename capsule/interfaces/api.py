from dataclasses import asdict
from capsule.core.engine import CapsuleEngine
from capsule.activities.lifecycle import ActivityLifecycle
from capsule.core.reconcile import Reconciler

class CapsuleAPI:
    def __init__(self,engine=None): self.engine=engine or CapsuleEngine(); self.lifecycle=ActivityLifecycle(self.engine)
    def list(self): return [asdict(a) for a in self.engine.list_activities()]
    def inspect(self,id): return asdict(self.engine.inspect(id))
    def capture(self,name,windows): return asdict(self.engine.capture(name,windows))
    def transition(self,id,status): return asdict(self.lifecycle.transition(id,status))
    def plan(self,id,windows):
        p=Reconciler().plan(self.engine.inspect(id),windows)
        return {'moves':len(p.moves),'missing':len(p.missing),'unchanged':len(p.unchanged)}

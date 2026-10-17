from dataclasses import dataclass,field
from capsule.core.models import Activity,Window

@dataclass
class Plan:
    moves: list[tuple[Window,Window]]=field(default_factory=list)
    missing: list[Window]=field(default_factory=list)
    unchanged: list[Window]=field(default_factory=list)

class Reconciler:
    def plan(self,activity:Activity,observed:list[Window]):
        remaining=list(observed); plan=Plan()
        for desired in activity.windows:
            candidates=[w for w in remaining if w.app_id==desired.app_id]
            if not candidates: plan.missing.append(desired); continue
            current=max(candidates,key=lambda w:4*(w.title==desired.title)+2*(bool(desired.role) and w.role==desired.role))
            remaining.remove(current)
            if all(getattr(current,k)==getattr(desired,k) for k in ('workspace','monitor')) and all(current.geometry.get(k)==desired.geometry.get(k) for k in ('x','y','width','height')):
                plan.unchanged.append(desired)
            else: plan.moves.append((current,desired))
        return plan

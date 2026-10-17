from enum import Enum
from capsule.core.events import Event, EventBus

class ActivityStatus(str,Enum):
    CREATED='created'; ACTIVE='active'; SUSPENDED='suspended'; ARCHIVED='archived'

TRANSITIONS={
    ActivityStatus.CREATED:{ActivityStatus.ACTIVE,ActivityStatus.ARCHIVED},
    ActivityStatus.ACTIVE:{ActivityStatus.SUSPENDED,ActivityStatus.ARCHIVED},
    ActivityStatus.SUSPENDED:{ActivityStatus.ACTIVE,ActivityStatus.ARCHIVED},
    ActivityStatus.ARCHIVED:set(),
}
class ActivityLifecycle:
    def __init__(self, engine, bus=None): self.engine=engine; self.bus=bus or EventBus()
    def status(self, activity_id):
        return ActivityStatus(self.engine.inspect(activity_id).metadata.get('status','created'))
    def transition(self, activity_id, status):
        target=ActivityStatus(status); current=self.status(activity_id)
        if target not in TRANSITIONS[current]: raise ValueError(f'invalid transition {current} -> {target}')
        activity=self.engine.inspect(activity_id)
        activity.metadata['status']=target.value
        self.engine.store.save(activity)
        self.bus.publish(Event('activity.transition',{'id':activity_id,'from':current.value,'to':target.value}))
        return activity

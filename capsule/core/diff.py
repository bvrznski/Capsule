"""Serializable activity comparisons and non-destructive previews."""
from dataclasses import dataclass, field
from capsule.core.models import Activity, Window

@dataclass
class ActivityDiff:
    added: list[Window] = field(default_factory=list)
    removed: list[Window] = field(default_factory=list)
    changed: list[tuple[Window,Window]] = field(default_factory=list)

def compare(before: Activity, after: Activity) -> ActivityDiff:
    """Duplicate app windows matched by role/title and occurrence, never by app ID alone."""
    def groups(activity):
        output={}
        for w in activity.windows:
            key=(w.app_id,w.role,w.title)
            output.setdefault(key,[]).append(w)
        return output
    left,right=groups(before),groups(after)
    diff=ActivityDiff()
    for key in sorted(left.keys()|right.keys()):
        a,b=left.get(key,[]),right.get(key,[])
        for x,y in zip(a,b):
            if x != y: diff.changed.append((x,y))
        diff.removed.extend(a[len(b):]); diff.added.extend(b[len(a):])
    return diff

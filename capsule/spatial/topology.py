"""Deterministic monitor topology matching and geometry projection."""
from dataclasses import dataclass, replace
from capsule.core.models import Window

@dataclass(frozen=True)
class Monitor:
    key: str
    x: int
    y: int
    width: int
    height: int
    primary: bool = False
    def __post_init__(self):
        if not self.key or self.width <= 0 or self.height <= 0:
            raise ValueError("invalid monitor")

def match_monitors(saved: list[Monitor], current: list[Monitor]) -> dict[str, str]:
    """Stable identity first, then primary, then closest resolution; no double allocation."""
    remaining = list(current)
    result = {}
    for old in saved:
        if not remaining: break
        exact = next((m for m in remaining if m.key == old.key), None)
        target = exact or min(remaining, key=lambda m: (
            0 if m.primary == old.primary else 1,
            abs(m.width-old.width)+abs(m.height-old.height), m.key))
        result[old.key] = target.key
        remaining.remove(target)
    return result

def project_window(window: Window, source: Monitor, target: Monitor, *, min_size: int = 64) -> Window:
    """Preserve relative placement and clamp visible geometry to target monitor."""
    g = window.geometry
    if not {'x','y','width','height'} <= g.keys():
        return replace(window, monitor=target.key)
    width = max(1, min(target.width, max(min_size, round(g['width'] * target.width/source.width))))
    height = max(1, min(target.height, max(min_size, round(g['height'] * target.height/source.height))))
    x = target.x + round((g['x']-source.x) * target.width/source.width)
    y = target.y + round((g['y']-source.y) * target.height/source.height)
    x = min(max(target.x, x), target.x+target.width-width)
    y = min(max(target.y, y), target.y+target.height-height)
    return replace(window, monitor=target.key, geometry={**g,'x':x,'y':y,'width':width,'height':height})

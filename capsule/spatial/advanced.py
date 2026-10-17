"""Pure geometry planners: master-stack, columns and golden-ratio splits."""
from dataclasses import replace
from capsule.core.models import Window
from capsule.spatial.composition import Rect

def master_stack(windows: list[Window], bounds: Rect, ratio: float = .62, gap: int = 8) -> list[Window]:
    if not 0.2 <= ratio <= 0.8 or gap < 0: raise ValueError('invalid ratio or gap')
    if not windows: return []
    if len(windows) == 1: return [_place(windows[0],bounds)]
    usable=bounds.width-gap
    if usable < 2: raise ValueError('viewport too narrow')
    master_w=max(1,min(usable-1,round(usable*ratio)))
    left=Rect(bounds.x,bounds.y,master_w,bounds.height)
    right_x=bounds.x+master_w+gap
    right_w=bounds.width-master_w-gap
    if right_w <= 0: raise ValueError('viewport too narrow')
    result=[_place(windows[0],left)]
    count=len(windows)-1
    if bounds.height < (count-1)*gap+count: raise ValueError('viewport too short')
    usable_h=bounds.height-(count-1)*gap
    for i,w in enumerate(windows[1:]):
        top=bounds.y+(usable_h*i//count)+i*gap
        bottom=bounds.y+(usable_h*(i+1)//count)+i*gap
        result.append(_place(w,Rect(right_x,top,right_w,bottom-top)))
    return result

def _place(window: Window, rect: Rect) -> Window:
    return replace(window,geometry={**window.geometry,'x':rect.x,'y':rect.y,'width':rect.width,'height':rect.height})

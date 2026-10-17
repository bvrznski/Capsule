from dataclasses import dataclass, replace
from capsule.core.models import Window

@dataclass(frozen=True)
class Rect:
    x: int; y: int; width: int; height: int
    def __post_init__(self):
        if self.width <= 0 or self.height <= 0: raise ValueError('invalid rectangle')
    def inset(self, gap: int):
        if gap < 0 or gap*2 >= min(self.width,self.height): raise ValueError('invalid gap')
        return Rect(self.x+gap,self.y+gap,self.width-2*gap,self.height-2*gap)

class Composer:
    def tile(self, windows: list[Window], bounds: Rect, columns: int=2, gap: int=0):
        if columns < 1 or gap < 0: raise ValueError('invalid layout')
        if not windows: return []
        cols=min(columns,len(windows)); rows=(len(windows)+cols-1)//cols
        result=[]
        for i,w in enumerate(windows):
            col=i%cols; row=i//cols
            x=bounds.x+col*bounds.width//cols; y=bounds.y+row*bounds.height//rows
            x2=bounds.x+(col+1)*bounds.width//cols; y2=bounds.y+(row+1)*bounds.height//rows
            rect=Rect(x,y,x2-x,y2-y).inset(gap)
            result.append(replace(w,geometry={**w.geometry,'x':rect.x,'y':rect.y,'width':rect.width,'height':rect.height}))
        return result
    def stack(self, windows: list[Window], bounds: Rect):
        return [replace(w,geometry={**w.geometry,'x':bounds.x,'y':bounds.y,'width':bounds.width,'height':bounds.height}) for w in windows]

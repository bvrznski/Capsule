from dataclasses import replace
from capsule.core.models import Window

def grid(windows: list[Window], width: int, height: int, columns: int = 2) -> list[Window]:
    if width <= 0 or height <= 0 or columns <= 0: raise ValueError('invalid viewport')
    if not windows: return []
    cols=min(columns,len(windows)); rows=(len(windows)+cols-1)//cols
    result=[]
    for i,w in enumerate(windows):
        col=i%cols; row=i//cols
        x=col*width//cols; y=row*height//rows
        geometry={'x':x,'y':y,'width':(col+1)*width//cols-x,'height':(row+1)*height//rows-y}
        result.append(replace(w,geometry=geometry))
    return result

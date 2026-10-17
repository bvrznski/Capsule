"""Declarative named placement zones."""
from dataclasses import dataclass
from capsule.spatial.composition import Rect

@dataclass(frozen=True)
class Zone:
    name: str
    x_fraction: float
    y_fraction: float
    width_fraction: float
    height_fraction: float
    def __post_init__(self):
        if not self.name or min(self.x_fraction,self.y_fraction) < 0 or min(self.width_fraction,self.height_fraction) <= 0 or self.x_fraction+self.width_fraction > 1.000001 or self.y_fraction+self.height_fraction > 1.000001:
            raise ValueError('invalid zone')
    def resolve(self, bounds: Rect) -> Rect:
        x=bounds.x+round(self.x_fraction*bounds.width)
        y=bounds.y+round(self.y_fraction*bounds.height)
        right=bounds.x+round((self.x_fraction+self.width_fraction)*bounds.width)
        bottom=bounds.y+round((self.y_fraction+self.height_fraction)*bounds.height)
        return Rect(x,y,right-x,bottom-y)

PRESETS=(Zone('left',0,0,.5,1),Zone('right',.5,0,.5,1),Zone('center',.25,.1,.5,.8),Zone('full',0,0,1,1))

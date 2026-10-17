import re
from uuid import UUID

def validate_id(value):
    parsed=UUID(value)
    if str(parsed)!=value: raise ValueError('noncanonical identifier')
    return value

def validate_name(value):
    if not isinstance(value,str) or not 1<=len(value.strip())<=128 or any(ord(c)<32 for c in value): raise ValueError('invalid name')
    return value.strip()

def validate_geometry(g):
    keys=('x','y','width','height')
    if not all(isinstance(g.get(k),int) and not isinstance(g.get(k),bool) for k in keys): raise ValueError('invalid geometry')
    if not (-32768<=g['x']<=32768 and -32768<=g['y']<=32768 and 1<=g['width']<=32768 and 1<=g['height']<=32768): raise ValueError('geometry out of bounds')
    return g

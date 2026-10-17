from dataclasses import dataclass, field

@dataclass
class RelationshipGraph:
    edges: dict[str,dict[str,str]] = field(default_factory=dict)
    def connect(self, a: str, b: str, relation: str='associated'):
        if not a or not b or a==b: raise ValueError('invalid relationship')
        if relation not in {'associated','parent','follows','paired'}: raise ValueError('unknown relation')
        self.edges.setdefault(a,{})[b]=relation
        if relation in {'associated','paired'}: self.edges.setdefault(b,{})[a]=relation
    def disconnect(self,a,b):
        self.edges.get(a,{}).pop(b,None); self.edges.get(b,{}).pop(a,None)
    def neighbors(self,a,relation=None):
        return {b for b,r in self.edges.get(a,{}).items() if relation is None or r==relation}
    def connected(self,a):
        visited={a}; pending=[a]
        while pending:
            for b in self.neighbors(pending.pop())-visited: visited.add(b); pending.append(b)
        return visited

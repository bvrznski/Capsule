from pathlib import Path
from capsule.core.models import Activity, Window
from capsule.core.graph import WindowGraph
from capsule.core.restore import RestoreEngine
from capsule.persistence.store import ActivityStore
from capsule.temporal.history import Timeline
from capsule.spatial.layout import grid
from capsule.reactive.rules import Rule,RuleEngine

def test_graph():
    g=WindowGraph(); w=Window('app');g.add('a',w);g.add('b',w);g.link('a','b');assert g.group('a')=={'a','b'}
def test_grid():
    out=grid([Window('a'),Window('b'),Window('c')],100,80);assert len(out)==3;assert out[0].geometry['width']==50

def test_snapshot(tmp_path):
    store=ActivityStore(tmp_path); a=Activity('test',windows=[Window('app')]);store.save(a)
    snapshot=Timeline(store).checkpoint(a);assert snapshot.id != a.id;assert Timeline(store).restore(snapshot.id).windows[0].app_id=='app'
def test_rules():
    events=[];e=RuleEngine();e.register(Rule('open',lambda p:events.append(p['name'])));assert e.dispatch('open',{'name':'x'})==1;assert events==['x']
def test_restore():
    class Adapter:
        def list_windows(self):return [Window('app',title='x')]
        def apply(self,a,b):return True
    activity=Activity('a',windows=[Window('app',title='x'),Window('missing')]);r=RestoreEngine(Adapter()).restore(activity,False)
    assert (r.matched,r.applied,r.missing)==(1,1,1)

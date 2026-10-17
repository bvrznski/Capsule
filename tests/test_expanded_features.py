import pytest
from capsule.core.models import Window,Activity
from capsule.spatial.topology import Monitor,match_monitors,project_window
from capsule.spatial.advanced import master_stack
from capsule.spatial.composition import Rect
from capsule.spatial.zones import PRESETS
from capsule.activities.profiles import Profile,apply_profile
from capsule.core.diff import compare
from capsule.core.undo import UndoStack,Command
from capsule.interfaces.commands import CommandRegistry,CommandSpec
from capsule.reactive.dispatcher import Dispatcher,DesktopEvent
from capsule.reactive.policies import PolicyEngine,Policy
from capsule.temporal.retention import retention_candidates
from capsule.temporal.history import Snapshot
from capsule.observability.audit import AuditTrail

def test_monitor_projection():
 a=Monitor('old',0,0,1920,1080,True); b=Monitor('new',100,50,1280,720,True)
 assert match_monitors([a],[b])=={'old':'new'}
 w=project_window(Window('editor',geometry={'x':960,'y':540,'width':960,'height':540}),a,b)
 assert w.geometry=={'x':740,'y':410,'width':640,'height':360}

def test_master_stack():
 ws=[Window(str(i)) for i in range(3)]
 result=master_stack(ws,Rect(0,0,1000,600))
 assert len(result)==3 and result[0].geometry['width']>result[1].geometry['width']

def test_profiles_and_diff():
 a=Activity('dev',windows=[Window('editor',title='one')]); b=apply_profile(a,Profile('coding',workspace='2'))
 assert a.windows[0].workspace=='' and b.windows[0].workspace=='2'
 assert len(compare(a,b).changed)==1

def test_undo_and_registry():
 state=[]; stack=UndoStack(); stack.apply(Command(lambda:state.append(1),lambda:state.pop()))
 assert stack.undo() and not state and stack.redo() and state==[1]
 registry=CommandRegistry(); registry.register(CommandSpec('clear','clear',state.clear,True))
 with pytest.raises(PermissionError): registry.execute('clear')
 registry.execute('clear',confirmed=True); assert state==[]

def test_dispatcher():
 hits=[]; engine=PolicyEngine({'hit':lambda:hits.append(1)})
 engine.add(Policy('p','window-open','hit')); dispatcher=Dispatcher(engine)
 dispatcher.submit(DesktopEvent('window-open',{}))
 assert dispatcher.drain(dry_run=False)==[('window-open',['p'])] and hits==[1]

def test_retention_and_zones():
 snaps=[Snapshot(str(i),'a',f'2026-01-0{i+1}T00:00:00+00:00') for i in range(3)]
 assert retention_candidates(snaps,keep_last=1)==['1','0']
 assert PRESETS[0].resolve(Rect(0,0,100,100)).width==50

def test_audit():
 audit=AuditTrail(2)
 for i in range(3): audit.record('core',str(i),'ok')
 assert [x.action for x in audit.recent()]==['1','2']

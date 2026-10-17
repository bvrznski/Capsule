import pytest
from capsule.core.models import Window
from capsule.core.engine import CapsuleEngine
from capsule.persistence.store import ActivityStore
from capsule.activities.lifecycle import ActivityLifecycle
from capsule.core.events import Event,EventBus
from capsule.core.transactions import Transaction
from capsule.core.relationships import RelationshipGraph
from capsule.core.reconcile import Reconciler
from capsule.spatial.composition import Rect,Composer
from capsule.reactive.policies import Policy,PolicyEngine
from capsule.temporal.journal import EventJournal
from capsule.persistence.export import ActivityExchange
from capsule.config.settings import Settings

def test_lifecycle(tmp_path):
    e=CapsuleEngine(ActivityStore(tmp_path)); a=e.capture('work',[]); lifecycle=ActivityLifecycle(e)
    assert lifecycle.transition(a.id,'active').metadata['status']=='active'
    assert lifecycle.transition(a.id,'suspended').metadata['status']=='suspended'
    with pytest.raises(ValueError): lifecycle.transition(a.id,'created')

def test_bus_and_transactions():
    bus=EventBus(); seen=[]; bus.subscribe('x',lambda e:seen.append(e.payload)); assert bus.publish(Event('x',{'n':1}))==[]; assert seen==[{'n':1}]
    values=[]; t=Transaction().add(lambda:values.append(1),lambda:values.pop()).add(lambda:False,lambda:None)
    r=t.execute(); assert not r.ok and r.rolled_back==1 and not values

def test_graph_and_composer():
    g=RelationshipGraph(); g.connect('a','b'); g.connect('b','c'); assert g.connected('a')=={'a','b','c'}
    windows=[Window('org.app'),Window('org.app2')]
    out=Composer().tile(windows,Rect(10,20,100,100),columns=2)
    assert out[0].geometry['x']==10 and out[1].geometry['x']==60

def test_policy_and_reconcile(tmp_path):
    seen=[]; engine=PolicyEngine({'mark':lambda value:seen.append(value)})
    engine.add(Policy('test','open','mark',{'app':'x'},{'value':1}))
    assert engine.evaluate('open',{'app':'x'})==['test'] and seen==[]
    engine.evaluate('open',{'app':'x'},dry_run=False); assert seen==[1]
    e=CapsuleEngine(ActivityStore(tmp_path)); a=e.capture('A',[Window('x',geometry={'x':1,'y':2,'width':3,'height':4})])
    assert len(Reconciler().plan(a,[]).missing)==1

def test_exchange_and_journal(tmp_path):
    store=ActivityStore(tmp_path/'store'); a=CapsuleEngine(store).capture('A',[])
    exchange=ActivityExchange(store); path=tmp_path/'activity.json'; exchange.export(a.id,path)
    with pytest.raises(FileExistsError): exchange.import_file(path)
    assert exchange.import_file(path,replace=True).id==a.id
    journal=EventJournal(tmp_path/'journal'); journal.append(Event('hello')); assert journal.read()[0]['topic']=='hello'

def test_settings():
    assert Settings().validate().default_columns==2
    with pytest.raises(ValueError): Settings(default_columns=0).validate()

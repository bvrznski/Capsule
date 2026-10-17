import json
import pytest
from capsule.core.models import Window
from capsule.core.engine import CapsuleEngine
from capsule.core.restore import RestoreEngine
from capsule.persistence.store import ActivityStore

class FakeAdapter:
    def __init__(self, windows): self.windows = windows; self.calls = []
    def list_windows(self): return self.windows
    def apply(self, current, desired): self.calls.append((current, desired)); return True

def test_roundtrip_rename_delete(tmp_path):
    engine = CapsuleEngine(ActivityStore(tmp_path))
    activity = engine.capture('  Work  ', [Window(app_id='editor', title='Code')])
    assert engine.inspect(activity.id).name == 'Work'
    engine.rename(activity.id, 'New')
    assert engine.inspect(activity.id).name == 'New'
    engine.delete(activity.id)
    assert engine.list_activities() == []

def test_path_traversal_rejected(tmp_path):
    store = ActivityStore(tmp_path)
    with pytest.raises(ValueError): store.load('../../etc/passwd')

def test_restore_duplicate_app_matches_titles(tmp_path):
    engine = CapsuleEngine(ActivityStore(tmp_path))
    activity = engine.capture('Work', [Window('editor','B'), Window('editor','A')])
    adapter = FakeAdapter([Window('editor','A'), Window('editor','B')])
    report = RestoreEngine(adapter).restore(activity, dry_run=False)
    assert (report.matched, report.applied, report.failed) == (2,2,0)
    assert [a.title for a,b in adapter.calls] == ['B','A']

def test_restore_dry_run(tmp_path):
    engine = CapsuleEngine(ActivityStore(tmp_path))
    activity = engine.capture('Work', [Window('editor','A')])
    adapter = FakeAdapter([Window('editor','A')])
    report = RestoreEngine(adapter).restore(activity)
    assert report.matched == 1 and report.applied == 0 and not adapter.calls

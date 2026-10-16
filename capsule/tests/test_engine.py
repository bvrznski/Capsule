from capsule.core.engine import CapsuleEngine
from capsule.core.models import Window
from capsule.persistence.store import ActivityStore

def test_capture_roundtrip(tmp_path):
    engine = CapsuleEngine(ActivityStore(tmp_path))
    saved = engine.capture('Development', [Window(app_id='org.gnome.Terminal', geometry={'x': 1, 'y': 2, 'width': 800, 'height': 600})])
    restored = engine.inspect(saved.id)
    assert restored == saved
    assert engine.list_activities() == [saved]

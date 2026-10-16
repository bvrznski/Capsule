from __future__ import annotations
import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from capsule.core.models import Activity, Window

class ActivityStore:
    def __init__(self, root: Path | None = None):
        self.root = root or Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state')) / 'capsule' / 'activities'
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)

    def save(self, activity: Activity) -> Path:
        path = self.root / f'{activity.id}.json'
        fd, tmp = tempfile.mkstemp(dir=self.root, prefix='.activity-', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                json.dump({'schema_version': 1, **asdict(activity)}, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(tmp, 0o600)
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        return path

    def load(self, activity_id: str) -> Activity:
        from uuid import UUID
        UUID(activity_id)
        data = json.loads((self.root / f'{activity_id}.json').read_text(encoding='utf-8'))
        if data.get('schema_version') != 1:
            raise ValueError('Unsupported Capsule schema')
        return Activity(name=data['name'], id=data['id'], windows=[Window(**w) for w in data['windows']], metadata=data.get('metadata', {}))

    def list_ids(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob('*.json'))

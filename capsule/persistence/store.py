from __future__ import annotations
import json, os, tempfile
from dataclasses import asdict
from pathlib import Path
from uuid import UUID
from capsule.core.models import Activity, Window

MAX_BYTES = 4 * 1024 * 1024
class ActivityStore:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state')) / 'capsule' / 'activities'
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)

    def _path(self, activity_id: str) -> Path:
        return self.root / f'{UUID(activity_id)}.json'

    def save(self, activity: Activity) -> Path:
        path = self._path(activity.id)
        content = json.dumps({'schema_version': 1, **asdict(activity)}, ensure_ascii=False, indent=2).encode('utf8')
        if len(content) > MAX_BYTES: raise ValueError('Activity exceeds size limit')
        fd, tmp = tempfile.mkstemp(dir=self.root, prefix='.activity-', suffix='.tmp')
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(content); stream.flush(); os.fsync(stream.fileno())
            os.chmod(tmp, 0o600)
            os.replace(tmp, path)
            directory_fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
            try: os.fsync(directory_fd)
            finally: os.close(directory_fd)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        return path

    def load(self, activity_id: str) -> Activity:
        path = self._path(activity_id)
        if path.stat().st_size > MAX_BYTES: raise ValueError('Activity exceeds size limit')
        data = json.loads(path.read_text(encoding='utf8'))
        if data.get('schema_version') != 1: raise ValueError('Unsupported Capsule schema')
        if data['id'] != str(UUID(activity_id)): raise ValueError('Activity ID mismatch')
        if not isinstance(data['windows'], list): raise ValueError('Invalid windows')
        return Activity(name=data['name'], id=data['id'],
                        windows=[Window(**w) for w in data['windows']], metadata=data.get('metadata', {}))

    def delete(self, activity_id: str) -> None: self._path(activity_id).unlink()
    def list_ids(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob('*.json') if _is_uuid(p.stem))

def _is_uuid(value):
    try: return str(UUID(value)) == value
    except ValueError: return False

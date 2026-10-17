import json
from dataclasses import asdict
from pathlib import Path
from uuid import UUID
from capsule.core.models import Activity,Window

class ActivityExchange:
    def __init__(self,store): self.store=store
    def export(self,activity_id,path):
        activity=self.store.load(activity_id)
        payload={'format':'rebuntu-capsule','schema_version':1,'activity':asdict(activity)}
        Path(path).write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
    def import_file(self,path,replace=False):
        p=Path(path)
        if p.stat().st_size>4*1024*1024: raise ValueError('import too large')
        data=json.loads(p.read_text(encoding='utf-8'))
        if data.get('format')!='rebuntu-capsule' or data.get('schema_version')!=1: raise ValueError('unsupported export')
        obj=data['activity']; UUID(obj['id'])
        activity=Activity(name=obj['name'],id=obj['id'],windows=[Window(**w) for w in obj['windows']],metadata=obj.get('metadata',{}))
        if not replace and self.store._path(activity.id).exists(): raise FileExistsError(activity.id)
        self.store.save(activity); return activity

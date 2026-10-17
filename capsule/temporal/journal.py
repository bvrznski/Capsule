import json, os, tempfile
from pathlib import Path
from capsule.core.events import Event

class EventJournal:
    def __init__(self,root:Path):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
    def append(self,event:Event):
        path=self.root/'events.jsonl'
        data=json.dumps(event.__dict__,ensure_ascii=False)+'\n'
        fd=os.open(path,os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
        with os.fdopen(fd,'a',encoding='utf-8') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    def read(self,limit=100):
        if not 1<=limit<=10000: raise ValueError('invalid limit')
        path=self.root/'events.jsonl'
        if not path.exists(): return []
        from collections import deque
        with path.open(encoding='utf-8') as f: return [json.loads(line) for line in deque(f,maxlen=limit)]

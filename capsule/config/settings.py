import json,os
from pathlib import Path
from dataclasses import dataclass,asdict

@dataclass
class Settings:
    snapshot_limit: int=100
    restore_dry_run: bool=True
    default_columns: int=2
    def validate(self):
        if not 1<=self.snapshot_limit<=10000: raise ValueError('snapshot_limit')
        if not 1<=self.default_columns<=32: raise ValueError('default_columns')
        if not isinstance(self.restore_dry_run,bool): raise ValueError('restore_dry_run')
        return self

def load(path=None):
    path=Path(path or Path(os.environ.get('XDG_CONFIG_HOME',Path.home()/'.config'))/'capsule'/'settings.json')
    if not path.exists(): return Settings()
    if path.stat().st_size>65536: raise ValueError('config too large')
    return Settings(**json.loads(path.read_text(encoding='utf-8'))).validate()

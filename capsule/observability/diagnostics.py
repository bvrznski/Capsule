import importlib.util,platform
from pathlib import Path

def diagnose(store=None):
    report={'python':platform.python_version(),'system':platform.system(),
            'gi_available':importlib.util.find_spec('gi') is not None,
            'store_writable':None,'activity_count':None}
    if store is not None:
        report['store_writable']=store.root.is_dir() and __import__('os').access(store.root,__import__('os').W_OK)
        report['activity_count']=len(store.list_ids())
    return report

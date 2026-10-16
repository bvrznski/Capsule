import argparse,json
from dataclasses import asdict
from capsule.core.engine import CapsuleEngine
from capsule.core.restore import RestoreEngine
from capsule.interfaces.dbus.client import ShellClient
from capsule.temporal.history import Timeline

def main(argv=None):
    parser=argparse.ArgumentParser(prog='capsulectl')
    sub=parser.add_subparsers(dest='command',required=True)
    capture=sub.add_parser('capture');capture.add_argument('name')
    sub.add_parser('list'); inspect=sub.add_parser('inspect');inspect.add_argument('id')
    restore=sub.add_parser('restore');restore.add_argument('id');restore.add_argument('--apply',action='store_true')
    snap=sub.add_parser('snapshot');snap.add_argument('id')
    args=parser.parse_args(argv);engine=CapsuleEngine()
    if args.command=='capture': result=asdict(engine.capture(args.name,ShellClient().list_windows()))
    elif args.command=='list': result=[{'id':a.id,'name':a.name} for a in engine.list_activities()]
    elif args.command=='inspect': result=asdict(engine.inspect(args.id))
    elif args.command=='snapshot':result=asdict(Timeline(engine.store).checkpoint(engine.inspect(args.id)))
    else: result=asdict(RestoreEngine(ShellClient()).restore(engine.inspect(args.id),dry_run=not args.apply))
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__': main()

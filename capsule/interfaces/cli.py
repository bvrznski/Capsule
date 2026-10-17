import argparse,json,sys
from dataclasses import asdict
from capsule.core.engine import CapsuleEngine
from capsule.core.restore import RestoreEngine
from capsule.temporal.history import Timeline
from capsule.persistence.export import ActivityExchange
from capsule.observability.diagnostics import diagnose
from capsule.activities.lifecycle import ActivityLifecycle

def main(argv=None):
    parser=argparse.ArgumentParser(prog='capsulectl')
    sub=parser.add_subparsers(dest='command',required=True)
    for command in ('list','doctor','workspaces'): sub.add_parser(command)
    for command in ('inspect','snapshot','delete'): sub.add_parser(command).add_argument('id')
    for command in ('capture','rename'):
        p=sub.add_parser(command)
        if command=='rename': p.add_argument('id')
        p.add_argument('name')
    p=sub.add_parser('restore'); p.add_argument('id'); p.add_argument('--apply',action='store_true')
    p=sub.add_parser('transition'); p.add_argument('id'); p.add_argument('status',choices=['active','suspended','archived'])
    p=sub.add_parser('export'); p.add_argument('id'); p.add_argument('path')
    p=sub.add_parser('import'); p.add_argument('path'); p.add_argument('--replace',action='store_true')
    p=sub.add_parser('plan'); p.add_argument('id')
    args=parser.parse_args(argv); engine=CapsuleEngine()
    try:
        if args.command=='doctor':
            result=diagnose(engine.store)
            try:
                from capsule.interfaces.dbus.client import ShellClient
                result['shell_connected']=True; result['windows']=len(ShellClient().list_windows())
            except (ImportError,RuntimeError,OSError) as exc: result['shell_connected']=False; result['shell_error']=str(exc)
        elif args.command=='capture':
            from capsule.interfaces.dbus.client import ShellClient
            result=asdict(engine.capture(args.name,ShellClient().list_windows()))
        elif args.command=='list': result=[{'id':a.id,'name':a.name,'status':a.metadata.get('status','created')} for a in engine.list_activities()]
        elif args.command=='inspect': result=asdict(engine.inspect(args.id))
        elif args.command=='rename': result=asdict(engine.rename(args.id,args.name))
        elif args.command=='delete': engine.delete(args.id); result={'deleted':args.id}
        elif args.command=='snapshot': result=asdict(Timeline(engine.store).checkpoint(engine.inspect(args.id)))
        elif args.command=='transition': result=asdict(ActivityLifecycle(engine).transition(args.id,args.status))
        elif args.command=='export': ActivityExchange(engine.store).export(args.id,args.path); result={'exported':args.path}
        elif args.command=='import': result=asdict(ActivityExchange(engine.store).import_file(args.path,args.replace))
        elif args.command=='workspaces':
            from capsule.interfaces.dbus.client import ShellClient
            result=ShellClient().list_workspaces()
        elif args.command=='plan':
            from capsule.interfaces.dbus.client import ShellClient
            from capsule.interfaces.api import CapsuleAPI
            result=CapsuleAPI(engine).plan(args.id,ShellClient().list_windows())
        else:
            from capsule.interfaces.dbus.client import ShellClient
            result=asdict(RestoreEngine(ShellClient()).restore(engine.inspect(args.id),dry_run=not args.apply))
        print(json.dumps(result,indent=2,ensure_ascii=False)); return 0
    except (ValueError,KeyError,FileNotFoundError,FileExistsError,RuntimeError,ImportError,OSError,TypeError) as exc:
        print(json.dumps({'error':str(exc),'type':type(exc).__name__}),file=sys.stderr); return 1
if __name__=='__main__': sys.exit(main())

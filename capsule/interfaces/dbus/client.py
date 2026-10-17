"""GNOME Shell session-bus adapter; requires python3-gi and enabled extension."""
import json
BUS='org.rebuntu.Capsule'; PATH='/org/rebuntu/Capsule'; IFACE=BUS
class ShellClient:
    def __init__(self):
        from gi.repository import Gio
        self.proxy=Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION,Gio.DBusProxyFlags.NONE,None,BUS,PATH,IFACE,None)
        if not self.proxy.get_name_owner(): raise RuntimeError('Capsule GNOME Shell extension is not running')
    def _call(self,method,argument=None):
        from gi.repository import GLib,Gio
        args=None if argument is None else GLib.Variant('(s)',(argument,))
        return self.proxy.call_sync(method,args,Gio.DBusCallFlags.NONE,5000,None).unpack()[0]
    def list_windows(self):
        from capsule.core.models import Window
        return [Window(**w) for w in json.loads(self._call('ListWindows'))]
    def list_workspaces(self): return json.loads(self._call('ListWorkspaces'))
    def activate_workspace(self,index): return bool(self._call('ActivateWorkspace',str(index)))
    def ensure_workspaces(self,count): return bool(self._call('EnsureWorkspaces',str(count)))
    def apply(self,current,desired):
        token=current.geometry.get('capsule_token')
        if not isinstance(token,int): return False
        payload={'token':token,'workspace':desired.workspace,'geometry':{k:v for k,v in desired.geometry.items() if k in ('x','y','width','height')}}
        return bool(self._call('ApplyWindow',json.dumps(payload)))

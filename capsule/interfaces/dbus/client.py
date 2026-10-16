"""Session bus client for the GNOME Shell Capsule extension. Requires gi/Gio."""
import json
BUS='org.rebuntu.Capsule'
PATH='/org/rebuntu/Capsule'
IFACE='org.rebuntu.Capsule'
class ShellClient:
    def __init__(self):
        from gi.repository import Gio
        self.proxy=Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION,Gio.DBusProxyFlags.NONE,None,BUS,PATH,IFACE,None)
    def _call(self,method,argument=None):
        from gi.repository import GLib,Gio
        args=None if argument is None else GLib.Variant('(s)',(argument,))
        result=self.proxy.call_sync(method,args,Gio.DBusCallFlags.NONE,5000,None)
        return result.unpack()[0]
    def list_windows(self):
        from capsule.core.models import Window
        return [Window(**w) for w in json.loads(self._call('ListWindows'))]
    def apply(self,current,desired):
        # The Shell adapter identifies windows by stable-in-session token in geometry metadata.
        token=current.geometry.get('capsule_token')
        if token is None: return False
        payload={'token':token,'workspace':desired.workspace,'geometry':desired.geometry}
        return bool(self._call('ApplyWindow',json.dumps(payload)))

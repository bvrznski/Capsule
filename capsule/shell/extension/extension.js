// GNOME Shell 45+ ESM extension; runs in the user's Shell session.
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Shell from 'gi://Shell';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const XML = `<node><interface name="org.rebuntu.Capsule">
<method name="ListWindows"><arg type="s" direction="out"/></method>
<method name="ListWorkspaces"><arg type="s" direction="out"/></method>
<method name="ActivateWorkspace"><arg type="s" direction="in"/><arg type="b" direction="out"/></method>
<method name="EnsureWorkspaces"><arg type="s" direction="in"/><arg type="b" direction="out"/></method>
<method name="ApplyWindow"><arg type="s" direction="in"/><arg type="b" direction="out"/></method>
</interface></node>`;

function windows() {
    return global.get_window_actors().map(a => a.meta_window)
        .filter(w => w && !w.is_override_redirect());
}
function describe(w) {
    const r = w.get_frame_rect();
    const app = Shell.WindowTracker.get_default().get_window_app(w);
    return {app_id: app?.get_id() || w.get_wm_class() || '',
        title: w.get_title() || '', workspace: String(w.get_workspace()?.index() ?? 0),
        monitor: String(w.get_monitor()),
        geometry: {x:r.x,y:r.y,width:r.width,height:r.height,capsule_token:w.get_id()},
        role: w.get_role() || ''};
}
export default class CapsuleExtension extends Extension {
    enable() {
        const service = {
            ListWindows() { return JSON.stringify(windows().map(describe)); },
            ListWorkspaces() {
                const wm=global.workspace_manager;
                return JSON.stringify(Array.from({length:wm.n_workspaces},(_,i)=>({index:i,name:wm.get_workspace_by_index(i)?.get_name()||''})));
            },
            ActivateWorkspace(raw) {
                const i=Number(raw), wm=global.workspace_manager;
                if (!Number.isInteger(i)||i<0||i>=wm.n_workspaces) return false;
                wm.get_workspace_by_index(i).activate(global.get_current_time()); return true;
            },
            EnsureWorkspaces(raw) {
                const n=Number(raw), wm=global.workspace_manager;
                // Do not alter dynamic-workspaces policy or remove user workspaces.
                if (!Number.isInteger(n)||n<1||n>64) return false;
                while (wm.n_workspaces<n) wm.append_new_workspace(false,global.get_current_time());
                return wm.n_workspaces>=n;
            },
            ApplyWindow(raw) {
                try {
                    const p = JSON.parse(raw);
                    if (!Number.isInteger(p.token)) return false;
                    const w = windows().find(w => w.get_id() === p.token);
                    if (!w) return false;
                    if (p.workspace !== undefined) {
                        const index = Number(p.workspace);
                        if (!Number.isInteger(index) || index < 0 || index >= global.workspace_manager.n_workspaces)
                            return false;
                        w.change_workspace_by_index(index, false);
                    }
                    const g = p.geometry || {};
                    if (['x','y','width','height'].every(k => Number.isInteger(g[k])) &&
                        g.width > 0 && g.height > 0 && g.width <= 16384 && g.height <= 16384)
                        w.move_resize_frame(true, g.x, g.y, g.width, g.height);
                    return true;
                } catch (e) { console.error(`Capsule ApplyWindow: ${e}`); return false; }
            },
        };
        this._object = Gio.DBusExportedObject.wrapJSObject(XML, service);
        this._object.export(Gio.DBus.session, '/org/rebuntu/Capsule');
        this._owner = Gio.bus_own_name(Gio.BusType.SESSION, 'org.rebuntu.Capsule',
            Gio.BusNameOwnerFlags.NONE, null, null, null);
    }
    disable() {
        this._object?.unexport(); this._object = null;
        if (this._owner) Gio.bus_unown_name(this._owner);
        this._owner = 0;
    }
}

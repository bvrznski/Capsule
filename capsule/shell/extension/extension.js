/* GNOME Shell 42-44 legacy extension API. Newer GNOME releases need ESM port. */
const { Gio, GLib, Meta } = imports.gi;
const Main = imports.ui.main;
const ExtensionUtils = imports.misc.extensionUtils;
const XML = `<node><interface name="org.rebuntu.Capsule">
<method name="ListWindows"><arg type="s" direction="out"/></method>
<method name="ApplyWindow"><arg type="s" direction="in"/><arg type="b" direction="out"/></method>
</interface></node>`;
let exported = null, owner = 0;
function windows() {
    return global.get_window_actors().map(a => a.meta_window).filter(w => w && !w.is_override_redirect());
}
function enable() {
    let obj = {
        ListWindows() {
            return JSON.stringify(windows().map(w => {
                let r = w.get_frame_rect();
                return {app_id: w.get_wm_class() || '', title: w.get_title() || '',
                    workspace: String(w.get_workspace()?.index() ?? 0), monitor: String(w.get_monitor()),
                    geometry: {x:r.x,y:r.y,width:r.width,height:r.height,capsule_token:w.get_id()},role:w.get_role() || ''};
            }));
        },
        ApplyWindow(raw) {
            try {
                let p=JSON.parse(raw), w=windows().find(w => w.get_id() === p.token);
                if (!w) return false;
                if (p.workspace !== undefined) {
                    let index=Number(p.workspace);
                    if (Number.isInteger(index) && index >= 0 && index < global.workspace_manager.n_workspaces)
                        w.change_workspace_by_index(index,false);
                }
                let g=p.geometry || {};
                if ([g.x,g.y,g.width,g.height].every(Number.isInteger) && g.width>0 && g.height>0)
                    w.move_resize_frame(true,g.x,g.y,g.width,g.height);
                return true;
            } catch(e) { logError(e); return false; }
        }
    };
    exported=Gio.DBusExportedObject.wrapJSObject(XML,obj);
    exported.export(Gio.DBus.session,'/org/rebuntu/Capsule');
    owner=Gio.bus_own_name(Gio.BusType.SESSION,'org.rebuntu.Capsule',Gio.BusNameOwnerFlags.NONE,null,null,null);
}
function disable() {
    if (exported) { exported.unexport(); exported=null; }
    if (owner) { Gio.bus_unown_name(owner); owner=0; }
}

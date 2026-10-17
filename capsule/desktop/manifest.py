from dataclasses import dataclass,field

@dataclass(frozen=True)
class DesktopIntegration:
    shell_extension_uuid: str='capsule@rebuntu'
    desktop_id: str='org.rebuntu.Capsule'
    dbus_name: str='org.rebuntu.Capsule'
    supports_wayland: bool=True
    features: tuple[str,...]=('activities','snapshots','layouts','restore','reactive-rules')

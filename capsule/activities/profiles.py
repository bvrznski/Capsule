"""Composable, validated activity presets without executable user content."""
from dataclasses import dataclass, field
from capsule.core.models import Activity

@dataclass(frozen=True)
class Profile:
    name: str
    layout: str = 'grid'
    workspace: str = ''
    preferred_monitor: str = ''
    metadata: dict[str, str] = field(default_factory=dict)
    def __post_init__(self):
        if not self.name.strip() or self.layout not in {'grid','stack','master-stack'}:
            raise ValueError('invalid profile')

def apply_profile(activity: Activity, profile: Profile) -> Activity:
    from copy import deepcopy
    clone=deepcopy(activity)
    clone.metadata={**clone.metadata,'profile':profile.name,'layout':profile.layout,**profile.metadata}
    for window in clone.windows:
        if profile.workspace: window.workspace=profile.workspace
        if profile.preferred_monitor: window.monitor=profile.preferred_monitor
    return clone

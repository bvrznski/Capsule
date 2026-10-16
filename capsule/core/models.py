from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass
class Window:
    app_id: str
    title: str = ''
    workspace: str = ''
    monitor: str = ''
    geometry: dict[str, int] = field(default_factory=dict)
    role: str = ''

@dataclass
class Activity:
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))
    windows: list[Window] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

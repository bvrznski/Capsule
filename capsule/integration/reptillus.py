from pathlib import Path
from urllib.parse import quote

class ReptillusBridge:
    """Generates standard file:// URIs; no private Nautilus/Reptillus ABI dependency."""
    @staticmethod
    def location_uri(path): return Path(path).expanduser().resolve().as_uri()
    @staticmethod
    def location_metadata(path):
        p=Path(path).expanduser().resolve()
        return {'uri':p.as_uri(),'exists':p.exists(),'is_directory':p.is_dir()}

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Environment:
    path: Path
    python_path: Path
    python_version: str

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Conflict:
    """
    Represents a dependency version conflict between environments.
    """

    package: str
    versions_by_env: Dict[str, str]
    selected_version: str
    strategy: str
    conflict_type: str = "VERSION_CONFLICT"
    warnings: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "package": self.package,
            "versions": self.versions_by_env,
            "selected": self.selected_version,
            "strategy": self.strategy,
            "type": self.conflict_type,
            "warnings": self.warnings,
        }

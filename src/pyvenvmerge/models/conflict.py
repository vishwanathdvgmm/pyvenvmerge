from dataclasses import dataclass, field
from typing import Any

@dataclass
class Conflict:
    """
    Represents a dependency conflict
    discovered during planning.
    """
    package: str
    versions_by_env: dict[str, str]
    selected_version: str
    strategy: str
    conflict_type: str = "VERSION_CONFLICT"
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "package": self.package,
            "versions": self.versions_by_env,
            "selected": self.selected_version,
            "strategy": self.strategy,
            "type": self.conflict_type,
            "warnings": self.warnings,
        }
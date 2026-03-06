from dataclasses import dataclass

@dataclass
class Conflict:
    """
    Represents a dependency version conflict between environments.
    """

    package: str
    versions_by_env: dict[str, str]
    selected_version: str
    strategy: str

    def to_dict(self):
        return {
            "package": self.package,
            "versions": self.versions_by_env,
            "selected": self.selected_version,
            "strategy": self.strategy,
        }
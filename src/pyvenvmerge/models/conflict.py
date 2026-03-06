from dataclasses import dataclass

@dataclass
class Conflict:
    """
    Represents a dependency version conflict between environments.
    """

    package: str
    versions_by_env: dict[str, str]
    selected_version: str | None
    strategy: str
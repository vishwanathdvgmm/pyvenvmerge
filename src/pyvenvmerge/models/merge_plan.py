from dataclasses import dataclass, field
from pathlib import Path
from pyvenvmerge.models.environment import Environment
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.models.conflict import Conflict

@dataclass
class MergePlan:
    """
    Represents the full merge decision before execution.
    """

    environments: list[Environment]
    python_version: str
    merged_requirements: dict[str, Requirement]
    conflicts: list[Conflict] = field(default_factory=list)
    strategy: str = "highest"

    def to_dict(self):
        return {
            "python_version": self.python_version,
            "strategy": self.strategy,
            "environments": [str(env.path) for env in self.environments],
            "conflicts": [c.to_dict() for c in self.conflicts],
            "packages": [
                req.raw_line for req in self.merged_requirements.values()
            ],
        }
from dataclasses import dataclass, field

from pyvenvmerge.models.conflict import Conflict
from pyvenvmerge.models.environment import Environment
from pyvenvmerge.models.requirement import Requirement

@dataclass
class MergePlan:
    """
    Represents the full merge decision model
    before environment execution.
    """
    environments: list[Environment]
    python_version: str
    merged_requirements: dict[str, Requirement]

    conflicts: list[Conflict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    compatibility_score: int = 100
    risk_level: str = "LOW"

    strategy: str = "highest"

    def to_dict(self):
        return {
            "python_version": self.python_version,
            "strategy": self.strategy,
            "compatibility_score": self.compatibility_score,
            "risk_level": self.risk_level,
            "environments": [
                str(env.path)
                for env in self.environments
            ],
            "conflicts": [
                conflict.to_dict()
                for conflict in self.conflicts
            ],
            "warnings": self.warnings,
            "packages": [
                req.raw_line
                for req in self.merged_requirements.values()
            ],
        }
from dataclasses import dataclass, field
from datetime import datetime, timezone
from platform import platform
from typing import Any

from pyvenvmerge.models.merge_plan import MergePlan

@dataclass
class MergeReport:
    """
    Serializable merge report artifact.

    Used for:

    - JSON exports
    - Audit persistence
    - CI reporting
    - Reproducible diagnostics
    - Future lockfile generation
    """
    created_at: str
    platform_info: str
    python_version: str
    strategy: str
    compatibility_score: int
    risk_level: str
    environments: list[str]
    conflicts: list[dict[str, Any]] = field(
        default_factory=list
    )
    warnings: list[str] = field(
        default_factory=list
    )
    packages: list[str] = field(
        default_factory=list
    )

    @classmethod
    def from_merge_plan(
        cls,
        plan: MergePlan,
    ):
        return cls(
            created_at=(
                datetime.now(timezone.utc)
                .replace(tzinfo=None)
                .isoformat()
                + "Z"
            ),
            platform_info=platform(),
            python_version=plan.python_version,
            strategy=plan.strategy,
            compatibility_score=(
                plan.compatibility_score
            ),
            risk_level=plan.risk_level,
            environments=[
                str(env.path)
                for env in plan.environments
            ],
            conflicts=[
                conflict.to_dict()
                for conflict in plan.conflicts
            ],
            warnings=plan.warnings,
            packages=[
                req.raw_line
                for req
                in plan.merged_requirements.values()
            ],
        )

    def to_dict(self):
        return {
            "created_at": self.created_at,
            "platform": self.platform_info,
            "python_version": self.python_version,
            "strategy": self.strategy,
            "compatibility_score": (
                self.compatibility_score
            ),
            "risk_level": self.risk_level,
            "environments": self.environments,
            "conflicts": self.conflicts,
            "warnings": self.warnings,
            "packages": self.packages,
        }
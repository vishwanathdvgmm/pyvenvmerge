import json
from pathlib import Path

from pyvenvmerge.models.merge_report import MergeReport
from pyvenvmerge.models.merge_plan import MergePlan

def generate_report(plan: MergePlan) -> MergeReport:
    """
    Convert MergePlan into serializable MergeReport.
    """

    return MergeReport.from_merge_plan(plan)

def save_json_report(report: MergeReport, output_file: str):
    """
    Persist report as JSON file.
    """

    path = Path(output_file)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2)

def save_lockfile(plan: MergePlan, output_file: str):
    """
    Persist deterministic lockfile snapshot.
    """

    lock_data = {
        "python_version": plan.python_version,
        "strategy": plan.strategy,
        "compatibility_score": plan.compatibility_score,
        "risk_level": plan.risk_level,
        "packages": [
            req.raw_line
            for req in plan.merged_requirements.values()
        ],
    }

    path = Path(output_file)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2)
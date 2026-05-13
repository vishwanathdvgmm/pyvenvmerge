import json

from pyvenvmerge.models.merge_plan import MergePlan

def generate_console_report(
    plan: MergePlan,
) -> str:
    """
    Generate human-readable dry-run report.
    """
    lines = []

    lines.append("\nDry Run Summary")
    lines.append("----------------")
    lines.append(
        f"Python version: {plan.python_version}"
    )
    lines.append(
        "Compatibility Score: "
        f"{plan.compatibility_score}/100"
    )
    lines.append(
        f"Risk Level: {plan.risk_level}"
    )

    if plan.conflicts:
        lines.append("\nConflicts detected:")
        lines.append("-----------------")
        for conflict in plan.conflicts:
            lines.append(
                f"{conflict.package} "
                f"({conflict.conflict_type})"
            )
            for env_name, version in (
                conflict.versions_by_env.items()
            ):
                lines.append(
                    f"  {env_name} → {version}"
                )
            lines.append(
                f"  selected → "
                f"{conflict.selected_version}"
            )
            lines.append(
                f"  strategy → "
                f"{conflict.strategy}"
            )
            if conflict.warnings:
                for warning in conflict.warnings:
                    lines.append(
                        f"  ⚠ {warning}"
                    )
            lines.append("")

    if plan.warnings:
        lines.append("\nWarnings:")
        lines.append("---------")
        for warning in plan.warnings:
            lines.append(
                f"⚠ {warning}"
            )

    lines.append("\nPackages to install:")
    lines.append("----------------")

    for requirement in (
        plan.merged_requirements.values()
    ):
        lines.append(
            f"  {requirement.raw_line}"
        )
    lines.append("\nNo environment created.")
    return "\n".join(lines)

def generate_json_report(
    plan: MergePlan,
) -> str:
    """
    Generate structured JSON dry-run report.
    """
    return json.dumps(
        plan.to_dict(),
        indent=2,
    )
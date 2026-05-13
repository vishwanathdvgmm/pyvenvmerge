import argparse
import json
import sys

from pyvenvmerge.core.planner import create_merge_plan
from pyvenvmerge.core.report_generator import (
    generate_console_report,
    generate_json_report,
)
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.merge_report import MergeReport
from pyvenvmerge.orchestrator import merge_environments

def save_json_report(
    report: MergeReport,
    output_path: str,
):
    """
    Save structured merge report to JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            report.to_dict(),
            file,
            indent=2,
        )

def save_lockfile(
    plan,
    output_path: str,
):
    """
    Export deterministic lockfile.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        for req in plan.merged_requirements.values():
            file.write(req.raw_line + "\n")

def main():
    parser = argparse.ArgumentParser(
        prog="pyvenvmerge",
        description=(
            "Safely merge multiple "
            "Python virtual environments."
        ),
    )
    parser.add_argument(
        "envs",
        nargs="+",
        help="Paths to virtual environments to merge",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path for merged environment",
    )
    parser.add_argument(
        "--strategy",
        choices=[
            "highest",
            "strict",
            "unpinned",
        ],
        default="highest",
        help="Conflict resolution strategy",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Show merge plan without "
            "creating environment"
        ),
    )
    parser.add_argument(
        "--report",
        choices=[
            "console",
            "json",
        ],
        default="console",
        help="Output format for dry-run reports",
    )
    parser.add_argument(
        "--save-report",
        help="Save merge report to JSON file",
    )
    parser.add_argument(
        "--export-lock",
        help="Export deterministic lockfile",
    )

    args = parser.parse_args()

    try:
        if args.dry_run:
            plan = create_merge_plan(
                args.envs,
                args.strategy,
            )
            report = MergeReport.from_merge_plan(
                plan
            )
            if args.save_report:
                save_json_report(
                    report,
                    args.save_report,
                )
            if args.export_lock:
                save_lockfile(
                    plan,
                    args.export_lock,
                )
            if args.report == "json":
                print(
                    generate_json_report(plan)
                )
                return
            print(
                generate_console_report(plan)
            )
            return
        if not args.output:
            raise PyvenvmergeError(
                "Output path required "
                "unless using --dry-run"
            )
        result = merge_environments(
            args.envs,
            args.output,
            strategy=args.strategy,
        )
        print(
            "\nMerge successful. "
            f"New environment created at: "
            f"{result}"
        )
    except PyvenvmergeError as error:
        print(f"\nERROR: {error}")
        sys.exit(1)
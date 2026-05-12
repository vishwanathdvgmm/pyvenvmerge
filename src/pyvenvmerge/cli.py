import argparse
import sys

from pyvenvmerge.orchestrator import merge_environments
from pyvenvmerge.core.planner import create_merge_plan
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.core.reporting import (
    generate_report,
    save_json_report,
    save_lockfile,
)

def main():
    parser = argparse.ArgumentParser(
        prog="pyvenvmerge",
        description="Safely merge multiple Python virtual environments."
    )

    parser.add_argument(
        "envs",
        nargs="+",
        help="Paths to virtual environments to merge"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output path for merged environment"
    )

    parser.add_argument(
        "--strategy",
        choices=["highest", "strict", "unpinned"],
        default="highest",
        help="Conflict resolution strategy"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show merge plan without creating environment"
    )

    parser.add_argument(
        "--report",
        choices=["console", "json"],
        default="console",
        help="Output format for dry-run reports"
    )

    parser.add_argument(
        "--save-report",
        help="Save merge report to JSON file"
    )

    parser.add_argument(
        "--export-lock",
        help="Export deterministic lockfile"
    )

    args = parser.parse_args()

    try:
        if args.dry_run:
            plan = create_merge_plan(args.envs, args.strategy)
            report = generate_report(plan)

            if args.save_report:
                save_json_report(report, args.save_report)

            if args.export_lock:
                save_lockfile(plan, args.export_lock)

            if args.report == "json":
                import json
                print(json.dumps(plan.to_dict(), indent=2))
                return

            print("\nDry Run Summary")
            print("----------------")
            print(f"Python version: {plan.python_version}")
            print(f"Compatibility Score: {plan.compatibility_score}/100")
            print(f"Risk Level: {plan.risk_level}")

            if plan.conflicts:
                print("\nConflicts detected:")
                print("-----------------")
                for conflict in plan.conflicts:
                    print(f"{conflict.package} ({conflict.conflict_type})")

                    for env_name, version in conflict.versions_by_env.items():
                        print(f"  {env_name} → {version}")

                    print(f"  selected → {conflict.selected_version}")
                    print(f"  strategy → {conflict.strategy}")

                    if conflict.warnings:
                        for w in conflict.warnings:
                            print(f"  ⚠ {w}")
                    print()

            if plan.warnings:
                print("\nWarnings:")
                print("---------")
                for w in plan.warnings:
                    print(f"⚠ {w}")

            print("\nPackages to install:")
            print("----------------")

            for req in plan.merged_requirements.values():
                print(f"  {req.raw_line}")

            print("\nNo environment created.")
            return
        
        if not args.output:
            raise PyvenvmergeError("Output path required unless using --dry-run")

        result = merge_environments(
            args.envs,
            args.output,
            strategy=args.strategy
        )

        print(f"\nMerge successful. New environment created at: {result}")

    except PyvenvmergeError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

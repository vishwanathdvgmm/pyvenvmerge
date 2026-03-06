import argparse
import sys

from pyvenvmerge.orchestrator import merge_environments
from pyvenvmerge.core.planner import create_merge_plan
from pyvenvmerge.infra.exceptions import PyvenvmergeError

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

    args = parser.parse_args()

    try:
        if args.dry_run:
            plan = create_merge_plan(args.envs, args.strategy)

            if args.report == "json":
                import json
                print(json.dumps(plan.to_dict(), indent=2))
                return

            print("\nDry Run Summary")
            print("----------------")
            print(f"Python version: {plan.python_version}")
            if plan.conflicts:
                print("\nConflicts detected:")
                print("-----------------")
                for conflict in plan.conflicts:
                    print(conflict.package)

                    for env_name, version in conflict.versions_by_env.items():
                        print(f"  {env_name} → {version}")
                    
                    print(f"  selected → {conflict.selected_version}")
                    print(f"  strategy → {conflict.strategy}\n")
            
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

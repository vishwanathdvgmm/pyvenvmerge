import argparse
import sys

from pyvenvmerge.orchestrator import merge_environments
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
        required=True,
        help="Output path for merged environment"
    )

    parser.add_argument(
        "--strategy",
        choices=["highest", "strict", "unpinned"],
        default="highest",
        help="Conflict resolution strategy"
    )

    args = parser.parse_args()

    try:
        result = merge_environments(args.envs, args.output, strategy=args.strategy)
        print(f"\nMerge successful. New environment created at: {result}")

    except PyvenvmergeError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

# if __name__ == "__main__":
#     main()
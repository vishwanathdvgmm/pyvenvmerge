import argparse

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
        help="Path to output virtual environment"
    )

    parser.add_argument(
        "--strategy",
        choices=["highest", "strict", "unpinned"],
        default="highest",
        help="Conflict resolution strategy"
    )

    args = parser.parse_args()

    print("Input environments:", args.envs)
    print("Output:", args.output)
    print("Strategy:", args.strategy)

if __name__ == "__main__":
    main()
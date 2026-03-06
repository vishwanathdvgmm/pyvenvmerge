from pathlib import Path
from pyvenvmerge.infra.subprocess_runner import run
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.core.validator import validate_environment
from pyvenvmerge.models.merge_plan import MergePlan

def execute_plan(plan: MergePlan, output_path: str):
    """
    Executes a MergePlan by creating a new environment
    and installing merged dependencies.
    """

    output_dir = Path(output_path)

    if output_dir.exists():
        raise PyvenvmergeError(
            f"Output path already exists: {output_path}"
        )

    # Create venv
    run(["python", "-m", "venv", output_path])

    # Detect python inside new venv
    windows_python = output_dir / "Scripts" / "python.exe"
    unix_python = output_dir / "bin" / "python"

    if windows_python.exists():
        python_path = windows_python
    elif unix_python.exists():
        python_path = unix_python
    else:
        raise PyvenvmergeError("Failed to locate Python in new environment.")

    # Upgrade base tools
    run([
        str(python_path),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        "setuptools",
        "wheel",
    ])

    # Write requirements file
    temp_file = output_dir / "merged_requirements.txt"

    with open(temp_file, "w", encoding="utf-8") as f:
        for req in plan.merged_requirements.values():
            f.write(req.raw_line + "\n")

    # Install dependencies
    run([str(python_path), "-m", "pip", "install", "-r", str(temp_file)])

    temp_file.unlink()

    # Validate environment
    validate_environment(python_path)

    return python_path
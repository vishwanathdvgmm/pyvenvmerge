from pathlib import Path
from pyvenvmerge.infra.subprocess_runner import run
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.requirement import Requirement

def build_environment(output_path: str, requirements: dict[str, Requirement]):
    """
    Creates a new virtual environment and installs merged requirements.
    """

    output_dir = Path(output_path)

    if output_dir.exists():
        raise PyvenvmergeError(
            f"Output path already exists: {output_path}"
        )

    # 1️⃣ Create venv
    run(["python", "-m", "venv", output_path])

    # 2️⃣ Detect python inside new venv (cross-platform)
    windows_python = output_dir / "Scripts" / "python.exe"
    unix_python = output_dir / "bin" / "python"

    if windows_python.exists():
        python_path = windows_python
    elif unix_python.exists():
        python_path = unix_python
    else:
        raise PyvenvmergeError("Failed to locate Python in new environment.")

    # 3️⃣ Upgrade base tools
    run([str(python_path), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # 4️⃣ Write temporary requirements file
    temp_file = output_dir / "merged_requirements.txt"

    with open(temp_file, "w", encoding="utf-8") as f:
        for req in requirements.values():
            f.write(req.raw_line + "\n")

    # 5️⃣ Install dependencies
    run([str(python_path), "-m", "pip", "install", "-r", str(temp_file)])

    # 6️⃣ Cleanup temp file
    temp_file.unlink()

    return python_path

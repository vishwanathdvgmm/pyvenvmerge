from pathlib import Path
from pyvenvmerge.models.environment import Environment
from pyvenvmerge.infra.subprocess_runner import run
from pyvenvmerge.infra.exceptions import PyvenvmergeError

def inspect_environment(path: str) -> Environment:
    env_path = Path(path)

    if not env_path.exists():
        raise PyvenvmergeError(f"Environment path does not exist: {path}")

    if not (env_path / "pyvenv.cfg").exists():
        raise PyvenvmergeError(f"Invalid virtual environment (missing pyvenv.cfg): {path}")

    # Cross-platform python detection
    python_path = None

    windows_python = env_path / "Scripts" / "python.exe"
    unix_python = env_path / "bin" / "python"

    if windows_python.exists():
        python_path = windows_python
    elif unix_python.exists():
        python_path = unix_python
    else:
        raise PyvenvmergeError(f"Python executable not found in: {path}")

    version_output = run([str(python_path), "--version"])

    # Expected format: "Python 3.x.x"
    try:
        if not version_output:
            raise PyvenvmergeError("Failed to retrieve Python version.")
        parts = version_output.split()
        if len(parts) < 2:
            raise PyvenvmergeError(f"Unexpected version output: {version_output}")
        python_version = parts[1]
    except IndexError:
        raise PyvenvmergeError(f"Unable to parse Python version from: {version_output}")

    return Environment(
        path=env_path,
        python_path=python_path,
        python_version=python_version,
    )

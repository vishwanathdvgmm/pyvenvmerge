from pathlib import Path
from pyvenvmerge.infra.subprocess_runner import run
from pyvenvmerge.infra.exceptions import PyvenvmergeError

def validate_environment(python_path: Path):
    """
    Runs pip check on the newly built environment.
    Raises error if dependency issues exist.
    """

    try:
        run([str(python_path), "-m", "pip", "check"])
    except Exception as e:
        raise PyvenvmergeError(
            f"Dependency validation failed:\n{e.stderr}"
        )

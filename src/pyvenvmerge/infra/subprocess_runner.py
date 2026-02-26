import subprocess
from pyvenvmerge.infra.exceptions import SubprocessExecutionError

def run(command: list[str]) -> str:
    """
    Executes a subprocess command and returns stdout.
    Raises SubprocessExecutionError on failure.
    """

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        error_output = result.stderr.strip() or result.stdout.strip()
        raise SubprocessExecutionError(command, error_output)
    
    return result.stdout.strip()
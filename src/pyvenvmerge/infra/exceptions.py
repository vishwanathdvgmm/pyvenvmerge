class PyvenvmergeError(Exception):
    """Base exception for pyvenvmerge."""
    pass

class SubprocessExecutionError(PyvenvmergeError):
    """Raised when subprocess execution fails."""

    def __init__(self, command, stderr):
        self.command = command
        self.stderr = stderr
        super().__init__(stderr)

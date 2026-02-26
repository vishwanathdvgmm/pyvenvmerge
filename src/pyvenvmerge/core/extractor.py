from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.infra.subprocess_runner import run
from pyvenvmerge.infra.exceptions import PyvenvmergeError

def extract_requirements(environment) -> dict[str, Requirement]:
    """
    Extracts pip freeze output from a virtual environment.
    Returns dictionary keyed by lowercase package name.
    """

    output = run([str(environment.python_path), "-m", "pip", "freeze"])

    requirements: dict[str, Requirement] = {}

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        # Only handle standard format: package==version
        if "==" in line:
            name, version = line.split("==", 1)

            normalized_name = name.lower()

            requirements[normalized_name] = Requirement(
                name=name,
                version=version,
                raw_line=line
            )
        else:
            # Ignore complex lines for v0.1 (editable, git, file installs)
            continue

    return requirements

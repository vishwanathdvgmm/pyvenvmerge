from packaging.requirements import Requirement as PackagingRequirement
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.infra.subprocess_runner import run

def detect_source_type(line: str) -> str:
    line = line.strip()

    if line.startswith("-e"):
        return "editable"
    elif "git+" in line:
        return "git"
    elif " @ file://" in line:
        return "file"
    else:
        return "pypi"

def extract_requirements(environment) -> dict[str, Requirement]:
    """
    Extracts pip freeze output and parses into structured Requirement objects.
    """

    output = run([str(environment.python_path), "-m", "pip", "freeze"])

    requirements: dict[str, Requirement] = {}

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        source_type = detect_source_type(line)

        # Handle only PyPI packages for now
        
        if source_type == "pypi":

            try:
                parsed = PackagingRequirement(line)

                normalized_name = parsed.name.lower()

                requirements[normalized_name] = Requirement(
                    name=parsed.name,
                    specifier=parsed.specifier,
                    extras=set(parsed.extras),
                    marker=parsed.marker,
                    source_type="pypi",
                    raw_line=line,
                )
            
            except Exception:
                continue
        
        else:
            name = line.lower()

            requirements[name] = Requirement(
                name=line,
                specifier=None,
                extras=set(),
                marker=None,
                source_type=source_type,
                raw_line=line,
            )

    return requirements

from packaging.requirements import Requirement as PackagingRequirement
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.infra.subprocess_runner import run

def detect_source_type(line: str) -> str:
    line = line.strip()

    if line.startswith("-e"):
        return "editable"
    elif "git+" in line:
        return "git"
    elif " @ " in line:
        return "file"
    else:
        return "pypi"

def extract_name_from_line(line: str, source_type: str) -> str:
    """
    Extract a stable name for non-PyPI dependencies.
    """

    if source_type == "editable":
        return line.replace("-e", "").strip()

    if source_type == "git":
        if "#egg=" in line:
            return line.split("#egg=")[-1].lower()
        return line.lower()

    if source_type == "file":
        # format: package @ file://...
        return line.split("@")[0].strip().lower()

    return line.lower()

def extract_requirements(environment) -> dict[str, Requirement]:

    output = run([str(environment.python_path), "-m", "pip", "freeze"])

    requirements: dict[str, Requirement] = {}

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        source_type = detect_source_type(line)

        if source_type == "pypi":
            try:
                parsed = PackagingRequirement(line)

                name = parsed.name.lower()

                requirements[name] = Requirement(
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
            name = extract_name_from_line(line, source_type)

            requirements[name] = Requirement(
                name=name,
                specifier=None,
                extras=set(),
                marker=None,
                source_type=source_type,
                raw_line=line,
            )

    return requirements

from pyvenvmerge.core.inspector import inspect_environment
from pyvenvmerge.core.extractor import extract_requirements
from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.core.builder import build_environment
from pyvenvmerge.core.validator import validate_environment
from pyvenvmerge.infra.exceptions import PyvenvmergeError

def merge_environments(env_paths: list[str], output_path: str, strategy="highest"):
    """
    Full pipeline:
    Inspect → Extract → Merge → Build → Validate
    """

    if len(env_paths) < 1:
        raise PyvenvmergeError("At least one environment must be provided.")

    # 1️⃣ Inspect
    environments = [inspect_environment(p) for p in env_paths]

    # 2️⃣ Ensure same Python version
    versions = {env.python_version for env in environments}
    if len(versions) != 1:
        raise PyvenvmergeError(
            f"Python version mismatch across environments: {versions}"
        )

    # 3️⃣ Extract
    requirement_sets = [
        extract_requirements(env) for env in environments
    ]

    # 4️⃣ Merge
    merged_requirements = merge_requirements(requirement_sets, strategy_name=strategy)

    # 5️⃣ Build
    new_python_path = build_environment(output_path, merged_requirements)

    # 6️⃣ Validate
    validate_environment(new_python_path)

    return output_path

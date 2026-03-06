from pyvenvmerge.core.inspector import inspect_environment
from pyvenvmerge.core.extractor import extract_requirements
from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.merge_plan import MergePlan

def create_merge_plan(env_paths: list[str], strategy: str) -> MergePlan:
    """
    Creates a MergePlan describing how environments will be merged.
    No side effects occur here.
    """

    if len(env_paths) < 1:
        raise PyvenvmergeError("At least one environment must be provided.")

    # Inspect environments
    environments = [inspect_environment(p) for p in env_paths]

    # Ensure same Python version
    versions = {env.python_version for env in environments}
    if len(versions) != 1:
        raise PyvenvmergeError(
            f"Python version mismatch across environments: {versions}"
        )

    python_version = versions.pop()

    # Extract requirements
    requirement_sets = [
        extract_requirements(env) for env in environments
    ]

    # Merge requirements
    merged_requirements = merge_requirements(
        requirement_sets,
        strategy_name=strategy
    )

    return MergePlan(
        environments=environments,
        python_version=python_version,
        merged_requirements=merged_requirements,
        strategy=strategy
    )
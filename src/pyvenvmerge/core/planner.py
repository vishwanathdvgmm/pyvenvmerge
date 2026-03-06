from pyvenvmerge.core.inspector import inspect_environment
from pyvenvmerge.core.extractor import extract_requirements
from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.merge_plan import MergePlan
from pyvenvmerge.models.conflict import Conflict

def create_merge_plan(env_paths: list[str], strategy: str) -> MergePlan:
    """
    Creates a MergePlan describing how environments will be merged.
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

    # Detect conflicts before merge
    conflicts: list[Conflict] = {}

    version_map: dict[str, dict[str, str]] = {}

    for env, reqs in zip(environments, requirement_sets):
        env_name = env.path.name
        for name, req in reqs.items():
            version_map.setdefault(name, {})
            version_map[name][env_name] = req.version
    
    conflicts_list = []

    for package, versions_by_env in version_map.items():
        unique_versions = set(versions_by_env.values())
        if len(unique_versions) > 1:
            conflicts_list.append(
                Conflict(
                    package=package,
                    versions_by_env=versions_by_env,
                    selected_version="",
                    strategy=strategy,
                )
            )

    # Merge requirements
    merged_requirements = merge_requirements(
        requirement_sets,
        strategy_name=strategy
    )

    for conflict in conflicts_list:
        selected = merged_requirements[conflict.package].version
        conflict.selected_version = selected

    return MergePlan(
        environments=environments,
        python_version=python_version,
        merged_requirements=merged_requirements,
        conflicts=conflicts_list,
        strategy=strategy
    )

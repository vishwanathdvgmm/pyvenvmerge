from pyvenvmerge.core.inspector import inspect_environment
from pyvenvmerge.core.extractor import extract_requirements
from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.core.dependency_graph import build_dependency_graph
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.merge_plan import MergePlan
from pyvenvmerge.models.conflict import Conflict

from packaging.requirements import Requirement as PackagingRequirement

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
    conflicts: list[Conflict] = []

    version_map: dict[str, dict[str, str]] = {}

    for env, reqs in zip(environments, requirement_sets):
        env_name = env.path.name
        for name, req in reqs.items():
            version_map.setdefault(name, {})
            version_map[name][env_name] = str(req.specifier) if req.specifier else ""
    
    conflicts_list = []
    warnings = []

    for package, versions_by_env in version_map.items():
        unique_versions = set(versions_by_env.values())

        if len(unique_versions) > 1:

            # Detect type
            if "" in unique_versions:
                conflict_type = "PARTIAL_SPECIFIER"
            elif len(unique_versions) > 1:
                conflict_type = "VERSION_CONFLICT"
            else:
                conflict_type = "UNKNOWN"

            conflict = Conflict(
                package=package,
                versions_by_env=versions_by_env,
                selected_version="",
                strategy=strategy,
                conflict_type=conflict_type,
            )

            if conflict_type == "VERSION_CONFLICT":
                warnings.append(
                    f"{package}: multiple versions detected {unique_versions}"
                )

            conflicts_list.append(conflict)

    # Merge requirements
    merged_requirements = merge_requirements(
        requirement_sets,
        strategy_name=strategy
    )

    for conflict in conflicts_list:
        selected = str(merged_requirements[conflict.package].specifier) if merged_requirements[conflict.package].specifier else ""
        conflict.selected_version = selected

        if conflict.conflict_type == "VERSION_CONFLICT":
            conflict.warnings.append(
                f"Selected version {selected} based on '{strategy}' strategy"
            )
        
    dep_graph = build_dependency_graph()

    for pkg_name, req in merged_requirements.items():

        if pkg_name not in dep_graph:
            continue

        dependencies = dep_graph[pkg_name]

        for dep in dependencies:
            try:
                parsed = PackagingRequirement(dep)
            except Exception:
                continue

            dep_name = parsed.name.lower()

            if dep_name not in merged_requirements:
                continue

            selected_dep = merged_requirements[dep_name]

            if selected_dep.specifier and parsed.specifier:

                # naive check: does selected version satisfy constraint string?
                selected_str = str(selected_dep.specifier)

                if selected_str and str(parsed.specifier) not in selected_str:

                    warning_msg = (
                        f"{pkg_name} requires {dep}, "
                        f"but selected {dep_name}{selected_str}"
                    )

                    warnings.append(warning_msg)

    return MergePlan(
        environments=environments,
        python_version=python_version,
        merged_requirements=merged_requirements,
        conflicts=conflicts_list,
        warnings=warnings,
        strategy=strategy
    )

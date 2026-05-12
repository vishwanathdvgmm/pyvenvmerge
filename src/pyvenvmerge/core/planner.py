from pyvenvmerge.core.inspector import inspect_environment
from pyvenvmerge.core.extractor import extract_requirements
from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.core.dependency_graph import build_dependency_graph
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.merge_plan import MergePlan
from pyvenvmerge.models.conflict import Conflict

from packaging.requirements import Requirement as PackagingRequirement
from packaging.version import Version, InvalidVersion

def calculate_risk_level(score: int) -> str:
    if score >= 90:
        return "LOW"
    
    if score >=70:
        return "MEDIUM"
    
    return "HIGH"

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
                # Semantic dependency validation (v0.7)

                selected_spec = selected_dep.specifier

                if selected_spec and parsed.specifier:

                    try:
                        selected_spec_str = str(selected_spec)

                        # Extract exact selected version
                        selected_version = None

                        for token in selected_spec_str.split(","):
                            token = token.strip()

                            if token.startswith("=="):
                                selected_version = token.replace("==", "").strip()
                                break

                            elif token.startswith(">="):
                                selected_version = token.replace(">=", "").strip()

                        if selected_version:

                            version_obj = Version(selected_version)

                            if not parsed.specifier.contains(version_obj):

                                warning_msg = (
                                    f"{pkg_name} requires "
                                    f"{dep_name}{parsed.specifier}, "
                                    f"but selected version is "
                                    f"{selected_version}"
                                )

                                warnings.append(warning_msg)

                    except InvalidVersion:
                        continue

    # ----------------------------
    # Compatibility Scoring (v0.8)
    # ----------------------------

    compatibility_score = 100

    for conflict in conflicts_list:

        if conflict.conflict_type == "VERSION_CONFLICT":
            compatibility_score -= 10

        elif conflict.conflict_type == "PARTIAL_SPECIFIER":
            compatibility_score -= 5

    # Dependency warnings
    for w in warnings:
        if "requires" in w:
            compatibility_score -= 20

    # Non-PyPI dependency penalties
    for req in merged_requirements.values():

        if req.source_type != "pypi":
            compatibility_score -= 8

    # Clamp score
    compatibility_score = max(0, compatibility_score)

    risk_level = calculate_risk_level(compatibility_score)

    return MergePlan(
        environments=environments,
        python_version=python_version,
        merged_requirements=merged_requirements,
        conflicts=conflicts_list,
        warnings=warnings,
        compatibility_score=compatibility_score,
        risk_level=risk_level,
        strategy=strategy
    )

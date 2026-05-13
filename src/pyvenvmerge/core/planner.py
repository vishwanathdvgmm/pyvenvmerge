from packaging.requirements import Requirement as PackagingRequirement
from packaging.version import Version, InvalidVersion

from pyvenvmerge.core.dependency_graph import build_dependency_graph
from pyvenvmerge.core.extractor import extract_requirements
from pyvenvmerge.core.inspector import inspect_environment
from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.conflict import Conflict
from pyvenvmerge.models.merge_plan import MergePlan

def calculate_risk_level(score: int) -> str:
    if score >= 90:
        return "LOW"

    if score >= 70:
        return "MEDIUM"

    return "HIGH"

def _extract_selected_version(specifier) -> str | None:
    """
    Extract a representative version from a SpecifierSet.
    """

    if not specifier:
        return None

    spec_str = str(specifier)

    for token in spec_str.split(","):
        token = token.strip()

        if token.startswith("=="):
            return token.replace("==", "").strip()

        if token.startswith(">="):
            return token.replace(">=", "").strip()

    return None

def _analyze_conflicts(
    environments,
    requirement_sets,
    strategy: str,
) -> tuple[list[Conflict], list[str]]:
    """
    Build conflict list and warning list.
    """

    version_map: dict[str, dict[str, str]] = {}

    for env, reqs in zip(environments, requirement_sets):
        env_name = env.path.name

        for name, req in reqs.items():
            version_map.setdefault(name, {})
            version_map[name][env_name] = (
                str(req.specifier) if req.specifier else ""
            )

    conflicts: list[Conflict] = []
    warnings: list[str] = []

    for package, versions_by_env in version_map.items():
        unique_versions = set(versions_by_env.values())

        if len(unique_versions) <= 1:
            continue

        if "" in unique_versions:
            conflict_type = "PARTIAL_SPECIFIER"
        else:
            conflict_type = "VERSION_CONFLICT"

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

        conflicts.append(conflict)

    return conflicts, warnings

def _validate_dependencies(
    merged_requirements,
    warnings: list[str],
):
    """
    Perform semantic dependency validation.
    """

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

            if not selected_dep.specifier or not parsed.specifier:
                continue

            try:
                selected_version = _extract_selected_version(
                    selected_dep.specifier
                )

                if not selected_version:
                    continue

                version_obj = Version(selected_version)

                if not parsed.specifier.contains(version_obj):

                    warnings.append(
                        f"{pkg_name} requires "
                        f"{dep_name}{parsed.specifier}, "
                        f"but selected version is "
                        f"{selected_version}"
                    )

            except InvalidVersion:
                continue

def _calculate_compatibility_score(
    conflicts: list[Conflict],
    warnings: list[str],
    merged_requirements,
) -> tuple[int, str]:
    """
    Compute compatibility score and risk level.
    """

    compatibility_score = 100

    for conflict in conflicts:

        if conflict.conflict_type == "VERSION_CONFLICT":
            compatibility_score -= 10

        elif conflict.conflict_type == "PARTIAL_SPECIFIER":
            compatibility_score -= 5

    for warning in warnings:
        if "requires" in warning:
            compatibility_score -= 20

    for req in merged_requirements.values():
        if req.source_type != "pypi":
            compatibility_score -= 8

    compatibility_score = max(0, compatibility_score)

    risk_level = calculate_risk_level(compatibility_score)

    return compatibility_score, risk_level

def create_merge_plan(env_paths: list[str], strategy: str) -> MergePlan:
    """
    Creates a MergePlan describing how environments will be merged.
    """

    if len(env_paths) < 1:
        raise PyvenvmergeError(
            "At least one environment must be provided."
        )

    environments = [inspect_environment(p) for p in env_paths]

    versions = {env.python_version for env in environments}

    if len(versions) != 1:
        raise PyvenvmergeError(
            f"Python version mismatch across environments: {versions}"
        )

    python_version = versions.pop()

    requirement_sets = [
        extract_requirements(env)
        for env in environments
    ]

    conflicts, warnings = _analyze_conflicts(
        environments,
        requirement_sets,
        strategy,
    )

    merged_requirements = merge_requirements(
        requirement_sets,
        strategy_name=strategy,
    )

    for conflict in conflicts:
        selected = (
            str(merged_requirements[conflict.package].specifier)
            if merged_requirements[conflict.package].specifier
            else ""
        )

        conflict.selected_version = selected

        if conflict.conflict_type == "VERSION_CONFLICT":
            conflict.warnings.append(
                f"Selected version {selected} "
                f"based on '{strategy}' strategy"
            )

    _validate_dependencies(
        merged_requirements,
        warnings,
    )

    compatibility_score, risk_level = (
        _calculate_compatibility_score(
            conflicts,
            warnings,
            merged_requirements,
        )
    )

    return MergePlan(
        environments=environments,
        python_version=python_version,
        merged_requirements=merged_requirements,
        conflicts=conflicts,
        warnings=warnings,
        compatibility_score=compatibility_score,
        risk_level=risk_level,
        strategy=strategy,
    )
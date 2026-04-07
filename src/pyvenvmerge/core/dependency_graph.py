from importlib.metadata import distributions
from packaging.requirements import Requirement as PackagingRequirement


def build_dependency_graph():
    """
    Builds dependency graph using installed metadata.
    Returns:
        dict[str, list[str]]  → package → list of dependency requirement strings
    """

    graph = {}

    for dist in distributions():
        name = dist.metadata["Name"].lower()
        requires = dist.requires or []

        deps = []
        for r in requires:
            try:
                parsed = PackagingRequirement(r)
                deps.append(r)
            except Exception:
                continue

        graph[name] = deps

    return graph

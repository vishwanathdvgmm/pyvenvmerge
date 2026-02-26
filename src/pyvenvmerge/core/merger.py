from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.core.resolver import (
    HighestVersionStrategy,
    StrictStrategy,
    UnpinnedStrategy,
)
from pyvenvmerge.infra.exceptions import PyvenvmergeError

def get_strategy(name: str):
    if name == "highest":
        return HighestVersionStrategy()
    elif name == "strict":
        return StrictStrategy()
    elif name == "unpinned":
        return UnpinnedStrategy()
    else:
        raise PyvenvmergeError(f"Unknown strategy: {name}")

def merge_requirements(
    requirement_sets: list[dict[str, Requirement]],
    strategy_name: str = "highest"
) -> dict[str, Requirement]:

    strategy = get_strategy(strategy_name)

    merged: dict[str, Requirement] = {}

    for req_set in requirement_sets:
        for name, requirement in req_set.items():

            if name not in merged:
                merged[name] = requirement
                continue

            merged[name] = strategy.resolve(
                merged[name],
                requirement
            )

    return merged

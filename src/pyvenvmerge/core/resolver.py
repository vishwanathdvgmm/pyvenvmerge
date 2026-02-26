from packaging.version import Version
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.infra.exceptions import PyvenvmergeError

class ResolutionStrategy:
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        raise NotImplementedError

class HighestVersionStrategy(ResolutionStrategy):
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        if Version(incoming.version) > Version(existing.version):
            return incoming
        return existing

class StrictStrategy(ResolutionStrategy):
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        if existing.version != incoming.version:
            raise PyvenvmergeError(
                f"Version conflict for package '{existing.name}': "
                f"{existing.version} vs {incoming.version}"
            )
        return existing

class UnpinnedStrategy(ResolutionStrategy):
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        return Requirement(
            name=existing.name,
            version="",
            raw_line=existing.name
        )

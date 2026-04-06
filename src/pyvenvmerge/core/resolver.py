from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.core.specifier_merge import merge_specifiers

class ResolutionStrategy:
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        raise NotImplementedError

class HighestVersionStrategy(ResolutionStrategy):
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:

        try:
            merged_spec = merge_specifiers(existing.specifier, incoming.specifier)
        except PyvenvmergeError:
            from pyvenvmerge.core.specifier_merge import _extract_bounds
            
            l_exist, _ = _extract_bounds(existing.specifier) if existing.specifier else (None, None)
            l_inc, _ = _extract_bounds(incoming.specifier) if incoming.specifier else (None, None)
            
            if l_inc and l_exist and l_inc > l_exist:
                return incoming
            elif l_exist and l_inc and l_exist > l_inc:
                return existing
            return incoming

        return Requirement(
            name=existing.name,
            specifier=merged_spec,
            extras=existing.extras.union(incoming.extras),
            marker=existing.marker or incoming.marker,
            source_type="pypi",
            raw_line=self._build_raw_line(existing.name, merged_spec),
        )

    def _build_raw_line(self, name, spec):
        if spec:
            return f"{name}{spec}"
        return name

class StrictStrategy(ResolutionStrategy):
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        if str(existing.specifier) != str(incoming.specifier):
            raise PyvenvmergeError(
                f"Version conflict for package '{existing.name}': "
                f"{existing.specifier} vs {incoming.specifier}"
            )
        return existing

class UnpinnedStrategy(ResolutionStrategy):
    def resolve(self, existing: Requirement, incoming: Requirement) -> Requirement:
        return Requirement(
            name=existing.name,
            specifier=None,
            extras=set(),
            marker=None,
            source_type="pypi",
            raw_line=existing.name,
        )

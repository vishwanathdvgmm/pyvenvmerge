from pyvenvmerge.core.specifier_merge import (
    _extract_bounds,
    merge_specifiers,
)
from pyvenvmerge.infra.exceptions import PyvenvmergeError
from pyvenvmerge.models.requirement import Requirement

class ResolutionStrategy:
    def resolve(
        self,
        existing: Requirement,
        incoming: Requirement,
    ) -> Requirement:
        raise NotImplementedError

class HighestVersionStrategy(ResolutionStrategy):

    def resolve(
        self,
        existing: Requirement,
        incoming: Requirement,
    ) -> Requirement:

        if (
            existing.source_type != "pypi"
            or incoming.source_type != "pypi"
        ):
            return self._resolve_non_pypi(
                existing,
                incoming,
            )

        return self._resolve_pypi(
            existing,
            incoming,
        )

    def _resolve_non_pypi(
        self,
        existing: Requirement,
        incoming: Requirement,
    ) -> Requirement:

        if existing.raw_line != incoming.raw_line:
            raise PyvenvmergeError(
                f"Conflict for non-PyPI dependency "
                f"'{existing.name}':\n"
                f"{existing.raw_line} vs {incoming.raw_line}"
            )

        return existing

    def _resolve_pypi(
        self,
        existing: Requirement,
        incoming: Requirement,
    ) -> Requirement:

        try:
            merged_spec = merge_specifiers(
                existing.specifier,
                incoming.specifier,
            )

        except PyvenvmergeError:

            lower_existing, _ = (
                _extract_bounds(existing.specifier)
                if existing.specifier
                else (None, None)
            )

            lower_incoming, _ = (
                _extract_bounds(incoming.specifier)
                if incoming.specifier
                else (None, None)
            )

            if (
                lower_incoming
                and lower_existing
                and lower_incoming > lower_existing
            ):
                return incoming

            if (
                lower_existing
                and lower_incoming
                and lower_existing > lower_incoming
            ):
                return existing

            return incoming

        return Requirement(
            name=existing.name,
            specifier=merged_spec,
            extras=existing.extras.union(incoming.extras),
            marker=existing.marker or incoming.marker,
            source_type="pypi",
            raw_line=self._build_raw_line(
                existing.name,
                merged_spec,
            ),
        )

    def _build_raw_line(self, name, specifier):

        if specifier:
            return f"{name}{specifier}"

        return name

class StrictStrategy(ResolutionStrategy):

    def resolve(
        self,
        existing: Requirement,
        incoming: Requirement,
    ) -> Requirement:

        if str(existing.specifier) != str(incoming.specifier):
            raise PyvenvmergeError(
                f"Version conflict for package "
                f"'{existing.name}': "
                f"{existing.specifier} vs "
                f"{incoming.specifier}"
            )

        return existing

class UnpinnedStrategy(ResolutionStrategy):

    def resolve(
        self,
        existing: Requirement,
        incoming: Requirement,
    ) -> Requirement:

        return Requirement(
            name=existing.name,
            specifier=None,
            extras=set(),
            marker=None,
            source_type="pypi",
            raw_line=existing.name,
        )
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pyvenvmerge.infra.exceptions import PyvenvmergeError

def _extract_bounds(spec: SpecifierSet):
    """
    Extract lower and upper bounds from a SpecifierSet.
    Returns: (lower_bound, upper_bound)
    """

    lower = None
    upper = None

    for s in spec:
        op = s.operator
        v = Version(s.version)

        if op in (">=", ">"):
            if lower is None or v > lower:
                lower = v

        elif op in ("<", "<="):
            if upper is None or v < upper:
                upper = v

        elif op == "==":
            return v, v

    return lower, upper

def merge_specifiers(spec1: SpecifierSet | None, spec2: SpecifierSet | None) -> SpecifierSet | None:
    """
    Merge two SpecifierSets by intersection.
    """

    if spec1 is None:
        return spec2
    if spec2 is None:
        return spec1

    lower1, upper1 = _extract_bounds(spec1)
    lower2, upper2 = _extract_bounds(spec2)

    # Determine new bounds
    new_lower = max(filter(None, [lower1, lower2]), default=None)
    new_upper = min(filter(None, [upper1, upper2]), default=None)

    # Conflict detection
    if new_lower and new_upper and new_lower > new_upper:
        raise PyvenvmergeError(
            f"Incompatible specifiers: {spec1} vs {spec2}"
        )

    # Build new specifier string
    
    if new_lower and new_upper and new_lower == new_upper:
        return SpecifierSet(f"=={new_lower}")

    parts = []

    if new_lower:
        parts.append(f">={new_lower}")
    if new_upper:
        parts.append(f"<={new_upper}")

    if not parts:
        return None

    return SpecifierSet(",".join(parts))

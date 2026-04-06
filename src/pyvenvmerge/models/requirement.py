from dataclasses import dataclass
from typing import Optional, Set
from packaging.specifiers import SpecifierSet
from packaging.markers import Marker

@dataclass
class Requirement:
    """
    Represents a parsed dependency requirement.
    """

    name: str
    specifier: Optional[SpecifierSet]
    extras: Set[str]
    marker: Optional[Marker]
    source_type: str
    raw_line: str

from packaging.specifiers import SpecifierSet
import pytest
from pyvenvmerge.core.specifier_merge import merge_specifiers

def test_merge_lower_bounds():

    s1 = SpecifierSet(">=1.20")
    s2 = SpecifierSet(">=1.25")

    result = merge_specifiers(s1, s2)

    assert "1.25" in str(result)

def test_merge_range():

    s1 = SpecifierSet(">=1.20,<2.0")
    s2 = SpecifierSet(">=1.25")

    result = merge_specifiers(s1, s2)

    assert "1.25" in str(result)
    assert "2.0" in str(result)

def test_conflict():

    s1 = SpecifierSet("<2.0")
    s2 = SpecifierSet(">=2.1")

    with pytest.raises(Exception):
        merge_specifiers(s1, s2)

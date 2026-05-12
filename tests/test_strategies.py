import pytest
from packaging.specifiers import SpecifierSet

from pyvenvmerge.core.merger import merge_requirements
from pyvenvmerge.models.requirement import Requirement

def make_req(name, version):
    return Requirement(
        name=name,
        specifier=SpecifierSet(f"=={version}"),
        extras=set(),
        marker=None,
        source_type="pypi",
        raw_line=f"{name}=={version}",
    )

def test_strict_strategy_conflict():

    env1 = {"numpy": make_req("numpy", "1.0")}
    env2 = {"numpy": make_req("numpy", "2.0")}

    with pytest.raises(Exception):
        merge_requirements([env1, env2], strategy_name="strict")

def test_unpinned_strategy():

    env1 = {"numpy": make_req("numpy", "1.0")}
    env2 = {"numpy": make_req("numpy", "2.0")}

    merged = merge_requirements([env1, env2], strategy_name="unpinned")

    assert merged["numpy"].raw_line == "numpy"

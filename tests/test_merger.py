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

def test_merge_same_versions():

    env1 = {"numpy": make_req("numpy", "1.0")}
    env2 = {"numpy": make_req("numpy", "1.0")}

    merged = merge_requirements([env1, env2], strategy_name="highest")

    assert str(merged["numpy"].specifier) == "==1.0"

def test_merge_highest_version():

    env1 = {"numpy": make_req("numpy", "1.0")}
    env2 = {"numpy": make_req("numpy", "2.0")}

    merged = merge_requirements([env1, env2], strategy_name="highest")

    assert "2.0" in str(merged["numpy"].specifier)

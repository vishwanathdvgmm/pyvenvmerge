import pytest
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.core.merger import merge_requirements

def test_git_dependency_pass_through():

    req = Requirement(
        name="mypkg",
        specifier=None,
        extras=set(),
        marker=None,
        source_type="git",
        raw_line="git+https://repo.git#egg=mypkg",
    )

    merged = merge_requirements([{"mypkg": req}], "highest")

    assert merged["mypkg"].raw_line.startswith("git+")

def test_git_conflict():

    req1 = Requirement(
        name="mypkg",
        specifier=None,
        extras=set(),
        marker=None,
        source_type="git",
        raw_line="git+https://repo1.git#egg=mypkg",
    )

    req2 = Requirement(
        name="mypkg",
        specifier=None,
        extras=set(),
        marker=None,
        source_type="git",
        raw_line="git+https://repo2.git#egg=mypkg",
    )

    with pytest.raises(Exception):
        merge_requirements([{"mypkg": req1}, {"mypkg": req2}], "highest")

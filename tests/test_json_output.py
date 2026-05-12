from pyvenvmerge.models.merge_plan import MergePlan
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.models.environment import Environment
from pyvenvmerge.models.conflict import Conflict
from pathlib import Path

def test_merge_plan_to_dict():

    env = Environment(
        path=Path("envA"),
        python_path=Path("envA/python"),
        python_version="3.12"
    )

    from packaging.specifiers import SpecifierSet
    req = Requirement("numpy", SpecifierSet("==1.0"), set(), None, "pypi", "numpy==1.0")

    conflict = Conflict(
        package="numpy",
        versions_by_env={"envA": "==1.0", "envB": "==2.0"},
        selected_version="2.0",
        strategy="highest",
    )

    plan = MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={"numpy": req},
        conflicts=[conflict],
        warnings=["test warning"],
        strategy="highest",
    )

    data = plan.to_dict()

    assert data["python_version"] == "3.12"
    assert data["packages"] == ["numpy==1.0"]
    assert data["conflicts"][0]["type"] == "VERSION_CONFLICT"
    assert "warnings" in data
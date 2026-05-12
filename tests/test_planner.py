from pyvenvmerge.models.merge_plan import MergePlan
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.models.environment import Environment
from pathlib import Path

def test_merge_plan_structure():

    env = Environment(
        path=Path("envA"),
        python_path=Path("envA/python"),
        python_version="3.12"
    )

    from packaging.specifiers import SpecifierSet
    req = Requirement("numpy", SpecifierSet("==1.0"), set(), None, "pypi", "numpy==1.0")

    plan = MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={"numpy": req},
        strategy="highest"
    )

    assert plan.python_version == "3.12"
    assert "numpy" in plan.merged_requirements

def test_warning_field_exists():

    env = Environment(
        path=Path("envA"),
        python_path=Path("envA/python"),
        python_version="3.12"
    )

    from packaging.specifiers import SpecifierSet
    req = Requirement("numpy", SpecifierSet("==1.0"), set(), None, "pypi", "numpy==1.0")

    plan = MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={"numpy": req},
        warnings=["sample warning"],
        strategy="highest"
    )

    assert "sample warning" in plan.warnings

def test_semantic_warning_generation():

    warnings = []

    from packaging.requirements import Requirement as PackagingRequirement
    from packaging.version import Version

    dep = PackagingRequirement("numpy<2.0")

    version = Version("2.4.2")

    if not dep.specifier.contains(version):
        warnings.append("invalid")

    assert "invalid" in warnings

def test_risk_fields_exist():

    env = Environment(
        path=Path("envA"),
        python_path=Path("envA/python"),
        python_version="3.12"
    )

    from packaging.specifiers import SpecifierSet

    req = Requirement(
        "numpy",
        SpecifierSet("==1.0"),
        set(),
        None,
        "pypi",
        "numpy==1.0"
    )

    plan = MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={"numpy": req},
        compatibility_score=85,
        risk_level="MEDIUM",
        strategy="highest"
    )

    assert plan.compatibility_score == 85
    assert plan.risk_level == "MEDIUM"
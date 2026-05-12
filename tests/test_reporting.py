from pathlib import Path

from packaging.specifiers import SpecifierSet

from pyvenvmerge.models.environment import Environment
from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.models.merge_plan import MergePlan

from pyvenvmerge.core.reporting import (
    generate_report,
    save_json_report,
    save_lockfile,
)

def make_plan():

    env = Environment(
        path=Path("envA"),
        python_path=Path("envA/python"),
        python_version="3.12",
    )

    req = Requirement(
        name="numpy",
        specifier=SpecifierSet("==1.0"),
        extras=set(),
        marker=None,
        source_type="pypi",
        raw_line="numpy==1.0",
    )

    return MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={"numpy": req},
        compatibility_score=95,
        risk_level="LOW",
        strategy="highest",
    )

def test_generate_report():

    plan = make_plan()

    report = generate_report(plan)

    data = report.to_dict()

    assert data["python_version"] == "3.12"
    assert data["compatibility_score"] == 95
    assert "numpy==1.0" in data["packages"]

def test_save_json_report(tmp_path):

    plan = make_plan()

    report = generate_report(plan)

    output = tmp_path / "report.json"

    save_json_report(report, str(output))

    assert output.exists()

def test_save_lockfile(tmp_path):

    plan = make_plan()

    output = tmp_path / "lock.json"

    save_lockfile(plan, str(output))

    assert output.exists()
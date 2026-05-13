from pathlib import Path

from packaging.specifiers import SpecifierSet

from pyvenvmerge.core.report_generator import (
    generate_console_report,
    generate_json_report,
)
from pyvenvmerge.models.environment import Environment
from pyvenvmerge.models.merge_plan import MergePlan
from pyvenvmerge.models.requirement import Requirement

def test_generate_console_report():

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
    plan = MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={
            "numpy": req
        },
        compatibility_score=95,
        risk_level="LOW",
    )
    report = generate_console_report(
        plan
    )

    assert "Compatibility Score" in report
    assert "numpy==1.0" in report
    assert "LOW" in report

def test_generate_json_report():
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
    plan = MergePlan(
        environments=[env],
        python_version="3.12",
        merged_requirements={
            "numpy": req
        },
        compatibility_score=90,
        risk_level="LOW",
    )
    report = generate_json_report(
        plan
    )

    assert '"python_version": "3.12"' in report
    assert '"risk_level": "LOW"' in report
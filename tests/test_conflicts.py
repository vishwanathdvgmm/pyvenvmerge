from pyvenvmerge.models.requirement import Requirement
from pyvenvmerge.models.conflict import Conflict

from packaging.version import Version
from packaging.specifiers import SpecifierSet

def test_conflict_model():

    conflict = Conflict(
        package="numpy",
        versions_by_env={"envA": "1.0", "envB": "2.0"},
        selected_version="2.0",
        strategy="highest",
    )

    assert conflict.package == "numpy"
    assert conflict.versions_by_env["envA"] == "1.0"
    assert conflict.selected_version == "2.0"
    assert conflict.conflict_type == "VERSION_CONFLICT"

def test_specifier_semantic_validation():
    spec = SpecifierSet("<2.0")

    assert spec.contains(Version("1.5"))
    assert not spec.contains(Version("2.4"))
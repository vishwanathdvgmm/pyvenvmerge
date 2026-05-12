import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

def run(cmd):
    subprocess.run(cmd, check=True)

def test_full_merge_pipeline():

    temp_dir = Path(tempfile.mkdtemp())

    try:

        envA = temp_dir / "envA"
        envB = temp_dir / "envB"
        merged = temp_dir / "mergedEnv"

        # create environments
        run([sys.executable, "-m", "venv", str(envA)])
        run([sys.executable, "-m", "venv", str(envB)])

        pyA = envA / "Scripts" / "python.exe"
        pyB = envB / "Scripts" / "python.exe"

        # install different versions
        run([str(pyA), "-m", "pip", "install", "numpy==1.26.4"])
        run([str(pyB), "-m", "pip", "install", "numpy==2.4.2"])

        # run merge tool
        run([
            sys.executable,
            "-m",
            "pyvenvmerge",
            str(envA),
            str(envB),
            "-o",
            str(merged),
        ])

        merged_python = merged / "Scripts" / "python.exe"

        # check installed version
        result = subprocess.check_output(
            [str(merged_python), "-m", "pip", "show", "numpy"],
            text=True,
        )

        assert "Version: 2.4.2" in result

        # ensure dependency integrity
        subprocess.run(
            [str(merged_python), "-m", "pip", "check"],
            check=True
        )

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
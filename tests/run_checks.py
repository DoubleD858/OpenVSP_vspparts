"""Run the repository components in an isolated OpenVSP session."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vspscript", help="Path to vspscript or vspscript.exe")
    executable = Path(parser.parse_args().vspscript).resolve(strict=True)
    tests = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        scripts = work / "CustomScripts"
        scripts.mkdir()
        # Distinct names and contents prevent a bundled or user-installed part
        # with the same name from satisfying a test intended for this checkout.
        for part in sorted(tests.parent.glob("*.vsppart")):
            (scripts / ("Verify" + part.name)).write_text(
                "// Isolated validation copy\n" + part.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        shutil.copy2(tests / "geometry.vspscript", work)
        run = subprocess.run(
            [str(executable), "-script", "geometry.vspscript"],
            cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        print(run.stdout, end="")
        bad = ("FAIL ", " : ERR ", "Error Code:", "Exception")
        return int(run.returncode != 0 or "CHECKS PASSED" not in run.stdout
                   or any(token in run.stdout for token in bad))


if __name__ == "__main__":
    sys.exit(main())

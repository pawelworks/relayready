import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_expected_m0_m1_files_exist() -> None:
    expected = [
        "LICENSE",
        "NOTICE",
        "HANDOFF.md",
        "README.md",
        "docs/BUILD_BRIEF.md",
        "docs/DECISIONS.md",
        "spec/SPEC.md",
        "spec/handoff.schema.json",
        "spec/readback.schema.json",
    ]
    assert all((ROOT / relative).is_file() for relative in expected)


def test_each_rule_has_valid_and_invalid_example() -> None:
    for number in range(1, 14):
        rule = f"S{number:03d}"
        assert (ROOT / "examples" / "valid" / f"{rule}.md").is_file()
        assert (ROOT / "examples" / "invalid" / f"{rule}.md").is_file()


def test_generated_rule_documentation_is_current() -> None:
    result = subprocess.run(
        [sys.executable, "tools/generate_rule_docs.py", "--check"],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode == 0

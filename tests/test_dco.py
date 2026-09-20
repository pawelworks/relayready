from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
SIGNOFF = "Signed-off-by: Test Contributor <test@example.invalid>"


@pytest.mark.parametrize(("message", "expected"), [
    ("Change\n\n" + SIGNOFF, 0),
    ("Change\n\nSigned-off-by: Other Contributor <other@example.invalid>", 1),
    ("Change without a signoff", 1),
    ("Change\n\n" + SIGNOFF + "\n\nAn ordinary final paragraph, not a trailer.", 1),
    ("Change\n\nSigned-off-by:\n Test Contributor\n <test@example.invalid>", 1),
    ("Change\n\nSigned-off-by: Reviewer <reviewer@example.invalid>\n" + SIGNOFF, 0),
    ("Change\n\nReviewed-by: Reviewer <reviewer@example.invalid>\u2028" + SIGNOFF, 1),
    ("Change\n\n" + SIGNOFF + "\n extra continuation text", 1),
])
def test_dco_requires_an_author_matching_final_trailer(
    tmp_path: Path, message: str, expected: int,
) -> None:
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-c", "user.name=Test Contributor", "-c", "user.email=test@example.invalid",
         "commit", "--quiet", "--allow-empty", "--no-gpg-sign", "-m", message],
        cwd=tmp_path, check=True, capture_output=True,
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_dco.py"), "HEAD"],
        cwd=tmp_path, check=False, capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == expected, result.stderr
    assert result.stderr == ""
    if expected:
        assert result.stdout.startswith("missing author-matching Signed-off-by trailer: ")

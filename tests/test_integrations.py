from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
INTEGRATIONS = ROOT / "integrations"


def test_all_native_integration_artifacts_exist() -> None:
    expected = [
        "AGENTS.md.snippet",
        "codex/relayready/SKILL.md",
        "claude-code/relayready/SKILL.md",
        "goose/relayready.yaml",
        "kimi/relayready/SKILL.md",
        "chat/WRITE_PROMPT.md",
        "chat/RESUME_PROMPT.md",
        "VERIFICATION.md",
    ]
    assert all((INTEGRATIONS / item).is_file() for item in expected)


def test_skills_have_required_frontmatter() -> None:
    for relative in (
        "codex/relayready/SKILL.md",
        "claude-code/relayready/SKILL.md",
        "kimi/relayready/SKILL.md",
    ):
        text = (INTEGRATIONS / relative).read_text(encoding="utf-8")
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        assert frontmatter["name"] == "relayready"
        assert "HANDOFF.md" in frontmatter["description"]


def test_goose_recipe_has_documented_core_fields() -> None:
    recipe = yaml.safe_load((INTEGRATIONS / "goose/relayready.yaml").read_text(encoding="utf-8"))
    assert recipe["version"] == "1.0.0"
    assert recipe["title"] == "RelayReady"
    assert "wait for the human" in recipe["instructions"]


def test_chat_resume_requires_readback_first_and_wait() -> None:
    resume = (INTEGRATIONS / "chat/RESUME_PROMPT.md").read_text(encoding="utf-8")
    assert "first response" in resume
    assert "fenced `yaml` block" in resume
    assert "Wait for" in resume
    assert "explicit go-ahead" in resume


def test_portable_instructions_cover_start_and_end() -> None:
    snippet = (INTEGRATIONS / "AGENTS.md.snippet").read_text(encoding="utf-8")
    assert "relayready readback check HANDOFF.md READBACK.yaml" in snippet
    assert "Do not continue the task until" in snippet
    assert "relayready lint HANDOFF.md --check-pointers" in snippet

# Integration verification

Checked on 2026-09-20. Documentation verification establishes the package
format; only an installed binary check establishes local runtime evidence.

| Harness | Native package | Authoritative source | Local evidence | Status |
| --- | --- | --- | --- | --- |
| Codex | Project skill at `.agents/skills/<name>/SKILL.md` | <https://developers.openai.com/plugins/concepts/plugins> | `codex-cli 0.155.0-alpha.9`; `codex --help` passed | Format and local CLI verified; live relay pending |
| Claude Code | Project skill at `.claude/skills/<name>/SKILL.md` | <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview> | `2.1.241 (Claude Code)`; `claude --help` passed | Format and local CLI verified; live relay pending |
| goose | YAML recipe, project location `.goose/recipes/` | <https://goose-docs.ai/docs/guides/recipes/recipe-reference/> and <https://goose-docs.ai/docs/guides/recipes/storing-recipes/> | Binary not installed | Format verified; runtime and live relay unverified |
| Kimi Code | Project skill under `.agents/skills/` or `.kimi/skills/` | <https://moonshotai.github.io/kimi-code/en/customization/skills> | Binary not installed | Format verified; runtime and live relay unverified |

The M4 acceptance exercise is intentionally pending: the owner must perform one
manual relay between two different vendors using only the chat prompts and pass
the resulting readback check. No result is claimed here.

# Codex integration

Copy `relayready/` to `.agents/skills/relayready/` in a project. Codex discovers the
`SKILL.md` skill and loads its full instructions when the relay workflow applies.

The package shape was verified against the official Codex plugin architecture
documentation on 2026-09-20. Local runtime availability was verified with Codex
CLI 0.155.0-alpha.9; a live cross-vendor relay remains an owner acceptance gate.

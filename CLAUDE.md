# dogfood-dev

Minimal Python CLI that prints "Hello, World!". Exists solely to dogfood the `dev` plugin's
GitHub Issues tracker backend against a real repo (issues, PRs, CI).

## Architecture

Single-module CLI (`src/dogfood_dev/`), no services, no persistence. `main()` parses argv
and prints a greeting; flags are `--name`, `--shout`, `--version` (see `docs/SPEC.md`
Contracts). One milestone only, one task per flag/behavior (see `docs/ROADMAP.md`); two
tasks double as deliberate tracker-backend test vehicles (a recoverable CI failure and an
exhausting one), one carries a manual DoD criterion.

- Product docs: `docs/PRD.md`, `docs/SPEC.md`, `docs/ROADMAP.md`.
- Decision records: `docs/adr/` (none yet; no contested architecture choices at this size).
- Promoted retro learnings: `.claude/rules/`.
- Tracker backend: GitHub Issues (see `.claude/dev.md`).

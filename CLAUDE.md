# dogfood-dev

Minimal Python CLI that prints "Hello, World!". Exists solely to dogfood the `dev` plugin's
tracker backends against a real repo (issues, PRs, CI) — GitHub Issues (Milestone 1, passed),
then Linear (Milestone 2).

## Architecture

Single-module CLI (`src/dogfood_dev/`), no services, no persistence. `main()` parses argv
and prints a greeting; flags are `--name`, `--shout`, `--version` (see `docs/SPEC.md`
Contracts). Milestone 1: one task per flag/behavior (see `docs/ROADMAP.md`), each moved
through the GitHub Issues backend; two tasks doubled as deliberate tracker-backend test
vehicles (a recoverable CI failure and an exhausting one), one carried a manual DoD
criterion. Milestone 2 switches the tracker backend to Linear (workspace `dogfood-dev`, team
`DOG`, see ADR-001) and folds in `dev:backlog` change-management flows, unattended `/loop`
safeguards, and `dev:retro` promotion-benefit evidence.

- Product docs: `docs/PRD.md`, `docs/SPEC.md`, `docs/ROADMAP.md`.
- Decision records: `docs/adr/` (ADR-001: tracker-backend switch to Linear for Milestone 2).
- Promoted retro learnings: `.claude/rules/`.
- Tracker backend: GitHub Issues for Milestone 1 (closed history), Linear for Milestone 2
  onward (see `.claude/dev.md`).

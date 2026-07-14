---
tracker: linear
linear_team: DOG
linear_project: dogfood-dev
linear_milestone: Milestone 2
test_command: "uv run pytest"
ci_workflow: ci.yml
merge_policy: squash
review_action_installed: false
work_in_progress_limit: 3
max_fix_attempts: 2
max_tasks_per_run: 5
auto_merge: true
context_file: AGENTS.md
---

Minimal Python CLI (`uv` + pytest). This project exists to dogfood the `dev` plugin's
tracker backends (Phase E). Milestone 1 (closed, GitHub Issues backend, issues #1-4) used
`tracker: github`; CI stays on GitHub Actions regardless of tracker backend
(`wilsonkichoi/dogfood-dev` repo, unchanged). Milestone 2 switches to `tracker: linear`
(workspace `dogfood-dev`, team `DOG`, project `dogfood-dev`, milestone "Milestone 2") per
ADR-001 (`docs/adr/001-linear-tracker-switch.md`): Linear backend end-to-end, `dev:backlog`
flows, `/loop` safeguards, `dev:retro` promotion benefit.

- Run tests: `uv run pytest`.
- Run the CLI: `uv run dogfood-dev`.

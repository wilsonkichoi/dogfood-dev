---
tracker: github
test_command: "uv run pytest"
ci_workflow: ci.yml
merge_policy: squash
review_action_installed: false
work_in_progress_limit: 3
max_fix_attempts: 3
max_tasks_per_run: 5
auto_merge: false
---

Minimal Python CLI (`uv` + pytest). This project exists to dogfood the `dev` plugin's
GitHub Issues backend (Phase E, dogfood-dev checklist item 2): real issues, real PRs, real CI,
including a deliberately failing CI run and a deliberately unmet DoD criterion.

- Run tests: `uv run pytest`.
- Run the CLI: `uv run dogfood-dev`.

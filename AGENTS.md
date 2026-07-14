# dogfood-dev

Shared project context for Codex and Claude Code.

- Product docs: `docs/PRD.md`, `docs/SPEC.md`, and `docs/ROADMAP.md`.
- Architecture decisions: `docs/adr/`.
- Dev workflow configuration: `.agent/dev.md`.
- Tracker backend: Linear, team `DOG`, project `dogfood-dev`, milestone `Milestone 2`.
- Tests: `uv run pytest`.

## Project context migrated from `CLAUDE.md`

Minimal Python CLI that prints "Hello, World!". Exists solely to dogfood the `dev` plugin's
tracker backends against a real repo (issues, PRs, CI) — GitHub Issues (Milestone 1, passed),
then Linear (Milestone 2).

### Architecture

Single-module CLI (`src/dogfood_dev/`), no services, no persistence. `main()` parses argv
and prints a greeting; supported flags are `--name`, `--upper`, `--shout`, `--reverse`,
`--exclaim`, `--color`, `--json`, `--repeat`, and `--farewell` (see `docs/SPEC.md`
Contracts). Milestone 1: one task per flag/behavior (see `docs/ROADMAP.md`), each moved
through the GitHub Issues backend; two tasks doubled as deliberate tracker-backend test
vehicles (a recoverable CI failure and an exhausting one), one carried a manual DoD
criterion. Milestone 2 switches the tracker backend to Linear (workspace `dogfood-dev`, team
`DOG`, see ADR-001) and folds in `dev:backlog` change-management flows, unattended `/loop`
safeguards, and `dev:retro` promotion-benefit evidence.

- Product docs: `docs/PRD.md`, `docs/SPEC.md`, `docs/ROADMAP.md`.
- Decision records: `docs/adr/` (ADR-001: tracker-backend switch to Linear for Milestone 2).
- Promoted retro learnings: `AGENTS.md`.
- Tracker backend: GitHub Issues for Milestone 1 (closed history), Linear for Milestone 2
  onward (see `.agent/dev.md`).

## Promoted rules

### Check `.agent/dev.md` for uncommitted drift before trusting its values

Any `dev:*` skill invocation (`execute`, `auto`, `verify`, `review-pr`) that reads a
numeric/boolean field from `.agent/dev.md` (`max_fix_attempts`, `auto_merge`,
`work_in_progress_limit`, `max_tasks_per_run`, ...) must first check
`git status --porcelain .agent/dev.md` (or `git diff .agent/dev.md`). If it reports
uncommitted changes, surface the exact diff to the user before consuming the values.
Do not silently treat the working-tree copy as stable ground truth or fall back to the
committed copy.

Why: during the milestone-1 dogfood run, `max_fix_attempts` changed from 3 to 2 in the
uncommitted working tree mid-session. A downstream subagent was briefed from the stale
value and drained 3 real fix cycles against a live config of 2, an evidenced mismatch
between intended and executed behavior (task #3, `dogfood-dev` issue comments
2026-07-06T22:07-22:10).

Apply this at the top of every `dev:*` skill run, immediately after reading
`.agent/dev.md`. Treat a dirty file as uncommitted work and flag it before acting.

### Task packet authoring conventions (`dev:plan` / `dev:backlog`)

Never hardcode a config-driven numeral in a packet's body text. Fields such as
`max_fix_attempts`, `work_in_progress_limit`, and `max_tasks_per_run` live in
`.agent/dev.md` and can change after the packet is written. Reference them symbolically,
for example, "the configured `max_fix_attempts` limit", never "3 fix cycles".

Why: task #3's packet said "do not attempt more than `max_fix_attempts` (3) fix cycles".
`max_fix_attempts` later changed to 2 in the configuration, and that stale numeral was
executed against the live config (issue #3, comments 2026-07-06T22:07-22:10).

Every proof-point packet, where the DoD demonstrates a pipeline or tracker mechanism such
as `Blocked`, a manual hold, or exhausted retries rather than shipping product functionality,
must state its post-proof disposition. Specify whether it closes as `Wont Do` with a stated
rationale or remains in that state pending a named follow-up task.

### Separate merge-gate and post-merge packet requirements

A Definition of Done that `dev:verify` must satisfy before merging may require only evidence
available before the merge. Do not require a merged PR, a Linear `Done` transition, or
`dev:retro` as pre-merge evidence. Put those in a separate post-merge action and state
explicitly that it does not block verification or merge.

Why: DOG-15's original lifecycle DoD required `dev:retro`, merged-PR evidence, and Linear
`Done` before verification could merge. The first verification stopped at 6/7 until
`dev:backlog` split pre-merge verification from the post-merge retro action (PR #18,
2026-07-14).

### Use state-filtered Linear issue lists for triage and next-task selection

An unfiltered `list_issues` call can silently omit issues that a state-filtered call for the
same team and project returns. For `next-task` selection or backlog triage, use state-filtered
calls, such as `state: "Todo"`, as the authoritative candidate set. Do not conclude that
nothing is claimable from an unfiltered result.

Why: `DOG-10` (Urgent, `Todo`) was missing from three unfiltered calls despite the project
having only six issues. `DOG-9` (Medium) was incorrectly claimed ahead of it
(2026-07-07).

### Hand the Linear task packet to the `dev:reviewer` agent

For Linear-backed projects, `dev:review-pr` must include the fetched task packet body and the
latest work-summary comment as literal text in the prompt to `dev:reviewer`. Do not rely on
the reviewer to call `get_issue` itself.

Why: the reviewer's tool allowlist lacked Linear MCP access during `DOG-5`; it could only
review the PR body and could not independently verify the task's lifecycle DoD.

### Verify Linear status transitions after writing them

Before transitioning a Linear task, consult the backend mapping in the plugin's
`docs/tracker.md`. Some lifecycle statuses, including `Blocked`, are represented by a label
and an unchanged workflow state. After every transition write, re-read the issue and verify
that its `status` field and labels reflect the intended state. Do not assume a write succeeded
or would raise an error.

Why: `DOG-8` was instructed to use a nonexistent `Blocked` workflow state. The write silently
no-op'd and was caught only later (2026-07-07).

### Expect merge conflicts for parallel same-milestone CLI tasks

This project's CLI is concentrated in `src/dogfood_dev/__init__.py` and `tests/test_cli.py`.
Parallel tasks that add flags will usually modify both files. After the first sibling PR merges,
subsequent unrebased task branches are expected to become `CONFLICTING` even if their earlier
CI run was green.

Before merging the second or later PR in a parallel batch, `dev:verify` must check
`gh pr view <n> --json mergeable`. For `CONFLICTING`, resolve in the task worktree by merging
`origin/main`, combining the changes, running the full `test_command`, pushing, and waiting
for CI again.

Why: `DOG-7` and `DOG-9` each conflicted after sibling tasks merged first (2026-07-07).

### Keep PR DoD checkboxes current

Whichever skill independently confirms a DoD criterion, including green CI, a lifecycle
transition, or a manual check, must tick that criterion's PR-body checkbox in the same action.
Do not leave confirmed criteria unchecked for a later pass.

Why: `DOG-5`'s PR left its CI and Linear-lifecycle boxes unchecked after confirmation,
misrepresenting review state (2026-07-07).

### Push direct `main` commits before creating the next task worktree

Any commit made directly on local `main`, such as a `dev:retro`-promoted rule, must be pushed
to `origin/main` before running `git worktree add -b task/<id>-<slug> <path> main`. A task
worktree created from unpushed local `main` inherits unrelated commits, which can then be
merged inside an unrelated task PR.

Why: rule commits locally created after `DOG-5` were inherited by the `DOG-9` worktree and
merged within the `DOG-9` PR rather than as their own traceable commit (2026-07-07).

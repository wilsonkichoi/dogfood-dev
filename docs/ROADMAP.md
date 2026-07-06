# ROADMAP: dogfood-dev

One milestone. This project's scope is fixed to what's needed for Phase E dogfood-dev
checklist item 2 (GitHub Issues tracker backend); there is no milestone 2 planned.

## Milestone 1: GitHub Issues backend, full lifecycle

**Outcome:** the CLI gains a small, real feature set, each feature moved through
claim -> PR -> CI -> review -> verify -> merge (or correctly blocked) on the GitHub Issues
backend, producing an audited evidence trail for Phase E item 2.

**Scope:** `docs/SPEC.md` Contracts table in full: `--name`, `--shout`, `--version`, and the
unknown-flag/exit-2 usage error path. Four tasks:

| Task (working title) | Feature | Test-scenario role |
|---|---|---|
| `--name` flag | `--name NAME` support | plain task: full lifecycle, normal green CI |
| `--shout` flag | `--shout` support, composes with `--name` | carries the **recoverable CI failure**: first CI run must fail, a follow-up commit fixes it and CI goes green, within `max_fix_attempts` |
| `--version` flag | prints installed package version | carries the **exhausting CI failure**: CI fails persistently across all `max_fix_attempts` fix cycles, task lands in `status:blocked` with a diagnostic comment |
| unknown-flag usage error | stderr usage message, exit code 2 | carries the **manual DoD criterion**: at least one DoD criterion here is not mechanically checkable (e.g. "usage message wording is clear to a human reader"), forcing `dev:verify` to stop for a human regardless of `auto_merge` |

**Success criteria:**

- All four issues created with `status:*`/`priority:*`/`size:*` labels, moved through the
  full label lifecycle to closed (Done) or `status:blocked` as designed.
- Four real PRs, each linked to its issue (`Closes #N`), each with real CI runs.
- The recoverable-CI-failure task shows at least one red CI run followed by a green one on
  the same PR.
- The exhausting-CI-failure task shows `max_fix_attempts` red runs and a `status:blocked`
  transition with a comment naming the attempts and failure mode.
- The manual-DoD task's PR is NOT auto-merged by `dev:verify` until the manual criterion is
  explicitly confirmed by a human.
- `dev:status` reports a clean, consistent board across all four issues at the end.

**Out of scope:** any second milestone, any Linear or local-backend work, the automatic
PR-review GitHub Action, concurrent/multi-session claim testing, CLI packaging or
distribution beyond the existing `uv`/console-script setup.

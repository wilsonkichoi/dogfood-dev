# PRD: dogfood-dev

*Approved 2026-07-06.*

## Problem

The `dev` plugin's tracker adapter has three backends (Linear, GitHub Issues, local files),
one interface. The GitHub Issues backend (labels for status/priority/size, `gh` CLI verbs,
PR-linked issues, CI-driven review) has never been exercised end-to-end against a real GitHub
repo. The local-file backend already passed full-lifecycle dogfooding on `dogfood-local`
(Phase E checklist item 1). Without an end-to-end pass on GitHub Issues, the plugin's second
most-likely-adopted backend ships unverified: label transitions, `Blocked by #N` dependency
parsing, PR-closes-issue auto-close, `max_fix_attempts` → Blocked, and DoD-refusal-to-merge
are all unproven claims until a real run exercises them.

## Target customer

The `dev` plugin's maintainer (Wilson), acting as the first adopter of the GitHub Issues
backend. Downstream: any future `dev` plugin user who picks `tracker: github` in
`dev:setup` and needs confidence the path works before trusting it on a real project.

Not for: end users of the `dogfood-dev` CLI itself. The CLI's own features (a hello-world
program with a couple of flags) have no real customer; they exist only as vehicles for
tracker-backend test cases. This PRD is about the meta-goal (validating the plugin), not
about `dogfood-dev` as a product.

## Value proposition

A real, replayable end-to-end run (issues created, claimed, PR'd, CI'd, reviewed, merged or
correctly blocked) is the only thing that turns "the GitHub backend should work per the
tracker.md contract" into "the GitHub backend does work." It converts an unverified adapter
into a verified one, the same way `dogfood-local` did for the local backend.

## North star

Phase E dogfood-dev checklist item 2 (`agent-toolkit/plugins/dev/DESIGN.md`) passes with a
full audited evidence trail: real GitHub issues moved through `status:todo` →
`status:in-progress` → `status:in-review` → closed (Done), a real PR per task, real CI runs,
at least one deliberate CI failure driving `max_fix_attempts` → `status:blocked`, and at
least one deliberate unmet DoD criterion that `dev:verify` correctly refuses to merge.

## Goals

Ranked, outcome-phrased:

1. A small, real feature set lands on the `dogfood-dev` CLI (2-4 small tasks: e.g. a `--name`
   flag, a `--shout` flag, an exit-code convention), each moved through the full GitHub-backend
   lifecycle via `dev:execute` → `dev:review-pr` → `dev:verify`.
2. One task is deliberately constructed so its first CI run fails and is then fixed within
   `max_fix_attempts`, proving the fix-and-continue path.
3. A separate task is deliberately constructed so CI fails persistently and exhausts
   `max_fix_attempts`, proving the `status:blocked` path with a diagnostic comment.
4. One task carries a DoD criterion that cannot be mechanically satisfied by the diff as
   written (a manual verification step, or a criterion the executor is expected to miss),
   proving `dev:verify` refuses to merge until it's genuinely met.
5. `gh label`-based status transitions, `Blocked by #N` dependency parsing, and PR-closes-issue
   auto-close are all observed at least once.

## Non-goals

- The `dogfood-dev` CLI is not a real product and will not grow beyond what's needed to create
  credible small task packets. No user-facing polish, no packaging/distribution, no versioning
  policy.
- No `Linear` or `local` backend work here; those are separate checklist items (already passed
  for local; Linear is a later item).
- No automatic PR review Action (`review_action: false` by standing decision, no
  `ANTHROPIC_API_KEY` configured) - review is manual `/dev:review-pr` only.
- Not attempting multi-developer concurrency or claim-race testing (single-session dogfood).

## Constraints & assumptions

- Single developer (Wilson), single session at a time; no concurrent claim-race scenario in
  scope for this milestone.
- `gh auth status` already verified working against `wilsonkichoi/dogfood-dev`, SSH remote.
- CI is GitHub Actions only (`.github/workflows/ci.yml`, already scaffolded, runs
  `uv run pytest`).
- Assumes the `work_in_progress_limit: 3` and `max_fix_attempts: 3` defaults in `.claude/dev.md`
  are the values to test against, not tuned per-task.

## Open questions

None outstanding. (Resolved during discovery: the deliberate-CI-failure scenario is split
across two tasks, one recovering within `max_fix_attempts`, one exhausting it.)

## Notes for architecture

- CLI is trivial (single-module Python package, `uv`-managed, `pytest` for tests) - no real
  architecture decisions needed. `docs/SPEC.md` should stay equally minimal: current-state
  description (CLI entry point, test layout) plus the small feature contracts (flag names,
  expected stdout/exit codes) the milestone's tasks will implement against.
- No data stores, no external services, no auth - keep `docs/SPEC.md` proportionate to that.

## Sources

None. `research/raw/` is empty; this PRD is drawn entirely from the interview in this session
and from `agent-toolkit/plugins/dev/DESIGN.md`'s Phase E checklist (item 2: GitHub Issues
backend).

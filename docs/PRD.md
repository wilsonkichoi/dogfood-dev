# PRD: dogfood-dev

*Approved 2026-07-06. Milestone 2 delta approved 2026-07-06 (see Change log).*

## Problem

The `dev` plugin's tracker adapter has three backends (Linear, GitHub Issues, local files),
one interface. The GitHub Issues backend (labels for status/priority/size, `gh` CLI verbs,
PR-linked issues, CI-driven review) had never been exercised end-to-end against a real GitHub
repo. The local-file backend already passed full-lifecycle dogfooding on `dogfood-local`
(Phase E checklist item 1). Without an end-to-end pass on GitHub Issues, the plugin's second
most-likely-adopted backend shipped unverified: label transitions, `Blocked by #N` dependency
parsing, PR-closes-issue auto-close, `max_fix_attempts` → Blocked, and DoD-refusal-to-merge
were all unproven claims until a real run exercised them. **That run passed (Milestone 1,
2026-07-06).**

Remaining unproven: the Linear backend (official MCP server, native priorities/estimates/
blocked-by relations, the preferred backend for multi-dev teams) has never run end-to-end
either. Nor has `dev:backlog`'s change-management surface (one-off intake, manual-ticket
packet validation, `Backlog → Todo` promotion, `Wont Do` with rationale, spec-impacting
routing to `dev:architect`), the unattended-loop safeguards (`work_in_progress_limit` gate,
`Blocked` on a stuck task), or `dev:retro`'s closed-memory-loop claim (a promoted rule
demonstrably changing a later session's behavior). Per `DESIGN.md`'s own plan ("Items 2+: gh
repo clone wilsonkichoi/dogfood-dev"), this same repo is where those remaining Phase E
checklist items get proven, rather than spinning up a fresh project per item.

## Target customer

The `dev` plugin's maintainer (Wilson), acting as the first adopter of the GitHub Issues
backend (Milestone 1) and now the Linear backend plus the backlog/loop-safeguard/retro
mechanisms (Milestone 2). Downstream: any future `dev` plugin user who picks `tracker: github`
or `tracker: linear` in `dev:setup`, or who relies on `dev:backlog`, unattended `/loop`, or
`dev:retro` promotion, and needs confidence those paths work before trusting them on a real
project.

Not for: end users of the `dogfood-dev` CLI itself. The CLI's own features (a hello-world
program with a couple of flags) have no real customer; they exist only as vehicles for
tracker-backend test cases. This PRD is about the meta-goal (validating the plugin), not
about `dogfood-dev` as a product.

## Value proposition

A real, replayable end-to-end run (issues created, claimed, PR'd, CI'd, reviewed, merged or
correctly blocked) is the only thing that turns "the GitHub backend should work per the
tracker.md contract" into "the GitHub backend does work." It converts an unverified adapter
into a verified one, the same way `dogfood-local` did for the local backend. Milestone 2
applies the same logic to the Linear backend and to the parts of the plugin that Milestone 1
didn't exercise: change management between planning cycles (`dev:backlog`), unattended
operation's failure-mode safeguards, and whether `dev:retro`'s memory loop actually closes
(a promoted rule changing a later session's behavior, not just getting written to a file).

## North star

Phase E dogfood-dev checklist items 2-through-the-remaining-Phase-E-items
(`agent-toolkit/plugins/dev/DESIGN.md`) pass with full audited evidence trails:

- **Item 2 (GitHub Issues backend) - passed 2026-07-06, Milestone 1.** Real GitHub issues
  moved through `status:todo` → `status:in-progress` → `status:in-review` → closed (Done), a
  real PR per task, real CI runs, one deliberate CI failure driving `max_fix_attempts` →
  `status:blocked`, one deliberate unmet DoD criterion `dev:verify` correctly refused to
  merge.
- **Item 3 (Linear backend) - Milestone 2.** Real Linear issues on workspace `dogfood-dev`,
  team `DOG`, moved through the full workflow-state lifecycle (`Backlog → Todo → In Progress →
  In Review → Done`), a real claim with the write-then-re-read confirmation guard exercised
  (single-session; see Non-goals), at least one issue reaching `Done` via the same
  execute → review → verify path Milestone 1 proved on GitHub.
- **Backlog-flows item - Milestone 2.** `dev:backlog` demonstrably handles: a one-off ticket
  intake producing a full packet, a manually-created ticket caught and completed by packet
  validation at claim time, an explicit `Backlog → Todo` promotion, a `Wont Do` closure with a
  surviving rationale comment, and a spec-impacting request correctly routed to a
  `dev:architect` delta rather than actioned directly.
- **Unattended-safeguards item - Milestone 2.** A `/loop /dev:execute` batch run observably
  hits the `work_in_progress_limit` gate and idles instead of over-claiming; a deliberately
  stuck task lands in `Blocked` with a diagnostic comment naming attempts and failure mode.
- **Retro-benefit item - Milestone 2.** `dev:retro` on a completed task proposes at least one
  concrete `.claude/rules/` or `CLAUDE.md` promotion backed by real PR/CI/comment evidence
  (not a generic platitude), the promotion is applied, and a subsequent `dev:execute` session
  demonstrably changes behavior because of it (not merely "the rule exists").

## Goals

Ranked, outcome-phrased:

**Milestone 1 (passed 2026-07-06):**

1. A small, real feature set landed on the `dogfood-dev` CLI (`--name`, `--shout`,
   `--version`, unknown-flag usage error), each moved through the full GitHub-backend
   lifecycle via `dev:execute` → `dev:review-pr` → `dev:verify`.
2. One task's first CI run failed and was fixed within `max_fix_attempts`, proving the
   fix-and-continue path.
3. A separate task's CI failed persistently and exhausted `max_fix_attempts`, proving the
   `status:blocked` path with a diagnostic comment.
4. One task carried a DoD criterion that could not be mechanically satisfied, proving
   `dev:verify` refuses to merge until it's genuinely met.
5. `gh label`-based status transitions, `Blocked by #N` dependency parsing, and
   PR-closes-issue auto-close were all observed at least once.

**Milestone 2 (this delta):**

6. The tracker backend switches to Linear (`tracker: linear`, workspace `dogfood-dev`, team
   `DOG`); at least one real task moves through `Backlog → Todo → In Progress → In Review →
   Done` on Linear via `dev:execute` → `dev:review-pr` → `dev:verify`, with the claim step's
   write-then-re-read guard exercised.
7. `dev:backlog` handles, against this milestone's real tasks: one-off ticket intake (full
   packet), a manually-created ticket completed by packet validation at claim time, an
   explicit `Backlog → Todo` promotion, a `Wont Do` closure with a surviving rationale, and a
   spec-impacting request correctly routed to a `dev:architect` delta.
8. An unattended `/loop /dev:execute` batch run observably hits the `work_in_progress_limit`
   gate and idles rather than over-claiming.
9. A deliberately stuck task lands in `Blocked` with a diagnostic comment (attempts, failure
   mode) under `max_fix_attempts`.
10. `dev:retro` on a completed Milestone-2 task proposes a concrete rule/CLAUDE.md promotion
    from real evidence; once applied, a subsequent `dev:execute` session demonstrably behaves
    differently because of it.

## Non-goals

- The `dogfood-dev` CLI is not a real product and will not grow beyond what's needed to create
  credible small task packets. No user-facing polish, no packaging/distribution, no versioning
  policy.
- No `local` file backend work here; that checklist item already passed on `dogfood-local`.
- True multi-session/concurrent claim-race testing is out of scope for Milestone 2: the claim
  guard is proven as a single-session code-path check (write, re-read, confirm), not by
  racing two real sessions against the same issue. (See "Claim race scope" decision below.)
- No automatic PR review Action (`review_action_installed: false` by standing decision, no
  `ANTHROPIC_API_KEY` configured) - review stays manual `/dev:review-pr` only.
- Brownfield-adoption and final-release Phase E checklist items are separate, not folded into
  this milestone.

## Constraints & assumptions

- Single developer (Wilson), single session at a time for Milestone 2's core lifecycle tasks;
  no concurrent-session infrastructure is being built for the claim-race guard (decided
  2026-07-06: single-session verification, not a true race between two coordinated sessions -
  matches Milestone 1's single-developer constraint and avoids new multi-process test infra
  that nothing else in this project needs).
- `gh auth status` already verified working against `wilsonkichoi/dogfood-dev`, SSH remote
  (still used for CI; the tracker backend changes, the GitHub *repo* does not).
- Linear MCP server already authenticated (OAuth, no API key) against workspace `dogfood-dev`;
  team `DOG` confirmed to exist with states Backlog/Todo/In Progress/In Review/Done/Canceled/
  Duplicate - no workflow-state creation needed. No Linear *project* exists yet under team
  `DOG`; creating one (and deciding the milestone-to-project-vs-label mapping per
  `tracker.md`) is a `dev:architect`/`dev:setup` task, not resolved here.
- CI is GitHub Actions only (`.github/workflows/ci.yml`, unchanged); the tracker backend
  switch does not touch CI.
- Assumes the `work_in_progress_limit` and `max_fix_attempts` values live in `.claude/dev.md`
  are the values to test against, not tuned per-task (per [[dev-config-drift]] rule: check for
  uncommitted drift before trusting them).

## Open questions

None outstanding for this delta. (Resolved during discovery: claim-race guard is
single-session verification, not a true concurrent-session race.)

## Notes for architecture

- Milestone 1 notes still apply: CLI is trivial, no real architecture decisions needed there.
- New for Milestone 2: `docs/SPEC.md`'s negative requirement "Must NOT depend on Linear or the
  local file tracker backend" needs revising - it's now a Milestone-1-scoped historical note,
  not a current constraint. `docs/ROADMAP.md` needs a Milestone 2 section (currently states
  "there is no milestone 2 planned" and lists Linear/second-milestone work as explicitly out
  of scope - both need updating).
- `dev:architect` should decide: Linear project name/creation for team `DOG`; whether
  "milestone" maps to a Linear project or a label (`tracker.md` prefers project); how the six
  Milestone-2 checklist-item goals decompose into a task list (the backlog-flows and
  retro-benefit goals likely need tasks specifically *shaped* to exercise those mechanisms,
  the way Milestone 1 engineered a recoverable-CI-failure task and an exhausting one).
- The spec-impacting-routed-to-architect-delta scenario (Goal 7) needs a deliberately designed
  request at plan/execute time, distinct from this PRD delta itself (this delta was the
  *project's own* scope change, triaged goal-impacting rather than spec-impacting; the
  in-milestone demo needs its own manufactured spec-impacting ticket).

## Sources

None. `research/raw/` is empty. Milestone 1 content is drawn from the interview in that
discovery session and `agent-toolkit/plugins/dev/DESIGN.md`'s Phase E checklist (item 2).
This delta is drawn from the same `DESIGN.md` checklist (items 3, backlog-flows,
unattended-safeguards, retro) and the 2026-07-06 interview confirming claim-race scope.

## Change log

- **2026-07-06** - Delta via `/dev:backlog` → `/dev:discover` (goal-impacting: request to fold
  Linear-backend + backlog-flows + unattended-safeguards + retro-benefit Phase E items into
  this same repo as Milestone 2). Changed: Problem (added remaining-unproven paragraph),
  Target customer (extended to Linear/backlog/loop/retro), Value proposition (extended),
  North star (added Milestone 2 items alongside Milestone 1's passed item), Goals (added 6-10),
  Non-goals (removed the blanket "no Linear or local backend work" line; local-only exclusion
  and true-concurrency exclusion stated precisely), Constraints (added Linear/team/claim-race
  specifics). Invalidates: `docs/SPEC.md`'s "Must NOT depend on Linear..." negative
  requirement and `docs/ROADMAP.md`'s "no milestone 2 planned" / "out of scope: any Linear...
  work" lines - both need a `dev:architect` delta before `dev:plan` can write Milestone 2
  task packets. Handed back to `dev:backlog` triage / `dev:architect`.

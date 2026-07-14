# ROADMAP: dogfood-dev

Two milestones. Milestone 1 covered Phase E dogfood-dev checklist item 2 (GitHub Issues
tracker backend) and passed 2026-07-06. Milestone 2 (added 2026-07-06, see `docs/PRD.md`
Change log and ADR-001) covers the Linear backend, `dev:backlog` change-management flows,
unattended `/loop` safeguards, and `dev:retro`'s memory-loop claim, per
`agent-toolkit/plugins/dev/DESIGN.md`'s plan to keep exercising Phase E items 2+ against
this same repo. No milestone 3 is planned.

## Milestone 1: GitHub Issues backend, full lifecycle

**Outcome:** the CLI gains a small, real feature set, each feature moved through
claim -> PR -> CI -> review -> verify -> merge (or correctly blocked) on the GitHub Issues
backend, producing an audited evidence trail for Phase E item 2.

**Historical scope:** `--name`, `--shout`, and the unknown-flag/exit-2 usage error path
became the merged CLI contract. `--version` was a historical Wont Do proof vehicle and is not
implemented. Four tasks:

| Task (working title) | Feature | Test-scenario role |
|---|---|---|
| `--name` flag | `--name NAME` support | plain task: full lifecycle, normal green CI |
| `--shout` flag | `--shout` support, composes with `--name` | carries the **recoverable CI failure**: first CI run must fail, a follow-up commit fixes it and CI goes green, within `max_fix_attempts` |
| `--version` flag | historical Wont Do, not implemented | carried the **exhausting CI failure** proof vehicle; it is not part of the current CLI contract |
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

**Out of scope:** the automatic PR-review GitHub Action, concurrent/multi-session claim
testing, CLI packaging or distribution beyond the existing `uv`/console-script setup.

## Milestone 2: Linear backend, backlog flows, unattended safeguards, retro benefit

**Outcome:** the tracker backend switches to Linear (`tracker: linear`, workspace
`dogfood-dev`, team `DOG`, per ADR-001) for a new batch of small real feature tasks, moved
through the full lifecycle as in Milestone 1 but now proving the Linear mapping, plus
`dev:backlog`'s change-management surface, `/loop /dev:execute`'s WIP-gate and Blocked
safeguards, and `dev:retro`'s promotion loop actually changing a later session's behavior —
closing out Phase E checklist items 3 through the retro-benefit item.

**Scope:** per `docs/SPEC.md` "Milestone-2 test-scenario tasks" and `docs/PRD.md` Goals 6-10.
Task count and exact seeding mechanisms are a `dev:plan` decision; scenario requirements
fixed by the spec:

**Historical initial `dev:plan` push** (2026-07-06): 5 tasks — T-R1 (`--repeat`), T-J
(`--json`), T-K (`--color`), T-X (`--pad`, later a historical Wont Do, priority: low), T-R2
(`--farewell`, depends on T-R1 via a real Linear "blocked by" relation). Scenarios "one-off intake",
"manually-created ticket", "Backlog → Todo promotion", "Wont Do", and "spec-impacting
routing" are deliberately *not* pre-created here — they must arrive later via `dev:backlog`/
a manual Linear ticket, since that arrival path is what each is proving.

**Current merged CLI scope:** the active flags are `--name`, `--upper`, `--shout`, `--reverse`,
`--exclaim`, `--color`, `--json`, `--repeat`, and `--farewell`, as specified in
`docs/SPEC.md` Contracts. Later completed dogfooding tasks added `--reverse` (`DOG-11`),
`--upper` (`DOG-12`), and `--exclaim` (`DOG-13` and `DOG-14`). `--version` and `--pad N` are
historical Wont Do items, not active scope; `DOG-8` was canceled.

**Demonstration order** (recorded here so a `/loop` session doesn't have to rediscover it):

1. Claim T-R1, T-J, T-K → all reach `In Review` → WIP = `work_in_progress_limit` → Linear
   full-lifecycle evidence on each.
2. `/loop /dev:execute` attempts a 4th claim. T-X is a genuinely claimable candidate
   (independent, no unmet deps) at this point, so the refusal is unambiguously the WIP gate,
   not "nothing to claim" — the next-task algorithm checks the gate before candidates. Loop
   idles.
3. Human verifies/merges T-R1, T-J, T-K → `Done`, WIP drains back down.
4. Historical record: T-X was the deliberate exhausting-CI proof vehicle. It is now a
   canceled historical Wont Do item, and `--pad N` is not an active contract.
5. `dev:retro` runs on T-R1 (now `Done`) → proposes/applies a rule.
6. T-R2's dependency (T-R1 `Done`) is now satisfied → claimable → its `dev:execute` session
   demonstrably follows the promoted rule, cited in T-R2's work-summary comment.

| Scenario | Checklist item | Notes |
|---|---|---|
| Full Linear lifecycle on ≥1 task, claim guard exercised | Linear backend | `Backlog → Todo → In Progress → In Review → Done`, single-session guard check |
| One-off ticket intake via `dev:backlog` | backlog flows | Full packet, not from the milestone dry-run |
| Manually-created ticket, incomplete packet | backlog flows | Caught and completed by `dev:execute`'s packet validation at claim |
| `Backlog → Todo` promotion | backlog flows | Explicit human decision, per `dev:backlog` |
| `Wont Do` closure with rationale | backlog flows | Reason must survive on the ticket |
| Spec-impacting request routed to an `dev:architect` delta | backlog flows | `dev:backlog` triage correctly stops and routes instead of actioning directly |
| ≥`work_in_progress_limit` tasks simultaneously In Progress/In Review | unattended safeguards | `/loop /dev:execute` observably idles at the gate; sequential unmerged tasks suffice, no true concurrency needed |
| One task exhausts `max_fix_attempts` | unattended safeguards | Lands in `Blocked` with a diagnostic comment, mirrors Milestone 1's exhausting-CI task |
| `dev:retro` promotes a rule from real evidence; a later task's `dev:execute` visibly follows it | retro benefit | Needs at least two sequenced tasks: one to retro, one to observe the behavior change on |

**Success criteria:**

- At least one Linear issue moves through the full workflow-state lifecycle to `Done` with a
  real PR, real CI run, and the claim guard exercised.
- Each backlog-flow scenario above is observed at least once, with the resulting ticket
  state/comment as evidence.
- A `/loop /dev:execute` run log shows the WIP gate being hit and the loop idling rather than
  over-claiming.
- A deliberately stuck task reaches `Blocked` with a diagnostic comment naming attempts and
  failure mode.
- A `dev:retro` promotion is applied to `.claude/rules/` or `CLAUDE.md`, and a subsequent
  task's `dev:execute` session shows a concrete behavior difference attributable to it (cited
  in that task's work-summary comment).
- `dev:status` reports a clean, consistent board across all Milestone 2 tasks at the end.

**Out of scope:** true multi-session/concurrent claim-race testing, the local file tracker
backend (separate, already passed), the automatic PR-review GitHub Action, brownfield
adoption and final-release Phase E items (separate checklist items, not folded in here), any
milestone 3.

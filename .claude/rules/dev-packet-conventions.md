# Task packet authoring conventions (dev:plan / dev:backlog)

**Never hardcode a config-driven numeral in a packet's body text.** Fields like
`max_fix_attempts`, `work_in_progress_limit`, `max_tasks_per_run` live in `.claude/dev.md`
and can change after the packet is written. Reference them symbolically - "the configured
`max_fix_attempts` limit" - never "3 fix cycles", so the packet can't drift out of sync
with the live config.

**Why:** task #3's packet said "do not attempt more than `max_fix_attempts` (3) fix
cycles". `max_fix_attempts` later changed to 2 in `.claude/dev.md`; the packet still said
3, and that stale numeral is what got executed against a live config of 2
(`dogfood-dev` issue #3, comments 2026-07-06T22:07-22:10). See also
[[dev-config-drift]].

**Every "proof-point" packet (DoD = demonstrate a pipeline/tracker mechanism reaches a
state, e.g. `Blocked`, a manual-hold, an exhausted-retry path - as opposed to shipping a
feature) must state its own post-proof disposition.** Say explicitly what happens once
the state is reached and evidenced: close as `Wont Do` with a given rationale, or stay in
that state pending a real follow-up task, and name which.

**Why:** task #3's packet specified the mechanism to prove (`max_fix_attempts` ->
`status:blocked`) but never said what should happen afterward. That produced an
unplanned mid-session interactive decision (human asked to choose Won't-Do vs. leave
Blocked) that a complete packet would have pre-empted.

**How to apply:** `dev:plan` drafting a packet whose DoD references a config field or
whose purpose is to demonstrate pipeline behavior (rather than deliver product
functionality) must satisfy both conventions above before the packet is considered
complete.

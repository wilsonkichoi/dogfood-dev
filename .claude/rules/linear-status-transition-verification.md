# Verify tracker-status transitions actually landed; check docs/tracker.md's backend mapping first

Before instructing any session or subagent to transition a task to a lifecycle status via
`mcp__linear__save_issue(state: ...)`, check `docs/tracker.md`'s backend-specific status
mapping table first. Some lifecycle statuses (`Blocked`) do not correspond to a workflow
state on this Linear team at all - they map to a label plus an unchanged state. A
`save_issue(state: "Blocked")` call against a team without that state does not error; it
silently no-ops, leaving the issue's state unchanged with no signal anything went wrong.

**Why:** DOG-8's proof-point task was briefed to "transition to Blocked via `save_issue`"
without checking `docs/tracker.md` first (which already documented the Linear mapping:
Blocked = keep state, add `blocked` label). The subagent's transition call silently no-opped;
the mistake was caught only by chance during a later comment review, not by any tool error
(`dogfood-dev` DOG-8, 2026-07-07).

**How to apply:** any `dev:*` skill or subagent prompt that instructs a status transition on
a Linear-backed project must (1) consult `docs/tracker.md`'s backend mapping table for that
specific status first, and (2) re-read the issue after the transition call to confirm the
`status` field actually changed to what was intended - never assume a `save_issue` call
either succeeded or would have raised on failure.

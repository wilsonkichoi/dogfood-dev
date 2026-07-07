# Cross-check unfiltered list_issues against a state-filtered call before trusting "nothing else is claimable"

`mcp__linear__list_issues` called without a `state` filter can silently omit issues that are
well within the stated `limit` and that a `state`-filtered call for the same team/project
does return.

**Why:** DOG-10 (Urgent priority, `Todo`) was missing from three unfiltered `list_issues`
calls in the same session, despite the team/project having only 6 issues total - well under
the 100-item limit used. Only a `state: "Todo"`-filtered call surfaced it. This caused
DOG-9 (Medium priority) to be claimed ahead of DOG-10 (Urgent), a real violation of the
next-task selection algorithm's priority ordering, caught only because the user asked why
(`dogfood-dev` DOG-9/DOG-10, 2026-07-07).

**How to apply:** any `next-task` selection or backlog/triage sweep against the Linear
backend must cross-check an unfiltered `list_issues` result with at least one
`state`-filtered call (e.g. `state: "Todo"`) before concluding the candidate set is complete.
Treat a mismatch between the two as the filtered result being authoritative.

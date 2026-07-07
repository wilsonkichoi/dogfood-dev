# Hand the dev:reviewer agent the fetched Linear packet directly, never let it self-fetch

On Linear-backed projects (`tracker: linear`), `dev:review-pr` must include the fetched
task packet body and the latest work-summary comment as literal text in the prompt it
gives the `dev:reviewer` agent. Never rely on that agent to call `get-task` itself.

**Why:** the `dev:reviewer` agent's tool allowlist is Read/Grep/Glob/Bash only - no
Linear MCP tools - so on DOG-5 it could not self-fetch the task packet via `get-task`,
contradicting `dev:review-pr`'s independence-rule instruction to hand it "nothing else."
It fell back to the PR body text alone, leaving the Linear-lifecycle DoD criterion
unverified by the independent review itself (`dogfood-dev` DOG-5 retro comment,
2026-07-07).

**How to apply:** `dev:review-pr`, at the point it spawns `dev:reviewer` for a
Linear-tracked task, must paste the packet body and latest work-summary comment into the
agent's prompt as plain text. This is additive to "nothing else" (no implementation
diff, no other context) - it does not give the reviewer implementation visibility, only
the same packet/summary text a GitHub-backend reviewer would get for free from the issue
body.

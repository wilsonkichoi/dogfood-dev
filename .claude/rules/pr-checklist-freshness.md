# Re-tick PR body DoD checkboxes the moment each criterion is confirmed

Whichever skill independently confirms a Definition-of-Done criterion true (CI green,
a lifecycle transition, a manual check) must also tick that criterion's checkbox in the
PR body **in the same action**, not leave it for a later pass or for a human to notice.

**Why:** PR #9's (DOG-5) body DoD checklist was left unchecked for "CI green" and the
Linear-lifecycle criterion even after both were independently confirmed true - the human
had to ask why before it got fixed (`dogfood-dev` DOG-5 retro comment, 2026-07-07). A
stale checkbox next to a confirmed-true criterion misrepresents review state to anyone
reading the PR without the tracker open.

**How to apply:** `dev:execute` (opening the PR, and each CI-fix cycle that turns a
check green) and `dev:verify` (posting the verification report) - each must edit the PR
body to tick the corresponding checkbox at the point it confirms that criterion, not
defer it to a later step or another skill.

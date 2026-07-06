# Check .claude/dev.md for uncommitted drift before trusting its values

Any `dev:*` skill invocation (`execute`, `auto`, `verify`, `review-pr`) that reads a
numeric/boolean field from `.claude/dev.md` (`max_fix_attempts`, `auto_merge`,
`work_in_progress_limit`, `max_tasks_per_run`, ...) must first check
`git status --porcelain .claude/dev.md` (or `git diff .claude/dev.md`). If it reports
uncommitted changes, surface the exact diff to the user before consuming the values -
do not silently treat the working-tree copy as stable ground truth, and do not silently
fall back to the committed copy either.

**Why:** during the milestone-1 dogfood run, `max_fix_attempts` changed from 3 to 2 in
the uncommitted working tree mid-session. A downstream subagent was briefed off the
stale value read earlier and drained 3 real fix cycles against a live config of 2 -
an actual, evidenced mismatch between intended and executed behavior (task #3,
`dogfood-dev` issue comments 2026-07-06T22:07-22:10).

**How to apply:** at the top of any `dev:*` skill run, right after reading
`.claude/dev.md`, run the drift check. Treat a dirty file the same as any other
uncommitted-work signal per the global git-safety guidance - flag it, don't act past it
silently.

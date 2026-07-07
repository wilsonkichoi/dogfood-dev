# Expect merge conflicts when multiple same-milestone tasks land in parallel on this single-module CLI

This project's entire CLI lives in two files (`src/dogfood_dev/__init__.py`,
`tests/test_cli.py`). Any two tasks worked in parallel within the same milestone will branch
from the same `main` commit and very likely both modify these same two files (each adding a
new flag). The first PR to merge will succeed cleanly; every subsequent PR merged before its
branch is rebased will show `mergeable: CONFLICTING` on GitHub, even though CI was green when
it was opened.

**Why:** DOG-7's PR (#11) and DOG-9's PR (#12) each independently conflicted with `main` after
DOG-6 (and then DOG-6+DOG-7) merged first - both edited the same `argparse` setup block and
test file. This wasn't a bug in either implementation; it's structurally guaranteed by this
project's one-module layout (`dogfood-dev` DOG-7/DOG-9, 2026-07-07).

**How to apply:** `dev:verify`, before merging the 2nd or later PR in a batch of same-milestone
parallel tasks, must check `gh pr view <n> --json mergeable` (not just CI status) - a green CI
run from before an earlier sibling task merged does not mean the PR is still mergeable. On
`CONFLICTING`, resolve in the task's worktree (`git merge origin/main`, combine the diffs by
hand, re-run the full `test_command`), push, and re-watch CI before merging - do not attempt
`gh pr merge` against a conflicting PR and assume GitHub will handle it.

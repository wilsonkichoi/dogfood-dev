# Push any main-branch commit before creating the next task worktree

A commit made directly to local `main` (e.g. a `dev:retro`-promoted rule file) must be pushed
to `origin/main` before running `git worktree add -b task/<id>-<slug> <path> main` for the
next task. `git worktree add` snapshots whatever `main` points to locally, including unpushed
commits - the new task branch silently inherits them as part of its own diff, and when that
PR is later squash-merged, the unrelated commit's content lands on `origin/main` bundled
into that PR instead of standing as its own dedicated commit.

**Why:** the two retro-promoted rule files from DOG-5 were committed locally as their own
dedicated commit (`8c7438f`), per `dev:retro`'s own "commit immediately, before any next task
starts" instruction - but the commit wasn't pushed before DOG-9's worktree was created from
that same local `main`. DOG-9's branch inherited the rule files as part of its diff; they
ended up merged into `main` bundled inside "DOG-9: --farewell flag (#12)" rather than as their
own traceable commit (`dogfood-dev` DOG-9, 2026-07-07).

**How to apply:** any `dev:*` skill that commits directly to `main` (retro promotions, backlog
doc deltas, spec deltas) must `git push origin main` in the same step as the commit, before
any subsequent `git worktree add ... main` call in the same session.

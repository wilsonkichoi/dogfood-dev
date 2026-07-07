# ADR-001: Switch tracker backend to Linear for Milestone 2

Date: 2026-07-06
Status: accepted

## Context

Milestone 1 validated the `dev` plugin's GitHub Issues tracker backend end-to-end on this
repo (`tracker: github` in `.claude/dev.md`, 4 issues through the full lifecycle). Phase E's
remaining checklist items include the Linear backend end-to-end, `dev:backlog` change-
management flows, unattended `/loop` safeguards, and `dev:retro`'s memory-loop claim.
`agent-toolkit/plugins/dev/DESIGN.md`'s own dogfood plan ("Where" section) designates this
same cloned repo (`~/src/dogfood-dev`) as the vehicle for every Phase E item from #2 onward,
rather than a fresh project per item. The question this ADR settles: how does a repo already
mid-lifecycle on one tracker backend pick up dogfooding a second backend.

## Options

| Option | Pros | Cons |
|---|---|---|
| A. Switch `tracker: github` → `tracker: linear` in place, same repo, new milestone | Matches `DESIGN.md`'s stated plan; GitHub repo/CI untouched (only task-state backend moves); Milestone 1's closed issues stay valid history; single `docs/` tree, no duplicated scaffolding | `.claude/dev.md` frontmatter is single-valued (`tracker:` is one field) — the two milestones' tasks live on different tracker backends, which `dev:status` and any cross-milestone query must handle as a fact of this project's history, not a bug |
| B. Fresh repo/project per backend (mirrors how `dogfood-local` got its own project for the local-backend item) | Clean isolation, no mixed-backend history in one repo | Contradicts `DESIGN.md`'s explicit plan for items 2+; duplicates scaffolding (`docs/`, CI, labels) for no dogfood value beyond what switching in-place already proves; the local-backend item's separate project was chosen *before* `DESIGN.md`'s "items 2+ reuse dogfood-dev" plan existed for a different reason (item 1 had no GitHub remote yet) |
| C. Run both backends simultaneously (dual-tracker) | Would prove backends don't interfere | Not a real deployment shape the plugin supports (`tracker:` is single-valued by design in `docs/tracker.md`); adds complexity with no corresponding PRD goal |

## Decision

Option A. Switch `.claude/dev.md`'s `tracker` field from `github` to `linear` in place,
scoped to Linear workspace `dogfood-dev` / team `DOG`, for Milestone 2 onward. Milestone 1's
GitHub issues remain closed and untouched as historical record; no migration of that state
into Linear. `docs/ROADMAP.md` gets a Milestone 2 section documenting the switch explicitly
so a future reader isn't confused by mixed backend history in one repo's tracker config.

## Consequences

- `.claude/dev.md`'s `tracker: linear` applies going forward; any tooling that assumes a
  repo's tracker field is constant for its whole history needs to instead read
  `docs/ROADMAP.md` per-milestone to know which backend governed which milestone's tasks.
- Loses nothing already proven: Milestone 1's evidence trail (issues #1-4, PRs, CI runs)
  stays valid and unaffected by the config change.
- Forecloses running a true multi-session Linear claim-race test in this project (see PRD
  Non-goals) — accepted, since Option A's scope is one dev/one repo continuing sequentially,
  not multi-developer infrastructure.
- If a future Phase E item needs yet another backend (`local` already passed elsewhere), the
  same in-place-switch pattern applies unless a contradicting reason emerges.

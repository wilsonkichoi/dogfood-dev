# SPEC: dogfood-dev

*Approved 2026-07-06. Milestone 2 delta approved 2026-07-06 (see Change log, ADR-001).*

## Architecture overview

Single-module Python CLI. No services, no network calls, no persistence. The entire system
is one process that parses argv and prints to stdout/stderr.

```mermaid
flowchart LR
    A[gh CLI / user] -->|invokes| B["dogfood-dev (console script)"]
    B --> C["dogfood_dev.__init__:main"]
    C -->|argv| D[arg parsing]
    D -->|valid| E[stdout: greeting]
    D -->|invalid| F[stderr: usage, exit 2]
```

## Components

- **`dogfood_dev` package** (`src/dogfood_dev/__init__.py`): owns `main()`, argument parsing,
  and greeting formatting. Sole component; no internal layering needed at this size.
- **`dogfood_dev.__main__`**: thin `python -m dogfood_dev` entry, delegates to `main()`.
- **Console script** `dogfood-dev` (`pyproject.toml` `[project.scripts]`): production entry
  point, delegates to `main()`.

## Contracts

`main()` reads `sys.argv`. Every flag is optional. `--repeat` and `--json` are mutually
exclusive; all other supported flags compose according to the transformation order below.

| Flag | Effect | Notes |
|---|---|---|
| *(none)* | stdout: `Hello, World!` + newline, exit 0 | current behavior, unchanged |
| `--name NAME` | stdout: `Hello, {NAME}!` + newline, exit 0 | replaces `World`; `NAME` taken verbatim, no escaping/sanitization needed (local CLI, not a security boundary) |
| `--upper` | uppercases `NAME` before the greeting is built | does not uppercase the salutation or punctuation by itself |
| `--shout` | uppercases the greeting | runs after `--upper`; uppercases the salutation, name, and punctuation-preserving text |
| `--reverse` | reverses the greeting string | runs after `--shout` |
| `--exclaim` | appends two literal `!` characters | the base greeting already ends in `!`, so output ends in `!!!`; runs after `--reverse` |
| `--color {blue,green,red,yellow}` | wraps the completed greeting in the ANSI escape code for the selected color plus `\x1b[0m` | invalid color is bad usage (exit 2); runs before `--json` serialization |
| `--json` | stdout: a JSON object with the completed greeting in its `message` member | mutually exclusive with `--repeat`; bad usage (exit 2) if both are supplied |
| `--repeat N` | stdout: the completed greeting printed `N` times, one per line | `N` is a positive integer (`>=1`); non-positive or non-integer `N` is bad usage (exit 2) |
| `--farewell` | selects `Goodbye` instead of `Hello` as the salutation | participates when the initial greeting is built |
| unknown flag / bad usage | stderr: a one-line usage message, exit code 2 | includes unknown flags, invalid `--color`, invalid `--repeat`, and `--repeat` with `--json`; exact wording is an implementation choice |

Transformation order is fixed:

1. Build the salutation (`Goodbye` with `--farewell`, otherwise `Hello`) and name (`NAME` with
   `--name`, otherwise `World`).
2. Apply `--upper` to the name only.
3. Build the greeting as `{salutation}, {name}!` and apply `--shout` to that greeting.
4. Apply `--reverse` to the greeting.
5. With `--exclaim`, append two extra exclamation marks.
6. With `--color`, wrap the greeting in the selected ANSI color sequence and reset sequence.
7. With `--json`, serialize the resulting greeting as the `message` member of the output JSON
   object. Otherwise, print it `--repeat` times, one line per occurrence.

### Historical Wont Do items

`--version` and `--pad N` are not implemented and are not active CLI contracts. They remain
only as historical dogfooding proof vehicles: `--version` in Milestone 1 and `--pad N` in
Milestone 2 (`DOG-8`, canceled).

No config files, no environment variables, no stdin reading.

## Data model

None. No entities, no persistence, no migrations.

## Non-functional requirements

- Startup-to-output latency: no explicit floor: a Python CLI printing one line has no
  measurable perf requirement at this scale.
- Python: `>=3.14` (pinned in `pyproject.toml`, matches the runtime already installed via `uv`).
- No availability/uptime requirement (not a running service).

## Security model

No authn/authz, no secrets, no user data. `--name` accepts arbitrary text printed verbatim to
stdout; not a template/shell context, so no injection surface.

## Negative requirements

(from PRD non-goals)

- The CLI must NOT grow user-facing polish, packaging/distribution tooling, or a versioning
  policy beyond what a milestone task explicitly requires; additions exist only to produce
  credible small task packets for tracker-backend testing.
- Must NOT depend on the local file tracker backend; that checklist item already passed on
  `dogfood-local`. (Milestone 1 was GitHub-Issues-only; Milestone 2 adds Linear — see
  ADR-001 and the Change log below.)
- Must NOT add the automatic PR-review GitHub Action (`review_action_installed: false`
  stands; no `ANTHROPIC_API_KEY` configured). Review stays manual `/dev:review-pr`.
- Must NOT introduce true multi-session/concurrent claim-race testing: the Linear claim
  guard (Milestone 2) is proven as a single-session write-then-re-read code-path check, not
  by racing two coordinated sessions (see ADR-001, PRD Non-goals).

## Development environment

- Language: Python 3.14, managed via `uv` (see `~/.claude/rules/python.md`-equivalent
  conventions: `uv run`, `uv add`, never bare `pip`).
- Test runner: `pytest`, invoked as `uv run pytest`.
- Package layout: `src/` layout, `uv_build` backend, console script `dogfood-dev`.
- Lint/format: none configured; not required by any milestone-1 task.

## Deployment architecture

None. Not deployed anywhere; runs locally via `uv run dogfood-dev` or the installed console
script. CI (`.github/workflows/ci.yml`) runs `uv run pytest` on push/PR to `main`. CI's
purpose here is exclusively to produce the pass/fail signal that `dev:execute`/`dev:verify`
consume, not to gate a deployment.

## Milestone-1 test-scenario tasks

Two of the milestone's feature tasks additionally serve as tracker-backend test vehicles
(per `docs/PRD.md` Goals 2-4). `docs/ROADMAP.md` names which task carries which scenario;
the exact seeding mechanism (how a CI failure is deliberately introduced, and what makes a
DoD criterion non-mechanical) is a `dev:plan` packet-drafting decision, not a contract fixed
here; only the *existence* of one recoverable-CI-failure task, one exhausting-CI-failure
task, and one manual-DoD task is fixed.

## Milestone-2 test-scenario tasks

Per `docs/PRD.md` Goals 6-10 (Linear backend, `dev:backlog` flows, unattended safeguards,
retro benefit). `docs/ROADMAP.md` names the scenario requirements; as with Milestone 1, the
exact task count, sequencing, and seeding mechanism are `dev:plan` packet-drafting decisions,
not fixed here. Fixed by this spec:

- At least one task moves through the full Linear workflow-state lifecycle
  (`Backlog → Todo → In Progress → In Review → Done`) via `dev:execute` → `dev:review-pr` →
  `dev:verify`, on team `DOG`, with the claim step's write-then-re-read guard exercised
  (single-session; see Negative requirements).
- At least one task is created via `dev:backlog` one-off intake (not from the milestone's
  original `dev:plan` dry-run) with a full packet.
- At least one ticket is created manually (directly in the Linear UI, incomplete packet) and
  is caught and completed by `dev:execute`'s packet-validation step at claim time.
- At least one task demonstrates an explicit `Backlog → Todo` promotion and one demonstrates
  a `Wont Do` closure with a surviving rationale comment.
- At least one request is deliberately spec-impacting and is correctly routed by
  `dev:backlog` to a `dev:architect` delta rather than actioned directly.
- Enough tasks reach `In Progress`/`In Review` simultaneously (at or above
  `work_in_progress_limit`) for a `/loop /dev:execute` batch run to observably hit the gate
  and idle, without requiring true multi-session concurrency (sequential unmerged
  in-review tasks satisfy the count).
- At least one task is deliberately constructed to exhaust `max_fix_attempts` and land in
  `Blocked` with a diagnostic comment (mirrors Milestone 1's exhausting-CI-failure task, now
  on the Linear backend).
- `dev:retro` runs on a completed Milestone-2 task, proposes a rule/CLAUDE.md promotion from
  real evidence, the promotion is applied, and a subsequent task's `dev:execute` session
  visibly follows it.

## Change log

- **2026-07-06** — Delta via `/dev:backlog` → `/dev:architect` (spec-impacting: Milestone 2
  request, following the approved PRD delta). Changed: Negative requirements (lifted the
  blanket Linear exclusion; local-backend and true-concurrency exclusions restated
  precisely), added "Milestone-2 test-scenario tasks" section. See ADR-001 for the
  tracker-backend-switch decision. `docs/ROADMAP.md` gets a matching Milestone 2 section.
- **2026-07-06** — Delta via `/dev:plan` (spec gap found while drafting Milestone 2 packets:
  no Contract rows existed for any new small feature to serve as a Milestone-2 task vehicle).
  Added Contracts rows: `--repeat N`, `--json`, `--pad N`, `--color`, `--farewell`. No ADR:
  trivial additions, no contested tradeoff. `--pad N` is the designated exhausting-CI-failure
  vehicle (mirrors Milestone 1's `--version` role).
- **2026-07-13** — Approved delta: reconciled the Contracts section with the
  merged CLI. Added `--upper`, `--reverse`, and `--exclaim`; fixed the complete composition
  order; and moved `--version` and `--pad N` to Historical Wont Do items.

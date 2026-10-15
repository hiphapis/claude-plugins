# worktree-teardown project config

Copy to `.claude/worktree-teardown.md` in your repository and edit.

## Issue labels

| State | Label | Title emoji |
| --- | --- | --- |
| ready | `ready to work` | 📋 |
| in-progress | `in progress` | 🚧 |
| in-review | `in review` | 👀 |
| blocked | `blocked` | ⛔ |
| on-hold | `on hold` | ⏸️ |
| done | closed (`completed`) | ✅ |

## Completion procedure

Follow `docs/dev/task-lifecycle.md` § "Finishing a task".

## Canonical paths

- `README.md`, `CLAUDE.md`, `AGENTS.md`
- `docs/product/**`, `docs/dev/**`
- `docs/adr/*.md` — tables, frontmatter and status banners only

## History paths

- `docs/plans/**`, `docs/specs/**`
- `docs/adr/*.md` — body text
- `CHANGELOG.md`

## Record files

- `docs/status.md`
- `.loop/memory/STATE.md`

## Extra skip patterns

- `public/_mock-videos/`

## Extra preserve patterns

- `assets/generated/`

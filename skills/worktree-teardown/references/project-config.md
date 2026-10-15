# Optional project config — `.claude/worktree-teardown.md`

Put this file in a project (main worktree) to tell the skill your project's policy. Every section is optional; missing sections fall back to the generic defaults in `audit-rules.md`. Plain Markdown so humans and agents read the same thing.

See [`../../../examples/worktree-teardown.md`](../../../examples/worktree-teardown.md) for a filled-in example.

## Sections the skill reads

| Section | Used by | Content |
| --- | --- | --- |
| `## Issue labels` | §3.5 | Which label means *ready* / *in-progress* / *in-review* / *blocked* / *on-hold*. Optional title-emoji mapping for the cross-check |
| `## Completion procedure` | §3.5, step 5 | A link to the project's completion doc, or the steps/commands inline. The skill follows it verbatim |
| `## Canonical paths` | §3.6 | Globs that state current facts (drift there → 🔴) |
| `## History paths` | §3.6 | Globs that are snapshots (drift there → skipped) |
| `## Record files` | §3.2, §3.7 | Where branch status / keep-discard reasons are recorded and grepped |
| `## Extra skip patterns` | §3.4 | Project-specific regenerable ignored paths |
| `## Extra preserve patterns` | §3.4 | Project-specific ignored paths that must never vanish |

Rules:

- The config **adds** to the blacklist; it never turns it into a whitelist.
- If the config points at a completion doc, read that doc rather than copying its commands here — two copies drift.

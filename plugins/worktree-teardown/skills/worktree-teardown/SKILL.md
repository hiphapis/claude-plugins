---
name: worktree-teardown
description: Audit a git worktree before it is deleted — what would be lost and which wrap-up steps were skipped. Use when asked "can I delete this worktree", "is it safe to remove", "did I leave anything behind", "clean up worktree", or in Korean "이 워크트리 지워도 돼 / 삭제해도 안전한지 / 흘린 거 없나 / 워크트리 정리 / 폐기해도 되나". Runs 11 audit items (uncommitted, untracked, unpushed, unmerged, stash, non-regenerable ignored assets, issue state, Orca state, child worktrees, canonical-doc drift, record consistency), judges SAFE / BLOCKED, performs approved wrap-up (issue comment/labels, docs, Orca status, asset copies), re-audits, then presents the delete command. The human always runs the deletion.
---

# Worktree teardown audit

Bring one worktree to a state where deleting it loses nothing.

**Read [`references/audit-rules.md`](references/audit-rules.md) at the start and follow it.** It holds every command, grading rule, the ignored-asset classes and the end states. Do not improvise checks from memory.

## Project policy layer

Labels, title emoji, completion steps, record files and canonical-vs-history doc paths are **project policy**, not rules of this skill. Resolve them in this order before auditing:

1. `.claude/worktree-teardown.md` in the main worktree (format: [`references/project-config.md`](references/project-config.md))
2. The project's `CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md` — look for an issue lifecycle, completion checklist or worktree rule, and follow what it says
3. The generic defaults in `audit-rules.md`

Never copy a project's completion commands into your report as if they were this skill's — cite where they came from.

## Boundaries

- **Does**: audit → `SAFE` / `BLOCKED(n)` → wrap-up after approval → re-audit → **present** the delete command
- **Does not**: delete the worktree · commit someone's changes · merge / rebase / push · delete or move files · close an issue as `not planned`
- Target is the main worktree → stop.
- If the human chooses to **merge** an unmerged branch, finish step 5 (wrap-up) **first**, then hand off — to `superpowers:finishing-a-development-branch` if installed, otherwise present the merge commands.

## Flow

1. **Resolve target** — Orca metadata if the worktree is Orca-managed, else `git worktree list --porcelain`
2. **Collect the 10 mechanical items** — independent commands, run in parallel
   Items 10 (doc drift) and 11 (records) are **not optional** — skipping them is how stale docs survive. If the branch changed no documented facts, say so explicitly.
3. **Evaluate the 1 judgment item** — record consistency. Never auto-assign BLOCKED
4. **Report + ask for approval** — each finding as `what is lost → where it is → one-line fix`
5. **Do the approved wrap-up** — preservation is **copy only**
6. **Re-audit** — mechanical items only
7. **End** — `SAFE` (present delete command) · `BLOCKED(n)` (no command) · `HANDOFF` · `ABORT`

## Traps

- **Don't stop after reporting.** Step 5 is the only step that turns findings into fixes. Any early exit — especially "let's merge" — leaves every 🟡 untouched.
- **Three states, not two.** A tool that is *not used by this project* (no Orca, non-GitHub remote, no issue convention) makes its item **N/A** and does not block SAFE. A tool that *is used but whose call failed* is 🟡 — unverified is never ✓.
- **Bypass output-rewriting shell hooks** (e.g. `rtk proxy <cmd>` when rtk is installed). They swallow format flags and replace output with summaries, which flips verdicts silently. Read raw output; don't trust `wc -l` counts.
- **Orca `workspaceStatus` alone means nothing** — it is usually `in-progress` everywhere. Judge it only crossed with the issue state.
- **Ignored assets use a blacklist.** Report everything not on the skip list; a whitelist lets new asset types vanish silently.
- **Judge `.env*` by `diff` against the main worktree, not by existence.** Worktree copies always "exist in main".
- **Base ref is never hardcoded.** Use Orca `baseRef`, else `origin/HEAD`, else ask.

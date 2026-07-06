# Track A — Consolidate & migrate docs into the vault (Claude Code)

This runs in the terminal with Claude Code operating **directly on the repo
files on disk**. It is deliberately phased with a human approval gate, because
misclassifying a doc (e.g. treating tool machinery as knowledge, or vice versa)
poisons everything downstream. **Do not run this inside an autonomous loop.**

## Phase 0 — Orient

Confirm the repo layout and that the vault will live at `<repo>/docs` (a
subfolder, never the repo root). Identify which doc-generating tools are in play
so their machinery can be protected:

- **superpowers** — skills / SKILL.md, often `specs/`, `plans/`
- **omc (oh-my-claude-code)** — config, commands
- **loopcraft** — loop state, run logs, memory
- **Claude Code itself** — `CLAUDE.md`, `.claude/` (settings, commands, hooks,
  skills), state files

## Phase 1 — Inventory (STOP for approval; move nothing)

1. Find every doc-like file in the repo (`.md`, `.mdx`, `.txt`, README, ADR,
   documentary YAML). Exclude `node_modules`, `.git`.
2. Classify each into exactly one bucket:
   - **[KEEP-tool]** machinery/config/state a tool needs → stays put
   - **[KEEP-log]** session scratch / run logs / trial-and-error → stays put
     (or propose archiving)
   - **[MOVE-knowledge]** real project knowledge (PRD, business plan, research,
     story planning, decision rationale) → migrate to vault
   - **[MIXED]** machinery that *contains* knowledge → extract the knowledge to
     the vault, leave the operational file in place
3. Output a table: `path | likely source (which tool) | bucket | one-line
   summary | proposed action`.
4. Separately flag duplicates/conflicts (same decision in two places) and stale
   candidates.
5. **Validate the folder skeleton**: treat the default in
   `assets/vault-structure.md` as a hypothesis; propose folder additions/
   merges/renames only where actual docs don't fit. Keep top-level folders to
   ~6–8; no one-folder-per-file. Justify every proposed change with a reason.
6. **Stop and wait for the human to confirm the table and skeleton.**

## Phase 2 — Migrate (only after approval)

1. Create the confirmed skeleton under `<repo>/docs`.
2. Move each **[MOVE-knowledge]** file into its folder. **Move, don't delete.**
   Leave a stub at the old path:
   ```markdown
   ---
   title: "<original title> (moved)"
   status: stub
   moved_to: docs/<new/path>.md
   updated: <today>
   ---

   > 📦 This document moved to the knowledge vault.
   > → [[<new/path>]]
   ```
3. For **[MIXED]**, extract only the knowledge into a vault note and cite the
   source file path at the top; leave the operational file untouched.
4. Add frontmatter to every note: `title`, `status` (draft|review|final),
   `source` (original path), `updated`. Story/template notes also get domain
   fields (e.g. `slug`, `theme`, `status`).
5. Reconstruct **ADRs** for recoverable past decisions under the ADR folder
   using `assets/adr-template.md` (decision / context / rationale / impact). If
   a rationale can't be verified, leave a "confirm needed" placeholder — never
   fabricate.
6. Connect related notes with Obsidian wikilinks `[[...]]`.
7. Build a dashboard note (e.g. `00-대시보드/홈.md` or `00-dashboard/home.md`)
   with an index + open items + placeholder list + deadlines.
8. Put note templates in `_templates/`.
9. **`.gitignore`** — ignore only the churn-y Obsidian files, NOT the whole
   `.obsidian/` (plugin/port settings should be shared across machines):
   ```
   docs/.obsidian/workspace.json
   docs/.obsidian/workspace-mobile.json
   docs/.obsidian/cache
   ```
10. **Update `CLAUDE.md`**: add a rule that the `/docs` vault is the source of
    truth and that refined conclusions get promoted there — this is what stops
    fragmentation from recurring.

## Guardrails

- Never delete (move + stub + keep a migration map).
- Never move/modify tool machinery (only `CLAUDE.md` gets the new rule).
- Small, well-described commits per step.
- When unsure, stop and ask.

## Model/effort suggestion

Phase 1 (classification + structure judgment) benefits from a strong model at
high reasoning effort. Phase 2 (mechanical execution) can run at lower effort,
though ADR reconstruction is judgment-heavy. If unsure, use the strongest model
at high effort throughout — a wrong move is annoying to reverse.

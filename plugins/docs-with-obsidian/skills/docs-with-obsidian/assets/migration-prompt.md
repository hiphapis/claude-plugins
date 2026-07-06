# Generalized migration prompt (paste into Claude Code)

Fill the `{{...}}` blanks, then paste into a **normal interactive** Claude Code
session (not an autonomous loop). Run Phase 1, review the table, then approve
Phase 2.

---

```markdown
# Goal
Consolidate this repo's scattered project docs into a single Obsidian vault at
`{{VAULT_PATH}}` (the repo's /docs folder), synced across machines via git.
Knowledge (planning, decisions, research, domain content) goes into /docs;
code and tool config stay where they are. Open /docs as the vault, NOT the repo
root.

# Do NOT touch (tool machinery — moving it breaks the tools)
These tools generate their own files; leave them in place:
- superpowers (skills / SKILL.md, specs/, plans/)
- omc (oh-my-claude-code) config/commands
- loopcraft (loop state / run logs / memory)
- Claude Code itself: CLAUDE.md, .claude/ (settings, commands, hooks, skills)

# Phase 1 — Inventory (STOP and report; move nothing yet)
1. Find every doc-like file (.md, .mdx, .txt, README, ADR, documentary YAML).
   Exclude node_modules and .git.
2. Classify each: [KEEP-tool] machinery/config/state → stays;
   [KEEP-log] session scratch/run logs → stays (or propose archive);
   [MOVE-knowledge] real project knowledge → vault;
   [MIXED] machinery containing knowledge → extract knowledge to vault, leave
   the operational file in place.
3. Output a table: path | likely source | bucket | one-line summary | action.
4. Flag duplicates/conflicts and stale candidates separately.
5. Treat this skeleton as a HYPOTHESIS; propose folder changes only where real
   docs don't fit. Keep top-level folders ≤ 8; no one-folder-per-file. Justify
   each change.
   Skeleton: 00-대시보드 / 01-사업 / 02-제품 / 03-의사결정(ADR) / 04-동화 /
   05-조사 / 06-개발규칙 / _templates   (rename/localize as appropriate)
6. STOP and wait for my approval. Do not start Phase 2.

# Phase 2 — Migrate (only after I approve)
1. Create the confirmed skeleton under /docs.
2. Move [MOVE-knowledge] files (move, not delete); leave a stub at the old path
   with frontmatter (status: stub, moved_to: ...) and a [[wikilink]].
3. [MIXED]: extract knowledge into a vault note citing the source path; leave
   the operational file untouched.
4. Add frontmatter to every note: title, status(draft|review|final), source,
   updated. Domain notes get extra fields (e.g. slug, theme).
5. Reconstruct ADRs for recoverable decisions (decision/context/rationale/
   impact). If a rationale is uncertain, leave a "confirm needed" placeholder —
   never invent one.
6. Link related notes with [[wikilinks]].
7. Build a dashboard note (00-*/home) with index + open items + placeholders +
   deadlines.
8. Put note templates in _templates/.
9. Add to repo .gitignore (only these, not all of .obsidian/):
   docs/.obsidian/workspace.json
   docs/.obsidian/workspace-mobile.json
   docs/.obsidian/cache
10. Update CLAUDE.md: the /docs vault is the source of truth; refined
    conclusions get promoted there.

# Guardrails
- Never delete (move + stub; keep a migration map).
- Never move/modify tool machinery (only CLAUDE.md gets the new rule).
- Small, well-described commits per step.
- If unsure, stop and ask.
```

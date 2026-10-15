# Project Custom Instructions template

Fill the `{{...}}` blanks and tailor the category bullets to the project's real
folders, then paste into the claude.ai project's **Custom Instructions**. Only
effective while the project has the `{{MCP_SERVER_NAME}}` MCP connected.

---

```
This project deals with {{PROJECT_NAME}}.

The source of truth for project knowledge is the Obsidian vault accessed via the
{{MCP_SERVER_NAME}} MCP (the repo's /docs folder). Attached project files may be
snapshots, so when current information is needed, query the vault first with the
{{MCP_SERVER_NAME}} tools — especially do NOT skip the lookup for:
- decision rationale → check the ADR folder (03-*)
- current status / milestones → check 00-dashboard (project-status, home)
- pricing / business policy → check 01-business
- PRD / feature specs → check 02-product
- {{DOMAIN}} work → check 04-* and _templates
- dev rules (git workflow, testing, verification, etc.) → check 06-dev-rules
  (adjust the bullets above to this project's actual folders)

When new conclusions, decisions, or research appear, before the conversation
ends, ask me first whether to write them into the relevant vault note via
{{MCP_SERVER_NAME}}:create or str_replace. Never overwrite a vault file
blindly; always view the current contents before editing.

The superpowers/, plans/, specs/ folders are Claude Code work logs, not source-
of-truth knowledge. Don't answer from them; cite only content promoted into the
knowledge folders (00–06), confirming with me if needed.

Vault notes are connected with wikilinks ([[...]]); when creating a note, link
related documents to prevent fragmentation.

Don't invent facts and write them into the vault. Leave unconfirmed values as a
placeholder tag or checklist item (keep the existing convention).
```

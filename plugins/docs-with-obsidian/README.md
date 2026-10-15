# docs-with-obsidian

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh-CN.md)

A [Claude Code](https://claude.com/claude-code) plugin that packages a complete,
battle-tested methodology for turning a software project's scattered
documentation into a single, well-organized, link-rich **Obsidian vault** that
lives in the repo's `/docs` folder — shared by Claude Code, Claude Desktop, and
you, all kept in sync by git.

Docs fragment. Some end up in `README`s, some in `.claude/`, some in tool output
(superpowers, omc, loopcraft), some in your head. This plugin encodes a proven
end-to-end process — **including the setup gotchas that cost real time** — for
consolidating all of it into one vault that every participant treats as the
source of truth.

## The mental model (read this first)

Three participants operate on the **same on-disk `<repo>/docs` folder**, kept in
sync by **git**:

| Participant | Role | Best for | Needs Obsidian open? |
|-------------|------|----------|:---:|
| **Claude Code** (terminal) | Works directly on repo files on disk | Bulk file surgery — consolidate, move, categorize, migrate, `.gitignore`, commits. Git-native. | No |
| **Claude Desktop** | Connects to the vault through the Obsidian "Claude Code MCP" plugin | Day-to-day read/update of notes, vault-aware, reflected live | Yes |
| **Obsidian** | The human's editing surface, and host of the MCP server | Reading, linking, graph view | — |

The vault lives at **`<repo>/docs`** — not the repo root (that would index
`node_modules` and code). One repo holds both code and docs, so a single
`git pull` syncs everything to the same point in time.

## What you get

One skill (`docs-with-obsidian`) encoding a two-track methodology plus the
templates and reference procedures to execute it:

| Component | What it does |
|-----------|--------------|
| **Track A — Consolidate & migrate** (`references/claude-code-setup.md`) | Inventory every doc across the repo → classify (`KEEP-tool` / `KEEP-log` / `MOVE-knowledge` / `MIXED`) → **stop for human approval** → move (never delete) leaving a stub at the old path → apply a folder skeleton → add frontmatter + `[[wikilinks]]` → reconstruct ADRs → update `.gitignore` and `CLAUDE.md`. |
| **Track B — Connect & instruct** (`references/desktop-mcp-setup.md`) | Open `<repo>/docs` as its own vault → install the "Claude Code MCP" plugin → give each vault a unique HTTP port → wire Claude Desktop via the `mcp-remote` stdio bridge → connect Claude Code via `/ide` → verify with a read + write test → generate project instructions so the vault becomes the source of truth. |
| **Vault skeleton** (`assets/vault-structure.md`) | A lifecycle-based folder starter (`00-dashboard` … `06-dev-rules`, `_templates`) — a hypothesis to adapt, not a mandate. Folder names can be localized. |
| **Migration prompt** (`assets/migration-prompt.md`) | A ready-to-paste, generalized Track-A prompt — fill the blanks, hand it to Claude Code. |
| **Project-instructions template** (`assets/project-instructions-template.md`) | Custom Instructions that make claude.ai consult the vault (via MCP) as source of truth and write conclusions back. |
| **ADR template** (`assets/adr-template.md`) | One note per past decision; leave a "confirm needed" placeholder rather than inventing a rationale. |
| **Desktop MCP config snippet** (`assets/claude-desktop-config-snippet.md`) | The exact `mcp-remote` bridge JSON — avoids the bare-`url` failure that silently drops the server. |
| **Troubleshooting** (`references/troubleshooting.md`) | The real-world gotchas: nvm node-version mismatch, port conflicts, bare-`url` failure, minimal PATH, two-machine sessions. |

## Installation

**Option A — marketplace (recommended):**

```
/plugin marketplace add hiphapis/docs-with-obsidian
/plugin install docs-with-obsidian@docs-with-obsidian
/reload-plugins
```

**Option B — local clone (for development):**

```bash
git clone https://github.com/hiphapis/docs-with-obsidian.git
claude --plugin-dir ./docs-with-obsidian
```

The skill registers as `docs-with-obsidian:docs-with-obsidian` and triggers
whenever you ask to organize project docs into Obsidian, set up a docs vault,
consolidate fragmented documentation, connect Obsidian to Claude Desktop/Code
via MCP, or migrate docs into a vault — even if you don't say "Obsidian" or
"skill" explicitly.

## Usage

The skill has **two tracks**. Most projects need both, in order.

### Track A — Consolidate & migrate (Claude Code)

Run this in a **normal interactive session** — it's judgment-heavy and needs
human approval gates, so do **not** run it inside an autonomous loop.

1. **Inventory first, move nothing yet.** Find every doc across the repo,
   including tool-generated files. Classify each and produce a table:
   `[KEEP-tool]` machinery · `[KEEP-log]` session scratch ·
   `[MOVE-knowledge]` real project knowledge · `[MIXED]` machinery containing
   knowledge. **Stop for human sign-off.**
2. **Never delete.** Move files, leaving a short **stub** at the old path
   (`status: stub`, `moved_to: …`, plus a wikilink) so nothing breaks.
3. **Folder skeleton as a hypothesis.** Start from `assets/vault-structure.md`;
   propose additions/merges only where the real docs don't fit. Keep top-level
   folders to ~6–8.
4. **Add frontmatter + wikilinks.** Every note gets `title`, `status`,
   `source`, `updated`, and `[[links]]` to related notes to prevent
   re-fragmentation.
5. **Reconstruct ADRs** where the rationale is recoverable; mark uncertain ones
   "confirm needed" — never invent one.
6. **Update `.gitignore`** (only the churn-y Obsidian files) and **`CLAUDE.md`**
   to declare the vault the source of truth.

### Track B — Connect Claude Desktop & apply instructions

1. **Open `<repo>/docs` as its own vault** in Obsidian, separate from any
   personal mega-vault, so the MCP only exposes this project.
2. **Install the "Claude Code MCP" community plugin.** It exposes two servers: a
   **WebSocket** server (for Claude Code via `/ide`) and an **HTTP/SSE** server
   (for Claude Desktop, at `http://localhost:<HTTP_PORT>/sse`).
3. **Unique HTTP port per vault** if you run more than one (e.g. this project
   `22361`, personal vault `22360`) — otherwise they fight over the port.
4. **Wire Claude Desktop via the `mcp-remote` stdio bridge.** Do **not** paste a
   bare `"url"` into `claude_desktop_config.json` — Desktop validates stdio only
   and silently drops it. Snippet in `assets/claude-desktop-config-snippet.md`.
   Fully quit (Cmd+Q) and relaunch afterward.
5. **Connect Claude Code:** `claude` → `/ide` → select **Obsidian**. No config
   file needed.
6. **Verify** with a read test (list vault files) and a write test (create a
   note, confirm it appears live in Obsidian).
7. **Generate project instructions** from
   `assets/project-instructions-template.md`, tailored to this project's MCP
   server name and folder categories, and paste into the claude.ai project's
   Custom Instructions.

## Vault structure

A lifecycle-based starting skeleton (adapt to the project during inventory):

```
<repo>/docs/                 ← open THIS as the Obsidian vault
├── .obsidian/               # Obsidian + plugin settings
├── 00-dashboard/            # index, project status, open TODOs, deadlines
├── 01-business/             # business plan, pricing, market research
├── 02-product/              # PRD, feature specs, checklists
├── 03-decisions-adr/        # ADRs (one per decision)
├── 04-<domain-content>/     # domain artifacts
├── 05-research/             # investigations, comparisons
├── 06-dev-rules/            # engineering conventions (git, testing…)
└── _templates/              # note templates (ADR, domain notes)
```

**Top layer = lifecycle-based** (business vs product vs decisions vs research):
these rarely change and are expensive to re-org because it breaks links.
Sub-folders and names are cheap and should grow from real content.

## Parameters to fill per project

Resolve these first (ask if unknown):

| Placeholder | Meaning | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | Human-facing project name | OurStory |
| `{{MCP_SERVER_NAME}}` | Name of the server in Desktop config | obsidian-ourstory |
| `{{VAULT_PATH}}` | Absolute path to the vault | /Users/you/ourstory/docs |
| `{{HTTP_PORT}}` | Obsidian plugin HTTP/SSE port (unique per vault) | 22361 |
| `{{NPX_PATH}}` | Absolute path to npx (`which npx`) | /Users/you/.nvm/.../bin/npx |

## Guardrails (non-negotiable)

- **Never delete docs** — move + stub, or archive. Keep a migration map.
- **Never touch tool machinery** (`superpowers/`, `plans/`, `specs/`,
  `.claude/`) except to *update* `CLAUDE.md` with the source-of-truth rule.
- **Inventory before migrating**; get human sign-off on the classification.
- **Don't run Track A inside an autonomous loop** — it needs approval gates.
- **Never invent facts** written into the vault; mark unconfirmed values with a
  placeholder.

## Layout

Single-plugin repo — the repo root **is** the plugin, and also its own
one-plugin marketplace (`source: "./"`):

```
.
├── .claude-plugin/
│   ├── marketplace.json     # marketplace registry (source: "./")
│   └── plugin.json          # plugin manifest
├── skills/docs-with-obsidian/
│   ├── SKILL.md             # the methodology
│   ├── references/          # detailed Track A / Track B / troubleshooting
│   └── assets/              # templates, prompts, config snippets
└── README.md
```

## Publishing

Authored by [Johan Kim](https://github.com/hiphapis). The repo must be
**public** for Claude Code to fetch it. Bump `version` in
`.claude-plugin/plugin.json` on every change that should reach installed users —
a version bump is the update signal.

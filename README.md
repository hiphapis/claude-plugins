# docs-with-obsidian

A Claude Code plugin that packages a full methodology for turning a software
project's documentation into a single, well-organized, link-rich **Obsidian
vault** shared by Claude Code, Claude Desktop, and you via git.

It bundles one skill (`docs-with-obsidian`) covering:

- **Claude Code side** — consolidate scattered docs into `<repo>/docs`,
  categorize, migrate existing files (inventory → approve → move + stub), add
  frontmatter and wikilinks, reconstruct ADRs, update `.gitignore` and
  `CLAUDE.md`.
- **Claude Desktop side** — install/configure the Obsidian "Claude Code MCP"
  plugin, wire Claude Desktop via the `mcp-remote` bridge, connect Claude Code
  via `/ide`, verify, and generate + apply project instructions.
- **Troubleshooting** — the real gotchas (nvm node-version mismatch, vault port
  conflicts, bare-`url` config failure, minimal PATH, two-machine sessions).

## Layout

Single-plugin repo — the repo root **is** the plugin, and also its own
one-plugin marketplace (`source: "./"`):

```
.
├── .claude-plugin/
│   ├── marketplace.json   # marketplace registry (source: "./")
│   └── plugin.json        # plugin manifest
├── skills/docs-with-obsidian/
│   ├── SKILL.md
│   ├── references/
│   └── assets/
└── README.md
```

## Install

```
/plugin marketplace add hiphapis/docs-with-obsidian
/plugin install docs-with-obsidian@docs-with-obsidian
/reload-plugins
```

The skill then registers as `docs-with-obsidian:docs-with-obsidian` and
triggers when you ask to organize project docs into Obsidian, set up a docs
vault, consolidate fragmented docs, connect Obsidian to Claude Desktop/Code via
MCP, or migrate docs into a vault.

## Publishing

Authored by [Johan Kim](https://github.com/hiphapis). The repo must be
**public** for Claude Code to fetch it. Bump `version` in
`.claude-plugin/plugin.json` on every change that should reach installed users —
a version bump is the update signal.

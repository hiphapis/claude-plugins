# docs-with-obsidian

A personal [Claude Code plugin marketplace](https://code.claude.com/docs/en/discover-plugins).
Currently ships one plugin: **docs-with-obsidian**.

## Structure

```
.
├── .claude-plugin/marketplace.json     # marketplace registry
└── plugins/
    └── docs-with-obsidian/
        ├── .claude-plugin/plugin.json  # plugin manifest
        ├── skills/docs-with-obsidian/
        │   ├── SKILL.md
        │   ├── references/
        │   └── assets/
        └── README.md
```

## Publish (do this from Claude Code / your machine)

1. Create a **public** GitHub repo named `docs-with-obsidian`.
2. Push:
   ```bash
   git init
   git add .
   git commit -m "docs-with-obsidian plugin v0.1.0"
   git branch -M main
   git remote add origin git@github.com:hiphapis/docs-with-obsidian.git
   git push -u origin main
   ```

## Install (in Claude Code)

```
/plugin marketplace add hiphapis/docs-with-obsidian
/plugin install docs-with-obsidian@docs-with-obsidian
/reload-plugins
```

## Versioning

Bump `version` in **both** `marketplace.json` and the plugin's `plugin.json`
on every change that should reach installed users — a version bump is the update
signal.

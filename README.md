# obsidian-docs-marketplace

A personal [Claude Code plugin marketplace](https://code.claude.com/docs/en/discover-plugins).
Currently ships one plugin: **obsidian-project-docs**.

## Structure

```
.
├── .claude-plugin/marketplace.json     # marketplace registry
└── plugins/
    └── obsidian-project-docs/
        ├── .claude-plugin/plugin.json  # plugin manifest
        ├── skills/obsidian-project-docs/
        │   ├── SKILL.md
        │   ├── references/
        │   └── assets/
        └── README.md
```

## Publish (do this from Claude Code / your machine)

1. Create a **public** GitHub repo named `obsidian-docs-marketplace`.
2. Push:
   ```bash
   git init
   git add .
   git commit -m "obsidian-project-docs plugin v0.1.0"
   git branch -M main
   git remote add origin git@github.com:hiphapis/obsidian-docs-marketplace.git
   git push -u origin main
   ```

## Install (in Claude Code)

```
/plugin marketplace add hiphapis/obsidian-docs-marketplace
/plugin install obsidian-project-docs@obsidian-docs-marketplace
/reload-plugins
```

## Versioning

Bump `version` in **both** `marketplace.json` and the plugin's `plugin.json`
on every change that should reach installed users — a version bump is the update
signal.

# hiphapis/claude-plugins

[English](README.md) | [한국어](README.ko.md)

A [Claude Code](https://claude.com/claude-code) plugin marketplace with the plugins I build and use every day.

## Install

```
/plugin marketplace add hiphapis/claude-plugins
/plugin install <plugin>@hiphapis
```

## Plugins

| Plugin | What it does | Source |
|---|---|---|
| [docs-with-obsidian](plugins/docs-with-obsidian) | Turn a project's docs into an Obsidian vault in the repo's `/docs` folder, shared by Claude Code, Claude Desktop, and you via git | this repo |
| [worktree-teardown](plugins/worktree-teardown) | Audit a git worktree before deleting it so nothing gets lost. The human runs the delete | this repo |
| [common-rules](plugins/common-rules) | Merge my personal agent working rules (orchestrator/worker split, Orca worktrees, issue lifecycle, gates, git, completion reports, docs) into a repo's existing rules. Asks how to resolve each conflict and records the decisions | this repo |
| [loopcraft](https://github.com/hiphapis/loopcraft) | Loop engineering: persistent memory vault, self-correction hooks, failure-to-knowledge distillation | [hiphapis/loopcraft](https://github.com/hiphapis/loopcraft) |

Small plugins live under `plugins/`. Larger plugins with their own tests, hooks, and release cadence keep their own repository and are listed here by reference.

## Layout

```
.claude-plugin/marketplace.json   # catalog of every plugin
plugins/<name>/                   # one plugin per folder
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
```

## Adding a plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json` and `skills/`.
2. Add an entry to `.claude-plugin/marketplace.json`.
3. Run `claude plugin validate .` and `claude plugin validate plugins/<name>`.

## License

MIT

# common-rules

[한국어](README.ko.md)

A Claude Code skill that merges my personal set of agent working rules into **the rules a repo already has**.

The rules cover the orchestrator/worker split (the orchestrator never edits code — not even one line), Orca worktrees, the GitHub issue lifecycle, test gates, git, completion reports, and docs. They live in [`references/rules.md`](skills/common-rules/references/rules.md), each with an ID, a star rating, a reason, and prerequisite tags (`[gh]`, `[vault]`, `[ko]`, `[personal]`). The rules themselves are written in Korean. They assume you run an orchestrator and workers on Orca, so the Orca rules go into every repo.

## Why a merge, not a template

Workers such as Codex read the repo's `AGENTS.md` and `docs/`, not Claude skills, so the rules have to land in the repo as real files. And most repos already have rules. The skill:

1. reads every existing rule document end to end,
2. classifies each common rule as **same / partial / missing / conflict**,
3. adds what's missing and fills in partial rules without asking,
4. asks you how to resolve each conflict (replace, keep the repo's rule, or adjust),
5. records the version and your decisions in `AGENTS.md`, so the next run only looks at rules that are new or changed.

It never decides a conflict on its own. When it cannot ask (a subagent or a non-interactive run), it leaves conflicts untouched and reports them as undecided.

## Install

```
/plugin marketplace add hiphapis/claude-plugins
/plugin install common-rules@hiphapis
```

## Use

In the repo you want to update:

> /common-rules
> 이 리포에도 공통 룰 넣어줘

## License

MIT

# common-rules

[한국어](README.ko.md)

A Claude Code skill that merges my personal set of agent working rules into **the rules a repo already has**.

The rules cover the orchestrator/worker split (the orchestrator never edits code — not even one line), Orca worktrees, the GitHub issue lifecycle, test gates, git, completion reports, and docs. They live in [`references/rules.md`](skills/common-rules/references/rules.md), each with an ID, a star rating, a reason, and prerequisite tags (`[gh]`, `[vault]`, `[ko]`, `[personal]`). The rules themselves are written in Korean. They assume you run an orchestrator and workers on Orca, so the Orca rules go into every repo.

## Before you install

- **Built on the assumption that you work on [Orca](https://github.com/stablyai/orca).** Worktrees are created with `orca worktree`, and workers are launched and supervised (`dispatch`, waiting on `worker_done`) through `orca orchestration`. The Orca rules (R-ORCA) carry no prerequisite tag and go into every repo, so without Orca many of the role and worktree rules cannot be followed.
- **The orchestrator and workers are separate.** The session you talk to (the orchestrator) never edits code; workers launched by Orca write it. Worker settings are built into the rules as current values (implementation `claude-sonnet-5-5`, review `claude-opus-5-5`, effort `medium`). To change them, edit R-ROLE-04 in `rules.md`.
- **Some rules rely on other tools.** Have them ready if the repo will get those rules. If a tool is missing on the machine running the skill, it asks whether to install it and add the rules, add the rules only, or leave them out — plugins and `gh` are installed only with your consent, Orca and ego-browser get an install link (when it cannot ask, it adds the rules without installing anything and leaves a warning), and agents following the rules stop and ask instead of working around a missing tool (R-BASE-10):
  - the [worktree-teardown](../worktree-teardown) plugin — worktree audit right after a merge (R-ORCA-12)
  - `ccg` from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) — three-model consensus, only for irreversible changes (R-ROLE-09)
  - the `gh` CLI — GitHub issue lifecycle (`[gh]` rules)
  - the `ego-browser` skill — browser checks (`[personal]` rules)
- **These are personal rules.** The rule text is in Korean, and personal preferences such as output language and browser choice are tagged `[personal]`. In a repo shared with others, you will usually want to leave `[personal]` rules out.
- **Some rules act outside the repo.** `[outward]` rules — auto-pushing doc commits, pushing work that has already been deployed to production, closing issues automatically, deploying without asking — are confirmed with you before they go in, even when nothing in the repo's rules conflicts with them.
- **It edits files in your repo.** It writes rules and an application record into `AGENTS.md` and `docs/` rule documents. Run it on a clean working tree and review the result with `git diff`.

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

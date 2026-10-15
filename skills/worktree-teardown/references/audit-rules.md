# Audit rules

The full procedure for `worktree-teardown`. `SKILL.md` is the entry point; this file is the rulebook.

## 0. Why this exists

Deleting a worktree rarely loses *commits* — git refuses to remove a dirty worktree without `--force`. Real losses come from three other places:

1. **Gitignored assets** — handoff notes, plans, generated media, locally edited `.env` files live only in that directory.
2. **Skipped wrap-up** — the issue is still `in progress`, the tool's workspace status was never updated, docs were never touched.
3. **Records that disagree with reality** — notes say "unmerged" when it was merged (or the reverse, and someone re-implements it).

**Don't assume what the delete command does.** Whether it deletes the branch or uses `--force` varies by tool and UI. If commits are unpushed or unmerged, it is BLOCKED regardless.

## 1. Resolve the target

**Orca-managed** (the `orca` CLI exists and the path appears in `orca worktree list --json`):

```bash
orca worktree show --worktree <selector> --json
```

- Default selector: `active`. Use `path:` · `branch:` · `issue:` selectors. **Never `name:`** — display names contain spaces and symbols and differ from the directory name. If the human gives a name, look up its path in `orca worktree list --json` and use `path:`.
- Read: `branch` (strip `refs/heads/`), `baseRef`, `linkedIssue`, `workspaceStatus`, `childWorktreeIds`, `path`, `isMainWorktree`.

**Plain git** (no Orca, or not Orca-managed):

```bash
git worktree list --porcelain
```

- The **first entry is the main worktree.** If the target path equals it → `ABORT`.
- Base ref: `git -C <wt> symbolic-ref --short refs/remotes/origin/HEAD` (e.g. `origin/main`). If that fails, **ask** — never hardcode `main`.
- Linked issue: try the branch name (`issue-<n>`, `<n>-…`, `…/#<n>`). Otherwise "unlinked".
- Child worktrees: N/A (git has no lineage).

Run **every** git command as `git -C <worktree-path>`, even for the current worktree, so the target can't drift.

## 2. Item states

| Mark | Meaning | To reach SAFE |
| --- | --- | --- |
| 🔴 BLOCKED | Unrecoverable loss on delete, or a required procedure not done | Must be resolved |
| 🟡 Check | Needs human judgment, or not a loss but at risk of being forgotten | Human says "fine" |
| ✓ OK | — | Folded into one line |
| N/A | The project doesn't use this tool/convention | Mention once, doesn't block |

**N/A vs 🟡:** `orca` not installed, worktree not Orca-managed, remote is not GitHub, project has no issue convention → N/A. Tool is used but the call **failed** (auth, network, unknown issue) → 🟡 with the error. Unverified is never ✓.

> ⚠️ **Output-rewriting shell hooks flip verdicts silently.** If a hook such as rtk rewrites commands, run audit commands through its bypass (`rtk proxy git …`). Observed failures: the `--format` argument of `git stash list` was swallowed (owner branch vanished), and `git log … | wc -l` counted the hook's one-line `ok` summary, reporting a merged branch as "1 unmerged commit". Mechanical checks depend on raw output, so a rewriting layer turns bugs into *wrong OK verdicts*, not errors. Prefer reading the raw output over counting lines.

## 3. Audit items

10 mechanical items (decided by command output) and 1 judgment item. Item 10 has one judgment step (extraction), then is mechanical. **Judgment items never auto-assign BLOCKED.**

| # | Item | How | BLOCKED when |
| --- | --- | --- | --- |
| 1 | Uncommitted tracked changes | `git -C <wt> status --porcelain --untracked-files=no` | Output not empty |
| 2 | Untracked, not ignored | `git -C <wt> ls-files --others --exclude-standard` | Output not empty |
| 3 | Unpushed commits | §3.1 | See table |
| 4 | Unmerged commits | §3.2 | Commits exist → 3-way choice |
| 5 | Stash | §3.3 | Branch-owned stash + branch discarded |
| 6 | Non-regenerable ignored assets | §3.4 | Preserve-class assets exist |
| 7 | Issue state | §3.5 | Per project policy |
| 8 | Orca workspace status | §3.5 (crossed with 7) | — |
| 9 | Child worktrees | Orca `childWorktreeIds` | Not empty |
| 10 | Canonical-doc drift | §3.6 | A fact this work removed survives in a canonical path |
| 11 | Record consistency | §3.7 (judgment) | never |

Item 2: entries matching the §3.4 **skip** class (e.g. a tool-state `.omc/state/` that isn't gitignored yet) fold into one ✓ line with a suggestion to add them to `.gitignore` — they're regenerable, not a loss. Everything else is 🔴.

Items 1–2: **propose only** — commit, add to `.gitignore`, or copy to main. Never commit on the human's behalf (pathspec accidents sweep in other people's files).

Item 9: children may depend on the parent path; clean them up first or break the lineage.

### 3.1 Unpushed commits

```bash
git -C <wt> rev-parse --abbrev-ref --symbolic-full-name @{u}   # upstream?
git -C <wt> log --oneline @{u}..HEAD                            # with upstream
git -C <wt> log --oneline <baseRef>..HEAD                       # without upstream
```

| Upstream | Verdict |
| --- | --- |
| Yes, `@{u}..HEAD` empty | ✓ |
| Yes, commits exist | 🔴 → `git -C <wt> push` |
| **No**, commits vs base exist | 🔴 no remote copy → `git -C <wt> push -u origin <branch>` |
| No, no commits | ✓ (empty branch) |

### 3.2 Unmerged commits

```bash
git -C <wt> log --oneline <baseRef>..HEAD
git -C <wt> cherry <baseRef> <branch>          # squash / cherry-pick merges
```

If `log` shows commits but `cherry` returns only `-` lines, **the content is already in base** (squash merge). Downgrade to "content merged · ref ahead". Look at both signals.

Truly unmerged → **ask the human to choose**:

| Choice | What the skill does |
| --- | --- |
| **Merge** | **Run step 5 (wrap-up) first** — issue, records and docs don't depend on the merge. Then hand off (`superpowers:finishing-a-development-branch` if installed, else present merge commands) and end as `HANDOFF`. Ask them to re-run the audit after merging |
| **Keep** | Keep the branch, delete only the worktree. Record the reason and the resume trigger (issue comment + the project's status record) |
| **Discard** | Record the reason. **Present** — don't run — the `not planned` close and branch deletion |

For Keep and Discard, **the record is the completion condition.** Branches that vanish without a record cause duplicate work.

### 3.3 Stash

```bash
git -C <wt> stash list --format='%gd|%gs'
```

Stash is repo-wide, so deleting the worktree doesn't lose it. Identify the owner from `WIP on <branch>` / `On <branch>`.

| Owner | Branch fate | Verdict |
| --- | --- | --- |
| Target branch | Keep / merge | 🟡 forgotten work |
| Target branch | Discard | 🔴 nowhere to apply it. `git stash show -p`, then drop or move |
| **Branch that no longer exists** | — | 🟡 **orphan stash** — a worktree was deleted without this audit |
| Another live branch | — | Not reported |

### 3.4 Non-regenerable ignored assets

```bash
git -C <wt> ls-files --others --ignored --exclude-standard --directory
```

**Blacklist** — skip only what matches the skip rules, **report everything else.**

| Class | Patterns | Handling |
| --- | --- | --- |
| Skip | Build/deps: `node_modules/` `.next/` `dist/` `build/` `out/` `.turbo/` `coverage/` `.vercel/` `target/` `__pycache__/` `.venv/` `venv/` `.pytest_cache/` `.mypy_cache/` `.gradle/` `*.tsbuildinfo` `*.log` `.DS_Store`. Tool state (if present): `.omc/state/` `.omc/sessions/` `.omc/project-memory.json` `.loop/state/` | One-line count |
| Conditional skip | `.env` `.env.*` | **Compare contents**: `diff -q <wt>/<rel> <main>/<rel>`. Identical → skip. **Different or missing in main → 🔴.** Existence is useless: a worktree `.env` is a copy of main's |
| 🔴 Preserve | Agent notes (if present): `.omc/handoffs/` `.omc/plans/` `.omc/research/` `.omc/artifacts/` `.omc/notepad.md` `.omc/ultragoal/` | Lost with the worktree. Propose `cp -r` into main |
| 🔴 Preserve | Media / generated: `*.png` `*.jpg` `*.webp` `*.gif` `*.mp4` `*.wav` `*.mp3` `*.pdf` `*.docx` `*.pptx` `*.xlsx` | May be the only copy |
| 🟡 Check | Open-document lock files: `.~lock.*#` (LibreOffice) · `~$*` (MS Office) | Being edited right now. Close the app, re-audit |
| 🔴 Preserve | Anything not matched above | Unknown = for the human to judge |

Report size with `du -sh` (the human decides whether to copy hundreds of MB).

Path rules:

1. Skip patterns are **not anchored** — `.omc/` etc. can appear in subdirectories. Apply them anywhere in the path.
2. `--directory` **folds** directories. Expand a folded directory one level; if everything inside is skip-class, skip it too. Otherwise a nested `sub/.omc/` holding only `state/` shows up as 🔴 every time.

### 3.5 Issue state + Orca status (items 7 · 8)

Only when the remote is GitHub and an issue is linked:

```bash
gh issue view <n> --json state,stateReason,title,labels,comments
```

**Generic default** (project declares no labels):

| Issue | Verdict |
| --- | --- |
| closed | ✓ |
| open | 🟡 — is the work done? Close it or record why it stays open |
| unlinked | 🟡 — work without an issue, or just a missing link? (N/A if the project has no issue convention) |

**With project labels** (from the project policy layer), map them onto these rows:

| Issue | Orca status | Verdict |
| --- | --- | --- |
| open + *in-progress* label | any | 🔴 completion procedure not run |
| open + *in-review* label | any | 🔴 same row as in-progress — done but not wrapped up. If verification waits on something external, comment the reason + resume condition, finish the rest of wrap-up, then downgrade to 🟡 |
| **closed** | **not `completed`** | 🔴 issue finished but the workspace status didn't follow → `orca worktree set --worktree <sel> --workspace-status completed` |
| closed | `completed` | ✓ |
| open + *blocked* / *on-hold* | any | 🟡 intentional pause? Is the reason recorded? |
| open + *ready* label | any | 🟡 a "not started" label on a worktree with commits — the label didn't follow the work |
| open, no label | any | 🟡 |

**Cross-check redundant representations.** If the project encodes state twice (e.g. label *and* title emoji), a mismatch between them is itself a sign the procedure stopped halfway → 🟡. Reading labels alone lets that through.

Orca `workspaceStatus` alone is usually `in-progress` everywhere and only produces alert fatigue — judge it only crossed with the issue. No Orca → item 8 is N/A.

The wrap-up commands come from the project's completion procedure. Without one, the generic wrap-up is: comment changes/verification/remaining risk on the issue → update docs → close as completed (with approval).

### 3.6 Canonical-doc drift (item 10)

**"Did docs change?" is not a completeness check** — one changed line passes it while other docs still state the old fact. Instead ask: **did a fact this work removed survive in the docs?**

**Step 1 — extract (judgment).** Name **only 3–5** facts this work invalidated: versions, commands, providers, table names — things docs state as fact. The diff's `-` lines are raw material, not the list (a real run had 337 lines; 2 facts mattered).

```bash
git -C <wt> diff <baseRef>...HEAD | grep '^-' | grep -v '^---'
```

**Step 2 — find survivors (mechanical).**

```bash
grep -rn '<removed fact>' <wt>/docs <wt>/README.md <wt>/CLAUDE.md <wt>/AGENTS.md
```

If the project keeps sibling agent indexes (`CLAUDE.md` + `AGENTS.md`), scan **both**. Add the user's Claude memory directory (`~/.claude/projects/<project>/memory/`) explicitly — it's outside the repo.

**Step 3 — split by path.** Survivors aren't defects by themselves; **history records are usually the majority** (a real run: 21 survivors, 7 canonical, 14 history). Without the split you get 20+ 🔴 every run and people ignore the rule.

| Path | Nature | Handling |
| --- | --- | --- |
| Project-declared canonical paths; default: `README*`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING*`, `docs/**` outside history dirs, ADR tables/frontmatter/status banners | States current facts | 🔴 list file:line |
| Project-declared history paths; default: `**/plans/**`, `**/specs/**`, ADR bodies (past reasoning, alternatives, timeline), `CHANGELOG*`, completed-history table rows | Snapshot of the time | Skip — editing forges past reasoning |
| Everything else | Judgment | 🟡 show the human |

If a major decision changed (stack, vendor, policy), check whether an ADR is needed, and grep existing ADR follow-up lists for open items pointing at this work.

### 3.7 Record consistency (item 11 · judgment)

Grep the project's record files (from the policy layer; defaults: any status/roadmap doc, agent state files such as `.loop/memory/STATE.md`, the user's Claude memory dir) for **① branch name and issue number ② the removed facts from §3.6**, then compare with reality.

- Output example: 🟡 "notes say unmerged, actually merged — update the record".
- Branch/issue keys alone catch only half: a note can state a now-false command without mentioning any branch.
- **Both directions**: records lagging reality, and work that exists nowhere in the records.

## 4. Report format

Every finding has three parts: **what is lost → where it is → one-line fix.** Executable, not prose. The count in parentheses is **findings, not items**.

```
[audit] feature/search-filters  ·  /path/to/worktrees/search-filters

🔴 BLOCKED (4)
1. 2 unpushed commits — no remote copy
   → git -C <wt> push -u origin feature/search-filters
2. .omc/handoffs/ 3 files · 12KB — lost with the worktree
   → cp -r <wt>/.omc/handoffs <main>/.omc/
3. Issue #128 open · in progress — no completion comment
   → project completion procedure (run by the skill after approval)
4. 3 canonical docs still state removed fact 'Node 18' (9 history records excluded)
   → README.md:14 · docs/setup.md:22 · AGENTS.md:40

🟡 Check (1)
5. .~lock.Q3-report.docx# — open in LibreOffice
   → close the app and re-audit

✓ OK (5): no uncommitted · no untracked · merged · no stash · regenerable assets skipped
N/A (1): Orca status (worktree not Orca-managed)

→ Handle 2·3·4 now? (5 is your call)
```

## 5. Flow detail

1. **Resolve target** (§1). Main worktree → stop
2. **Collect mechanical items** 1–10 (item 10 after its extraction step). Parallel
3. **Evaluate judgment item** 11
4. **Report + approval** — batch everything fixable into one question
5. **Approved wrap-up** — issue comment/labels/title, Orca status, docs, record updates, asset copies. **Copy, never move or delete**
6. **Re-audit** mechanical items
7. **End** (§6)

Choosing "merge" in §3.2 does **not** hand off at step 4. Step 5 is the only step that turns findings into fixes; exiting early skips step 5, step 6 and the SAFE gate, and every 🟡 already reported is silently dropped. Merge is the most common exit path, so this hole sits on the default path.

## 6. End states

| State | When | Output |
| --- | --- | --- |
| `SAFE` | 0 BLOCKED · all 🟡 passed by the human | Present the delete command — `orca worktree rm --worktree path:<p>` (Orca) or `git worktree remove <path>` (git). **Never `--force`. The human runs it** |
| `BLOCKED(n)` | Unresolved BLOCKED remain | Remaining items and why. **No delete command** |
| `HANDOFF` | "Merge" chosen | After step 5: the hand-off, plus anything that couldn't be done before the merge |
| `ABORT` | Target unresolved · main worktree · required tool failed in a way that prevents auditing | Where and why |

## 7. Safety contract

1. Never delete the worktree. Present the command only.
2. Never commit uncommitted changes on the human's behalf.
3. Never merge, rebase or push. Present push commands only.
4. Never delete or move files. Preserve by **copying**.
5. Never close an issue without approval. Never run a `not planned` close even with approval — present it.
6. Never report a failed check as OK.

Read-only audit + minimal writes after approval: even a wrong audit can't be destructive.

## 8. Adding a new audit item

Check that the trigger actually implies the condition. "Docs changed" is not "docs are correct"; "issue number is mentioned" is not "the record is true". Weak proxies were the root cause of the misses this rulebook was revised for.

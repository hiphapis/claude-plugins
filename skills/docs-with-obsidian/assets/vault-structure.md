# Default vault skeleton (a hypothesis, not a mandate)

Use this as the starting structure, then adjust to the project's actual docs
during Phase-1 inventory. Keep top-level folders to ~6–8; avoid one-folder-per-
file. Folder names can be localized (the reference project used Korean labels).

```
<repo>/docs/                     ← open THIS as the Obsidian vault
├── .obsidian/                   # Obsidian + plugin settings (mostly committed)
├── 00-dashboard/                # index, project-status, service-overview
│   └── home.md                  # deadlines, open items, placeholder list
├── 01-business/                 # business plan, pricing, market research
├── 02-product/                  # PRD, feature specs, checklists
├── 03-decisions-adr/            # ADRs (one per decision)
│   ├── README.md
│   ├── template.md
│   └── 0001-*.md ...
├── 04-<domain-content>/         # domain artifacts (e.g. story templates)
├── 05-research/                 # investigations, comparisons
├── 06-dev-rules/                # engineering conventions (git, testing, TTS…)
└── _templates/                  # note templates (ADR, domain notes)
```

Localized example (reference project):
`00-대시보드 / 01-사업 / 02-제품 / 03-의사결정(ADR) / 04-동화 / 05-조사 /
06-개발규칙 / _templates`

## Principles
- **Top layer = lifecycle-based** (business vs product vs decisions vs research).
  These rarely change and are expensive to re-org (breaks links). Sub-folders
  and names are cheap to adjust and should grow from real content.
- A dashboard note in `00-*` is the entry point: index + open TODOs +
  unconfirmed-value placeholders + deadlines.
- Tool logs (superpowers/, plans/, specs/) are NOT knowledge folders. Keep them
  out of the numbered knowledge tree, or clearly separated.

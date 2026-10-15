# ADR note template

Copy into `_templates/` and into the ADR folder as `NNNN-<slug>.md`.

---

```markdown
---
title: "ADR-{{NNNN}}: {{short decision title}}"
status: proposed        # proposed | accepted | superseded
date: {{YYYY-MM-DD}}
supersedes:             # ADR number(s) this replaces, if any
source:                 # where this rationale was recovered from
---

# ADR-{{NNNN}}: {{short decision title}}

## Decision
{{The choice made, in one or two sentences.}}

## Context
{{What situation/constraint forced a decision. Note hard drivers
(e.g. a payment/voucher restriction, a region requirement).}}

## Rationale
{{Why this option over the alternatives. If a rationale can't be verified,
write: 〔confirm needed〕 and leave it — do not fabricate.}}

## Alternatives considered
- {{option A}} — {{why not}}
- {{option B}} — {{why not}}

## Impact
{{What this changes downstream: architecture, cost, other docs. Link them
with [[wikilinks]].}}
```

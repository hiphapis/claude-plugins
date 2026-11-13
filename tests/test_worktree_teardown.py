"""worktree-teardown: 스킬 설명과 감사 규칙 표의 항목 수가 일치하는지 검사.

감사 항목 수는 SKILL.md description(트리거·요약)과 audit-rules.md 표, 표 위 요약 문장
세 곳에 있다. 항목을 추가할 때(audit-rules.md §8) 한 곳만 고치면 스킬이 항목을 빠뜨린다.
"""

from __future__ import annotations

import re

from conftest import PLUGINS_DIR, read, split_frontmatter

SKILL_DIR = PLUGINS_DIR / "worktree-teardown" / "skills" / "worktree-teardown"
AUDIT = read(SKILL_DIR / "references" / "audit-rules.md")
SECTION3 = AUDIT.split("## 3. Audit items", 1)[1].split("\n### ", 1)[0]
ROWS = [
    [c.strip() for c in line.strip().strip("|").split("|")]
    for line in SECTION3.splitlines()
    if re.match(r"^\|\s*\d+\s*\|", line)
]


def test_audit_items_are_numbered_sequentially():
    assert [int(r[0]) for r in ROWS] == list(range(1, len(ROWS) + 1))


def test_skill_description_count_matches_table():
    meta, _ = split_frontmatter(read(SKILL_DIR / "SKILL.md"))
    m = re.search(r"Runs (\d+) audit items", meta["description"])
    assert m, "description에서 감사 항목 수를 찾지 못했다"
    assert int(m.group(1)) == len(ROWS)


def test_mechanical_plus_judgment_matches_table():
    m = re.search(r"(\d+) mechanical items .*? and (\d+) judgment item", SECTION3)
    assert m, "§3 요약 문장을 찾지 못했다"
    mechanical, judgment = int(m.group(1)), int(m.group(2))
    assert mechanical + judgment == len(ROWS)
    # 판단 항목은 자동으로 BLOCKED를 주지 않는다 → 표의 BLOCKED 칸이 never
    never = [r for r in ROWS if r[-1].lower() == "never"]
    assert len(never) == judgment


def test_section_references_in_table_exist():
    sections = set(re.findall(r"^### (3\.\d+) ", AUDIT, re.M))
    cited = set(re.findall(r"§(3\.\d+)", "\n".join("|".join(r) for r in ROWS)))
    assert cited <= sections, f"표가 없는 절을 가리킨다: {cited - sections}"

"""common-rules 룰 카탈로그(rules.md)의 버전·ID 규약 검사.

스킬은 재실행 때 `(vN 변경|추가)` 표시와 룰 ID 주석으로 "새로 바뀐 룰만" 다시 대조한다.
그래서 버전 표기, 변경 표시, ID 참조가 어긋나면 이미 적용한 리포에서 룰이 조용히 누락된다.
"""

from __future__ import annotations

import re
from collections import defaultdict

import pytest

from conftest import PLUGINS_DIR, load_json, read

PLUGIN = PLUGINS_DIR / "common-rules"
SKILL_DIR = PLUGIN / "skills" / "common-rules"
RULES_MD = SKILL_DIR / "references" / "rules.md"
RULES = read(RULES_MD)

ALLOWED_TAGS = {"gh", "vault", "ko", "personal", "outward"}
HEADING = re.compile(
    r"^### (?P<id>R-(?P<cat>[A-Z]+)-(?P<num>\d{2})) (?P<title>.+?) (?P<stars>★{1,5})"
    r"(?P<tags>(?: \[[a-z]+\])*)(?: \(v(?P<ver>\d+) (?P<kind>변경|추가)\))?$"
)
# R-ROLE-06~08·10·11, R-BASE-01～03·08 같은 묶음 표기도 개별 ID로 풀어낸다
ID_GROUP = re.compile(r"R-([A-Z]+)-(\d{2})((?:[~～·]\d{2})*)")

HEADER_VERSION = int(re.search(r"^- 버전: \*\*v(\d+)\*\*", RULES, re.M).group(1))
HISTORY = RULES.split("## 변경 이력", 1)[1]
HISTORY_ENTRIES = {
    int(m.group(1)): m.group(2)
    for m in re.finditer(r"^- v(\d+) \([\d-]+\): (.*)$", HISTORY, re.M)
}


def _rule_headings() -> list[re.Match]:
    return [HEADING.match(l) for l in RULES.splitlines() if l.startswith("### R-")]


def expand_ids(text: str) -> set[str]:
    ids = set()
    for cat, first, tail in ID_GROUP.findall(text):
        nums = [int(first)]
        for sep, n in re.findall(r"([~～·])(\d{2})", tail):
            n = int(n)
            nums.extend(range(nums[-1] + 1, n + 1) if sep in "~～" else [n])
        ids.update(f"R-{cat}-{n:02d}" for n in nums)
    return ids


DEFINED = [m.group("id") for m in _rule_headings() if m]


def test_every_rule_heading_follows_format():
    bad = [l for l in RULES.splitlines() if l.startswith("### R-") and not HEADING.match(l)]
    assert not bad, f"형식(### ID 제목 ★ [태그] (vN 변경|추가))을 벗어난 헤딩: {bad}"


def test_rule_ids_are_unique():
    dupes = {i for i in DEFINED if DEFINED.count(i) > 1}
    assert not dupes, f"중복된 룰 ID: {dupes}"


def test_rule_numbers_have_no_gaps_per_category():
    """새 룰은 범주의 다음 번호를 쓰고 번호를 다시 매기지 않는다(SKILL.md 유지보수 절)."""
    by_cat = defaultdict(list)
    for m in _rule_headings():
        by_cat[m.group("cat")].append(int(m.group("num")))
    for cat, nums in by_cat.items():
        assert sorted(nums) == list(range(1, max(nums) + 1)), f"R-{cat} 번호에 빈 곳이 있다: {sorted(nums)}"


def test_rule_tags_are_known():
    for m in _rule_headings():
        tags = set(re.findall(r"\[([a-z]+)\]", m.group("tags")))
        assert tags <= ALLOWED_TAGS, f"{m.group('id')}에 정의되지 않은 태그: {tags - ALLOWED_TAGS}"


def test_each_rule_has_rule_and_reason():
    blocks = re.split(r"^(?=### R-)", RULES.split("## 변경 이력")[0], flags=re.M)[1:]
    for block in blocks:
        rid = block.split()[1]
        assert re.search(r"^- 룰: \S", block, re.M), f"{rid}에 '- 룰:' 줄이 없다"
        assert re.search(r"^- 이유: \S", block, re.M), f"{rid}에 '- 이유:' 줄이 없다"


def test_rules_sit_under_matching_section_and_toc():
    toc = dict(re.findall(r"^(\d+)\. .+ \(R-([A-Z]+)\)$", RULES, re.M))
    sections = re.findall(r"^## (\d+)\. ", RULES, re.M)
    assert sorted(toc, key=int) == sections, "목차와 '## N.' 절이 일치하지 않는다"

    current = None
    for line in RULES.splitlines():
        if m := re.match(r"^## (\d+)\. ", line):
            current = toc[m.group(1)]
        elif m := HEADING.match(line):
            assert m.group("cat") == current, f"{m.group('id')}가 R-{current} 절 안에 있다"


# ---- 버전 규약 ----


def test_plugin_version_tracks_catalog_version():
    """관례: plugin.json 0.N.0 ↔ rules.md vN (지금까지 모든 버전업이 둘을 함께 올렸다)."""
    version = load_json(PLUGIN / ".claude-plugin" / "plugin.json")["version"]
    assert version == f"0.{HEADER_VERSION}.0", (
        f"rules.md는 v{HEADER_VERSION}인데 plugin.json은 {version}이다 — "
        "한쪽만 올리면 설치된 플러그인이 갱신되지 않거나 적용 기록 버전이 어긋난다"
    )


@pytest.mark.parametrize("readme", sorted(PLUGIN.glob("README*.md")), ids=lambda p: p.name)
def test_readme_states_current_version(readme):
    """README의 현재 버전 표기가 버전업 때 낡지 않게 한다."""
    text = read(readme)
    assert f"0.{HEADER_VERSION}.0" in text, f"{readme.name}에 현재 버전 0.{HEADER_VERSION}.0이 없다"
    assert f"v{HEADER_VERSION}," in text, f"{readme.name}에 룰 카탈로그 v{HEADER_VERSION} 표기가 없다"


def test_history_is_complete_and_matches_header():
    assert max(HISTORY_ENTRIES) == HEADER_VERSION, "변경 이력의 최신 버전이 머리 버전과 다르다"
    assert sorted(HISTORY_ENTRIES) == list(range(1, HEADER_VERSION + 1)), "변경 이력에 빠진 버전이 있다"


@pytest.mark.parametrize(
    "m", [m for m in _rule_headings() if m.group("ver")], ids=lambda m: m.group("id")
)
def test_version_tag_is_backed_by_history(m):
    ver = int(m.group("ver"))
    assert ver <= HEADER_VERSION, f"{m.group('id')}의 (v{ver})가 현재 버전보다 크다"
    assert m.group("id") in expand_ids(HISTORY_ENTRIES[ver]), (
        f"{m.group('id')}에 (v{ver} {m.group('kind')})가 붙었는데 변경 이력 v{ver}에 언급이 없다"
    )


def test_current_version_has_tagged_rules():
    """버전을 올렸으면 바뀐 룰에 (vN …) 표시가 있어야 재적용 때 대조 대상이 된다."""
    tagged = {m.group("id") for m in _rule_headings() if m.group("ver") == str(HEADER_VERSION)}
    assert tagged, f"v{HEADER_VERSION}으로 표시된 룰이 하나도 없다"
    assert tagged <= expand_ids(HISTORY_ENTRIES[HEADER_VERSION])


# ---- 룰 ID 참조 ----


def _id_reference_sources():
    yield RULES_MD
    yield SKILL_DIR / "SKILL.md"
    yield from sorted((SKILL_DIR / "references").glob("*.md"))
    yield from sorted((SKILL_DIR / "evals").rglob("*.md"))
    yield from sorted(PLUGIN.glob("README*.md"))


@pytest.mark.parametrize("src", sorted(set(_id_reference_sources())), ids=lambda p: str(p.relative_to(PLUGIN)))
def test_referenced_rule_ids_exist(src):
    unknown = sorted(expand_ids(read(src)) - set(DEFINED))
    assert not unknown, f"정의되지 않은 룰 ID를 참조한다: {unknown}"


def test_tool_dependency_table_names_existing_rules():
    table = [l for l in RULES.split("## 목차")[0].splitlines() if l.strip().startswith("| ")]
    assert len(table) >= 3, "도구 의존 표를 찾지 못했다"
    referenced = expand_ids("\n".join(table))
    assert referenced, "도구 의존 표에서 룰 ID를 하나도 찾지 못했다"
    assert referenced <= set(DEFINED)


def test_expand_ids_handles_grouped_notation():
    assert expand_ids("R-ROLE-06~08·10·11") == {
        "R-ROLE-06", "R-ROLE-07", "R-ROLE-08", "R-ROLE-10", "R-ROLE-11"
    }
    assert expand_ids("R-BASE-01～03·08") == {"R-BASE-01", "R-BASE-02", "R-BASE-03", "R-BASE-08"}

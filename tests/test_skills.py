"""모든 스킬의 frontmatter, 번들 파일 참조, 문서 내부 링크 검사."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import PLUGINS_DIR, ROOT, read, skill_files, split_frontmatter, strip_code

SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# 스킬 본문이 번들 파일을 가리키는 방식: `references/x.md`, `assets/y.md`
BUNDLED_PATH = re.compile(r"(?<![\w/.])((?:references|assets|examples)/[\w./-]+\.\w+)")
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")


def _skill_id(p: Path) -> str:
    return f"{p.parents[2].name}:{p.parent.name}"


@pytest.mark.parametrize("skill", skill_files(), ids=_skill_id)
def test_skill_frontmatter(skill):
    meta, body = split_frontmatter(read(skill))
    assert meta.get("name") == skill.parent.name, "frontmatter name은 스킬 폴더 이름과 같아야 한다"
    assert SKILL_NAME.match(meta["name"]) and len(meta["name"]) <= 64
    desc = meta.get("description", "")
    assert desc, "description이 비어 있으면 스킬이 트리거되지 않는다"
    # Agent Skills 규격의 description 상한
    assert len(desc) <= 1024, f"description이 {len(desc)}자로 1024자를 넘는다"
    assert body.strip(), "SKILL.md 본문이 비어 있다"


@pytest.mark.parametrize("skill", skill_files(), ids=_skill_id)
def test_skill_bundled_paths_exist(skill):
    """SKILL.md가 읽으라고 지시하는 references/·assets/ 파일이 실제로 있어야 한다."""
    skill_dir = skill.parent
    missing = sorted(
        {
            rel
            for rel in BUNDLED_PATH.findall(read(skill))
            if not (skill_dir / rel).is_file()
        }
    )
    assert not missing, f"존재하지 않는 번들 파일 참조: {missing}"


def _docs_with_links() -> list[Path]:
    files = list(ROOT.glob("README*.md"))
    for plugin in PLUGINS_DIR.iterdir():
        files += plugin.glob("README*.md")
        files += plugin.glob("examples/*.md")
        files += plugin.glob("skills/*/SKILL.md")
        files += plugin.glob("skills/*/references/*.md")
        files += plugin.glob("skills/*/assets/*.md")
    return sorted(files)


@pytest.mark.parametrize("doc", _docs_with_links(), ids=lambda p: str(p.relative_to(ROOT)))
def test_relative_markdown_links_resolve(doc):
    broken = []
    for target in MD_LINK.findall(strip_code(read(doc))):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue  # 외부 URL, mailto, 같은 문서 앵커
        path = target.split("#", 1)[0]
        if not (doc.parent / path).exists():
            broken.append(target)
    assert not broken, f"깨진 상대 링크: {broken}"

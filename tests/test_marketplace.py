"""마켓플레이스와 플러그인 매니페스트 검사."""

from __future__ import annotations

import re

import pytest

from conftest import PLUGINS_DIR, ROOT, load_json, local_plugin_dirs

MARKETPLACE = load_json(ROOT / ".claude-plugin" / "marketplace.json")
ENTRIES = MARKETPLACE["plugins"]
LOCAL_ENTRIES = [e for e in ENTRIES if isinstance(e["source"], str)]

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def test_marketplace_plugin_names_are_unique():
    names = [e["name"] for e in ENTRIES]
    assert len(names) == len(set(names)), f"중복된 플러그인 이름: {names}"


@pytest.mark.parametrize("entry", ENTRIES, ids=lambda e: e["name"])
def test_marketplace_entry_has_description(entry):
    assert entry.get("description", "").strip(), "마켓플레이스 항목에 description이 없다"


@pytest.mark.parametrize("entry", LOCAL_ENTRIES, ids=lambda e: e["name"])
def test_local_source_matches_plugin_manifest(entry):
    plugin_dir = (ROOT / entry["source"]).resolve()
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    assert manifest.is_file(), f"{entry['source']}에 plugin.json이 없다"
    assert load_json(manifest)["name"] == entry["name"], (
        "마켓플레이스 이름과 plugin.json 이름이 다르면 설치 ID가 어긋난다"
    )


def test_every_plugin_dir_is_listed_in_marketplace():
    listed = {(ROOT / e["source"]).resolve() for e in LOCAL_ENTRIES}
    orphans = [p.name for p in local_plugin_dirs() if p.resolve() not in listed]
    assert not orphans, f"marketplace.json에 등록되지 않은 플러그인: {orphans}"


@pytest.mark.parametrize("plugin_dir", local_plugin_dirs(), ids=lambda p: p.name)
def test_plugin_manifest_fields(plugin_dir):
    m = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
    assert KEBAB.match(m["name"]), f"이름은 kebab-case여야 한다: {m['name']}"
    assert m["name"] == plugin_dir.name, "플러그인 폴더 이름과 name이 다르다"
    assert SEMVER.match(m.get("version", "")), f"version이 semver가 아니다: {m.get('version')}"
    for field in ("description", "author", "license", "repository"):
        assert m.get(field), f"plugin.json에 {field}가 없다"


@pytest.mark.parametrize("plugin_dir", local_plugin_dirs(), ids=lambda p: p.name)
def test_plugin_has_at_least_one_skill(plugin_dir):
    assert list(plugin_dir.glob("skills/*/SKILL.md")), "skills/<name>/SKILL.md가 하나도 없다"

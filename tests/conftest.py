"""플러그인 테스트 공용 헬퍼.

플러그인은 실행 코드 없이 마크다운 스킬로만 이뤄져 있으므로, 이 스위트는
매니페스트·스킬 frontmatter·참조 경로·common-rules 카탈로그의 버전/ID 규약처럼
"깨지면 스킬이 잘못 동작하는" 구조 불변식을 검사한다.
리포 루트는 항상 이 파일 위치에서 계산한다(cwd에 의존하지 않는다).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read(path))


def local_plugin_dirs() -> list[Path]:
    return sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))


def skill_files() -> list[Path]:
    return sorted(PLUGINS_DIR.glob("*/skills/*/SKILL.md"))


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """`---`로 감싼 frontmatter를 최소한으로 파싱한다.

    `key: value`와 `key: >-` / `key: |` 다음 들여쓴 줄(블록 스칼라)만 지원한다.
    값은 문자열 그대로 둔다. frontmatter가 없으면 ValueError.
    """
    if not text.startswith("---\n"):
        raise ValueError("frontmatter가 없다")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter가 닫히지 않았다")
    block, body = text[4:end], text[end + 4 :].lstrip("\n")

    data: dict[str, str] = {}
    key = None
    folded: list[str] = []
    for line in block.splitlines():
        if key is not None and (line.startswith(" ") or not line.strip()):
            folded.append(line.strip())
            continue
        if key is not None:
            data[key] = " ".join(x for x in folded if x)
            key, folded = None, []
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            raise ValueError(f"해석할 수 없는 frontmatter 줄: {line!r}")
        k, v = m.group(1), m.group(2)
        if v in (">-", ">", "|", "|-"):
            key = k
        else:
            data[k] = v.strip().strip('"').strip("'")
    if key is not None:
        data[key] = " ".join(x for x in folded if x)
    return data, body


_FENCE = re.compile(r"^```.*?^```", re.M | re.S)
_INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """펜스 코드블록과 인라인 코드를 지운다(예시 링크를 실제 링크로 오인하지 않게)."""
    return _INLINE_CODE.sub("", _FENCE.sub("", text))

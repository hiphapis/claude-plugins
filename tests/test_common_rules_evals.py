"""common-rules eval 케이스의 구조 검사와 scaffold 스크립트 실제 실행.

LLM 채점(`claude plugin eval`)은 비용이 들어 이 스위트에서 돌리지 않는다.
여기서는 eval이 돌기 전에 깨질 수 있는 부분 — 케이스 정의, 입력 파일, scaffold — 을 확인한다.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess

import pytest

from conftest import PLUGINS_DIR, read, split_frontmatter

EVALS = PLUGINS_DIR / "common-rules" / "skills" / "common-rules" / "evals"
# .omc/ 같은 도구 작업 폴더(gitignore 대상)는 케이스가 아니다
CASES = sorted(p for p in EVALS.iterdir() if p.is_dir() and not p.name.startswith("."))


def _case_field(case_dir, key):
    m = re.search(rf"^\s*{key}:\s*(.+)$", read(case_dir / "case.yaml"), re.M)
    return m.group(1).strip().strip('"') if m else None


def _input_files(case_dir) -> list[str]:
    m = re.search(r"^Input files:\s*(.+)$", read(case_dir / "prompt.md"), re.M)
    return [f.strip() for f in m.group(1).split(",")] if m else []


def test_there_are_eval_cases():
    assert CASES


@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_case_definition(case):
    assert _case_field(case, "schema_version")
    assert _case_field(case, "name") == case.name, "case.yaml의 name은 폴더 이름과 같아야 한다"
    assert _case_field(case, "expected_outcome"), "expected_outcome이 없다"
    script = case / _case_field(case, "scaffold_script")
    assert script.is_file(), f"scaffold 스크립트가 없다: {script.name}"
    assert os.access(script, os.X_OK), f"scaffold 스크립트에 실행 권한이 없다: {script.name}"


@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_prompt_and_inputs(case):
    meta, body = split_frontmatter(read(case / "prompt.md"))
    assert meta.get("allowed_tools"), "prompt.md에 allowed_tools가 없다"
    assert "/common-rules" in body, "eval 프롬프트가 스킬을 호출하지 않는다"
    inputs = _input_files(case)
    assert inputs, "prompt.md에 'Input files:' 줄이 없다"
    missing = [f for f in inputs if not (case / "files" / f).is_file()]
    assert not missing, f"files/에 없는 입력 파일: {missing}"


@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_graders(case):
    graders = sorted((case / "graders").glob("*.md"))
    assert graders, "grader가 하나도 없다"
    for g in graders:
        meta, body = split_frontmatter(read(g))
        assert meta.get("type") in {"llm", "code"}, f"{g.name}: type이 없거나 알 수 없다"
        assert float(meta.get("weight", "0")) > 0, f"{g.name}: weight가 0 이하다"
        assert body.strip(), f"{g.name}: 채점 기준 본문이 비어 있다"


@pytest.mark.skipif(shutil.which("git") is None, reason="git이 없다")
@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_scaffold_builds_clean_repo(case, tmp_path):
    """scaffold를 빈 폴더에서 실제로 돌려, 스킬의 사전 점검(깨끗한 git 리포)을 통과하는 상태가 되는지 본다."""
    script = case / _case_field(case, "scaffold_script")
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
    subprocess.run(["bash", str(script)], cwd=tmp_path, env=env, check=True, capture_output=True)

    for f in _input_files(case):
        assert (tmp_path / f).read_bytes() == (case / "files" / f).read_bytes(), f"{f}가 그대로 복사되지 않았다"

    git = lambda *a: subprocess.run(  # noqa: E731
        ["git", *a], cwd=tmp_path, env=env, check=True, capture_output=True, text=True
    ).stdout
    assert git("status", "--porcelain") == "", "scaffold 뒤 작업 트리가 깨끗하지 않다"
    assert len(git("log", "--oneline").splitlines()) == 1, "초기 커밋이 하나여야 한다"
    tracked = set(git("ls-files").split())
    assert set(_input_files(case)) <= tracked, "입력 파일이 커밋되지 않았다"

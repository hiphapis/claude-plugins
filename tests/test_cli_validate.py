"""`claude plugin validate`로 공식 스키마 검증. CLI가 없으면 건너뛴다.

CI는 이 검증을 별도 단계로 이미 돌리므로 pytest에서는 `-m "not cli"`로 뺀다.
"""

from __future__ import annotations

import shutil
import subprocess

import pytest

from conftest import ROOT, local_plugin_dirs

pytestmark = [
    pytest.mark.cli,
    pytest.mark.skipif(shutil.which("claude") is None, reason="claude CLI가 없다"),
]


@pytest.mark.parametrize("target", [ROOT, *local_plugin_dirs()], ids=lambda p: p.name)
def test_claude_plugin_validate(target):
    r = subprocess.run(
        ["claude", "plugin", "validate", str(target)], capture_output=True, text=True, timeout=120
    )
    assert r.returncode == 0, r.stdout + r.stderr

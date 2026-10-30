# common-rules

[English](README.md)

제 개인 공통 작업 룰을 **리포에 이미 있는 룰**에 병합하는 Claude Code 스킬입니다.

룰은 오케스트레이터·워커 분담(오케스트레이터는 코드를 한 줄도 고치지 않음), Orca 워크트리, GitHub 이슈 수명주기, 테스트 게이트, Git, 완료 보고, 문서 관리를 다룹니다. [`references/rules.md`](skills/common-rules/references/rules.md)에 룰마다 ID·별점·이유·전제 태그(`[gh]`, `[vault]`, `[ko]`, `[personal]`)를 달아 두었습니다. Orca 위에서 오케스트레이터·워커로 일하는 방식을 전제로 하므로, Orca 룰은 모든 리포에 들어갑니다.

## 설치 전에 알아 두세요

- **[Orca](https://github.com/stablyai/orca) 위에서 돌아간다는 가정으로 만들었습니다.** 워크트리는 `orca worktree`로 만들고, 워커를 띄우고 감독하는 일(`dispatch`, `worker_done` 대기)은 `orca orchestration`으로 합니다. Orca 룰(R-ORCA)은 전제 태그 없이 모든 리포에 들어가므로, Orca를 쓰지 않는 환경에서는 역할 분담·워크트리 룰 상당수를 지킬 수 없습니다.
- **오케스트레이터와 워커가 나뉩니다.** 지금 대화하는 세션(오케스트레이터)은 코드를 한 줄도 고치지 않고, 코드는 Orca가 띄운 워커가 씁니다. 워커 설정은 작업 등급별 현재값으로 룰에 박혀 있습니다(구현은 기계적·일반 `claude-sonnet-5-5` `low`·`medium`, 어려움 `claude-opus-5-5` `high` / 리뷰는 `claude-opus-5-5` `high`, 고위험 `xhigh`). 바꾸려면 `rules.md`의 R-ROLE-04를 고칩니다.
- **함께 쓰는 도구가 있습니다.** 해당 룰을 넣을 리포라면 미리 준비해 두세요. 실행한 머신에 도구가 없으면 스킬이 "설치하고 넣기 / 룰만 넣기 / 빼기"를 묻고(플러그인과 `gh`는 동의하면 설치하고, Orca·ego-browser는 링크만 안내함. 물을 수 없으면 설치 없이 넣고 경고로 남김), 룰을 따르는 에이전트는 도구가 없을 때 다른 수단으로 우회하지 않고 멈춰서 묻습니다(R-BASE-10).
  - [worktree-teardown](../worktree-teardown) 플러그인 — 머지 직후 워크트리 감사(R-ORCA-12)
  - [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)의 `ccg` — 되돌릴 수 없는 변경에만 쓰는 3중 합의(R-ROLE-09)
  - `gh` CLI — GitHub 이슈 수명주기(`[gh]` 룰)
  - `ego-browser` 스킬 — 브라우저 확인(`[personal]` 룰)
- **개인 룰입니다.** 룰 본문은 한국어이고, 출력 언어·브라우저 같은 개인 선호는 `[personal]` 태그로 구분해 두었습니다. 여러 사람이 쓰는 리포라면 `[personal]` 룰은 빼는 편이 맞습니다.
- **리포 밖으로 나가는 행동이 포함됩니다.** 문서 커밋 자동 push, 운영 배포까지 마친 작업의 push, 이슈 자동 종료, 묻지 않는 배포 같은 `[outward]` 룰은 기존 룰과 겹치지 않아도 넣기 전에 따로 확인합니다.
- **리포의 파일을 직접 고칩니다.** `AGENTS.md`·`docs/` 규칙 문서에 룰과 적용 기록을 써 넣습니다. 작업 트리가 깨끗할 때 실행하고, 결과는 `git diff`로 검토하세요.

## 템플릿이 아니라 병합인 이유

Codex 같은 워커는 Claude 스킬이 아니라 리포의 `AGENTS.md`와 `docs/`를 읽습니다. 그래서 룰은 리포 안에 실제 파일로 들어가야 합니다. 그리고 대부분의 리포에는 이미 룰이 있습니다. 스킬은 이렇게 동작합니다.

1. 기존 룰 문서를 처음부터 끝까지 읽습니다.
2. 공통 룰마다 **동일 / 보강 / 누락 / 충돌**을 판정합니다.
3. 누락은 추가하고, 보강은 빠진 부분만 덧붙입니다(묻지 않음).
4. 충돌은 어떻게 할지(공통 룰로 교체, 기존 유지, 조정) 사용자에게 묻습니다.
5. 적용 버전과 결정을 `AGENTS.md`에 기록해, 다음 실행 때는 새로 생기거나 바뀐 룰만 봅니다.

충돌을 스스로 정하지 않습니다. 물을 수 없는 환경(서브에이전트, 비대화형 실행)에서는 충돌을 건드리지 않고 미결정으로 보고합니다.

## 설치

```
/plugin marketplace add hiphapis/claude-plugins
/plugin install common-rules@hiphapis
```

## 사용

룰을 맞출 리포에서:

> /common-rules
> 이 리포에도 공통 룰 넣어줘

## 라이선스

MIT

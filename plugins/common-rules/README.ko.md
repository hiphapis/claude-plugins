# common-rules

[English](README.md)

제 개인 공통 작업 룰을 **리포에 이미 있는 룰**에 병합하는 Claude Code 스킬입니다.

룰은 오케스트레이터·워커 분담(오케스트레이터는 코드를 한 줄도 고치지 않음), Orca 워크트리, GitHub 이슈 수명주기, 테스트 게이트, Git, 완료 보고, 문서 관리를 다룹니다. [`references/rules.md`](skills/common-rules/references/rules.md)에 룰마다 ID·별점·이유·전제 태그(`[gh]`, `[vault]`, `[ko]`, `[personal]`)를 달아 두었습니다. Orca 위에서 오케스트레이터·워커로 일하는 방식을 전제로 하므로, Orca 룰은 모든 리포에 들어갑니다.

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

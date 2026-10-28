# 배치 규칙 — 공통 룰을 리포의 어디에 넣을까

## 1. 기존 체계가 있으면 그 안에서

리포의 룰 문서 체계를 먼저 파악한다. `AGENTS.md`·`CLAUDE.md`의 문서 인덱스나 링크를 따라가면 대개 보인다. 공통 룰의 범주(R-BASE, R-ROLE …)를 **주제가 맞는 기존 파일**에 넣는다.

- 파일 이름이 달라도 주제가 같으면 그 파일이다(예: `commit-rules.md`가 R-GIT의 자리).
- 한 기존 파일이 여러 범주를 다 담고 있으면(예: 큰 `AGENTS.md` 하나) 그 파일 안에서 주제가 맞는 절을 찾아 넣고, 맞는 절이 없으면 절을 새로 만든다.
- 주제가 맞는 파일이 없는 범주만, 같은 폴더에 새 파일을 만든다. 파일 이름은 그 폴더의 기존 이름 규칙(언어, 케밥 케이스 등)을 따르고, 인덱스에 한 줄을 추가한다.

## 2. 체계가 없으면 기본 구조를 제안한다

룰이 루트 `AGENTS.md`·`CLAUDE.md` 정도뿐이거나 아예 없으면 아래 구조를 제안하고, **만들기 전에 사용자에게 한 번 묻는다.** 거절하면 `AGENTS.md`(없으면 `CLAUDE.md`)에 범주별 절로 넣는다.

```
AGENTS.md                         # 인덱스·레이아웃 규약만 (R-DOC-01)
docs/rules/
  agent-roles.md                  # R-BASE-01～03·08, R-ROLE, R-SPEC
  task-lifecycle.md               # R-ISSUE, R-ORCA
  testing.md                      # R-TEST
  git-workflow.md                 # R-GIT
  verification-handoff.md         # R-REPORT
  doc-maintenance.md              # R-DOC-01～06·09
  writing.md                      # R-BASE-04·05·09, R-DOC-07·08
```

- 리포가 이미 `docs/` 아래에 번호 폴더(예: `docs/06-개발규칙/`)를 쓰고 있으면 `docs/rules/` 대신 그 규칙을 따른다.
- frontmatter는 SKILL.md 4단계 판정을 따른다. 새 구조를 만드는 리포에는 따를 관례가 없으므로 R-DOC-08대로 붙인다.
- 각 파일 첫머리에 TL;DR 몇 줄을 두고, `AGENTS.md`의 인덱스 표에 파일마다 한 줄을 추가한다. (이 절은 새 구조를 만들 때만 적용된다. 기존 체계 안에 파일을 추가할 때는 §1대로 그 폴더의 관례를 따른다.)

## 3. CLAUDE.md와 AGENTS.md가 둘 다 있을 때

- 한쪽이 다른 쪽을 가리키기만 하면(예: `CLAUDE.md`가 `@AGENTS.md` 한 줄) 실제 본문이 있는 쪽에 쓴다.
- 둘 다 본문이 있으면, 워커(Codex 등)가 읽는 `AGENTS.md`를 우선한다. Claude 전용 내용(스킬 이름, Claude Code 기능)만 `CLAUDE.md`에 둔다.

## 4. 리포마다 값이 다른 자리

다음은 공통 룰이 아니라 리포가 채울 값이다. 리포에서 확인할 수 있으면 채우고, 없으면 `<미정: …>`으로 표시해 보고서에 올린다.

- 게이트 명령과 기대 출력
- 원격 리포 이름, 기본 브랜치
- 디렉토리 레이아웃 표
- 문서 린터 명령
- 배포 절차

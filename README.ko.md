# hiphapis/claude-plugins

[English](README.md) | [한국어](README.ko.md)

제가 직접 만들어 매일 쓰는 [Claude Code](https://claude.com/claude-code) 플러그인을 모아 둔 마켓플레이스입니다.

## 설치

```
/plugin marketplace add hiphapis/claude-plugins
/plugin install <plugin>@hiphapis
```

## 플러그인

| 플러그인 | 하는 일 | 위치 |
|---|---|---|
| [docs-with-obsidian](plugins/docs-with-obsidian) | 프로젝트 문서를 저장소 `/docs` 폴더의 Obsidian vault로 정리합니다. Claude Code, Claude Desktop, 사람이 git으로 함께 씁니다 | 이 저장소 |
| [worktree-teardown](plugins/worktree-teardown) | git 워크트리를 지우기 전에 감사해서 잃는 것이 없게 합니다. 삭제는 사람이 직접 합니다 | 이 저장소 |
| [loopcraft](https://github.com/hiphapis/loopcraft) | 루프 엔지니어링: 세션을 넘어 유지되는 메모리 vault, 자기 교정 훅, 실패를 지식으로 증류하는 프로토콜 | [hiphapis/loopcraft](https://github.com/hiphapis/loopcraft) |

작은 플러그인은 `plugins/` 아래에 둡니다. 테스트, 훅, 릴리스 주기가 따로 있는 큰 플러그인은 별도 저장소에 두고 여기서는 참조만 합니다.

## 구조

```
.claude-plugin/marketplace.json   # 전체 플러그인 카탈로그
plugins/<name>/                   # 플러그인 하나당 폴더 하나
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
```

## 플러그인 추가하기

1. `plugins/<name>/`에 `.claude-plugin/plugin.json`과 `skills/`를 만듭니다.
2. `.claude-plugin/marketplace.json`에 항목을 추가합니다.
3. `claude plugin validate .`와 `claude plugin validate plugins/<name>`을 실행합니다.

## 라이선스

MIT

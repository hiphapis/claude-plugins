# docs-with-obsidian

[English](README.md) | **한국어** | [日本語](README.ja.md) | [中文](README.zh-CN.md)

소프트웨어 프로젝트 곳곳에 흩어져 있는 문서를, 잘 정리되고 링크가 풍부한 하나의
**Obsidian vault**로 통합하기 위한 검증된 방법론을 완결된 형태로 담은
[Claude Code](https://claude.com/claude-code) 플러그인입니다. 이 vault는 저장소의
`/docs` 폴더에 존재하며, Claude Code, Claude Desktop, 그리고 사용자가 함께
공유하고 git으로 동기화됩니다.

문서는 흩어지기 마련입니다. 어떤 것은 `README`에, 어떤 것은 `.claude/`에, 어떤
것은 도구가 생성한 출력물(superpowers, omc, loopcraft)에, 어떤 것은 사용자의
머릿속에 남습니다. 이 플러그인은 이 모든 것을 모든 참여자가 source of truth로
취급하는 하나의 vault로 통합하기 위한 검증된 처음부터 끝까지의 프로세스를 —
**실제로 시간을 잡아먹는 설정상의 함정까지 포함하여** — 담고 있습니다.

## 멘탈 모델 (먼저 읽어 주세요)

세 참여자가 **디스크상의 동일한 `<repo>/docs` 폴더**를 대상으로 작업하며, **git**으로
서로 동기화됩니다:

| Participant | Role | Best for | Needs Obsidian open? |
|-------------|------|----------|:---:|
| **Claude Code** (터미널) | 디스크상의 저장소 파일을 직접 다룸 | 대량 파일 작업 — 통합, 이동, 분류, 마이그레이션, `.gitignore`, 커밋. git 네이티브. | No |
| **Claude Desktop** | Obsidian "Claude Code MCP" 플러그인을 통해 vault에 연결 | 노트의 일상적인 읽기/수정, vault를 인식하며 실시간으로 반영됨 | Yes |
| **Obsidian** | 사람이 편집하는 표면이자 MCP 서버의 호스트 | 읽기, 링크 연결, 그래프 뷰 | — |

vault는 저장소 루트가 아닌 **`<repo>/docs`**에 존재합니다(루트에 두면
`node_modules`와 코드까지 인덱싱됩니다). 하나의 저장소가 코드와 문서를 모두
담고 있으므로, 단 한 번의 `git pull`로 모든 것을 동일한 시점으로 동기화할 수
있습니다.

## 무엇을 얻게 되나요

두 트랙으로 구성된 방법론과 이를 실행하기 위한 템플릿 및 참조 절차를 담은 하나의
skill(`docs-with-obsidian`):

| Component | What it does |
|-----------|--------------|
| **Track A — Consolidate & migrate** (`references/claude-code-setup.md`) | 저장소 전체의 모든 문서를 인벤토리화 → 분류(`KEEP-tool` / `KEEP-log` / `MOVE-knowledge` / `MIXED`) → **사람의 승인을 위해 멈춤** → 이동(절대 삭제하지 않음)하며 기존 경로에 stub을 남김 → 폴더 스켈레톤 적용 → frontmatter + `[[wikilinks]]` 추가 → ADR 재구성 → `.gitignore`와 `CLAUDE.md` 업데이트. |
| **Track B — Connect & instruct** (`references/desktop-mcp-setup.md`) | `<repo>/docs`를 독립된 vault로 열기 → "Claude Code MCP" 플러그인 설치 → 각 vault에 고유한 HTTP 포트 부여 → `mcp-remote` stdio 브리지로 Claude Desktop 연결 → `/ide`로 Claude Code 연결 → 읽기 + 쓰기 테스트로 검증 → vault가 source of truth가 되도록 프로젝트 지침 생성. |
| **Vault skeleton** (`assets/vault-structure.md`) | 라이프사이클 기반 폴더 스타터(`00-dashboard` … `06-dev-rules`, `_templates`) — 강제 규칙이 아니라 적응시켜 나갈 하나의 가설입니다. 폴더 이름은 현지화할 수 있습니다. |
| **Migration prompt** (`assets/migration-prompt.md`) | 바로 붙여넣을 수 있는 일반화된 Track A 프롬프트 — 빈칸을 채워 Claude Code에 전달하세요. |
| **Project-instructions template** (`assets/project-instructions-template.md`) | claude.ai가 vault를 (MCP를 통해) source of truth로 참조하고 결론을 다시 기록하도록 만드는 Custom Instructions. |
| **ADR template** (`assets/adr-template.md`) | 과거의 결정 하나당 노트 하나; 근거를 지어내는 대신 "confirm needed" 플레이스홀더를 남깁니다. |
| **Desktop MCP config snippet** (`assets/claude-desktop-config-snippet.md`) | 정확한 `mcp-remote` 브리지 JSON — 서버를 조용히 누락시키는 bare-`url` 실패를 방지합니다. |
| **Troubleshooting** (`references/troubleshooting.md`) | 실제로 마주치는 함정들: nvm node 버전 불일치, 포트 충돌, bare-`url` 실패, 최소 PATH, 두 대의 머신 세션. |

## 설치

**Option A — marketplace (권장):**

```
/plugin marketplace add hiphapis/claude-plugins
/plugin install docs-with-obsidian@hiphapis
/reload-plugins
```

**Option B — local clone (개발용):**

```bash
git clone https://github.com/hiphapis/claude-plugins.git
claude --plugin-dir ./claude-plugins/plugins/docs-with-obsidian
```

이 skill은 `docs-with-obsidian:docs-with-obsidian`으로 등록되며, 프로젝트 문서를
Obsidian으로 정리하거나, docs vault를 설정하거나, 흩어진 문서를 통합하거나, MCP를
통해 Obsidian을 Claude Desktop/Code에 연결하거나, 문서를 vault로 마이그레이션하도록
요청할 때마다 — "Obsidian"이나 "skill"이라고 명시적으로 말하지 않더라도 —
트리거됩니다.

## 사용법

이 skill에는 **두 개의 트랙**이 있습니다. 대부분의 프로젝트는 둘 다, 순서대로
필요합니다.

### Track A — Consolidate & migrate (Claude Code)

이 작업은 **일반적인 대화형 세션**에서 실행하세요 — 판단이 많이 필요하고 사람의
승인 게이트가 있어야 하므로, 자율 루프 안에서는 실행하지 **마세요**.

1. **먼저 인벤토리화하고, 아직 아무것도 옮기지 마세요.** 도구가 생성한 파일을
   포함하여 저장소 전체의 모든 문서를 찾습니다. 각각을 분류하고 표를 만듭니다:
   `[KEEP-tool]` 기계적 파일 · `[KEEP-log]` 세션 스크래치 ·
   `[MOVE-knowledge]` 실제 프로젝트 지식 · `[MIXED]` 지식을 포함한 기계적 파일.
   **사람의 승인을 위해 멈춥니다.**
2. **절대 삭제하지 마세요.** 파일을 이동하되, 기존 경로에 짧은 **stub**을
   남겨(`status: stub`, `moved_to: …`, 그리고 wikilink) 아무것도 깨지지 않도록
   합니다.
3. **폴더 스켈레톤은 가설로.** `assets/vault-structure.md`에서 시작하되, 실제
   문서가 맞지 않는 곳에서만 추가/병합을 제안합니다. 최상위 폴더는 ~6~8개로
   유지합니다.
4. **frontmatter + wikilinks 추가.** 모든 노트에 `title`, `status`, `source`,
   `updated`를 부여하고, 재분산을 막기 위해 관련 노트로의 `[[links]]`를
   추가합니다.
5. **ADR 재구성** — 근거를 복원할 수 있는 곳에서 재구성하고, 불확실한 것은
   "confirm needed"로 표시하며 — 절대 지어내지 마세요.
6. **`.gitignore` 업데이트**(변경이 잦은 Obsidian 파일만)와 **`CLAUDE.md`**
   업데이트로 vault가 source of truth임을 선언합니다.

### Track B — Connect Claude Desktop & apply instructions

1. **`<repo>/docs`를 독립된 vault로 열기** — 개인용 대형 vault와 분리하여 MCP가
   이 프로젝트만 노출하도록 Obsidian에서 엽니다.
2. **"Claude Code MCP" 커뮤니티 플러그인 설치.** 이 플러그인은 두 개의 서버를
   노출합니다: **WebSocket** 서버(`/ide`를 통한 Claude Code용)와 **HTTP/SSE**
   서버(Claude Desktop용, `http://localhost:<HTTP_PORT>/sse`).
3. **vault마다 고유한 HTTP 포트** — 둘 이상을 실행한다면(예: 이 프로젝트 `22361`,
   개인 vault `22360`) 그렇지 않으면 포트를 두고 충돌합니다.
4. **`mcp-remote` stdio 브리지로 Claude Desktop 연결.** `claude_desktop_config.json`에
   bare `"url"`을 붙여넣지 **마세요** — Desktop은 stdio만 검증하며 이를 조용히
   누락시킵니다. 스니펫은 `assets/claude-desktop-config-snippet.md`에 있습니다.
   이후 완전히 종료(Cmd+Q)했다가 다시 실행하세요.
5. **Claude Code 연결:** `claude` → `/ide` → **Obsidian** 선택. 설정 파일은
   필요 없습니다.
6. **검증** — 읽기 테스트(vault 파일 목록 확인)와 쓰기 테스트(노트를 생성하고,
   Obsidian에 실시간으로 나타나는지 확인)로 검증합니다.
7. **프로젝트 지침 생성** — `assets/project-instructions-template.md`를 바탕으로
   이 프로젝트의 MCP 서버 이름과 폴더 카테고리에 맞게 조정한 뒤, claude.ai
   프로젝트의 Custom Instructions에 붙여넣습니다.

## Vault 구조

라이프사이클 기반의 시작 스켈레톤(인벤토리 과정에서 프로젝트에 맞게 적응):

```
<repo>/docs/                 ← open THIS as the Obsidian vault
├── .obsidian/               # Obsidian + plugin settings
├── 00-dashboard/            # index, project status, open TODOs, deadlines
├── 01-business/             # business plan, pricing, market research
├── 02-product/              # PRD, feature specs, checklists
├── 03-decisions-adr/        # ADRs (one per decision)
├── 04-<domain-content>/     # domain artifacts
├── 05-research/             # investigations, comparisons
├── 06-dev-rules/            # engineering conventions (git, testing…)
└── _templates/              # note templates (ADR, domain notes)
```

**최상위 계층 = 라이프사이클 기반**(business vs product vs decisions vs
research): 이 계층은 거의 변하지 않으며, 재구성하면 링크가 깨지므로 비용이
큽니다. 하위 폴더와 이름은 비용이 적으므로 실제 콘텐츠로부터 자라나야 합니다.

## 프로젝트별로 채워야 할 매개변수

먼저 다음을 확정하세요(모르면 물어보세요):

| Placeholder | Meaning | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | 사람이 보는 프로젝트 이름 | OurStory |
| `{{MCP_SERVER_NAME}}` | Desktop 설정에서의 서버 이름 | obsidian-ourstory |
| `{{VAULT_PATH}}` | vault의 절대 경로 | /Users/you/ourstory/docs |
| `{{HTTP_PORT}}` | Obsidian 플러그인 HTTP/SSE 포트(vault마다 고유) | 22361 |
| `{{NPX_PATH}}` | npx의 절대 경로(`which npx`) | /Users/you/.nvm/.../bin/npx |

## 가드레일 (타협 불가)

- **문서를 절대 삭제하지 마세요** — 이동 + stub, 또는 아카이브. 마이그레이션
  맵을 유지하세요.
- **도구 기계 장치를 절대 건드리지 마세요**(`superpowers/`, `plans/`, `specs/`,
  `.claude/`) — source-of-truth 규칙으로 `CLAUDE.md`를 *업데이트*하는 경우는
  예외입니다.
- **마이그레이션 전에 인벤토리화하세요**; 분류에 대해 사람의 승인을 받으세요.
- **Track A를 자율 루프 안에서 실행하지 마세요** — 승인 게이트가 필요합니다.
- **vault에 기록되는 사실을 절대 지어내지 마세요**; 확인되지 않은 값은
  플레이스홀더로 표시하세요.

## 레이아웃

단일 플러그인 저장소 — 저장소 루트 자체가 플러그인이며, 동시에 자기 자신을 담은
하나의 플러그인 마켓플레이스입니다(`source: "./"`):

```
.
├── .claude-plugin/
│   ├── marketplace.json     # marketplace registry (source: "./")
│   └── plugin.json          # plugin manifest
├── skills/docs-with-obsidian/
│   ├── SKILL.md             # the methodology
│   ├── references/          # detailed Track A / Track B / troubleshooting
│   └── assets/              # templates, prompts, config snippets
└── README.md
```

## 배포

작성자: [Johan Kim](https://github.com/hiphapis). Claude Code가 가져올 수 있도록
저장소는 **public**이어야 합니다. 설치된 사용자에게 전달되어야 하는 변경이 있을
때마다 `.claude-plugin/plugin.json`의 `version`을 올리세요 — 버전을 올리는 것이
업데이트 신호입니다.

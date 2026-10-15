# docs-with-obsidian

[English](README.md) | [한국어](README.ko.md) | **日本語** | [中文](README.zh-CN.md)

ソフトウェアプロジェクトに散在するドキュメントを、リポジトリの `/docs`
フォルダに置かれた単一の、よく整理されリンクの充実した **Obsidian vault**
へと変換するための、完成度が高く実践で鍛えられた方法論をパッケージ化した
[Claude Code](https://claude.com/claude-code) プラグインです。この vault は
Claude Code、Claude Desktop、そしてあなたの三者で共有され、すべて git
によって同期され続けます。

ドキュメントは断片化します。あるものは `README` に、あるものは `.claude/`
に、あるものはツールの出力（superpowers、omc、loopcraft）に、そしてあるものは
あなたの頭の中に散らばります。このプラグインは、それらすべてを、すべての
参加者が source of truth として扱う一つの vault へと統合するための、
**実際に時間を浪費させるセットアップの落とし穴も含めた**、実証済みの
エンドツーエンドのプロセスを体系化します。

## メンタルモデル（まずこれを読んでください）

三者の参加者が、**ディスク上の同一の `<repo>/docs` フォルダ**を対象に動作し、
それは **git** によって同期され続けます。

| 参加者 | 役割 | 最適な用途 | Obsidian を開く必要は？ |
|-------------|------|----------|:---:|
| **Claude Code**（ターミナル） | ディスク上のリポジトリファイルを直接操作 | ファイルの一括処理 — 統合、移動、分類、移行、`.gitignore`、コミット。git ネイティブ。 | 不要 |
| **Claude Desktop** | Obsidian の「Claude Code MCP」プラグインを通じて vault に接続 | ノートの日常的な読み書き・更新。vault を認識し、リアルタイムに反映される。 | 必要 |
| **Obsidian** | 人間の編集の場であり、MCP サーバーのホスト | 閲覧、リンク付け、グラフビュー | — |

vault は **`<repo>/docs`** に置かれます — リポジトリのルートではありません
（ルートに置くと `node_modules` やコードがインデックスされてしまいます）。
一つのリポジトリがコードとドキュメントの両方を保持するため、一度の
`git pull` ですべてを同一の時点へと同期できます。

## 得られるもの

一つのスキル（`docs-with-obsidian`）が、二トラックの方法論と、それを実行する
ためのテンプレートおよびリファレンス手順を体系化します。

| コンポーネント | 内容 |
|-----------|--------------|
| **トラック A — 統合と移行**（`references/claude-code-setup.md`） | リポジトリ全体のあらゆるドキュメントを棚卸し → 分類（`KEEP-tool` / `KEEP-log` / `MOVE-knowledge` / `MIXED`）→ **人間の承認のために停止** → 移動（決して削除せず）し、元のパスには stub を残す → フォルダのスケルトンを適用 → frontmatter と `[[wikilinks]]` を追加 → ADR を再構築 → `.gitignore` と `CLAUDE.md` を更新。 |
| **トラック B — 接続と指示**（`references/desktop-mcp-setup.md`） | `<repo>/docs` を独立した vault として開く → 「Claude Code MCP」プラグインをインストール → 各 vault に一意の HTTP ポートを割り当てる → `mcp-remote` の stdio ブリッジ経由で Claude Desktop を接続 → `/ide` 経由で Claude Code を接続 → 読み取り + 書き込みテストで検証 → vault が source of truth となるようプロジェクトの指示を生成。 |
| **vault スケルトン**（`assets/vault-structure.md`） | ライフサイクルに基づくフォルダのスターター（`00-dashboard` … `06-dev-rules`、`_templates`）— 従うべき規範ではなく、適応させるための仮説です。フォルダ名はローカライズ可能です。 |
| **移行プロンプト**（`assets/migration-prompt.md`） | そのまま貼り付けて使える、一般化されたトラック A のプロンプト — 空欄を埋めて Claude Code に渡してください。 |
| **プロジェクト指示テンプレート**（`assets/project-instructions-template.md`） | claude.ai が（MCP 経由で）vault を source of truth として参照し、結論を書き戻すようにする Custom Instructions。 |
| **ADR テンプレート**（`assets/adr-template.md`） | 過去の各決定につき一つのノート。根拠を捏造するのではなく、「confirm needed」のプレースホルダを残します。 |
| **Desktop MCP 設定スニペット**（`assets/claude-desktop-config-snippet.md`） | 正確な `mcp-remote` ブリッジの JSON — サーバーを黙って切り捨ててしまう、bare-`url` の失敗を回避します。 |
| **トラブルシューティング**（`references/troubleshooting.md`） | 実際に起こる落とし穴。nvm の node バージョン不一致、ポート競合、bare-`url` の失敗、最小限の PATH、二台のマシンでのセッション。 |

## インストール

**オプション A — marketplace（推奨）:**

```
/plugin marketplace add hiphapis/claude-plugins
/plugin install docs-with-obsidian@hiphapis
/reload-plugins
```

**オプション B — ローカルクローン（開発用）:**

```bash
git clone https://github.com/hiphapis/claude-plugins.git
claude --plugin-dir ./claude-plugins/plugins/docs-with-obsidian
```

このスキルは `docs-with-obsidian:docs-with-obsidian` として登録され、
プロジェクトのドキュメントを Obsidian に整理する、ドキュメントの vault
をセットアップする、断片化したドキュメントを統合する、MCP 経由で Obsidian
を Claude Desktop/Code に接続する、あるいはドキュメントを vault
へ移行するといった依頼をしたときに — たとえ「Obsidian」や「スキル」と
明示的に言わなくても — トリガーされます。

## 使い方

このスキルには**二つのトラック**があります。ほとんどのプロジェクトでは、
両方を順番に必要とします。

### トラック A — 統合と移行（Claude Code）

これは**通常のインタラクティブなセッション**で実行してください — 判断を多く
要し、人間の承認ゲートを必要とするため、自律的なループの中で実行しては
**いけません**。

1. **まず棚卸しし、まだ何も移動しないこと。** ツールが生成したファイルも
   含め、リポジトリ全体のあらゆるドキュメントを見つけます。それぞれを分類し、
   表を作成します。`[KEEP-tool]` 仕組み・`[KEEP-log]` セッションの走り書き・
   `[MOVE-knowledge]` 実際のプロジェクト知識・`[MIXED]` 知識を含む仕組み。
   **人間の承認のために停止します。**
2. **決して削除しないこと。** ファイルを移動し、元のパスには短い **stub**
   （`status: stub`、`moved_to: …`、および wikilink）を残して、何も壊れない
   ようにします。
3. **フォルダのスケルトンは仮説として扱うこと。** `assets/vault-structure.md`
   から始め、実際のドキュメントが収まらない箇所についてのみ追加・統合を提案
   します。トップレベルのフォルダは約 6〜8 個に抑えます。
4. **frontmatter と wikilink を追加すること。** すべてのノートに `title`、
   `status`、`source`、`updated`、および関連ノートへの `[[links]]` を付与し、
   再断片化を防ぎます。
5. **ADR を再構築すること。** 根拠が復元可能な箇所で再構築し、不確かなものは
   「confirm needed」とマークします — 決して捏造しないでください。
6. **`.gitignore`**（頻繁に変化する Obsidian のファイルのみ）と **`CLAUDE.md`**
   を更新し、vault を source of truth と宣言します。

### トラック B — Claude Desktop を接続し、指示を適用する

1. **`<repo>/docs` を独立した vault として開くこと。** Obsidian で、個人用の
   巨大な vault とは分離して開き、MCP がこのプロジェクトのみを公開するように
   します。
2. **「Claude Code MCP」コミュニティプラグインをインストールすること。** これは
   二つのサーバーを公開します。**WebSocket** サーバー（`/ide` 経由の
   Claude Code 用）と **HTTP/SSE** サーバー（Claude Desktop 用、
   `http://localhost:<HTTP_PORT>/sse`）です。
3. **vault ごとに一意の HTTP ポートを割り当てること。** 複数を動かす場合
   （例えばこのプロジェクトは `22361`、個人 vault は `22360`）— そうしないと
   ポートを奪い合ってしまいます。
4. **`mcp-remote` の stdio ブリッジ経由で Claude Desktop を接続すること。**
   `claude_desktop_config.json` に bare な `"url"` を貼り付けては**いけません**
   — Desktop は stdio のみを検証し、それを黙って切り捨てます。スニペットは
   `assets/claude-desktop-config-snippet.md` にあります。その後、完全に終了
   （Cmd+Q）して再起動してください。
5. **Claude Code を接続する:** `claude` → `/ide` → **Obsidian** を選択。設定
   ファイルは不要です。
6. **検証する。** 読み取りテスト（vault のファイル一覧を取得）と書き込み
   テスト（ノートを作成し、Obsidian にリアルタイムで表示されることを確認）で
   検証します。
7. **プロジェクトの指示を生成する。**
   `assets/project-instructions-template.md` から、このプロジェクトの MCP
   サーバー名とフォルダのカテゴリに合わせて生成し、claude.ai プロジェクトの
   Custom Instructions に貼り付けます。

## vault 構造

ライフサイクルに基づく開始用スケルトン（棚卸しの際にプロジェクトへ適応
させてください）:

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

**トップ層 = ライフサイクルに基づく**（ビジネス vs プロダクト vs 決定 vs
リサーチ）: これらはめったに変わらず、再編成するとリンクが壊れるため
コストが高くつきます。サブフォルダと名前はコストが低く、実際のコンテンツ
から育てていくべきです。

## プロジェクトごとに埋めるパラメータ

まずこれらを解決してください（不明な場合は確認します）:

| プレースホルダ | 意味 | 例 |
|---|---|---|
| `{{PROJECT_NAME}}` | 人間向けのプロジェクト名 | OurStory |
| `{{MCP_SERVER_NAME}}` | Desktop 設定でのサーバー名 | obsidian-ourstory |
| `{{VAULT_PATH}}` | vault への絶対パス | /Users/you/ourstory/docs |
| `{{HTTP_PORT}}` | Obsidian プラグインの HTTP/SSE ポート（vault ごとに一意） | 22361 |
| `{{NPX_PATH}}` | npx への絶対パス（`which npx`） | /Users/you/.nvm/.../bin/npx |

## ガードレール（交渉の余地なし）

- **決してドキュメントを削除しないこと** — 移動 + stub、またはアーカイブ。
  移行マップを保持します。
- **決してツールの仕組みに手を触れないこと**（`superpowers/`、`plans/`、
  `specs/`、`.claude/`）。ただし source-of-truth のルールで `CLAUDE.md`
  を*更新*する場合を除きます。
- **移行の前に棚卸しすること。** 分類について人間の承認を得ます。
- **トラック A を自律的なループの中で実行しないこと** — 承認ゲートを
  必要とします。
- **vault に書き込む事実を決して捏造しないこと。** 未確認の値は
  プレースホルダでマークします。

## レイアウト

単一プラグインのリポジトリ — リポジトリのルートが**そのまま**プラグインで
あり、同時にそれ自体が一プラグインの marketplace でもあります
（`source: "./"`）:

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

## 公開

[Johan Kim](https://github.com/hiphapis) が作成しました。Claude Code が
取得できるよう、リポジトリは**公開**されている必要があります。インストール
済みのユーザーに届けるべき変更を加えるたびに、`.claude-plugin/plugin.json`
の `version` を更新してください — バージョンの更新が、アップデートの
シグナルとなります。

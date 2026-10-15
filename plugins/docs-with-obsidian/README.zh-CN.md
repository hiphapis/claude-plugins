# docs-with-obsidian

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **中文**

一个 [Claude Code](https://claude.com/claude-code) 插件，它封装了一套完整、
久经实战的方法论，用于把软件项目中零散分布的文档整理成一个组织良好、链接丰富的
**Obsidian vault**。该 vault 位于仓库的 `/docs` 文件夹中，由 Claude Code、
Claude Desktop 以及你共享，并全部通过 git 保持同步。

文档往往支离破碎。有些散落在 `README` 里，有些在 `.claude/` 中，有些藏在工具输出里
（superpowers、omc、loopcraft），还有些只存在于你的脑海中。本插件将一套经过验证的
端到端流程固化下来——**包括那些实实在在耗费时间的配置坑**——把所有这些内容整合进一个
vault，让每一位参与者都把它当作唯一可信来源（source of truth）。

## 心智模型（请先读这一段）

三位参与者作用于**磁盘上同一个 `<repo>/docs` 文件夹**，并通过 **git** 保持同步：

| 参与者 | 角色 | 最适合 | 需要打开 Obsidian 吗？ |
|-------------|------|----------|:---:|
| **Claude Code**（终端） | 直接对磁盘上的仓库文件进行操作 | 批量文件处理——整合、移动、分类、迁移、`.gitignore`、提交。原生支持 git。 | 否 |
| **Claude Desktop** | 通过 Obsidian 的 "Claude Code MCP" 插件连接到 vault | 笔记的日常读取/更新，可感知 vault，实时同步 | 是 |
| **Obsidian** | 人类的编辑界面，也是 MCP 服务器的宿主 | 阅读、建立链接、关系图视图 | — |

vault 位于 **`<repo>/docs`**——而非仓库根目录（那样会把 `node_modules` 和代码也索引进来）。
一个仓库同时承载代码和文档，因此单次 `git pull` 就能把所有内容同步到同一时间点。

## 你将获得什么

一个技能（`docs-with-obsidian`），封装了一套双轨方法论，外加执行它所需的模板和参考流程：

| 组件 | 作用 |
|-----------|--------------|
| **Track A —— 整合与迁移**（`references/claude-code-setup.md`） | 盘点仓库中的每一份文档 → 分类（`KEEP-tool` / `KEEP-log` / `MOVE-knowledge` / `MIXED`）→ **暂停以等待人工批准** → 移动（绝不删除），在原路径留下一个 stub → 应用文件夹骨架 → 添加 frontmatter 和 `[[wikilinks]]` → 重建 ADR → 更新 `.gitignore` 和 `CLAUDE.md`。 |
| **Track B —— 连接与指令**（`references/desktop-mcp-setup.md`） | 把 `<repo>/docs` 作为独立 vault 打开 → 安装 "Claude Code MCP" 插件 → 为每个 vault 分配唯一的 HTTP 端口 → 通过 `mcp-remote` stdio 桥接 Claude Desktop → 通过 `/ide` 连接 Claude Code → 用一次读取 + 写入测试进行验证 → 生成项目指令，让 vault 成为唯一可信来源。 |
| **Vault 骨架**（`assets/vault-structure.md`） | 一套基于生命周期的文件夹起步结构（`00-dashboard` … `06-dev-rules`、`_templates`）——它是一个可供调整的假设，而非强制规定。文件夹名称可以本地化。 |
| **迁移提示词**（`assets/migration-prompt.md`） | 一份可直接粘贴、已通用化的 Track-A 提示词——填空后交给 Claude Code。 |
| **项目指令模板**（`assets/project-instructions-template.md`） | 一套自定义指令（Custom Instructions），让 claude.ai（通过 MCP）把 vault 作为唯一可信来源进行查询，并把结论写回去。 |
| **ADR 模板**（`assets/adr-template.md`） | 每个历史决策对应一条笔记；对于无法确定的理由，留下 "confirm needed" 占位符，而不是凭空编造。 |
| **Desktop MCP 配置片段**（`assets/claude-desktop-config-snippet.md`） | 精确的 `mcp-remote` 桥接 JSON——避免那种裸 `url` 导致服务器被静默丢弃的失败。 |
| **故障排查**（`references/troubleshooting.md`） | 真实世界中的各种坑：nvm node 版本不匹配、端口冲突、裸 `url` 失败、极简 PATH、双机会话。 |

## 安装

**方式 A —— 通过 marketplace（推荐）：**

```
/plugin marketplace add hiphapis/docs-with-obsidian
/plugin install docs-with-obsidian@docs-with-obsidian
/reload-plugins
```

**方式 B —— 本地克隆（用于开发）：**

```bash
git clone https://github.com/hiphapis/docs-with-obsidian.git
claude --plugin-dir ./docs-with-obsidian
```

该技能注册为 `docs-with-obsidian:docs-with-obsidian`，每当你请求把项目文档整理进
Obsidian、搭建文档 vault、整合零散文档、通过 MCP 把 Obsidian 连接到
Claude Desktop/Code，或把文档迁移进 vault 时，它都会被触发——即便你没有明确说出
"Obsidian" 或 "skill"。

## 用法

该技能包含**两条 track**。大多数项目两条都需要，且需按顺序进行。

### Track A —— 整合与迁移（Claude Code）

请在**普通的交互式会话**中运行它——它高度依赖判断，需要人工批准关卡，因此**不要**在
自主循环中运行它。

1. **先盘点，暂不移动任何文件。** 找出仓库中的每一份文档，包括工具生成的文件。
   对每一份进行分类并生成一张表：
   `[KEEP-tool]` 工具机制 · `[KEEP-log]` 会话草稿 ·
   `[MOVE-knowledge]` 真正的项目知识 · `[MIXED]` 包含知识的工具机制文件。
   **暂停以等待人工确认。**
2. **绝不删除。** 移动文件，在原路径留下一条简短的 **stub**
   （`status: stub`、`moved_to: …`，外加一个 wikilink），以免破坏任何引用。
3. **文件夹骨架只是一个假设。** 从 `assets/vault-structure.md` 起步；
   仅在真实文档确实不适合时才提议增加/合并。顶层文件夹保持在约 6–8 个。
4. **添加 frontmatter + wikilinks。** 每条笔记都要有 `title`、`status`、
   `source`、`updated`，并用 `[[links]]` 链接到相关笔记，以防止再次碎片化。
5. **重建 ADR**——在理由可复原之处进行；对不确定的标记为
   "confirm needed"，绝不凭空编造。
6. **更新 `.gitignore`**（只忽略那些频繁变动的 Obsidian 文件）以及 **`CLAUDE.md`**，
   声明 vault 为唯一可信来源。

### Track B —— 连接 Claude Desktop 并应用指令

1. **把 `<repo>/docs` 作为独立 vault 打开**，与任何个人的超大 vault 分开，
   这样 MCP 只暴露本项目。
2. **安装 "Claude Code MCP" 社区插件。** 它暴露两个服务器：一个
   **WebSocket** 服务器（供 Claude Code 通过 `/ide` 使用），一个 **HTTP/SSE** 服务器
   （供 Claude Desktop 使用，地址为 `http://localhost:<HTTP_PORT>/sse`）。
3. 如果你运行了多个 vault，则**为每个 vault 分配唯一的 HTTP 端口**（例如本项目
   `22361`、个人 vault `22360`）——否则它们会争抢端口。
4. **通过 `mcp-remote` stdio 桥接 Claude Desktop。** **不要**把裸的
   `"url"` 粘贴进 `claude_desktop_config.json`——Desktop 只校验 stdio，
   会静默地把它丢弃。片段见 `assets/claude-desktop-config-snippet.md`。
   之后请彻底退出（Cmd+Q）并重新启动。
5. **连接 Claude Code：** `claude` → `/ide` → 选择 **Obsidian**。无需配置文件。
6. **验证**：做一次读取测试（列出 vault 文件）和一次写入测试（创建一条笔记，
   确认它在 Obsidian 中实时出现）。
7. **生成项目指令**——基于
   `assets/project-instructions-template.md`，按本项目的 MCP
   服务器名称和文件夹分类进行定制，然后粘贴进 claude.ai 项目的自定义指令中。

## Vault 结构

一套基于生命周期的起步骨架（在盘点过程中根据项目进行调整）：

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

**顶层 = 基于生命周期**（business、product、decisions、research）：
这些很少变动，且重新组织代价高昂，因为会破坏链接。
子文件夹和名称则代价低廉，应从真实内容中自然生长出来。

## 每个项目需要填写的参数

请先确定这些参数（不清楚就询问）：

| 占位符 | 含义 | 示例 |
|---|---|---|
| `{{PROJECT_NAME}}` | 面向人类的项目名称 | OurStory |
| `{{MCP_SERVER_NAME}}` | Desktop 配置中的服务器名称 | obsidian-ourstory |
| `{{VAULT_PATH}}` | vault 的绝对路径 | /Users/you/ourstory/docs |
| `{{HTTP_PORT}}` | Obsidian 插件的 HTTP/SSE 端口（每个 vault 唯一） | 22361 |
| `{{NPX_PATH}}` | npx 的绝对路径（`which npx`） | /Users/you/.nvm/.../bin/npx |

## 护栏（不可妥协）

- **绝不删除文档**——移动 + stub，或归档。保留一份迁移映射表。
- **绝不触碰工具机制**（`superpowers/`、`plans/`、`specs/`、
  `.claude/`），唯一例外是*更新* `CLAUDE.md` 以加入唯一可信来源规则。
- **迁移前先盘点**；就分类结果取得人工确认。
- **不要在自主循环中运行 Track A**——它需要批准关卡。
- **绝不把凭空编造的事实**写入 vault；对未经确认的值用占位符标记。

## 目录结构

单插件仓库——仓库根目录**就是**该插件，同时也是它自身的
单插件 marketplace（`source: "./"`）：

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

## 发布

由 [Johan Kim](https://github.com/hiphapis) 编写。仓库必须是**公开的**，
Claude Code 才能拉取它。每次需要触达已安装用户的改动，都要在
`.claude-plugin/plugin.json` 中提升 `version`——版本号的提升就是更新信号。

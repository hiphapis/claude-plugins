# Track B — Connect Claude Desktop (and Claude Code) to the vault

Goal: Claude Desktop reads vault notes and writes results back into the vault,
vault-aware and live. This works through the **Obsidian "Claude Code MCP"
community plugin**, which runs an MCP server *inside* Obsidian.

> ⚠️ The MCP server lives inside the Obsidian plugin, so **Obsidian must be
> running** for Desktop/Code to reach it. For work that must run headless, keep
> Claude Code's direct-on-disk access as the fallback.

## Step 1 — Open the project's docs as its own vault

In Obsidian: `Open another vault` → select `<repo>/docs`. Keep this separate
from any large personal vault, so the MCP only exposes this project's docs (not
unrelated personal/career notes). Each machine that participates needs the
plugin installed in its own Obsidian.

## Step 2 — Install & configure the plugin

Install the **Claude Code MCP** community plugin in this vault (via Community
plugins, or BRAT for beta). It shows two servers under its settings:

- **WebSocket Server (Claude Code)** — for Claude Code IDE integration via lock
  files; connect with the `claude` CLI and pick "Obsidian" from `/ide`.
- **MCP Server (HTTP/SSE transport)** — for Claude Desktop and other MCP
  clients, at `http://localhost:<HTTP_PORT>/sse`.

## Step 3 — Give each vault a unique port (if you run more than one)

If you also run another vault with this plugin, the servers will fight over the
same ports when both are open. In the plugin's **HTTP Server Port** field, set a
distinct port per vault (e.g. project A = 22361, personal vault = 22360). Note
the WebSocket port too; it may auto-pick a free port.

## Step 4 — Wire Claude Desktop (mcp-remote bridge)

**Do NOT** paste the plugin's suggested `"url": "http://localhost:<port>/sse"`
straight into `claude_desktop_config.json`. Claude Desktop's local config
validates **stdio** servers only; a bare `url` field is silently dropped, or the
app boots with zero tools, or crashes. Use the **`mcp-remote` stdio bridge**
instead. See `assets/claude-desktop-config-snippet.md` for the exact JSON.

Config file (macOS): `~/Library/Application Support/Claude/claude_desktop_config.json`
(open via `Settings → Developer → Edit Config`).

After saving, **fully quit** Claude Desktop (Cmd+Q) and relaunch — config is
read only at startup. An MCP tools indicator should appear at the bottom-right
of the input box.

If you already have other MCP servers configured, add the new entry **inside**
the existing `mcpServers` object rather than overwriting the whole file.

## Step 5 — Connect Claude Code (if used on this machine)

No config file needed. With Obsidian open, run `claude` in the terminal →
type `/ide` → select **Obsidian**. It auto-discovers via the lock file. Two
machines can each run their own Claude Code independently — the lock files are
local, so there's no shared-session conflict; the only shared surface is git.

## Step 6 — Verify

- **Read test**: ask Claude Desktop to list the vault's files.
- **Write test**: ask it to create a small test note; confirm it appears live in
  Obsidian (an approval prompt per file operation is normal).

Success = green/connected status + visible tool list + the note actually
appearing in Obsidian. A log line like "Server started and connected
successfully" alone is not proof — it can die immediately after on a module
error (see troubleshooting).

## Step 7 — Generate & apply project instructions

Fill `assets/project-instructions-template.md` with this project's
`{{MCP_SERVER_NAME}}` and its actual folder categories, then paste into the
claude.ai project's **Custom Instructions**. This makes Claude consult the vault
as source of truth (instead of relying only on attached snapshots) and offer to
write conclusions back — but only while that project has the same MCP connected.

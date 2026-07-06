# Troubleshooting — the gotchas that actually bite

These are the failure modes seen in practice, with the fix that worked.

## 1. `Cannot find module 'node:path'` / server disconnects immediately (nvm)

**Symptom:** Desktop MCP shows `failed` / "Server disconnected". Logs show the
process started then died with `Error: Cannot find module 'node:path'` and a
`MODULE_NOT_FOUND` stack from an old node path.

**Cause:** You pointed `command` at the correct (new) `npx`, but that npx
internally resolves `node` from PATH — and the config's PATH lists **old nvm
node versions first** (e.g. v8/v12), so an ancient node runs npx and dies (old
node has no `node:path` scheme).

**Fixes (any one):**
- **Set a default nvm node** so PATH resolution is sane:
  `nvm alias default <version>` (e.g. `24.18.0`), then restart Desktop. This is
  the cleanest fix.
- **Run node directly** instead of npx:
  ```json
  {
    "command": "/abs/path/.nvm/versions/node/vXX/bin/node",
    "args": ["/abs/path/.nvm/versions/node/vXX/bin/npx", "-y", "mcp-remote",
             "http://localhost:<PORT>/sse"]
  }
  ```
- **Pin PATH via `env`** so only the desired node is visible:
  ```json
  "env": { "PATH": "/abs/.nvm/versions/node/vXX/bin:/usr/local/bin:/usr/bin:/bin" }
  ```

**Note:** an nvm-versioned path breaks when you upgrade node. If Desktop MCP
suddenly stops connecting later, suspect a node version bump and re-check the
path / re-run `nvm alias default`.

## 2. Bare `"url"` in claude_desktop_config.json does nothing

**Symptom:** You added `"url": "http://localhost:<port>/sse"` as the plugin
suggested; Desktop shows no tools, drops the entry, or crashes on next save.

**Cause:** Claude Desktop's local config schema validates **stdio** servers
only. `url`/`type:"http"` are for a *different* client (Claude Code CLI reads a
richer schema). The two products have different parsers.

**Fix:** Use the `mcp-remote` stdio bridge (see
`assets/claude-desktop-config-snippet.md`), or register it as a Custom Connector
in Settings (Pro/Max+; localhost may be blocked by CORS, so mcp-remote is more
reliable for local servers).

## 3. Minimal PATH — short `npx`/`node` not found

**Symptom:** Works in your terminal, fails from Desktop config.

**Cause:** Claude Desktop launches config commands with a minimal PATH, so bare
`npx`/`node`/`docker` often aren't found.

**Fix:** Always use the **absolute path** to the executable. Find it with
`which npx`.

## 4. Port conflict between two vaults

**Symptom:** Opening a second vault (also running the plugin) fails to start its
MCP server, or one vault's server won't bind.

**Cause:** Both plugin instances try to bind the same HTTP/WebSocket ports.

**Fix:** Give each vault a distinct **HTTP Server Port** in the plugin settings
(e.g. 22360 vs 22361), and point each Desktop config entry at the right port. Or
only keep one vault open at a time.

## 5. "Connected successfully" but still no tools

The log line "Server started and connected successfully" only means the process
launched. Real success = the tools indicator appears and a live list/read works.
If it's absent, scroll the logs for a later crash (usually issue #1 above).

## 6. Two machines — is there a session conflict?

No. Claude Code is a local process; the WebSocket lock file lives in each
machine's `~/.claude/ide/` and each Claude Code pairs with its **own local**
Obsidian. There's no shared session. The **only** shared surface is the git
repo, so the only real risk is a git merge conflict from near-simultaneous edits
to the same note. Habit: `git pull` before working, `git push` when leaving.
Markdown conflicts are text and easy to resolve by hand.

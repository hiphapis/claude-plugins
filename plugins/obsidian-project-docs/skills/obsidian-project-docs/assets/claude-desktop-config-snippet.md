# Claude Desktop config — Obsidian MCP via mcp-remote bridge

Location (macOS): `~/Library/Application Support/Claude/claude_desktop_config.json`
(open via `Settings → Developer → Edit Config`). After saving, **Cmd+Q** to fully
quit Claude Desktop, then relaunch (config is read only at startup).

If you already have other MCP servers, add this entry **inside** the existing
`mcpServers` object; don't overwrite the whole file.

## Standard form

```json
{
  "mcpServers": {
    "{{MCP_SERVER_NAME}}": {
      "command": "{{NPX_PATH}}",
      "args": ["-y", "mcp-remote", "http://localhost:{{HTTP_PORT}}/sse"]
    }
  }
}
```

- `{{NPX_PATH}}` = absolute path from `which npx` (Desktop uses a minimal PATH,
  so a bare `npx` often fails).
- `{{HTTP_PORT}}` = the plugin's HTTP Server Port for THIS vault (unique per
  vault, e.g. 22361).

## nvm-hardened form (use if the standard form disconnects immediately)

If logs show `Cannot find module 'node:path'` / MODULE_NOT_FOUND, an old nvm
node is being resolved. Best fix: `nvm alias default <version>` then restart.
If that's not viable, run node directly:

```json
{
  "mcpServers": {
    "{{MCP_SERVER_NAME}}": {
      "command": "/Users/you/.nvm/versions/node/vXX.XX.X/bin/node",
      "args": [
        "/Users/you/.nvm/versions/node/vXX.XX.X/bin/npx",
        "-y", "mcp-remote", "http://localhost:{{HTTP_PORT}}/sse"
      ]
    }
  }
}
```

Or pin PATH:

```json
{
  "mcpServers": {
    "{{MCP_SERVER_NAME}}": {
      "command": "{{NPX_PATH}}",
      "args": ["-y", "mcp-remote", "http://localhost:{{HTTP_PORT}}/sse"],
      "env": { "PATH": "/Users/you/.nvm/versions/node/vXX.XX.X/bin:/usr/local/bin:/usr/bin:/bin" }
    }
  }
}
```

## Do NOT do this

```json
// ❌ Claude Desktop validates stdio only — a bare url is silently dropped.
{ "mcpServers": { "x": { "url": "http://localhost:22361/sse" } } }
```

Success check: relaunch → MCP tools indicator appears bottom-right of the input
box → ask Claude to list vault files.

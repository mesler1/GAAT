# Web UI Guide

CheetahClaws includes a built-in web interface that runs entirely from the Python stdlib — no Node.js, no React, no external dependencies. Start it with `--web` and open your browser.

## Quick Start

```bash
cheetahclaws --web                          # localhost:8080
cheetahclaws --web --port 8008              # custom port
cheetahclaws --web --no-auth                # no password (local only)
cheetahclaws --web --host 0.0.0.0           # accessible from network
```

The server prints a random password on startup:

```
  CheetahClaws Web Terminal
  ────────────────────────────────────────
  Terminal: http://localhost:8080
  Chat UI:  http://localhost:8080/chat
  Password: aBcDeF
  ────────────────────────────────────────
  Press Ctrl+C to stop
```

## Two Interfaces

### Chat UI — `http://localhost:8080/chat`

A rich, structured chat interface. Messages, tool calls, and approval requests are rendered as separate UI components — not raw terminal text.

**Layout:**
- **Left sidebar** — session list, "+" New button
- **Center** — chat messages, tool cards, approval cards, activity indicator
- **Top bar** — status dot, theme toggle (☾/☀), settings gear (⚙)

**Features:**

| Feature | How It Works |
|---------|-------------|
| Streaming text | Assistant responses stream word-by-word via Server-Sent Events |
| Tool cards | Each tool call gets a collapsible card showing name, inputs, outputs, and status badge (running/done/denied) |
| Permission cards | When the agent needs approval, an Allow/Deny card appears inline |
| Activity indicator | Spinner + label shows current state: "Processing...", "Thinking...", "Running Bash...", etc. |
| Slash commands | All 45+ commands work. Quick commands (`/status`, `/help`) return results instantly. Long-running commands (`/brainstorm`, `/worker`) stream events in real-time via SSE |
| SSJ Mode | `/ssj` shows a clickable 12-item menu. Sub-commands like `/ssj debate` and `/ssj commit` run directly without the menu |
| Brainstorm | `/brainstorm` asks for a topic first (with input box), then streams the multi-agent debate. `/brainstorm <topic>` starts immediately |
| Settings panel | Change model, toggle thinking/verbose, set API keys, run quick commands |
| Dark/Light theme | Click ☾/☀ in the top bar. Choice persisted in localStorage |
| Feature dashboard | Welcome screen shows 24 features in 6 categories with clickable cards |
| Mobile responsive | Sidebar becomes an overlay on small screens |

### PTY Terminal — `http://localhost:8080/`

A full xterm.js terminal emulator in the browser — identical to using CheetahClaws in a native terminal. 100% feature parity.

- WebSocket transport with automatic SSE fallback (works through VS Code port forwarding)
- xterm.js v5.5 with fit addon, web-links addon, 256-color ANSI support
- Auto-resize on window change

## Authentication

By default, the server generates a random 6-character password displayed on startup. Enter it in the login form to get a session cookie.

```
Password: aBcDeF
```

- Cookie: `cctoken`, `HttpOnly`, `SameSite=Strict`, `Path=/`, 24h expiry
- `--no-auth` disables the password entirely (suitable for localhost only)
- API endpoints return `401 Unauthorized` without a valid cookie
- Static pages (`/chat`, `/`) are served without auth; API calls require it

## Settings Panel

Click the ⚙ gear icon in the top bar to open the settings panel.

### Model Selection

Browse models grouped by provider (Anthropic, OpenAI, Gemini, Ollama, DeepSeek, etc.). Click any model to switch. The current model is highlighted.

Providers that need an API key but don't have one configured show a red "no key" badge.

### Behavior

| Setting | Options | Description |
|---------|---------|-------------|
| Permission Mode | auto / accept-all / manual | How tool calls are approved |
| Thinking | on/off | Enable extended thinking (Claude) |
| Verbose | on/off | Show token counts |
| Max Tokens | number | Maximum output tokens |
| Thinking Budget | number | Token budget for thinking |

### API Keys

Each provider shows a green dot (configured) or gray dot (not configured). Enter a key to set it for the current session. Keys are not persisted to disk — use environment variables for permanent storage.

### Quick Actions

Buttons for common commands: `Compact Context`, `Status`, `Context Usage`, `Cost`.

### Advanced

- **Open Terminal** — opens the PTY terminal in a new tab
- **Health Check** — runs `/doctor`
- **Help** — runs `/help`

## API Reference

All endpoints require authentication (cookie or `--no-auth` mode).

### `POST /api/prompt`

Submit a prompt or slash command.

**Request:**
```json
{
  "prompt": "/brainstorm improve testing",
  "session_id": "abc123"        // omit to create new session
}
```

**Response (quick command):**
```json
{
  "session_id": "abc123",
  "events": [
    {"type": "command_result", "data": {"command": "/status", "output": "..."}}
  ]
}
```

**Response (long-running, with `Accept: text/event-stream`):**
Server keeps the connection open and streams SSE:
```
data: {"type":"session","data":{"session_id":"abc123"}}
data: {"type":"status","data":{"state":"running"}}
data: {"type":"text_chunk","data":{"text":"Generating personas..."}}
data: {"type":"text_chunk","data":{"text":"Agent 1 thinking..."}}
...
data: {"type":"status","data":{"state":"idle"}}
data: {"type":"done"}
```

### `WS /api/events`

WebSocket connection for real-time event streaming.

**Connect:** `ws://localhost:8080/api/events` (browser sends cookie automatically)

**First frame (client → server):**
```json
{"session_id": "abc123"}
```

**Subsequent frames (client → server):**
```json
{"type": "prompt", "prompt": "hello"}
{"type": "approve", "granted": true}
```

**Events (server → client):**
```json
{"type": "text_chunk", "data": {"text": "Hello!"}, "ts": 1234567890.0}
{"type": "tool_start", "data": {"name": "Bash", "inputs": {"command": "ls"}}}
{"type": "tool_end", "data": {"name": "Bash", "result": "...", "permitted": true}}
{"type": "permission_request", "data": {"description": "Write to file.txt"}}
{"type": "turn_done", "data": {"input_tokens": 1234, "output_tokens": 567}}
{"type": "status", "data": {"state": "running"}}
{"type": "status", "data": {"state": "idle"}}
{"type": "command_result", "data": {"command": "/status", "output": "..."}}
{"type": "interactive_menu", "data": {"menu": "ssj", "items": [...]}}
{"type": "input_request", "data": {"prompt": "...", "command": "/brainstorm"}}
{"type": "error", "data": {"message": "..."}}
```

### `POST /api/approve`

Respond to a pending permission request.

```json
{"session_id": "abc123", "granted": true}
```

### `GET /api/sessions`

List all chat sessions.

```json
{
  "sessions": [
    {"id": "abc123", "created_at": 1234.5, "last_active": 1234.5,
     "busy": false, "message_count": 10}
  ]
}
```

### `GET /api/sessions/{id}`

Get session details with full message history.

```json
{
  "id": "abc123",
  "messages": [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hi! How can I help?", "tool_calls": [...]}
  ],
  "config": {"model": "anthropic/claude-sonnet-4-6", ...},
  "busy": false
}
```

### `GET/PATCH /api/config`

Read or update session configuration.

**GET:** `GET /api/config?sid=abc123`

**PATCH:**
```json
{"session_id": "abc123", "config": {"model": "openai/gpt-4o", "thinking": true}}
```

Writable keys: `model`, `permission_mode`, `verbose`, `thinking`, `thinking_budget`, `max_tokens`, plus API keys (session-only, not persisted).

### `GET /api/models`

List all providers and available models.

```json
{
  "providers": [
    {
      "provider": "anthropic",
      "models": ["claude-opus-4-6", "claude-sonnet-4-6", ...],
      "context_limit": 200000,
      "needs_api_key": true,
      "has_api_key": true
    },
    ...
  ]
}
```

### `POST /api/auth`

Login and get a session cookie.

```json
{"token": "aBcDeF"}
```

Returns `Set-Cookie: cctoken=...; HttpOnly; SameSite=Strict; Path=/; Max-Age=86400`.

## Architecture

```
web/
  server.py     — Pure-stdlib HTTP server, WebSocket (RFC 6455), SSE, routing
  api.py        — ChatSession, event broadcasting, slash command handling
  chat.html     — Self-contained chat UI (CSS + JS, no build step)
  marked.min.js — Markdown renderer (bundled)
  xterm.min.js  — Terminal emulator (bundled)
  xterm.min.css — Terminal styles
  addon-*.js    — xterm addons (fit, web-links)
```

**Key design decisions:**

- **Pure stdlib** — no Flask, no aiohttp, no external Python deps. The server is a raw socket handler with manual HTTP parsing and RFC 6455 WebSocket implementation.
- **In-process agent** — the Chat UI runs `agent.run()` directly (not via a PTY subprocess). Events are broadcast through a `queue.Queue` fan-out to WebSocket subscribers.
- **Event buffer** — events are buffered so late-connecting WebSocket clients can replay missed events.
- **Thread-local stdout** — long-running commands redirect their thread's stdout to broadcast `text_chunk` events without affecting other threads.
- **SSE for long commands** — `/brainstorm`, `/worker`, `/plan`, `/agent` use Server-Sent Events over a kept-alive HTTP connection. No WebSocket required.
- **Cookie auth** — `HttpOnly` + `SameSite=Strict` cookie. WebSocket and EventSource connections carry the cookie automatically. No token in URL query strings.

## Comparison: Chat UI vs PTY Terminal

| Aspect | Chat UI (`/chat`) | PTY Terminal (`/`) |
|--------|--------------------|--------------------|
| Rendering | Structured (Markdown, cards, buttons) | Raw ANSI terminal |
| Tool calls | Collapsible cards with status badges | Text output |
| Permissions | Click Allow/Deny buttons | Type y/N |
| Slash commands | Interactive menus, input boxes | Text prompts |
| Theme | Dark/Light toggle | Dark only |
| Settings | GUI panel | `/config` command |
| Feature parity | Most features via structured events | 100% (it IS the terminal) |
| Best for | Regular use, mobile, demo | Power users, debugging, features not yet in Chat UI |

## Troubleshooting

**Chat shows "disconnected"**
The WebSocket connection dropped. The UI auto-reconnects with exponential backoff. For slash commands, results are delivered via POST (no WS needed). For streaming prompts, the event buffer replays missed events on reconnect.

**"Failed to send" error**
Check that the server is running and the cookie is valid. Try refreshing the page to re-authenticate.

**Brainstorm shows "Working..." with no progress**
If using the POST fallback (WS unavailable), the brainstorm runs server-side and results appear when the command completes. For real-time streaming, ensure the SSE path is used (the Chat UI does this automatically for `/brainstorm`).

**Can't connect from another device**
Use `--host 0.0.0.0` to listen on all interfaces. The password is printed on the server's terminal.

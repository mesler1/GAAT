English | [中文](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/README.CN.MD) | [한국어](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/README.KO.MD) | [日本語](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/README.JP.MD) | [Français](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/README.FR.MD) | [Deutsch](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/README.DE.MD) | [Español](https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/README.ES.MD) | [Português](https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/README.PT.MD)

<br> 

<div align="center">
  <a href="[https://github.com/SafeRL-Lab/Robust-Gymnasium](https://github.com/SafeRL-Lab/clawspring)">
    <img src="docs/logo-5.png" alt="Logo" width="280"> 
  </a>

  
<h2 align="center" style="font-size: 30px;"><strong><em>CheetahClaws (Nano Claude Code) </em></strong>: A Fast, Easy-to-Use, Python-Native Personal AI Assistant for Any Model, Inspired by OpenClaw and Claude Code, Built to Work for You Autonomously 24/7</h2>
<p align="center">
    <a href="https://github.com/chauncygu/collection-claude-code-source-code">The newest source of Claude Code</a>
    ·
    <a href="https://github.com/SafeRL-Lab/clawspring/issues">Issue</a>
  ·
    <a href="https://deepwiki.com/SafeRL-Lab/clawspring">Brief Intro</a>
  
  </p>
</div>


 <div align=center>
 <img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Task Excution</center>
 </div>
 
 
---

  <div align=center>
 <img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/brainstorm_demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Brainstorm Mode: Multi-Agent Brainstorm</center>
 </div>



---

  <div align=center>
 <img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/proactive_demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Proactive Mode: Autonomous Agent</center>
 </div>

---

  <div align=center>
 <img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/ssj_demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">SSJ Developer Mode: Power Menu Workflow</center>
 </div>

---

  <div align=center>
 <img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/telegram_demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Telegram Bridge: Control cheetahclaws from Your Phone</center>
 </div>

---

  <div align=center>
 <img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/wechat_demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">WeChat Bridge: Control cheetahclaws from WeChat (微信)</center>
 </div>

---

  <div align=center>
 <img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/slack_demo.gif" width="850"/> 
 </div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Slack Bridge: Control cheetahclaws from Slack</center>
 </div>

---


 
## 🔥🔥🔥 News (Pacific Time)

 
- Apr 14, 2026 (**v3.05.69**): **Actionable error messages, dependency sync, and contributor guide**
  - **Actionable API error messages** (`cheetahclaws.py`) — the REPL error handler now detects 6 common failure modes (invalid API key, network timeout, Ollama not running, rate limit, model not found, insufficient credits) and prints a specific hint alongside the error instead of a generic message. The proactive watcher background thread no longer dumps raw Python tracebacks to stdout — errors are routed through `logging_utils` instead.
  - **Dependency sync** (`pyproject.toml`, `requirements.txt`) — `pyte>=0.8.0` added to `pyproject.toml` core dependencies (was only in `requirements.txt`, causing import failures after `pip install .`). `requirements.txt` rewritten to mirror `pyproject.toml` as single source of truth, with optional deps (`sounddevice`, `Pillow`) clearly marked.
  - **`CONTRIBUTING.md`** — new contributor guide covering project structure, architecture (config vs RuntimeContext, tool/plugin/hooks systems), development conventions, and a PR checklist. Addresses recurring PR issues where contributors misunderstood the plugin loader (`TOOL_DEFS` vs `register_tool()`), hooks system (no event-based hooks), and runtime state management.
  - **Version bumped to 3.05.69.**

- Apr 14, 2026 (**v3.05.68**): **CI/CD, config/runtime separation, and module reorganization**
  - **GitHub Actions CI** (`.github/workflows/ci.yml`) — added automated testing on every push and PR: `pytest` across Python 3.10–3.13, plus a package smoke test that installs via `pip install .` and verifies all modules are importable. No more silent packaging regressions.
  - **Config/runtime separation** (`runtime.py`) — runtime state (`_proactive_thread`, `_pending_image`, `_plan_file`, bridge turn flags, etc.) moved out of the `config` dict into `RuntimeContext` fields. The `config` dict now holds only serializable user configuration. Added `runtime.get_ctx(config)` helper for easy access. Migrated 18 files; 327 tests pass.
  - **Tool module reorganization** — 7 top-level `tools_*.py` files consolidated into a `tools/` package (`tools/security.py`, `tools/fs.py`, `tools/shell.py`, `tools/web.py`, `tools/notebook.py`, `tools/diagnostics.py`, `tools/interaction.py`). All existing `from tools import ...` code continues to work unchanged via `tools/__init__.py`.
  - **Version bumped to 3.05.68.**

- Apr 14, 2026 (**v3.05.67**): **Packaging fix, `/config` safety, and readline completion fix**
  - **Fix `ModuleNotFoundError` on `pip install` / `uv tool install`** (`pyproject.toml`) — 16 missing top-level modules (`logging_utils`, `agent_runner`, `tools_fs`, `tools_shell`, etc.) and the `monitor` package were not declared in `pyproject.toml`, causing `No module named 'logging_utils'` and similar crashes after installation (#36). All runtime modules are now correctly packaged.
  - **`/config` no longer exposes secrets** (`commands/config_cmd.py`) — the `/config` display now filters out sensitive keys (`api_key`, `telegram_token`, `wechat_token`, and any key ending in `_key`, `_token`, or `_secret`) as well as internal runtime keys (prefixed with `_`). Previously, `/config` crashed with `TypeError` on non-serializable `threading.Thread` objects and leaked credentials.
  - **Readline completion condition fix** (`cheetahclaws.py`) — changed `"/" in line` to `line.startswith("/")` in the completer and display hook, preventing false matches on non-slash input containing `/`. Completion menu now redisplays the prompt line correctly after showing matches.
  - **Version bumped to 3.05.67.**

- Apr 12, 2026 (**v3.05.66**): **Auto max_tokens cap per model + tool robustness fixes**
  - **Automatic `max_tokens` capping** (`providers.py`) — a new `resolve_max_tokens()` function automatically caps `max_tokens` to the model's actual limit before every API call, eliminating `BadRequestError: max_tokens cannot be greater than max_model_len` errors when using vLLM or other bounded local endpoints. Priority: (1) per-model hard limit from a built-in table of 30+ known models; (2) for `custom` provider, `GET /v1/models` is queried at first call and the `max_model_len` field is used (result cached per base URL); (3) provider-level `context_limit // 2` as a conservative fallback. The user's configured value is always treated as an upper bound — never increased.
  - **`KeyError: 'file_path'` in agent tool calls** (`tools.py`) — when a model (e.g. Qwen) generates a malformed tool call omitting the required `file_path` parameter for `Read` / `Write` / `Edit`, the agent runner now returns a descriptive error string (`"Error: missing required parameter 'file_path'"`) instead of crashing with an unhandled `KeyError`. The agent can then self-correct on the next iteration.
  - **`KeyError: 'white'` in `/agent` SSJ wizard** (`ui/render.py`) — `"white": "\033[37m"` added to the ANSI color table `C`; the agent wizard's summary box used `clr(name, 'white')` which crashed on startup.
  - **Version bumped to 3.05.66.**

- Apr 12, 2026 (**v3.05.65**): **`/agent` SSJ entry, bridge-compatible wizard, and `/monitor` interactive wizard fix**
  - **SSJ entry 14 — 🤖 Agent** (`commands/advanced.py`) — The SSJ power menu now has a 14th option that launches the `/agent` interactive wizard directly, covering all four autonomous templates (Research Assistant, Auto Bug Fixer, Paper Writer, Auto Coder).
  - **Bridge-compatible agent wizard** (`commands/agent_cmd.py`) — The wizard's input helper `_ask()` now routes through `ask_input_interactive()` so it works correctly over Telegram, Slack, and WeChat bridges (previously used bare `input()` which is terminal-only).
  - **`/monitor` interactive wizard input fix** (all three bridges) — When the `/monitor` wizard sends a menu to a bridge and waits for user input, the next message from the user was incorrectly treated as a new AI query. Each bridge's poll loop now checks `session_ctx.tg/slack/wx_input_event` before dispatching to the AI — wizard replies are correctly routed back to the waiting prompt.
  - **Version bumped to 3.05.65.**








 
For more news, see [here](https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/news.md)


---

# CheetahClaws

CheetahClaws: **A Lightweight** and **Easy-to-Use** Python Reimplementation of Claude Code **Supporting Any Model**, such as Claude, GPT, Gemini, Kimi, Qwen, Zhipu, DeepSeek, MiniMax, and local open-source models via Ollama or any OpenAI-compatible endpoint.

---

## Content
  * [Why CheetahClaws](#why-cheetahclaws)
  * [CheetahClaws vs OpenClaw](#cheetahclaws-vs-openclaw)
  * [Features](#features)
  * [Supported Models](#supported-models)
  * [Installation](#installation)
  * [Usage: Closed-Source API Models](#usage--closed-source-api-models)
  * [Usage: Open-Source Models (Local)](#usage--open-source-models--local-)
  * [Model Name Format](#model-name-format)
  * [CLI Reference](#cli-reference)
  * [Slash Commands (REPL)](#slash-commands--repl-)
  * [Configuring API Keys](#configuring-api-keys)
  * [Permission System](#permission-system)
  * [Built-in Tools](#built-in-tools)
  * [Memory](#memory)
  * [Skills](#skills)
  * [Sub-Agents](#sub-agents)
  * [MCP (Model Context Protocol)](#mcp-model-context-protocol)
  * [Plugin System](#plugin-system)
  * [AskUserQuestion Tool](#askuserquestion-tool)
  * [Task Management](#task-management)
  * [Voice Input](#voice-input)
  * [Brainstorm](#brainstorm)
  * [SSJ Developer Mode](#ssj-developer-mode)
  * [Telegram Bridge](#telegram-bridge)
  * [WeChat Bridge](#wechat-bridge)
  * [Slack Bridge](#slack-bridge)
  * [Remote Control (Phone → Computer)](#remote-control-phone--computer)
  * [Monitor — AI Subscriptions & Alerts](#monitor--ai-subscriptions--alerts)
  * [Autonomous Agents](#autonomous-agents)
  * [Video Content Factory](#video-content-factory)
  * [TTS Content Factory](#tts-content-factory)
  * [Tmux Integration](#tmux-integration)
  * [Shell Escape](#shell-escape)
  * [Proactive Background Monitoring](#proactive-background-monitoring)
  * [Checkpoint System](#checkpoint-system)
  * [Plan Mode](#plan-mode)
  * [Context Compression](#context-compression)
  * [Diff View](#diff-view)
  * [CLAUDE.md Support](#claudemd-support)
  * [Session Management](#session-management)
  * [Cloud Sync (GitHub Gist)](#cloud-sync-github-gist)
  * [Project Structure](#project-structure)
  * [FAQ](#faq)
  * [Citation](#citation)




## Why CheetahClaws

Claude Code is a powerful, production-grade AI coding assistant — but its source code is a compiled, 12 MB TypeScript/Node.js bundle (~1,300 files, ~283K lines). It is tightly coupled to the Anthropic API, hard to modify, and impossible to run against a local or alternative model.

**CheetahClaws** reimplements the same core loop in ~10K lines of readable Python, keeping everything you need and dropping what you don't. See here for more detailed analysis (CheetahClaws v3.03), [English version](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/comparison_claude_code_vs_nano_v3.03_en.md) and [Chinese version](https://github.com/SafeRL-Lab/clawspring/blob/main/docs/comparison_claude_code_vs_nano_v3.03_cn.md)

### At a glance

| Dimension | Claude Code (TypeScript) | CheetahClaws (Python) |
|-----------|--------------------------|---------------------------|
| Language | TypeScript + React/Ink | Python 3.8+ |
| Source files | ~1,332 TS/TSX files | ~85 Python files |
| Lines of code | ~283K | ~12K |
| Built-in tools | 44+ | 27 |
| Slash commands | 88 | 36 |
| Voice input | Proprietary Anthropic WebSocket (OAuth required) | Local Whisper / OpenAI API — works offline, no subscription |
| Model providers | Anthropic only | 8+ (Anthropic · OpenAI · Gemini · Kimi · Qwen · DeepSeek · MiniMax · Ollama · …) |
| Local models | No | Yes — Ollama, LM Studio, vLLM, any OpenAI-compatible endpoint |
| Build step required | Yes (Bun + esbuild) | No — run directly with `python cheetahclaws.py` (or install to use `cheetahclaws`) |
| Runtime extensibility | Closed (compile-time) | Open — `register_tool()` at runtime, Markdown skills, git plugins |
| Task dependency graph | No | Yes — `blocks` / `blocked_by` edges in `task/` package |

### Where Claude Code wins

- **UI quality** — React/Ink component tree with streaming rendering, fine-grained diff visualization, and dialog systems.
- **Tool breadth** — 44 tools including `RemoteTrigger`, `EnterWorktree`, and more UI-integrated tools.
- **Enterprise features** — MDM-managed config, team permission sync, OAuth, keychain storage, GrowthBook feature flags.
- **AI-driven memory extraction** — `extractMemories` service proactively extracts knowledge from conversations without explicit tool calls.
- **Production reliability** — single distributable `cli.js`, comprehensive test coverage, version-locked releases.

### Where CheetahClaws wins

- **Multi-provider** — switch between Claude, GPT-4o, Gemini 2.5 Pro, DeepSeek, Qwen, MiniMax, or a local Llama model with `--model` or `/model` — no recompile needed.
- **Local model support** — run entirely offline with Ollama, LM Studio, or any vLLM-hosted model.
- **Readable source** — the full agent loop is 174 lines (`agent.py`). Any Python developer can read, fork, and extend it in minutes.
- **Zero build** — `pip install -r requirements.txt` and you're running. Changes take effect immediately.
- **Dynamic extensibility** — register new tools at runtime with `register_tool(ToolDef(...))`, install skill packs from git URLs, or wire in any MCP server.
- **Task dependency graph** — `TaskCreate` / `TaskUpdate` support `blocks` / `blocked_by` edges for structured multi-step planning (not available in Claude Code).
- **Two-layer context compression** — rule-based snip + AI summarization, configurable via `preserve_last_n_turns`.
- **Notebook editing** — `NotebookEdit` directly manipulates `.ipynb` JSON (replace/insert/delete cells) with no kernel required.
- **Diagnostics without LSP server** — `GetDiagnostics` chains pyright → mypy → flake8 → py_compile for Python and tsc/shellcheck for other languages, with zero configuration.
- **Offline voice input** — `/voice` records via `sounddevice`/`arecord`/SoX, transcribes with local `faster-whisper` (no API key, no subscription), and auto-submits. Keyterms from your git branch and project files boost coding-term accuracy.
- **Cloud session sync** — `/cloudsave` backs up conversations to private GitHub Gists with zero extra dependencies; restore any past session on any machine with `/cloudsave load <id>`.
- **SSJ Developer Mode** — `/ssj` opens a persistent power menu with 10 workflow shortcuts: Brainstorm → TODO → Worker pipeline, expert debate, code review, README generation, commit helper, and more. Stays open between actions; supports `/command` passthrough.
- **Telegram Bot Bridge** — `/telegram <token> <chat_id>` turns cheetahclaws into a Telegram bot: receive user messages, run the model, and send back responses — all from your phone. Slash commands pass through, and a typing indicator keeps the chat feeling live.
- **WeChat Bridge** — `/wechat login` authenticates with WeChat via a QR code scan (the same iLink Bot API used by the official WeixinClawBot / `openclaw-weixin` plugin), then starts a long-poll bridge. Slash command passthrough, interactive menu routing, typing indicator, session auto-recovery, and per-peer `context_token` management all work out of the box.
- **Slack Bridge** — `/slack <xoxb-token> <channel_id>` connects cheetahclaws to a Slack channel using the Slack Web API (stdlib only — no `slack_sdk` required). Polls `conversations.history` every 2 seconds; replies update an in-place "Thinking…" placeholder. Slash command passthrough, interactive menu routing, and auto-start on launch.
- **Worker command** — `/worker` auto-implements pending tasks from `brainstorm_outputs/todo_list.txt`, marks each one done after completion, and supports task selection by number (e.g. `1,4,6`).
- **Force quit** — 3× Ctrl+C within 2 seconds triggers immediate `os._exit(1)`, unblocking any frozen I/O.
- **Proactive background monitoring** — `/proactive 5m` activates a sentinel daemon that wakes the agent automatically after a period of inactivity, enabling continuous monitoring loops, scheduled checks, or trading bots without user prompts.
- **Rich Live streaming rendering** — When `rich` is installed, responses stream as live-updating Markdown in place (no duplicate raw text), with clean tool-call interleaving.
- **Native Ollama reasoning** — Local reasoning models (deepseek-r1, qwen3, gemma4) stream their `<think>` tokens directly to the terminal via `ThinkingChunk` events; enable with `/verbose` and `/thinking`.
- **Native Ollama vision** — `/image [prompt]` captures the clipboard and sends it to local vision models (llava, gemma4, llama3.2-vision) via Ollama's native image API. No cloud required.
- **Reliable multi-line paste** — Bracketed Paste Mode (`ESC[?2004h`) collects any pasted text — code blocks, multi-paragraph prompts, long diffs — as a single turn with zero latency and no blank-line artifacts.
- **Rich Tab completion** — Tab after `/` shows all commands with one-line descriptions and subcommand hints; subcommand Tab-complete works for `/mcp`, `/plugin`, `/tasks`, `/cloudsave`, and more.
- **Checkpoint & rewind** — `/checkpoint` lists all auto-snapshots of conversation + file state; `/checkpoint <id>` rewinds both files and history to any earlier point in the session.
- **Plan mode** — `/plan <desc>` (or the `EnterPlanMode` tool) puts Claude into a structured read-only analysis phase; only the plan file is writable. Claude writes a detailed plan, then `/plan done` restores full write permissions for implementation.

---

## CheetahClaws vs OpenClaw

[OpenClaw](https://github.com/openclaw/openclaw) is another popular open-source AI assistant built on TypeScript/Node.js. The two projects have **different primary goals** — here is how they compare.

### At a glance

| Dimension | OpenClaw (TypeScript) | CheetahClaws (Python) |
|-----------|----------------------|---------------------|
| Language | TypeScript + Node.js | Python 3.8+ |
| Source files | ~10,349 TS/JS files | ~85 Python files |
| Lines of code | ~245K | ~12K |
| Primary focus | Personal life assistant across messaging channels | AI **coding** assistant / developer tool |
| Architecture | Always-on Gateway daemon + companion apps | Zero-install terminal REPL |
| Messaging channels | 20+ (WhatsApp · Telegram · Slack · Discord · Signal · iMessage · Matrix · WeChat · …) | Terminal + Telegram bridge + WeChat bridge (iLink) + Slack bridge (Web API) |
| Model providers | Multiple (cloud-first) | 7+ including full local support (Ollama · vLLM · LM Studio · …) |
| Local / offline models | Limited | Full — Ollama, vLLM, any OpenAI-compatible endpoint |
| Voice | Wake word · PTT · Talk Mode (macOS/iOS/Android) | Offline Whisper STT (local, no API key) |
| Code editing tools | Browser control, Canvas workspace | Read · Write · Edit · Bash · Glob · Grep · NotebookEdit · GetDiagnostics |
| Build step required | Yes (`pnpm install` + daemon setup) | No — `pip install` and run |
| Mobile companion | macOS menu bar + iOS/Android apps | — |
| Live Canvas / UI | Yes (A2UI agent-driven visual workspace) | — |
| MCP support | — | Yes (stdio/SSE/HTTP) |
| Runtime extensibility | Skills platform (bundled/managed/workspace) | `register_tool()` at runtime, MCP, git plugins, Markdown skills |
| Hackability | Large codebase (245K lines), harder to modify | ~12K lines — full agent loop visible in one file |

### Where OpenClaw wins

- **Omni-channel inbox** — connects to 20+ messaging platforms (WhatsApp, Signal, iMessage, Discord, Teams, Matrix, WeChat…); users interact from wherever they already are.
- **Always-on daemon** — Gateway runs as a background service (launchd/systemd); no terminal required for day-to-day use.
- **Mobile-first** — macOS menu bar, iOS Voice Wake / Talk Mode, Android camera/screen recording — feels like a native app, not a CLI tool.
- **Live Canvas** — agent-driven visual workspace rendered in the browser; supports A2UI push/eval/snapshot.
- **Browser automation** — dedicated Chrome/Chromium profile with snapshot, actions, and upload tools.
- **Production reliability** — versioned npm releases, comprehensive CI, onboarding wizard, `openclaw doctor` diagnostics.

### Where CheetahClaws wins

- **Coding toolset** — Read/Write/Edit/Bash/Glob/Grep/NotebookEdit/GetDiagnostics are purpose-built for software development; CheetahClaws understands diffs, file trees, and code structure.
- **True local model support** — full Ollama/vLLM/LM Studio integration with streaming, tool-calling, and vision — no cloud required.
- **8+ model providers** — switch between Claude, GPT-4o, Gemini, DeepSeek, Qwen, MiniMax, and local models with a single `--model` flag.
- **Hackable in minutes** — 12K lines of readable Python; the entire agent loop is in `agent.py`; extend with `register_tool()` at runtime without rebuilding.
- **Zero setup** — `pip install cheetahclaws` and run `cheetahclaws`; no daemon, no pairing, no onboarding wizard.
- **MCP support** — connect any MCP server (stdio/SSE/HTTP); tools auto-registered.
- **SSJ Developer Mode** — `/ssj` power menu chains Brainstorm → TODO → Worker → Debate in a persistent interactive session; automates entire dev workflows.
- **Offline voice** — `/voice` transcribes locally with `faster-whisper`; no subscription, no OAuth, works without internet.
- **Session cloud sync** — `/cloudsave` backs up full conversations to private GitHub Gists with zero extra dependencies.

### When to choose which

| If you want… | Use |
|---|---|
| A personal assistant you can message on WhatsApp/Signal/Discord | **OpenClaw** |
| An AI coding assistant in your terminal | **CheetahClaws** |
| Full offline / local model support | **CheetahClaws** |
| A mobile-friendly always-on experience | **OpenClaw** |
| To read and modify the source in an afternoon | **CheetahClaws** |
| Browser automation and a visual Canvas | **OpenClaw** |
| Multi-provider LLM switching without rebuilding | **CheetahClaws** |

---

### Key design differences

**Agent loop** — CheetahClaws uses a Python generator that `yield`s typed events (`TextChunk`, `ToolStart`, `ToolEnd`, `TurnDone`). The entire loop is visible in one file, making it easy to add hooks, custom renderers, or logging.

**Tool registration** — every tool is a `ToolDef(name, schema, func, read_only, concurrent_safe)` dataclass. Any module can call `register_tool()` at import time; MCP servers, plugins, and skills all use the same mechanism.

**Context compression**

| | Claude Code | CheetahClaws |
|-|-------------|-----------------|
| Trigger | Exact token count | `len / 3.5` estimate, fires at 70 % |
| Layer 1 | — | Snip: truncate old tool outputs (no API cost) |
| Layer 2 | AI summarization | AI summarization of older turns |
| Control | System-managed | `preserve_last_n_turns` parameter |

**Memory** — Claude Code's `extractMemories` service has the model proactively surface facts. CheetahClaws's `memory/` package is tool-driven: the model calls `MemorySave` explicitly, which is more predictable and auditable. Each memory now carries `confidence`, `source`, `last_used_at`, and `conflict_group` metadata; search re-ranks by confidence × recency; and `/memory consolidate` offers a manual consolidation pass without silently modifying memories in the background.

### Who should use CheetahClaws

- Developers who want to **use a local or non-Anthropic model** as their coding assistant.
- Researchers studying **how agentic coding assistants work** — the entire system fits in one screen.
- Teams who need a **hackable baseline** to add proprietary tools, custom permission policies, or specialised agent types.
- Anyone who wants Claude Code-style productivity **without a Node.js build chain**.

---

## Features

| Feature | Details |
|---|---|
| Multi-provider | Anthropic · OpenAI · Gemini · Kimi · Qwen · Zhipu · DeepSeek · MiniMax · Ollama · LM Studio · Custom endpoint |
| Interactive REPL | readline history, Tab-complete slash commands with descriptions + subcommand hints; Bracketed Paste Mode for reliable multi-line paste |
| Agent loop | Streaming API + automatic tool-use loop |
| 27 built-in tools | Read · Write · Edit · Bash · Glob · Grep · WebFetch · WebSearch · **NotebookEdit** · **GetDiagnostics** · MemorySave · MemoryDelete · MemorySearch · MemoryList · Agent · SendMessage · CheckAgentResult · ListAgentTasks · ListAgentTypes · Skill · SkillList · AskUserQuestion · TaskCreate/Update/Get/List · **SleepTimer** · **EnterPlanMode** · **ExitPlanMode** · *(MCP + plugin tools auto-added at startup)* |
| MCP integration | Connect any MCP server (stdio/SSE/HTTP), tools auto-registered and callable by Claude |
| Plugin system | Install/uninstall/enable/disable/update plugins from git URLs or local paths; multi-scope (user/project); recommendation engine |
| AskUserQuestion | Claude can pause and ask the user a clarifying question mid-task, with optional numbered choices |
| Task management | TaskCreate/Update/Get/List tools; sequential IDs; dependency edges; metadata; persisted to `.cheetahclaws/tasks.json`; `/tasks` REPL command |
| Diff view | Git-style red/green diff display for Edit and Write |
| Context compression | Auto-compact long conversations to stay within model limits |
| Persistent memory | Dual-scope memory (user + project) with 4 types, confidence/source metadata, conflict detection, recency-weighted search, `last_used_at` tracking, and `/memory consolidate` for auto-extraction |
| Multi-agent | Spawn typed sub-agents (coder/reviewer/researcher/…), git worktree isolation, background mode |
| Skills | Built-in `/commit` · `/review` + custom markdown skills with argument substitution and fork/inline execution |
| Plugin tools | Register custom tools via `tool_registry.py` |
| Permission system | `auto` / `accept-all` / `manual` / `plan` modes |
| Checkpoints | Auto-snapshot conversation + file state after each turn; `/checkpoint` to list, `/checkpoint <id>` to rewind; `/rewind` alias; 100-snapshot sliding window |
| Plan mode | `/plan <desc>` enters read-only analysis mode; Claude writes only to the plan file; `EnterPlanMode` / `ExitPlanMode` agent tools for autonomous planning |
| 36 slash commands | `/model` · `/config` · `/save` · `/cost` · `/memory` · `/skills` · `/agents` · `/voice` · `/proactive` · `/checkpoint` · `/plan` · `/compact` · `/status` · `/doctor` · … |
| Voice input | Record → transcribe → auto-submit. Backends: `sounddevice` / `arecord` / SoX + `faster-whisper` / `openai-whisper` / OpenAI API. Works fully offline. |
| Brainstorm | `/brainstorm [topic]` generates N expert personas suited to the topic (2–100, default 5, chosen interactively), runs an iterative debate, saves results to `brainstorm_outputs/`, and synthesizes a Master Plan + auto-generates `brainstorm_outputs/todo_list.txt`. |
| SSJ Developer Mode | `/ssj` opens a persistent interactive power menu with **14 shortcuts**: Brainstorm, TODO viewer, Worker, Expert Debate, Propose, Review, Readme, Commit, Scan, Promote, Video factory, TTS factory, Monitor, Agent. Stays open between actions; `/command` passthrough supported. |
| Monitor | `/monitor` (no args → wizard) subscribes to AI-monitored topics on a schedule and pushes reports to Telegram/Slack/console. Topics: `ai_research` (arxiv), `stock_<TICKER>`, `crypto_<SYMBOL>`, `world_news` (Reuters/BBC/AP), `custom:<query>`. Schedules: 15m to weekly. Background scheduler daemon with `/monitor start/stop/status`. |
| Autonomous Agents | `/agent` (no args → wizard) launches autonomous background agent loops driven by Markdown task templates. 4 built-in templates: `research_assistant`, `auto_bug_fixer`, `paper_writer`, `auto_coder`. Iteration summaries pushed via bridge. Custom templates: drop a `.md` file into `~/.cheetahclaws/agent_templates/`. |
| Remote Control job queue | All three bridges (Telegram/Slack/WeChat) maintain a per-bridge FIFO job queue when the AI is busy. `!jobs` / `!j` — dashboard; `!job <id>` — detail; `!retry <id>` — re-run a failed job; `!cancel [id]` — stop current job. Tool step tracking with `on_tool_start`/`on_tool_end` hooks. Persistent log at `~/.cheetahclaws/jobs.json`. |
| Worker | `/worker [task#s]` reads `brainstorm_outputs/todo_list.txt`, implements each pending task with a dedicated model prompt, and marks it done (`- [x]`). Supports task selection (`/worker 1,4,6`), custom path (`--path`), and worker count limit (`--workers`). Detects and redirects accidental brainstorm `.md` paths. |
| Telegram bridge | `/telegram <token> <chat_id>` starts a bot bridge: receive messages from Telegram, run the model, and reply — all from your phone. Typing indicator, slash command passthrough (including interactive menus), and auto-start on launch if configured. |
| WeChat bridge | `/wechat login` authenticates via QR code scan (same as WeixinClawBot / openclaw-weixin plugin), then starts the iLink long-poll bridge. `context_token` echoed per peer, typing indicator, slash command passthrough, session expiry auto-recovery. Credentials saved for auto-start on next launch. |
| Slack bridge | `/slack <xoxb-token> <channel_id>` connects to a Slack channel via the Web API (no external packages). Polls `conversations.history` every 2 s; replies update an in-place "Thinking…" placeholder. Slash command passthrough, interactive menu routing, auth validation on start, auto-start on next launch. |
| Video factory | `/video [topic]` runs the full AI video pipeline: story generation (active model) → TTS narration (Edge/Gemini/ElevenLabs) → AI images (Gemini Web free or placeholders) → subtitle burn (Whisper) → FFmpeg assembly → final `.mp4`. 10 viral content niches, landscape or short format, zero-cost path available. |
| TTS factory | `/tts` interactive wizard: AI writes script (or paste your own) → synthesize to MP3 in any voice style (narrator, newsreader, storyteller, ASMR, motivational, documentary, children, podcast, meditation, custom). Engine auto-selects: Gemini TTS → ElevenLabs → Edge TTS (always-free). CJK text auto-switches to a matching voice. |
| Vision input | `/image` (or `/img`) captures the clipboard image and sends it to any vision-capable model — Ollama (`llava`, `gemma4`, `llama3.2-vision`) via native format, or cloud models (GPT-4o, Gemini 2.0 Flash, …) via OpenAI `image_url` multipart format. Requires `pip install cheetahclaws[vision]`; Linux also needs `xclip`. |
| Tmux integration | 11 tmux tools for direct terminal control: create sessions/windows/panes, send commands, capture output. Auto-detected; zero impact if tmux is absent. Enables long-running tasks that outlive Bash tool timeouts. Cross-platform (tmux on Unix, psmux on Windows). |
| Shell escape | Type `!command` in the REPL to execute any shell command directly without AI involvement (`!git status`, `!ls`, `!python --version`). Output prints inline. |
| Proactive monitoring | `/proactive [duration]` starts a background sentinel daemon; agent wakes automatically after inactivity, enabling continuous monitoring loops without user prompts |
| Force quit | 3× Ctrl+C within 2 seconds triggers `os._exit(1)` — kills the process immediately regardless of blocking I/O |
| Rich Live streaming | When `rich` is installed, responses render as live-updating Markdown in place. Auto-disabled in SSH sessions to prevent repeated output; override with `/config rich_live=false`. |
| Context injection | Auto-loads `CLAUDE.md`, git status, cwd, persistent memory |
| Session persistence | Autosave on exit to `daily/YYYY-MM-DD/` (per-day limit) + `history.json` (master, all sessions) + `session_latest.json` (/resume); sessions include `session_id` and `saved_at` metadata; `/load` grouped by date |
| Cloud sync | `/cloudsave` syncs sessions to private GitHub Gists; auto-sync on exit; load from cloud by Gist ID. No new dependencies (stdlib `urllib`). |
| Extended Thinking | Toggle on/off for Claude models; native `<think>` block streaming for local Ollama reasoning models (deepseek-r1, qwen3, gemma4) |
| Cost tracking | Token usage + estimated USD cost |
| Non-interactive mode | `--print` flag for scripting / CI |

---

## Supported Models

### Closed-Source (API)

| Provider | Model | Context | Strengths | API Key Env |
|---|---|---|---|---|
| **Anthropic** | `claude-opus-4-6` | 200k | Most capable, best for complex reasoning | `ANTHROPIC_API_KEY` |
| **Anthropic** | `claude-sonnet-4-6` | 200k | Balanced speed & quality | `ANTHROPIC_API_KEY` |
| **Anthropic** | `claude-haiku-4-5-20251001` | 200k | Fast, cost-efficient | `ANTHROPIC_API_KEY` |
| **OpenAI** | `gpt-4o` | 128k | Strong multimodal & coding | `OPENAI_API_KEY` |
| **OpenAI** | `gpt-4o-mini` | 128k | Fast, cheap | `OPENAI_API_KEY` |
| **OpenAI** | `gpt-4.1` | 128k | Latest GPT-4 generation | `OPENAI_API_KEY` |
| **OpenAI** | `gpt-4.1-mini` | 128k | Fast GPT-4.1 | `OPENAI_API_KEY` |
| **OpenAI** | `gpt-5` | 128k | Next-gen flagship | `OPENAI_API_KEY` |
| **OpenAI** | `gpt-5-nano` | 128k | Fastest GPT-5 variant | `OPENAI_API_KEY` |
| **OpenAI** | `gpt-5-mini` | 128k | Balanced GPT-5 variant | `OPENAI_API_KEY` |
| **OpenAI** | `o4-mini` | 200k | Fast reasoning | `OPENAI_API_KEY` |
| **OpenAI** | `o3` | 200k | Strong reasoning | `OPENAI_API_KEY` |
| **OpenAI** | `o3-mini` | 200k | Compact reasoning | `OPENAI_API_KEY` |
| **OpenAI** | `o1` | 200k | Advanced reasoning | `OPENAI_API_KEY` |
| **Google** | `gemini-2.5-pro-preview-03-25` | 1M | Long context, multimodal | `GEMINI_API_KEY` |
| **Google** | `gemini-2.0-flash` | 1M | Fast, large context | `GEMINI_API_KEY` |
| **Google** | `gemini-1.5-pro` | 2M | Largest context window | `GEMINI_API_KEY` |
| **Moonshot (Kimi)** | `moonshot-v1-8k` | 8k | Chinese & English | `MOONSHOT_API_KEY` |
| **Moonshot (Kimi)** | `moonshot-v1-32k` | 32k | Chinese & English | `MOONSHOT_API_KEY` |
| **Moonshot (Kimi)** | `moonshot-v1-128k` | 128k | Long context | `MOONSHOT_API_KEY` |
| **Alibaba (Qwen)** | `qwen-max` | 32k | Best Qwen quality | `DASHSCOPE_API_KEY` |
| **Alibaba (Qwen)** | `qwen-plus` | 128k | Balanced | `DASHSCOPE_API_KEY` |
| **Alibaba (Qwen)** | `qwen-turbo` | 1M | Fast, cheap | `DASHSCOPE_API_KEY` |
| **Alibaba (Qwen)** | `qwq-32b` | 32k | Strong reasoning | `DASHSCOPE_API_KEY` |
| **Zhipu (GLM)** | `glm-4-plus` | 128k | Best GLM quality | `ZHIPU_API_KEY` |
| **Zhipu (GLM)** | `glm-4` | 128k | General purpose | `ZHIPU_API_KEY` |
| **Zhipu (GLM)** | `glm-4-flash` | 128k | Free tier available | `ZHIPU_API_KEY` |
| **DeepSeek** | `deepseek-chat` | 64k | Strong coding | `DEEPSEEK_API_KEY` |
| **DeepSeek** | `deepseek-reasoner` | 64k | Chain-of-thought reasoning | `DEEPSEEK_API_KEY` |
| **MiniMax** | `MiniMax-Text-01` | 1M | Long context, strong reasoning | `MINIMAX_API_KEY` |
| **MiniMax** | `MiniMax-VL-01` | 1M | Vision + language | `MINIMAX_API_KEY` |
| **MiniMax** | `abab6.5s-chat` | 256k | Fast, cost-efficient | `MINIMAX_API_KEY` |
| **MiniMax** | `abab6.5-chat` | 256k | Balanced quality | `MINIMAX_API_KEY` |

### Open-Source (Local via Ollama)

| Model | Size | Strengths | Pull Command |
|---|---|---|---|
| `llama3.3` | 70B | General purpose, strong reasoning | `ollama pull llama3.3` |
| `llama3.2` | 3B / 11B | Lightweight | `ollama pull llama3.2` |
| `qwen2.5-coder` | 7B / 32B | **Best for coding tasks** | `ollama pull qwen2.5-coder` |
| `qwen2.5` | 7B / 72B | Chinese & English | `ollama pull qwen2.5` |
| `deepseek-r1` | 7B–70B | Reasoning, math | `ollama pull deepseek-r1` |
| `deepseek-coder-v2` | 16B | Coding | `ollama pull deepseek-coder-v2` |
| `mistral` | 7B | Fast, efficient | `ollama pull mistral` |
| `mixtral` | 8x7B | Strong MoE model | `ollama pull mixtral` |
| `phi4` | 14B | Microsoft, strong reasoning | `ollama pull phi4` |
| `gemma3` | 4B / 12B / 27B | Google open model | `ollama pull gemma3` |
| `codellama` | 7B / 34B | Code generation | `ollama pull codellama` |
| `llava` | 7B / 13B | **Vision** — image understanding | `ollama pull llava` |
| `llama3.2-vision` | 11B | **Vision** — multimodal reasoning | `ollama pull llama3.2-vision` |

> **Note:** Tool calling requires a model that supports function calling. Recommended local models: `qwen2.5-coder`, `llama3.3`, `mistral`, `phi4`.

> **OpenAI newer models (gpt-5 / o3 / o4 family):** These models require `max_completion_tokens` instead of the legacy `max_tokens` parameter. CheetahClaws handles this automatically — no configuration needed.

> **Reasoning models:** `deepseek-r1`, `qwen3`, and `gemma4` stream native `<think>` blocks. Enable with `/verbose` and `/thinking` to see thoughts in the terminal. Note: models fed a large system prompt (like cheetahclaws's 25 tool schemas) may suppress their thinking phase to avoid breaking the expected JSON format — this is model behavior, not a bug.

---

## Installation

### Recommended: install as a global command with `uv`

[uv](https://docs.astral.sh/uv/) installs `cheetahclaws` into an isolated environment and puts it on your PATH so you can run it from anywhere:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone git@github.com:SafeRL-Lab/cheetahclaws.git
cd cheetahclaws
uv tool install .
```

After that, `cheetahclaws` is available as a global command:

```bash
cheetahclaws                        # start REPL
cheetahclaws --model gpt-4o         # choose a model
cheetahclaws -p "explain this"      # non-interactive
```

To update after pulling new code:

```bash
uv tool install . --reinstall
```

To uninstall:

```bash
uv tool uninstall cheetahclaws
```

### Alternative: run directly from the repo

```bash
git clone git@github.com:SafeRL-Lab/cheetahclaws.git
cd cheetahclaws

pip install -r requirements.txt
# or manually (sounddevice is optional — only needed for /voice):
pip install anthropic openai httpx rich
pip install sounddevice  # optional: voice input

python cheetahclaws.py
```

---

## Usage: Closed-Source API Models

### Anthropic Claude

Get your API key at [console.anthropic.com](https://console.anthropic.com).

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Default model (claude-opus-4-6)
cheetahclaws

# Choose a specific model
cheetahclaws --model claude-sonnet-4-6
cheetahclaws --model claude-haiku-4-5-20251001

# Enable Extended Thinking
cheetahclaws --model claude-opus-4-6 --thinking --verbose
```

### OpenAI GPT

Get your API key at [platform.openai.com](https://platform.openai.com).

```bash
export OPENAI_API_KEY=sk-...

cheetahclaws --model gpt-4o
cheetahclaws --model gpt-4o-mini
cheetahclaws --model gpt-4.1-mini
cheetahclaws --model o3-mini
```

### Google Gemini

Get your API key at [aistudio.google.com](https://aistudio.google.com).

```bash
export GEMINI_API_KEY=AIza...

cheetahclaws --model gemini/gemini-2.0-flash
cheetahclaws --model gemini/gemini-1.5-pro
cheetahclaws --model gemini/gemini-2.5-pro-preview-03-25
```

### Kimi (Moonshot AI)

Get your API key at [platform.moonshot.cn](https://platform.moonshot.cn).

```bash
export MOONSHOT_API_KEY=sk-...

cheetahclaws --model kimi/moonshot-v1-32k
cheetahclaws --model kimi/moonshot-v1-128k
```

### Qwen (Alibaba DashScope)

Get your API key at [dashscope.aliyun.com](https://dashscope.aliyun.com).

```bash
export DASHSCOPE_API_KEY=sk-...

cheetahclaws --model qwen/Qwen3.5-Plus
cheetahclaws --model qwen/Qwen3-MAX
cheetahclaws --model qwen/Qwen3.5-Flash
```

### Zhipu GLM

Get your API key at [open.bigmodel.cn](https://open.bigmodel.cn).

```bash
export ZHIPU_API_KEY=...

cheetahclaws --model zhipu/glm-4-plus
cheetahclaws --model zhipu/glm-4-flash   # free tier
```

### DeepSeek

Get your API key at [platform.deepseek.com](https://platform.deepseek.com).

```bash
export DEEPSEEK_API_KEY=sk-...

cheetahclaws --model deepseek/deepseek-chat
cheetahclaws --model deepseek/deepseek-reasoner
```

### MiniMax

Get your API key at [platform.minimaxi.chat](https://platform.minimaxi.chat).

```bash
export MINIMAX_API_KEY=...

cheetahclaws --model minimax/MiniMax-Text-01
cheetahclaws --model minimax/MiniMax-VL-01
cheetahclaws --model minimax/abab6.5s-chat
```

---

## Usage: Open-Source Models (Local)

### Option A — Ollama (Recommended)

Ollama runs models locally with zero configuration. No API key required.

**Step 1: Install Ollama**

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com/download
```

**Step 2: Pull a model**

```bash
# Best for coding (recommended)
ollama pull qwen2.5-coder          # 4.7 GB (7B)
ollama pull qwen2.5-coder:32b      # 19 GB (32B)

# General purpose
ollama pull llama3.3               # 42 GB (70B)
ollama pull llama3.2               # 2.0 GB (3B)

# Reasoning
ollama pull deepseek-r1            # 4.7 GB (7B)
ollama pull deepseek-r1:32b        # 19 GB (32B)

# Other
ollama pull phi4                   # 9.1 GB (14B)
ollama pull mistral                # 4.1 GB (7B)
```

**Step 3: Start Ollama server** (runs automatically on macOS; on Linux run manually)

```bash
ollama serve     # starts on http://localhost:11434
```

**Step 4: Run cheetahclaws**

```bash
cheetahclaws --model ollama/qwen2.5-coder
cheetahclaws --model ollama/llama3.3
cheetahclaws --model ollama/deepseek-r1
```

Or

```bash
python cheetahclaws.py --model ollama/qwen2.5-coder
python cheetahclaws.py --model ollama/llama3.3
python cheetahclaws.py --model ollama/deepseek-r1
python cheetahclaws.py --model ollama/qwen3.5:35b
```

**List your locally available models:**

```bash
ollama list
```

Then use any model from the list:

```bash
cheetahclaws --model ollama/<model-name>
```

---

### Option B — LM Studio

LM Studio provides a GUI to download and run models, with a built-in OpenAI-compatible server.

**Step 1:** Download [LM Studio](https://lmstudio.ai) and install it.

**Step 2:** Search and download a model inside LM Studio (GGUF format).

**Step 3:** Go to **Local Server** tab → click **Start Server** (default port: 1234).

**Step 4:**

```bash
cheetahclaws --model lmstudio/<model-name>
# e.g.:
cheetahclaws --model lmstudio/phi-4-GGUF
cheetahclaws --model lmstudio/qwen2.5-coder-7b
```

The model name should match what LM Studio shows in the server status bar.

---

### Option C — vLLM / Self-Hosted OpenAI-Compatible Server

For self-hosted inference servers (vLLM, TGI, llama.cpp server, etc.) that expose an OpenAI-compatible API:

Quick Start for option C:
Step 1: Start vllm:
 ```
CUDA_VISIBLE_DEVICES=7 python -m vllm.entrypoints.openai.api_server \
      --model Qwen/Qwen2.5-Coder-7B-Instruct \
      --host 0.0.0.0 \
      --port 8000 \
      --enable-auto-tool-choice \
      --tool-call-parser hermes
```


 Step 2: Start cheetahclaws：
```
  export CUSTOM_BASE_URL=http://localhost:8000/v1
  export CUSTOM_API_KEY=none
  cheetahclaws --model custom/Qwen/Qwen2.5-Coder-7B-Instruct
```


```bash
# Example: vLLM serving Qwen2.5-Coder-32B
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-Coder-32B-Instruct \
    --port 8000 \
    --enable-auto-tool-choice \
    --tool-call-parser hermes

# Then run cheetahclaws pointing to your server:
cheetahclaws
```

Inside the REPL:

```
/config custom_base_url=http://localhost:8000/v1
/config custom_api_key=token-abc123    # skip if no auth
/model custom/Qwen2.5-Coder-32B-Instruct
```

Or set via environment:

```bash
export CUSTOM_BASE_URL=http://localhost:8000/v1
export CUSTOM_API_KEY=token-abc123

cheetahclaws --model custom/Qwen2.5-Coder-32B-Instruct
```

For a remote GPU server:

```bash
/config custom_base_url=http://192.168.1.100:8000/v1
/model custom/your-model-name
```

---

## Model Name Format

Three equivalent formats are supported:

```bash
# 1. Auto-detect by prefix (works for well-known models)
cheetahclaws --model gpt-4o
cheetahclaws --model gemini-2.0-flash
cheetahclaws --model deepseek-chat

# 2. Explicit provider prefix with slash
cheetahclaws --model ollama/qwen2.5-coder
cheetahclaws --model kimi/moonshot-v1-128k

# 3. Explicit provider prefix with colon (also works)
cheetahclaws --model kimi:moonshot-v1-32k
cheetahclaws --model qwen:qwen-max
```

**Auto-detection rules:**

| Model prefix | Detected provider |
|---|---|
| `claude-` | anthropic |
| `gpt-`, `o1`, `o3` | openai |
| `gemini-` | gemini |
| `moonshot-`, `kimi-` | kimi |
| `qwen`, `qwq-` | qwen |
| `glm-` | zhipu |
| `deepseek-` | deepseek |
| `MiniMax-`, `minimax-`, `abab` | minimax |
| `llama`, `mistral`, `phi`, `gemma`, `mixtral`, `codellama` | ollama |

---

## CLI Reference

```
cheetahclaws [OPTIONS] [PROMPT]
# or: python cheetahclaws.py [OPTIONS] [PROMPT]

Options:
  -p, --print          Non-interactive: run prompt and exit
  -m, --model MODEL    Override model (e.g. gpt-4o, ollama/llama3.3)
  --accept-all         Auto-approve all operations (no permission prompts)
  --verbose            Show thinking blocks and per-turn token counts
  --thinking           Enable Extended Thinking (Claude only)
  --version            Print version and exit
  -h, --help           Show help
```

**Examples:**

```bash
# Interactive REPL with default model
cheetahclaws

# Switch model at startup
cheetahclaws --model gpt-4o
cheetahclaws -m ollama/deepseek-r1:32b

# Non-interactive / scripting
cheetahclaws --print "Write a Python fibonacci function"
cheetahclaws -p "Explain the Rust borrow checker in 3 sentences" -m gemini/gemini-2.0-flash

# CI / automation (no permission prompts)
cheetahclaws --accept-all --print "Initialize a Python project with pyproject.toml"

# Debug mode (see tokens + thinking)
cheetahclaws --thinking --verbose
```

---

## Slash Commands (REPL)

Type `/` and press **Tab** to see all commands with descriptions. Continue typing to filter, then Tab again to auto-complete. After a command name, press **Tab** again to see its subcommands (e.g. `/plugin ` → `install`, `uninstall`, `enable`, …).

| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/clear` | Clear conversation history |
| `/model` | Show current model + list all available models |
| `/model <name>` | Switch model (takes effect immediately) |
| `/config` | Show all current config values |
| `/config key=value` | Set a config value (persisted to disk) |
| `/save` | Save session (auto-named by timestamp) |
| `/save <filename>` | Save session to named file |
| `/load` | Interactive list grouped by date; enter number, `1,2,3` to merge, or `H` for full history |
| `/load <filename>` | Load a saved session by filename |
| `/resume` | Restore the last auto-saved session (`mr_sessions/session_latest.json`) |
| `/resume <filename>` | Load a specific file from `mr_sessions/` (or absolute path) |
| `/history` | Print full conversation history |
| `/context` | Show message count and token estimate |
| `/cost` | Show token usage and estimated USD cost |
| `/verbose` | Toggle verbose mode (tokens + thinking) |
| `/thinking` | Toggle Extended Thinking (Claude only) |
| `/permissions` | Show current permission mode |
| `/permissions <mode>` | Set permission mode: `auto` / `accept-all` / `manual` |
| `/cwd` | Show current working directory |
| `/cwd <path>` | Change working directory |
| `/memory` | List all persistent memories |
| `/memory <query>` | Search memories by keyword (ranked by confidence × recency) |
| `/memory consolidate` | AI-extract up to 3 long-term insights from the current session |
| `/skills` | List available skills |
| `/agents` | Show sub-agent task status |
| `/mcp` | List configured MCP servers and their tools |
| `/mcp reload` | Reconnect all MCP servers and refresh tools |
| `/mcp reload <name>` | Reconnect a single MCP server |
| `/mcp add <name> <cmd> [args]` | Add a stdio MCP server to user config |
| `/mcp remove <name>` | Remove a server from user config |
| `/voice` | Record voice, transcribe with Whisper, auto-submit as prompt |
| `/voice status` | Show recording and STT backend availability |
| `/voice lang <code>` | Set STT language (e.g. `zh`, `en`, `ja`; `auto` to detect) |
| `/voice device` | List available input microphones and select one interactively |
| `/image [prompt]` | Capture clipboard image and send to vision model with optional prompt |
| `/img [prompt]` | Alias for `/image` |
| `/proactive` | Show current proactive polling status (ON/OFF and interval) |
| `/proactive <duration>` | Enable background sentinel polling (e.g. `5m`, `30s`, `1h`) |
| `/proactive off` | Disable background polling |
| `/cloudsave setup <token>` | Configure GitHub Personal Access Token for Gist sync |
| `/cloudsave` | Upload current session to a private GitHub Gist |
| `/cloudsave push [desc]` | Upload with an optional description |
| `/cloudsave auto on\|off` | Toggle auto-upload on `/exit` |
| `/cloudsave list` | List your cheetahclaws Gists |
| `/cloudsave load <gist_id>` | Download and restore a session from Gist |
| `/brainstorm` | Run a multi-persona AI brainstorm; prompts for agent count (2–100, default 5) |
| `/brainstorm <topic>` | Focus the brainstorm on a specific topic; prompts for agent count |
| `/ssj` | Open SSJ Developer Mode — interactive power menu with 14 workflow shortcuts |
| `/monitor` | Interactive wizard: add subscriptions, run now, start/stop scheduler, configure notifications |
| `/monitor run [topic]` | Run all (or one) subscription(s) immediately and print the AI report |
| `/monitor start` | Start the background scheduler daemon |
| `/monitor stop` | Stop the background scheduler daemon |
| `/monitor status` | Show scheduler status, subscriptions, and configured delivery channels |
| `/monitor set telegram <token> <chat_id>` | Configure Telegram delivery for monitor reports |
| `/monitor set slack <token> <channel_id>` | Configure Slack delivery for monitor reports |
| `/monitor topics` | List all built-in topics |
| `/subscribe <topic> [schedule] [--telegram] [--slack]` | Subscribe to a monitoring topic (e.g. `ai_research`, `stock_TSLA`, `crypto_BTC`, `world_news`, `custom:quantum computing`) |
| `/subscriptions` | List active subscriptions with schedule and last-run time |
| `/subs` | Alias for `/subscriptions` |
| `/unsubscribe <topic>` | Remove a subscription |
| `/agent` | Interactive wizard: choose template, answer questions, start background agent loop |
| `/agent start <template> [args]` | Direct launch — e.g. `/agent start research_assistant ~/papers/` |
| `/agent stop <name\|all>` | Stop a running agent (or all agents) |
| `/agent list` | Show all currently running agents and their status |
| `/agent status <name>` | Show recent iteration log for a named agent |
| `/agent templates` | List available templates (built-in + user-defined) |
| `/worker` | Auto-implement all pending tasks from `brainstorm_outputs/todo_list.txt` |
| `/worker <n,m,…>` | Implement specific pending tasks by number (e.g. `/worker 1,4,6`) |
| `/worker --path <file>` | Use a custom todo file path instead of the default |
| `/worker --workers <n>` | Limit the batch to N tasks per run (e.g. `/worker --workers 3`) |
| `/telegram <token> <chat_id>` | Configure and start the Telegram bot bridge |
| `/telegram` | Start the bridge using previously saved token + chat_id |
| `/telegram stop` | Stop the Telegram bridge |
| `/telegram status` | Show whether the bridge is running and the configured chat_id |
| `/wechat login` | Scan QR code with WeChat to authenticate, then start the bridge |
| `/wechat` | Start with saved credentials; triggers QR login if none saved |
| `/wechat stop` | Stop the WeChat bridge |
| `/wechat status` | Show running state and account info |
| `/wechat logout` | Clear saved credentials and stop the bridge |
| `/slack <token> <channel_id>` | Configure and start the Slack bridge |
| `/slack` | Start with saved credentials |
| `/slack stop` | Stop the Slack bridge |
| `/slack status` | Show running state and channel |
| `/slack logout` | Clear saved credentials and stop the bridge |
| `/video [topic]` | AI video factory: story → voice → images → subtitles → `.mp4` |
| `/video status` | Show video pipeline dependency availability |
| `/video niches` | List all 10 viral content niches |
| `/video --niche <id> [topic]` | Use a specific content niche |
| `/video --short [topic]` | Generate vertical short format (9:16) |
| `/tts [topic]` | TTS Content Factory: AI script → any voice style → MP3 audio file |
| `/tts status` | Show TTS dependency availability (ffmpeg, edge-tts, API keys) |
| `/checkpoint` | List all checkpoints (snapshots) for the current session |
| `/checkpoint <id>` | Rewind to checkpoint — restore files and conversation to that snapshot |
| `/checkpoint clear` | Delete all checkpoints for the current session |
| `/rewind` | Alias for `/checkpoint` |
| `/plan <description>` | Enter plan mode: read-only analysis, writes only to the plan file |
| `/plan` | Show current plan file contents |
| `/plan done` | Exit plan mode and restore original permissions |
| `/plan status` | Show whether plan mode is active |
| `/compact` | Manually compact the conversation (same as auto-compact but user-triggered) |
| `/compact <focus>` | Compact with focus instructions (e.g. `/compact keep the auth refactor context`) |
| `/init` | Create a `CLAUDE.md` template in the current working directory |
| `/export` | Export the conversation as a Markdown file to `.nano_claude/exports/` |
| `/export <filename>` | Export as Markdown or JSON (detected by `.json` extension) |
| `/copy` | Copy the last assistant response to the clipboard |
| `/status` | Show version, model, provider, permissions, session ID, token usage, and context % |
| `/doctor` | Diagnose installation health: Python, git, API key, optional deps, CLAUDE.md, checkpoint disk usage |
| `/exit` / `/quit` | Exit |

**Switching models inside a session:**

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/multimodel_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Multi-Model Switching: Claude → GPT-4o → Ollama → back, full history preserved</center>
</div>

```
[myproject] ❯ /model
  Current model: claude-opus-4-6  (provider: anthropic)

  Available models by provider:
    anthropic     claude-opus-4-6, claude-sonnet-4-6, ...
    openai        gpt-4o, gpt-4o-mini, o3-mini, ...
    ollama        llama3.3, llama3.2, phi4, mistral, ...
    ...

[myproject] ❯ /model gpt-4o
  Model set to gpt-4o  (provider: openai)

[myproject] ❯ /model ollama/qwen2.5-coder
  Model set to ollama/qwen2.5-coder  (provider: ollama)
```

---

## Configuring API Keys

### Method 1: Environment Variables (recommended)

```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GEMINI_API_KEY=AIza...
export MOONSHOT_API_KEY=sk-...       # Kimi
export DASHSCOPE_API_KEY=sk-...      # Qwen
export ZHIPU_API_KEY=...             # Zhipu GLM
export DEEPSEEK_API_KEY=sk-...       # DeepSeek
export MINIMAX_API_KEY=...           # MiniMax
```

### Method 2: Set Inside the REPL (persisted)

```
/config anthropic_api_key=sk-ant-...
/config openai_api_key=sk-...
/config gemini_api_key=AIza...
/config kimi_api_key=sk-...
/config qwen_api_key=sk-...
/config zhipu_api_key=...
/config deepseek_api_key=sk-...
/config minimax_api_key=...
```

Keys are saved to `~/.cheetahclaws/config.json` and loaded automatically on next launch.

### Method 3: Edit the Config File Directly

```json
// ~/.cheetahclaws/config.json
{
  "model": "qwen/qwen-max",
  "max_tokens": 8192,
  "permission_mode": "auto",
  "verbose": false,
  "thinking": false,
  "qwen_api_key": "sk-...",
  "kimi_api_key": "sk-...",
  "deepseek_api_key": "sk-...",
  "minimax_api_key": "..."
}
```

---

## Permission System

| Mode | Behavior |
|---|---|
| `auto` (default) | Read-only operations always allowed. Prompts before Bash commands and file writes. |
| `accept-all` | Never prompts. All operations proceed automatically. |
| `manual` | Prompts before every single operation, including reads. |
| `plan` | Read-only analysis mode. Only the plan file (`.nano_claude/plans/`) is writable. Entered via `/plan <desc>` or the `EnterPlanMode` tool. |

**When prompted:**

```
  Allow: Run: git commit -am "fix bug"  [y/N/a(ccept-all)]
```

- `y` — approve this one action
- `n` or Enter — deny
- `a` — approve and switch to `accept-all` for the rest of the session

**Commands always auto-approved in `auto` mode:**
`ls`, `cat`, `head`, `tail`, `wc`, `pwd`, `echo`, `git status`, `git log`, `git diff`, `git show`, `find`, `grep`, `rg`, `python`, `node`, `pip show`, `npm list`, and other read-only shell commands.

---

## Built-in Tools

### Core Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `Read` | Read file with line numbers | `file_path`, `limit`, `offset` |
| `Write` | Create or overwrite file (shows diff) | `file_path`, `content` |
| `Edit` | Exact string replacement (shows diff) | `file_path`, `old_string`, `new_string`, `replace_all` |
| `Bash` | Execute shell command | `command`, `timeout` (default 30s) |
| `Glob` | Find files by glob pattern | `pattern` (e.g. `**/*.py`), `path` |
| `Grep` | Regex search in files (uses ripgrep if available) | `pattern`, `path`, `glob`, `output_mode` |
| `WebFetch` | Fetch and extract text from URL | `url`, `prompt` |
| `WebSearch` | Search the web via DuckDuckGo | `query` |

### Notebook & Diagnostics Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `NotebookEdit` | Edit a Jupyter notebook (`.ipynb`) cell | `notebook_path`, `new_source`, `cell_id`, `cell_type`, `edit_mode` (`replace`/`insert`/`delete`) |
| `GetDiagnostics` | Get LSP-style diagnostics for a source file (pyright/mypy/flake8 for Python; tsc/eslint for JS/TS; shellcheck for shell) | `file_path`, `language` (optional override) |

### Memory Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `MemorySave` | Save or update a persistent memory | `name`, `type`, `description`, `content`, `scope` |
| `MemoryDelete` | Delete a memory by name | `name`, `scope` |
| `MemorySearch` | Search memories by keyword (or AI ranking) | `query`, `scope`, `use_ai`, `max_results` |
| `MemoryList` | List all memories with age and metadata | `scope` |

### Sub-Agent Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `Agent` | Spawn a sub-agent for a task | `prompt`, `subagent_type`, `isolation`, `name`, `model`, `wait` |
| `SendMessage` | Send a message to a named background agent | `name`, `message` |
| `CheckAgentResult` | Check status/result of a background agent | `task_id` |
| `ListAgentTasks` | List all active and finished agent tasks | — |
| `ListAgentTypes` | List available agent type definitions | — |

### Background & Autonomy Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `SleepTimer` | Schedule a silent background timer; injects an automated wake-up prompt when it fires so the agent can resume monitoring or deferred tasks | `seconds` |

### Skill Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `Skill` | Invoke a skill by name from within the conversation | `name`, `args` |
| `SkillList` | List all available skills with triggers and metadata | — |

### MCP Tools

MCP tools are discovered automatically from configured servers and registered under the name `mcp__<server>__<tool>`. Claude can use them exactly like built-in tools.

| Example tool name | Where it comes from |
|---|---|
| `mcp__git__git_status` | `git` server, `git_status` tool |
| `mcp__filesystem__read_file` | `filesystem` server, `read_file` tool |
| `mcp__myserver__my_action` | custom server you configured |

> **Adding custom tools:** See [Architecture Guide](docs/architecture.md#tool-registry) for how to register your own tools.

---

## Memory

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/memory_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Memory: save preferences in session 1 → auto-recalled in session 2, no re-explanation needed</center>
</div>

The model can remember things across conversations using the built-in memory system.

### Storage

Memories are stored as individual markdown files in two scopes:

| Scope | Path | Visibility |
|---|---|---|
| **User** (default) | `~/.cheetahclaws/memory/` | Shared across all projects |
| **Project** | `.cheetahclaws/memory/` in cwd | Local to the current repo |

A `MEMORY.md` index (≤ 200 lines / 25 KB) is auto-rebuilt on every save or delete and injected into the system prompt so the model always has an overview of what's been remembered.

### Memory types

| Type | Use for |
|---|---|
| `user` | Your role, preferences, background |
| `feedback` | How you want the model to behave (corrections AND confirmations) |
| `project` | Ongoing work, deadlines, decisions not in git history |
| `reference` | Links to external systems (Linear, Grafana, Slack, etc.) |

### Memory file format

Each memory is a markdown file with YAML frontmatter:

```markdown
---
name: coding_style
description: Python formatting preferences
type: feedback
created: 2026-04-02
confidence: 0.95
source: user
last_used_at: 2026-04-05
conflict_group: coding_style
---
Prefer 4-space indentation and full type hints in all Python code.
**Why:** user explicitly stated this preference.
**How to apply:** apply to every Python file written or edited.
```

**Metadata fields** (new — auto-managed):

| Field | Default | Description |
|---|---|---|
| `confidence` | `1.0` | Reliability score 0–1. Explicit user statements = 1.0; inferred preferences ≈ 0.8; auto-consolidated ≈ 0.8 |
| `source` | `user` | Origin: `user` / `model` / `tool` / `consolidator` |
| `last_used_at` | — | Updated automatically each time this memory is returned by MemorySearch |
| `conflict_group` | — | Groups related memories (e.g. `writing_style`) for conflict tracking |

### Conflict detection

When `MemorySave` is called with a name that already exists but different content, the system reports the conflict before overwriting:

```
Memory saved: 'writing_style' [feedback/user]
⚠ Replaced conflicting memory (was user-sourced, 100% confidence, written 2026-04-01).
  Old content: Prefer formal, academic style...
```

### Ranked retrieval

`MemorySearch` ranks results by **confidence × recency** (30-day exponential decay) rather than plain keyword order. Memories that haven't been used recently fade in priority. Each search hit also updates `last_used_at` so frequently-accessed memories stay prominent.

```
You: /memory python
  [feedback/user] coding_style [conf:95% src:user]
    Python formatting preferences
    Prefer 4-space indentation and full type hints...
```

### `/memory consolidate` — auto-extract long-term insights

After a meaningful session, run:

```
[myproject] ❯ /memory consolidate
  Analyzing session for long-term memories…
  ✓ Consolidated 2 memory/memories: user_prefers_direct_answers, avoid_trailing_summaries
```

The command sends a condensed session transcript to the model and asks it to identify up to **3** insights worth keeping long-term (user preferences, feedback corrections, project decisions). Extracted memories are saved with `confidence: 0.80` and `source: consolidator` — they **never overwrite** an existing memory that already has higher confidence.

Good times to run `/memory consolidate`:
- After correcting the model's behavior several times in a row
- After a session where you shared project background or decisions
- After completing a task with clear planning choices

### Example interaction

```
You: Remember that I prefer 4-space indentation and type hints.
AI: [calls MemorySave] Memory saved: 'coding_style' [feedback/user]

You: /memory
  1 memory/memories:
  [feedback  |user   ] coding_style.md
    Python formatting preferences

You: /memory python
  Found 1 relevant memory for 'python':
  [feedback/user] coding_style
    Prefer 4-space indentation and full type hints in all Python code.

You: /memory consolidate
  ✓ Consolidated 1 memory: user_prefers_verbose_commit_messages
```

**Staleness warnings:** Memories older than 1 day show a `⚠ stale` caveat — claims about file:line citations or code state may be outdated; verify before acting.

**AI-ranked search:** `MemorySearch(query="...", use_ai=true)` uses the model to rank candidates by relevance before applying the confidence × recency re-ranking.

---

## Skills

Skills are reusable prompt templates that give the model specialized capabilities. Two built-in skills ship out of the box — no setup required.

**Built-in skills:**

| Trigger | Description |
|---|---|
| `/commit` | Review staged changes and create a well-structured git commit |
| `/review [PR]` | Review code or PR diff with structured feedback |

**Quick start — custom skill:**

```bash
mkdir -p ~/.cheetahclaws/skills
```

Create `~/.cheetahclaws/skills/deploy.md`:

```markdown
---
name: deploy
description: Deploy to an environment
triggers: [/deploy]
allowed-tools: [Bash, Read]
when_to_use: Use when the user wants to deploy a version to an environment.
argument-hint: [env] [version]
arguments: [env, version]
context: inline
---

Deploy $VERSION to the $ENV environment.
Full args: $ARGUMENTS
```

Now use it:

```
You: /deploy staging 2.1.0
AI: [deploys version 2.1.0 to staging]
```

**Argument substitution:**
- `$ARGUMENTS` — the full raw argument string
- `$ARG_NAME` — positional substitution by named argument (first word → first name)
- Missing args become empty strings

**Execution modes:**
- `context: inline` (default) — runs inside current conversation history
- `context: fork` — runs as an isolated sub-agent with fresh history; supports `model` override

**Priority** (highest wins): project-level > user-level > built-in

**List skills:** `/skills` — shows triggers, argument hint, source, and `when_to_use`

**Skill search paths:**

```
./.cheetahclaws/skills/     # project-level (overrides user-level)
~/.cheetahclaws/skills/     # user-level
```

---

## Sub-Agents

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/subagent_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Sub-Agents: spawn coder + security agents in parallel, merge results automatically</center>
</div>

The model can spawn independent sub-agents to handle tasks in parallel.

**Specialized agent types** — built-in:

| Type | Optimized for |
|---|---|
| `general-purpose` | Research, exploration, multi-step tasks |
| `coder` | Writing, reading, and modifying code |
| `reviewer` | Security, correctness, and code quality analysis |
| `researcher` | Web search and documentation lookup |
| `tester` | Writing and running tests |

**Basic usage:**
```
You: Search this codebase for all TODO comments and summarize them.
AI: [calls Agent(prompt="...", subagent_type="researcher")]
    Sub-agent reads files, greps for TODOs...
    Result: Found 12 TODOs across 5 files...
```

**Background mode** — spawn without waiting, collect result later:
```
AI: [calls Agent(prompt="run all tests", name="test-runner", wait=false)]
AI: [continues other work...]
AI: [calls CheckAgentResult / SendMessage to follow up]
```

**Git worktree isolation** — agents work on an isolated branch with no conflicts:
```
Agent(prompt="refactor auth module", isolation="worktree")
```
The worktree is auto-cleaned up if no changes were made; otherwise the branch name is reported.

**Custom agent types** — create `~/.cheetahclaws/agents/myagent.md`:
```markdown
---
name: myagent
description: Specialized for X
model: claude-haiku-4-5-20251001
tools: [Read, Grep, Bash]
---
Extra system prompt for this agent type.
```

**List running agents:** `/agents`

Sub-agents have independent conversation history, share the file system, and are limited to 3 levels of nesting.

---

## MCP (Model Context Protocol)

MCP lets you connect any external tool server — local subprocess or remote HTTP — and Claude can use its tools automatically. This is the same protocol Claude Code uses to extend its capabilities.

### Supported transports

| Transport | Config `type` | Description |
|---|---|---|
| **stdio** | `"stdio"` | Spawn a local subprocess (most common) |
| **SSE** | `"sse"` | HTTP Server-Sent Events stream |
| **HTTP** | `"http"` | Streamable HTTP POST (newer servers) |

### Configuration

Place a `.mcp.json` file in your project directory **or** edit `~/.cheetahclaws/mcp.json` for user-wide servers.

```json
{
  "mcpServers": {
    "git": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-git"]
    },
    "filesystem": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/tmp"]
    },
    "my-remote": {
      "type": "sse",
      "url": "http://localhost:8080/sse",
      "headers": {"Authorization": "Bearer my-token"}
    }
  }
}
```

Config priority: `.mcp.json` (project) overrides `~/.cheetahclaws/mcp.json` (user) by server name.

### Quick start

```bash
# Install a popular MCP server
pip install uv        # uv includes uvx
uvx mcp-server-git --help   # verify it works

# Add to user config via REPL
/mcp add git uvx mcp-server-git

# Or create .mcp.json in your project dir, then:
/mcp reload
```

### REPL commands

```
/mcp                          # list servers + their tools + connection status
/mcp reload                   # reconnect all servers, refresh tool list
/mcp reload git               # reconnect a single server
/mcp add myserver uvx mcp-server-x   # add stdio server
/mcp remove myserver          # remove from user config
```

### How Claude uses MCP tools

Once connected, Claude can call MCP tools directly:

```
You: What files changed in the last git commit?
AI: [calls mcp__git__git_diff_staged()]
    → shows diff output from the git MCP server
```

Tool names follow the pattern `mcp__<server_name>__<tool_name>`. All characters
that are not alphanumeric or `_` are automatically replaced with `_`.

### Popular MCP servers

| Server | Install | Provides |
|---|---|---|
| `mcp-server-git` | `uvx mcp-server-git` | git operations (status, diff, log, commit) |
| `mcp-server-filesystem` | `uvx mcp-server-filesystem <path>` | file read/write/list |
| `mcp-server-fetch` | `uvx mcp-server-fetch` | HTTP fetch tool |
| `mcp-server-postgres` | `uvx mcp-server-postgres <conn-str>` | PostgreSQL queries |
| `mcp-server-sqlite` | `uvx mcp-server-sqlite --db-path x.db` | SQLite queries |
| `mcp-server-brave-search` | `uvx mcp-server-brave-search` | Brave web search |

> Browse the full registry at [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers)

---

## Plugin System

The `plugin/` package lets you extend cheetahclaws with additional tools, skills, and MCP servers from git repositories or local directories.

### Install a plugin

```bash
/plugin install my-plugin@https://github.com/user/my-plugin
/plugin install local-plugin@/path/to/local/plugin
```

### Manage plugins

```bash
/plugin                   # list installed plugins
/plugin enable my-plugin  # enable a disabled plugin
/plugin disable my-plugin # disable without uninstalling
/plugin disable-all       # disable all plugins
/plugin update my-plugin  # pull latest from git
/plugin uninstall my-plugin
/plugin info my-plugin    # show manifest details
```

### Plugin recommendation engine

```bash
/plugin recommend                    # auto-detect from project files
/plugin recommend "docker database"  # recommend by keyword context
```

The engine matches your context against a curated marketplace (git-tools, python-linter, docker-tools, sql-tools, test-runner, diagram-tools, aws-tools, web-scraper) using tag and keyword scoring.

### Plugin manifest (plugin.json)

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Does something useful",
  "author": "you",
  "tags": ["git", "python"],
  "tools": ["tools"],        // Python module(s) that export TOOL_DEFS
  "skills": ["skills/my.md"],
  "mcp_servers": {},
  "dependencies": ["httpx"]  // pip packages
}
```

Alternatively use YAML frontmatter in `PLUGIN.md`.

### Scopes

| Scope | Location | Config |
|-------|----------|--------|
| user (default) | `~/.cheetahclaws/plugins/` | `~/.cheetahclaws/plugins.json` |
| project | `.cheetahclaws/plugins/` | `.cheetahclaws/plugins.json` |

Use `--project` flag: `/plugin install name@url --project`

---

## AskUserQuestion Tool

Claude can pause mid-task and interactively ask you a question before proceeding.

**Example invocation by Claude:**
```json
{
  "tool": "AskUserQuestion",
  "question": "Which database should I use?",
  "options": [
    {"label": "SQLite", "description": "Simple, file-based"},
    {"label": "PostgreSQL", "description": "Full-featured, requires server"}
  ],
  "allow_freetext": true
}
```

**What you see in the terminal:**
```
❓ Question from assistant:
   Which database should I use?

  [1] SQLite — Simple, file-based
  [2] PostgreSQL — Full-featured, requires server
  [0] Type a custom answer

Your choice (number or text):
```

- Select by number or type free text directly
- Claude receives your answer and continues the task
- 5-minute timeout (returns "(no answer — timeout)" if unanswered)

---

## Task Management

The `task/` package gives Claude (and you) a structured task list for tracking multi-step work within a session.

### Tools available to Claude

| Tool | Parameters | What it does |
|------|-----------|--------------|
| `TaskCreate` | `subject`, `description`, `active_form?`, `metadata?` | Create a task; returns `#id created: subject` |
| `TaskUpdate` | `task_id`, `subject?`, `description?`, `status?`, `owner?`, `add_blocks?`, `add_blocked_by?`, `metadata?` | Update any field; `status='deleted'` removes the task |
| `TaskGet` | `task_id` | Return full details of one task |
| `TaskList` | _(none)_ | List all tasks with status icons and pending blockers |

**Valid statuses:** `pending` → `in_progress` → `completed` / `cancelled` / `deleted`

### Dependency edges

```
TaskUpdate(task_id="3", add_blocked_by=["1","2"])
# Task 3 is now blocked by tasks 1 and 2.
# Reverse edges are set automatically: tasks 1 and 2 get task 3 in their "blocks" list.
```

Completed tasks are treated as resolved — `TaskList` hides their blocking effect on dependents.

### Persistence

Tasks are saved to `.cheetahclaws/tasks.json` in the current working directory after every mutation and reloaded on first access.

### REPL commands

```
/tasks                    list all tasks
/tasks create <subject>   quick-create a task
/tasks start <id>         mark in_progress
/tasks done <id>          mark completed
/tasks cancel <id>        mark cancelled
/tasks delete <id>        remove a task
/tasks get <id>           show full details
/tasks clear              delete all tasks
```

### Typical Claude workflow

```
User: implement the login feature

Claude:
  TaskCreate(subject="Design auth schema", description="JWT vs session")  → #1
  TaskCreate(subject="Write login endpoint", description="POST /auth/login") → #2
  TaskCreate(subject="Write tests", description="Unit + integration") → #3
  TaskUpdate(task_id="2", add_blocked_by=["1"])
  TaskUpdate(task_id="3", add_blocked_by=["2"])

  TaskUpdate(task_id="1", status="in_progress", active_form="Designing schema")
  ... (does the work) ...
  TaskUpdate(task_id="1", status="completed")
  TaskList()  → task 2 is now unblocked
  ...
```

---

## Voice Input

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/voice_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Voice Input: speak your prompt → offline Whisper transcription → AI responds</center>
</div>

CheetahClaws v3.05 adds a fully offline voice-to-prompt pipeline. Speak your request — it is transcribed and submitted as if you had typed it.

### Quick start

```bash
# 1. Install a recording backend (choose one)
pip install sounddevice        # recommended: cross-platform, no extra binary
# sudo apt install alsa-utils  # Linux arecord fallback
# sudo apt install sox         # SoX rec fallback

# 2. Install a local STT backend (recommended — works offline, no API key)
pip install faster-whisper numpy

# 3. Start CheetahClaws and speak
cheetahclaws
[myproject] ❯ /voice
  🎙  Listening… (speak now, auto-stops on silence, Ctrl+C to cancel)
  🎙  ████
✓  Transcribed: "fix the authentication bug in user.py"
[auto-submitting…]
```

### STT backends (tried in order)

| Backend | Install | Notes |
|---|---|---|
| `faster-whisper` | `pip install faster-whisper` | **Recommended** — local, offline, fastest, GPU optional |
| `openai-whisper` | `pip install openai-whisper` | Local, offline, original OpenAI model |
| OpenAI Whisper API | set `OPENAI_API_KEY` | Cloud, requires internet + API key |

Override the Whisper model size with `NANO_CLAUDE_WHISPER_MODEL` (default: `base`):

```bash
export NANO_CLAUDE_WHISPER_MODEL=small   # better accuracy, slower
export NANO_CLAUDE_WHISPER_MODEL=tiny    # fastest, lightest
```

### Recording backends (tried in order)

| Backend | Install | Notes |
|---|---|---|
| `sounddevice` | `pip install sounddevice` | **Recommended** — cross-platform, Python-native |
| `arecord` | `sudo apt install alsa-utils` | Linux ALSA, no pip needed |
| `sox rec` | `sudo apt install sox` / `brew install sox` | Built-in silence detection |

### Keyterm boosting

Before each recording, CheetahClaws extracts coding vocabulary from:
- **Git branch** (e.g. `feat/voice-input` → "feat", "voice", "input")
- **Project root name** (e.g. "cheetahclaws")
- **Recent source file stems** (e.g. `authentication_handler.py` → "authentication", "handler")
- **Global coding terms**: `MCP`, `grep`, `TypeScript`, `OAuth`, `regex`, `gRPC`, …

These are passed as Whisper's `initial_prompt` so the STT engine prefers correct spellings of coding terms.

### Commands

| Command | Description |
|---|---|
| `/voice` | Record voice and auto-submit the transcript as your next prompt |
| `/voice status` | Show which recording and STT backends are available, plus the active microphone |
| `/voice lang <code>` | Set transcription language (`en`, `zh`, `ja`, `de`, `fr`, … default: `auto`) |
| `/voice device` | List all available input microphones and select one interactively; persisted for the session |

### Selecting a microphone

On systems with multiple audio interfaces (USB headsets, virtual devices, etc.) you can pick the exact input device:

```
[myproject] ❯ /voice device
  🎙  Available input devices:
    0. Built-in Microphone
    1. USB Headset (USB Audio)  ◀  (currently selected)
    2. Virtual Input (BlackHole)
  Select device # (Enter to cancel): 1
✓  Microphone set to: [1] USB Headset (USB Audio)
```

The selected device is shown in `/voice status` and used for all subsequent recordings until you change it or restart.

### How it compares to Claude Code

| | Claude Code | CheetahClaws v3.05 |
|---|---|---|
| STT service | Anthropic private WebSocket (`voice_stream`) | `faster-whisper` / `openai-whisper` / OpenAI API |
| Requires Anthropic OAuth | Yes | **No** |
| Works offline | No | **Yes** (with local Whisper) |
| Keyterm hints | Deepgram `keyterms` param | Whisper `initial_prompt` (git + files + vocab) |
| Language support | Server-allowlisted codes | Any language Whisper supports |

---

## Brainstorm

`/brainstorm` runs a structured multi-persona AI debate over your project, then synthesizes all perspectives into an actionable plan.

### How it works

1. **Context snapshot** — reads `README.md`, `CLAUDE.md`, and root file listing from the current working directory.
2. **Agent count** — you are prompted to choose how many agents (2–100, default 5). Press Enter to use the default.
3. **Dynamic persona generation** — the model generates N expert roles tailored to your topic. Software topics get architects and engineers; geopolitics gets analysts, diplomats, and economists; business gets strategists and market experts. Falls back to built-in tech personas if generation fails.
4. **Agents debate sequentially**, each building on the previous responses.
5. **Output saved** to `brainstorm_outputs/brainstorm_YYYYMMDD_HHMMSS.md` in the current directory.
6. **Synthesis** — the main agent reads the saved file and produces a prioritized Master Plan.

**Example personas by topic:**

| Topic | Example Generated Personas |
|---|---|
| Software architecture | 🏗️ Architect · 💡 Product Innovator · 🛡️ Security Engineer · 🔧 Code Quality Lead · ⚡ Performance Specialist |
| US-Iran geopolitics | 🌍 Geopolitical Analyst · ⚖️ International Law Expert · 💰 Energy Economist · 🎖️ Military Strategist · 🕊️ Conflict Mediator |
| Business strategy | 📈 Market Strategist · 💼 Operations Lead · 🔍 Competitive Intelligence · 💡 Innovation Director · 📊 Financial Analyst |

### Usage

```
[myproject] ❯ /brainstorm
  How many agents? (2-100, default 5) > 5

[myproject] ❯ /brainstorm improve plugin architecture
  How many agents? (2-100, default 5) > 3

[myproject] ❯ /brainstorm US-Iran geopolitics
  How many agents? (2-100, default 5) > 7
```

### Example output

```
[myproject] ❯ /brainstorm medical research funding
  How many agents? (2-100, default 5) > 3
Generating 3 topic-appropriate expert personas...
Starting 3-Agent Brainstorming Session on: medical research funding
Generating diverse perspectives...
🩺 Clinical Trials Director is thinking...
  └─ Perspective captured.
⚖️ Medical Ethics Committee Member is thinking...
  └─ Perspective captured.
💰 Health Economics Policy Analyst is thinking...
  └─ Perspective captured.
✓  Brainstorming complete! Results saved to brainstorm_outputs/brainstorm_20260405_224117.md

   ── Analysis from Main Agent ──
[synthesized Master Plan streams here…]
```

### Notes

- Brainstorm uses the **currently selected model** (`/model` to check). A capable model (Claude Sonnet/Opus, GPT-4o, or a large local model) gives the best results.
- With many agents (20+) the session can take several minutes depending on model speed.
- Install `faker` (`pip install faker`) for randomized persona names; falls back to built-in names otherwise.
- Output files accumulate in `brainstorm_outputs/` — already added to `.gitignore` by v3.05.5.
- If output looks garbled in SSH (repeated lines), run `/config rich_live=false` to disable Rich Live streaming.

---

## SSJ Developer Mode

`/ssj` opens a persistent interactive power menu — a single entry point for the most common development workflows, so you never have to remember command names.

<div align=center>
<img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/ssj_demo.gif" width="850"/>
</div>

### Menu options

| # | Name | What it does |
|---|------|--------------|
| 1 | 💡 Brainstorm | Multi-persona AI debate → Master Plan → auto-generates `brainstorm_outputs/todo_list.txt` |
| 2 | 📋 Show TODO | View `brainstorm_outputs/todo_list.txt` with ✓/○ indicators and pending task numbers |
| 3 | 👷 Worker | Auto-implement pending tasks (all, or select by number) |
| 4 | 🧠 Debate | Pick a file and choose agent count — expert panel debates design round-by-round; result saved next to the file |
| 5 | ✨ Propose | Pick a file — AI proposes specific improvements with code |
| 6 | 🔎 Review | Pick a file — structured code review with 1–10 ratings per dimension |
| 7 | 📘 Readme | Pick a file — auto-generate a professional README for it |
| 8 | 💬 Commit | Analyse git diff and suggest a conventional commit message |
| 9 | 🧪 Scan | Summarise all staged/unstaged changes and suggest next steps |
| 10 | 📝 Promote | Read the latest brainstorm output → convert ideas to `todo_list.txt` tasks |
| 11 | 🎬 Video | Launch the Video Content Factory wizard (if `modular/video` is available) |
| 12 | 🎙 TTS | Launch the TTS Content Factory wizard (if `modular/voice` is available) |
| 13 | 📡 Monitor | Launch the AI Monitor wizard — add subscriptions, run now, configure push notifications |
| 14 | 🤖 Agent | Launch the Autonomous Agent wizard — Research Assistant / Auto Bug Fixer / Paper Writer / Auto Coder / Custom |
| 0 | 🚪 Exit | Return to the main REPL |

### Usage

```
[myproject] ❯ /ssj

╭─ SSJ Developer Mode ⚡ ─────────────────────────
│
│   1.  💡  Brainstorm — Multi-persona AI debate
│   2.  📋  Show TODO  — View todo_list.txt
│   3.  👷  Worker     — Auto-implement pending tasks
│   4.  🧠  Debate     — Expert debate on a file
│   5.  ✨  Propose    — AI improvement for a file
│   6.  🔎  Review     — Quick file analysis
│   7.  📘  Readme     — Auto-generate README.md
│   8.  💬  Commit     — AI-suggested commit message
│   9.  🧪  Scan       — Analyze git diff
│  10.  📝  Promote    — Idea to tasks
│  11.  🎬  Video      — Video Content Factory
│  12.  🎙  TTS        — TTS Content Factory
│  13.  📡  Monitor    — AI subscriptions & alerts
│  14.  🤖  Agent      — Autonomous task agents
│   0.  🚪  Exit SSJ Mode
│
╰──────────────────────────────────────────────

  ⚡ SSJ » 1
  Topic (Enter for general): cheetahclaws plugin system

  # → Brainstorm spins up, saves to brainstorm_outputs/, generates todo_list.txt
  # → Menu re-opens automatically after each action

  ⚡ SSJ » 2
  # → Shows numbered pending tasks from brainstorm_outputs/todo_list.txt

  ⚡ SSJ » 3
  Task # (Enter for all, or e.g. 1,4,6): 2
  # → Worker implements task #2 and marks it done
```

### Slash command passthrough

Any `/command` typed at the `⚡ SSJ »` prompt is passed through to the REPL:

```
  ⚡ SSJ » /model gpt-4o
  # → switches model, then re-opens SSJ menu

  ⚡ SSJ » /exit
  # → exits cheetahclaws immediately
```

### Worker command

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/worker_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">/worker: brainstorm → 5-task queue → auto-implement each with progress bar</center>
</div>

`/worker` (also accessible as SSJ option 3) reads `brainstorm_outputs/todo_list.txt` and auto-implements each pending task:

```
[myproject] ❯ /worker
  ✓ Worker starting — 3 task(s) to implement
    1. ○ Add animated brainstorm spinner
    2. ○ Implement Telegram typing indicator
    3. ○ Write SSJ demo GIF for README

  ── Worker (1/3): Add animated brainstorm spinner ──
  [model reads code, implements the change, marks task done]

[myproject] ❯ /worker 2,3
  # Implement only tasks 2 and 3

[myproject] ❯ /worker --path docs/tasks.md
  # Use a custom todo file

[myproject] ❯ /worker --workers 2
  # Process only the first 2 pending tasks this run
```

**Smart path detection** — if you pass a brainstorm output file (`.md`) by mistake, Worker detects it and offers to redirect to the matching `todo_list.txt` in the same folder. If that file does not yet exist, it offers to generate `todo_list.txt` from the brainstorm output first (SSJ Promote), then run Worker automatically.

### Debate command

SSJ option 4 runs a structured multi-round expert debate on any file:

```
  ⚡ SSJ » 4

  Files in brainstorm_outputs/:
    1. brainstorm_20260406_143022.md
    2. cheetahclaws.py

  File to debate #: 2
  Number of debate agents (Enter for 2): 3
  ℹ Debate result will be saved to: cheetahclaws_debate_143055.md

⚔️  Assembling expert panel...
  Expert 1: 🏗️ Architecture Lead — focus: system design & modularity
  Expert 2: 🔐 Security Engineer — focus: attack surface & input validation
  Expert 3: ⚡ Performance Specialist — focus: latency & memory usage

⚔️  Round 1/5 — Expert 1 thinking...
  [Architecture Lead gives opening argument...]

💬  Round 1/5 — Expert 2 formulating...
  [Security Engineer responds...]
  ...

📜  Drafting final consensus...
  [model writes consensus + saves transcript]
✓ Debate complete. Saved to cheetahclaws_debate_143055.md
```

- Agent count is configurable (minimum 2, default 2). Rounds are set to `agents × 2 − 1` for a full open-close structure.
- An animated spinner shows the current round and expert (`⚔️ Round 2/3 — Expert 1 thinking...`), stopping the moment that expert starts outputting.
- The full debate transcript and ranked consensus are saved to `<filename>_debate_HHMMSS.md` **in the same directory as the debated file**.

---

## Telegram Bridge

`/telegram` turns cheetahclaws into a Telegram bot — receive messages from your phone, run the model with full tool access, and reply automatically.

<div align=center>
<img src="https://github.com/SafeRL-Lab/clawspring/blob/main/docs/telegram_demo.gif" width="850"/>
</div>

### Setup (one-time)

1. Open [@BotFather](https://t.me/BotFather) in Telegram → `/newbot` → copy the token.
2. Send any message to your new bot (e.g. "hi"), then open the URL below in your browser — replace `<TOKEN>` with your real token:

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

The response is JSON. Find `"chat"` → `"id"` — that number is your chat ID:

```json
{
  "ok": true,
  "result": [
    {
      "update_id": 100000001,
      "message": {
        "from": { "id": 987654321, "first_name": "Zhang" },
        "chat": {
          "id": 987654321,
          "type": "private"
        },
        "text": "hi"
      }
    }
  ]
}
```

> **Tip:** if `result` is empty, go back to Telegram, send another message to your bot, then refresh the URL.

3. Configure cheetahclaws (example with the values above):

```
[myproject] ❯ /telegram 7812345678:AAFxyz123abcDEF456ghiJKL789 987654321
  ✓ Telegram config saved.
  ✓ Connected to @your_bot_name. Starting bridge...
  ✓ Telegram bridge active. Chat ID: 987654321
  ℹ Send messages to your bot — they'll be processed here.
  ℹ Stop with /telegram stop or send /stop in Telegram.
```

Token and chat_id are saved to `~/.cheetahclaws/config.json`. On next launch the bridge **auto-starts** if configured — the startup banner shows `flags: [telegram]`.

### How it works

```
Phone (Telegram)                  cheetahclaws terminal
──────────────────                ──────────────────────────
"List Python files"      →        📩 Telegram: List Python files
                                  [typing indicator sent...]
                                  ⚙ Glob(**/*.py) → 5 files
                                  ⚙ response assembled
                          ←       "agent.py, tools.py, ..."
```

- **Typing indicator** is sent every 4 seconds while the model processes, so the chat feels responsive.
- **Unauthorized senders** receive `⛔ Unauthorized.` and their messages are dropped.
- **Slash command passthrough**: send `/cost`, `/model gpt-4o`, `/clear`, `/monitor`, `/agent`, etc. from Telegram and they execute in cheetahclaws.
- **Interactive menus over Telegram**: commands with interactive prompts (e.g. `/monitor` wizard, `/agent` wizard, `/permission`, `/checkpoint`) run in a background thread. The menu is sent as a Telegram message; your next reply is used as the selection.
- **Job queue & remote control**: `!jobs` / `!job <id>` / `!retry <id>` / `!cancel` — see [Remote Control](#remote-control-phone--computer).
- **`/stop` or `/off`** sent from Telegram stops the bridge gracefully.

### Photo & Voice support

You can send photos and voice messages directly to the bot — no extra commands needed.

**Photos**

Send any photo (with or without a caption). CheetahClaws downloads the highest-resolution version, encodes it as Base64, and passes it to the active vision model alongside the caption text. If no caption is provided, the default prompt is `"What do you see in this image? Describe it in detail."`.

> **Requirement:** the active model must support vision (e.g. `claude-opus-4-6`, `gpt-4o`, `gemini-2.0-flash`, or any Ollama vision model such as `llava`). Use `/model` to switch if needed.

**Voice messages & audio files**

Send a voice note (OGG) or audio file (MP3). CheetahClaws transcribes it automatically and submits the transcript as your next query. The transcription is echoed back to the chat before the model responds.

> **Requirements:**
> - **`ffmpeg`** must be installed for audio conversion (`sudo apt install ffmpeg` / `brew install ffmpeg`).
> - At least one STT backend must be available (tried in order):
>   1. `faster-whisper` — `pip install faster-whisper` (local, offline, recommended)
>   2. `openai-whisper` — `pip install openai-whisper` (local, offline)
>   3. OpenAI Whisper API — set `OPENAI_API_KEY` (cloud fallback, requires internet)
>
> If `ffmpeg` is missing, voice messages will fail with `⚠ Could not download voice message.`

### Commands

| Command | Description |
|---|---|
| `/telegram <token> <chat_id>` | Configure token + chat_id, then start the bridge |
| `/telegram` | Start the bridge using saved config |
| `/telegram status` | Show running state and chat_id |
| `/telegram stop` | Stop the bridge |

### Auto-start

If both `telegram_token` and `telegram_chat_id` are set in `~/.cheetahclaws/config.json`, the bridge starts automatically on every cheetahclaws launch:

```
╭─ CheetahClaws ────────────────────────────────╮
│  Model:       claude-opus-4-6
│  Permissions: auto   flags: [telegram]
│  Type /help for commands, Ctrl+C to cancel        │
╰───────────────────────────────────────────────────╯
✓ Telegram bridge started (auto). Bot: @your_bot_name
```

---

## WeChat Bridge

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/wechat_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">WeChat Bridge: Control cheetahclaws from WeChat (微信)</center>
</div>

`/wechat` connects cheetahclaws to WeChat via **Tencent's iLink Bot API** — the same underlying protocol used by the official [WeixinClawBot](https://www.npmjs.com/package/@tencent-weixin/openclaw-weixin) plugin. Authenticate by scanning a QR code with your WeChat app; no manual token setup required.

### Prerequisites

**Enable the ClawBot plugin inside WeChat:**
WeChat → Me → Settings → Plugins → find and enable **ClawBot** (WeixinClawBot)

> This feature is being rolled out gradually by Tencent and may not yet be available on all accounts.

### Setup (one-time, ~30 seconds)

Run `/wechat login` in cheetahclaws. A QR code URL appears in the terminal — open it in a browser or scan it directly if you installed the `qrcode` package:

```
[myproject] ❯ /wechat login
  ℹ Fetching WeChat QR code from iLink...

  请用微信扫描以下二维码 / Scan with WeChat:

  https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=ccf1fb71...&bot_type=3

(Install 'qrcode' for inline QR rendering: pip install qrcode)
  等待扫码中... / Waiting for scan...
  ✓ 微信登录成功 / WeChat authenticated (account: 3cdf6fb6d104@im.bot)
  ✓ WeChat bridge started.
  ℹ Send a message from WeChat — it will be processed here.
  ℹ Stop with /wechat stop or send /stop from WeChat.
```

Scan the QR code URL with WeChat. Once confirmed, the bridge starts immediately. Credentials (`token` + `base_url`) are saved to `~/.cheetahclaws/config.json` and reused on every subsequent launch — you only need to scan once.

> **Tip:** `pip install qrcode` renders the QR code directly in the terminal as ASCII art, so you can scan without opening a browser.

### How it works

```
Phone (WeChat)          cheetahclaws terminal
──────────────          ──────────────────────────────────
"你好"          →       📩 WeChat [o9cq80_Q]: 你好
                        [typing indicator...]
                        ⚙ model processes query
                ←       "你好！有什么我可以帮你的吗？..."
```

The bridge long-polls `POST /ilink/bot/getupdates` (35-second window) in a daemon thread. The server holds the connection until a message arrives or the window closes — normal timeouts are handled transparently. Every outbound reply echoes the peer's latest `context_token` as required by the iLink protocol.

### Features

- **QR code authentication** — scan once; credentials are saved for future launches. Expired sessions (`errcode -14`) clear saved credentials and the next `/wechat` re-triggers the QR flow automatically.
- **Typing indicator** — sent every 4 seconds while the model processes, so the chat feels responsive.
- **context_token echo** — per-peer `context_token` is cached in memory and echoed on every reply (iLink protocol requirement).
- **Slash command passthrough** — send `/cost`, `/model gpt-4o`, `/clear`, `/monitor`, `/agent`, etc. from WeChat and they execute in cheetahclaws. The result is sent back to the same WeChat conversation.
- **Interactive menu routing** — commands with interactive prompts (e.g. `/monitor` wizard, `/agent` wizard, `/permission`, `/checkpoint`) run in a background thread and route the prompt to WeChat; your next WeChat reply is used as the selection input.
- **Per-user job queue** — each WeChat user has an independent job queue; `!任务` / `!job <id>` / `!retry <id>` / `!cancel` for remote control. See [Remote Control](#remote-control-phone--computer).
- **`/stop` or `/off`** sent from WeChat stops the bridge gracefully.
- **Multi-user support** — each sender's `user_id` is tracked separately so `context_token`, job queue, and input routing stay per-peer.
- **Message deduplication** — `message_id` / `seq` dedup prevents double-processing on reconnect.

### Commands

| Command | Description |
|---|---|
| `/wechat login` | Scan QR code to authenticate and start the bridge |
| `/wechat` | Start with saved credentials; triggers QR login if none saved |
| `/wechat status` | Show running state and account ID |
| `/wechat stop` | Stop the bridge |
| `/wechat logout` | Clear saved credentials and stop the bridge |

### Auto-start

If `wechat_token` is set in `~/.cheetahclaws/config.json`, the bridge starts automatically on every cheetahclaws launch:

```
╭─ CheetahClaws ────────────────────────────────╮
│  Model:       claude-opus-4-6
│  Permissions: auto   flags: [wechat]
│  Type /help for commands, Ctrl+C to cancel        │
╰───────────────────────────────────────────────────╯
✓ WeChat bridge started.
```

---

## Slack Bridge

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/slack_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Slack Bridge: Control cheetahclaws from Slack</center>
</div>

`/slack` connects cheetahclaws to a Slack channel via the **Slack Web API** — no external packages required, just a Bot User OAuth Token and a channel ID. Messages are polled every 2 seconds using `conversations.history`; replies update an in-place "⏳ Thinking…" placeholder so the conversation feels responsive.

### Prerequisites

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → From scratch.
2. **OAuth & Permissions** → add **Bot Token Scopes**:
   - `channels:history` `chat:write` `groups:history` `im:history` `mpim:history` `channels:read`
3. **Install to Workspace** → copy the **Bot User OAuth Token** (`xoxb-...`).
4. Invite the bot to your target channel: `/invite @<bot_name>` in Slack.
5. Copy the **Channel ID** (right-click channel → **Copy Link** → the `C...` segment, or via the channel's **About** panel).

### Setup (one-time, ~2 minutes)

```
[myproject] ❯ /slack xoxb-12345-... C0123456789
  ℹ Slack credentials saved (channel: C0123456789).
  ℹ Slack authenticated as @cheetahclaws_bot
  ✓ Slack bridge started.
  ℹ Send a message in the configured Slack channel — it will be processed here.
  ℹ Stop with /slack stop or send /stop in Slack.
```

Credentials are saved to `~/.cheetahclaws/config.json` and the bridge auto-starts on every subsequent launch — you only need to configure once.

### How it works

```
Slack channel                    cheetahclaws terminal
─────────────                    ──────────────────────────────────
"List files here"      →         📩 Slack [U04ABZ]: List files here
                                 [⏳ Thinking… posted to Slack]
                                 ⚙ model processes query
                       ←         "Here are the files: …"  (placeholder updated)
```

Every 2 seconds, cheetahclaws polls `GET conversations.history?oldest=<last_ts>`. When a message arrives, a `⏳ Thinking…` placeholder is posted immediately via `chat.postMessage`, then updated in-place with the real reply via `chat.update` once the model finishes.

### Features

- **No external packages** — uses only Python's stdlib `urllib`; no `slack_sdk` or `requests` needed.
- **In-place reply update** — "⏳ Thinking…" placeholder is replaced with the actual response, keeping the channel tidy.
- **Slash command passthrough** — send `/cost`, `/model gpt-4o`, `/clear`, `/monitor`, `/agent`, etc. from Slack and they execute in cheetahclaws; results are sent back to the same channel.
- **Interactive menu routing** — `/monitor` wizard, `/agent` wizard, permission prompts, and other interactive menus route to Slack; your next message is used as the selection input.
- **Job queue & remote control**: `!jobs` / `!job <id>` / `!retry <id>` / `!cancel` — see [Remote Control](#remote-control-phone--computer).
- **Auth validation on start** — `auth.test` is called before the poll loop; invalid tokens surface a clear error immediately.
- **`/stop` or `/off`** sent from Slack stops the bridge gracefully.
- **Message deduplication** — `ts` (Slack timestamp) dedup prevents double-processing.
- **Error resilience** — after 5 consecutive connection failures the loop backs off for 30 s; auth errors (`invalid_auth`, `token_revoked`) stop the bridge with a clear message.

### Commands

| Command | Description |
|---|---|
| `/slack <token> <channel_id>` | Configure and start the bridge |
| `/slack` | Start with saved credentials |
| `/slack status` | Show running state and channel ID |
| `/slack stop` | Stop the bridge |
| `/slack logout` | Clear saved credentials and stop the bridge |

### Auto-start

If `slack_token` and `slack_channel` are set in `~/.cheetahclaws/config.json`, the bridge starts automatically on every cheetahclaws launch:

```
╭─ CheetahClaws ────────────────────────────────╮
│  Model:       claude-opus-4-6
│  Permissions: auto   flags: [slack]
│  Type /help for commands, Ctrl+C to cancel    │
╰───────────────────────────────────────────────╯
✓ Slack bridge started.
```

---

## Remote Control (Phone → Computer)

All three bridges (Telegram, Slack, WeChat) include a persistent job queue and remote management commands so you can control long-running work from your phone.

### Job queue

When the AI is processing a query and a new message arrives, it is queued automatically — nothing is dropped.

```
Phone: "Run all tests"
cheetahclaws: ⏳ Queued as job #a3f2 (position 1)
              "Run all tests"
              Use !jobs to check status.

Phone: !jobs
cheetahclaws: 📊 Job Dashboard
              ────────────────────────────────────
              🔄 #b7c1  [just now]  "Run all tests" — Bash: pytest…
              ✅ #a3f2  [2m ago]    "Explain auth flow" (3 steps 18s)
              ❌ #9d0e  [5m ago]    "Fix login bug" — ModuleNotFoundError

              !job <id>  !retry <id>  !cancel
```

### Bridge commands (all three bridges)

| Command | Description |
|---|---|
| `!jobs` or `!j` or `!status` | Show job dashboard (last 8 jobs, running first) |
| `!job <id>` | Show full detail card for a job — steps, result preview, error |
| `!retry <id>` | Re-run a failed job with the same prompt |
| `!cancel` | Cancel the currently running job |
| `!cancel <id>` | Cancel a specific job by ID |

### Job tracking

Each job records:
- **Status** — queued → running → done / failed / cancelled
- **Steps** — every tool call (`Bash`, `Read`, `Edit`, …) with result preview
- **Result preview** — last 600 chars of the AI's response
- **Duration** — wall-clock seconds from start to finish

Jobs are persisted to `~/.cheetahclaws/jobs.json` (last 100 kept).

### WeChat specifics

WeChat uses **per-user queues** — each `user_id` gets an independent queue, so multiple WeChat users never block each other. All commands above are in Chinese: `!任务`, `!取消`, etc. are also accepted.

---

## Monitor — AI Subscriptions & Alerts

`/monitor` turns cheetahclaws into a 24/7 AI research assistant that watches stocks, crypto, arxiv, world news, or any custom topic on a schedule and pushes AI-written reports to Telegram, Slack, or your terminal.

### Quick start — interactive wizard

```
[myproject] ❯ /monitor

╭─ AI Monitor + Decision Assistant ─────────────────────
│  Monitor anything 24/7. AI summarizes & pushes to you.
│
│  What do you want to do?
│
│  1.  Add a new subscription
│  2.  Run all subscriptions now  (preview reports)
│  3.  Start background scheduler
│  5.  Configure push notifications  (Telegram / Slack)
│  0.  Exit
╰────────────────────────────────────────────────────────

  » 1
```

The wizard walks you through topic → schedule → delivery channel → run now → start scheduler. Zero prior knowledge required.

### Available topics

| Topic | Source | Example |
|---|---|---|
| `ai_research` | arxiv RSS (cs.AI/cs.LG/cs.CL) + weekend API fallback | `/subscribe ai_research` |
| `stock_<TICKER>` | Yahoo Finance JSON API (no key) | `/subscribe stock_TSLA daily` |
| `crypto_<SYMBOL>` | CoinGecko public API (no key) | `/subscribe crypto_BTC 6h` |
| `world_news` | Reuters · BBC · Guardian · AP RSS | `/subscribe world_news --telegram` |
| `custom:<query>` | DuckDuckGo Instant Answer | `/subscribe custom:quantum computing weekly` |

### Schedules

`15m` · `30m` · `1h` · `2h` · `6h` · `12h` · `daily` · `weekly`

### Commands

```
/monitor                          # interactive wizard
/monitor run [topic]              # run now and print report
/monitor start                    # start background scheduler
/monitor stop                     # stop background scheduler
/monitor status                   # show scheduler state + subscriptions
/monitor set telegram <t> <id>    # configure Telegram delivery
/monitor set slack <t> <ch>       # configure Slack delivery
/monitor topics                   # list all built-in topics

/subscribe ai_research            # quick-add subscription (daily, auto channel)
/subscribe stock_TSLA daily --telegram
/subscriptions                    # list all active subscriptions
/unsubscribe ai_research          # remove a subscription
```

### Sample report output

```
📊 AI Research Digest — 2026-04-12

3 new papers on Large Language Models:

• **RLVR-Pro** (Chen et al.) — New RL training method achieves +4.2% on MMLU
  vs PPO baseline. Key insight: reward shaping with KL penalty prevents mode
  collapse on reasoning tasks.

• **FlashKV** (Park et al.) — KV-cache compression reducing memory 3× with
  <0.5% perplexity loss. Applicable to any transformer at inference time.

• **AgentBench-2** (Liu et al.) — 200-task evaluation suite for coding agents.
  Claude-3.7 leads at 73.4%, GPT-5 at 71.1%.
```

---

## Autonomous Agents

`/agent` starts autonomous background agent loops driven by Markdown task templates (inspired by Karpathy's `program.md` pattern). Each agent gets an isolated `AgentState`, calls the real model with full tools, and runs until stopped or the task is complete.

### Quick start — interactive wizard

```
[myproject] ❯ /agent

╭────────────────────────────────────────────────────────╮
│  🤖  Auto Agent  —  What do you want to do?            │
╰────────────────────────────────────────────────────────╯

  1  📚  Research Assistant
        Read papers → summarize → build related work

  2  🐛  Auto Bug Fixer
        Run tests → find failures → fix & commit

  3  ✍️   Paper Writer
        Write paper sections from an outline

  4  💻  Auto Coder
        Implement tasks from a backlog → test → commit

  5  📄  Custom template…
        Use your own .md program file

  q  Quit

  Choice [1-5, q]: 1
  Paper directory or search topic [.]: ~/papers/
  Output notes file [research_notes.md]:
  Agent name [research]:
  Auto-approve file writes? [Y/n]: Y
  Seconds between iterations [2]:

  ─── Summary ───────────────────────────────────
  Template  : research_assistant
  Name      : research
  Args      : ~/papers/ --output research_notes.md
  Interval  : 2.0s
  Auto-approve: True

  Start? [Y/n]: Y
✓ Agent 'research' is running.
  Log  : ~/.cheetahclaws/agents/research/log.jsonl
  Progress → this terminal (iterations print here).
  Stop : /agent stop research
```

### Built-in templates

| Template | What it does |
|---|---|
| `research_assistant` | Lists PDFs / searches topic → extracts key contributions → updates `research_notes.md` + `related_work.md` → repeats |
| `auto_bug_fixer` | Runs `<test_cmd>` → reads failing test + source → fixes root cause → commits → repeats until green |
| `paper_writer` | Reads outline → writes each section in academic style → appends to `paper_draft.md` → repeats section by section |
| `auto_coder` | Reads `tasks.md` backlog → implements one task → tests → commits → marks done → repeats |

### Direct launch (power user)

```bash
/agent start research_assistant ~/papers/
/agent start auto_bug_fixer --test-cmd "pytest tests/" --repo .
/agent start paper_writer outline.md --output paper_draft.md --style NeurIPS
/agent start auto_coder --task "add rate limiting to the API"
/agent start /path/to/my_template.md --name myagent
```

**Flags:** `--name <name>` · `--interval <seconds>` · `--no-auto-approve`

### Agent lifecycle commands

```
/agent list                   # show all running agents + current status
/agent status <name>          # show recent 3 iteration summaries
/agent stop <name>            # stop a specific agent
/agent stop all               # stop all running agents
/agent templates              # list built-in + user templates
```

### Custom templates

Drop any `.md` file into `~/.cheetahclaws/agent_templates/` following the program.md pattern:

```markdown
# My Custom Agent

You are an autonomous agent. Your goal: <describe the goal>.

## Setup (first iteration only)
1. ...

## Each iteration
1. ...
2. ...

## Rules
- Do not stop unless <condition>.
- NEVER STOP unless explicitly stopped.
```

Templates are plain Markdown — no special syntax. The agent runs them as a system prompt.

### Phone control

Agents push iteration summaries to the active bridge (Telegram/Slack/WeChat) automatically. From your phone:

```
!agent list           # see all running agents
!agent status research  # last 3 iterations of 'research'
!agent stop research  # stop the agent
```

Iteration log is also persisted to `~/.cheetahclaws/agents/<name>/log.jsonl` for offline review.

---

## Video Content Factory

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/video_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Video Factory: topic → AI story → TTS → images → subtitles → final .mp4</center>
</div>

`/video` is an AI-powered viral video pipeline. Give it a topic — or your own script — and it produces a fully narrated, illustrated, subtitle-burned `.mp4` ready to upload.

```
[AI mode]     Topic → AI Story → TTS Voice → Images → PIL Subtitles → Final Video
[Script mode] Your Text → TTS Voice → Images → PIL Subtitles (same text) → Final Video
```

### Quick start (zero-cost path)

```bash
# Install free dependencies
pip install edge-tts Pillow imageio-ffmpeg
sudo apt install ffmpeg          # or: brew install ffmpeg / conda install ffmpeg

# Launch interactive wizard
[myproject] ❯ /video
```

The wizard walks you through every setting with `Enter = Auto` defaults at every step. Type `b` to go back, `q` to quit at any point.

### Wizard walkthrough

```
╭─ 🎬 Video Content Factory ─────────────────────╮
│  Enter=Auto on every step  ·  b=back  ·  q=quit │
╰─────────────────────────────────────────────────╯

[0] Content mode
  1. Auto         (AI generates story from your topic)
  2. Custom script (you provide the text — TTS reads it as narration + subtitles)

[1] Topic / idea        ← skip if using custom script
[2] Source folder       ← optional: images / audio / video / text files
[3] Language            ← auto-detects from topic; supports custom language entry
[4] Style / Niche       ← 10 viral niches + auto-viral + custom style
[5] Format              ← Landscape 16:9 (YouTube) or Short 9:16 (TikTok / Reels)
[6] Duration            ← 30s · 1 min · 2 min · 3 min · 5 min · custom
[7] Voice (TTS)         ← auto / Edge (free) / Gemini / ElevenLabs
[8] Images              ← auto / web-search / gemini-web / placeholder
[9] Video Quality       ← auto / high / medium / low / minimal
[10] Subtitles          ← Auto (Whisper) / Story text / Custom text / None
[11] Output path        ← default: ./video_output/
```

#### Content mode: Custom script

Select **"2. Custom script"** to provide your own narration text instead of having the AI generate a story:

```
[0] Content mode
  Pick mode: 2

  Paste your narration text (type END on a new line when done):
  CheetahClaws is a lightweight Python AI coding assistant
  that supports any model — Claude, GPT, Gemini, or local Ollama.
  END
  → Script: 18 words
```

The TTS engine reads the script aloud. The same text is split into timed subtitle entries and burned into the video with PIL. No Whisper, no AI story generation — works fully offline.

Steps skipped in script mode: Topic, Style/Niche, Duration (auto-derived from word count).

### Pipeline steps

| Step | What happens |
|---|---|
| **1. Story / Script** | AI generates viral story (AI mode) OR uses your text directly (script mode) |
| **2. Voice (TTS)** | Edge TTS / Gemini TTS / ElevenLabs narrates the text |
| **3. Subtitles** | PIL renders subtitles as transparent PNGs; ffmpeg overlays them — works for any language |
| **4. Images** | Gemini Web (Imagen 3) → web search (Pexels / Wikimedia) → placeholder |
| **5. Assembly** | zoompan clips + audio → two-pass encode with PIL subtitle burn |

### Subtitle engine

Subtitles are rendered with **Pillow + NotoSansSC font** — not libass. This means:

- Chinese, Japanese, Korean, Cyrillic, Arabic, Thai all render correctly
- Font is downloaded once to `~/.cheetahclaws/fonts/` on first run (~8 MB)
- Two-pass approach: fast `-c:v copy` assembly, then PIL PNG overlays via `filter_complex`
- Falls back to no subtitles if PIL fails — never crashes the pipeline

**Subtitle source options** (wizard step 10):

| Option | How | Best for |
|---|---|---|
| Auto | Whisper transcription (`faster-whisper`) | When exact word timing matters |
| Story text | Same text TTS reads, timed proportionally | All languages; no Whisper needed |
| Custom text | Paste your own text | Translations, alternate language |
| None | Skip subtitles | Music videos, no-sub content |

### Image backends (vision input)

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/image_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">/image: paste UI screenshot → AI flags issues; paste code screenshot → AI spots bugs</center>
</div>

| Engine | How | Cost | Quality |
|---|---|---|---|
| `gemini-web` | Playwright + Imagen 3 via Gemini web | **Free** | High |
| `web-search` | Pexels → Wikimedia Commons → Picsum | **Free** | Medium |
| `placeholder` | Gradient slides with prompt text | **Free** | N/A |
| `auto` | gemini-web → web-search → placeholder | — | Best available |

**Gemini Web images (recommended free path):**

One-time login (session is saved):

```bash
cd ../v-content-creator
python -c "from gemini_image_gen import verify_login_interactive; verify_login_interactive()"
```

**Web search images** work out-of-the-box with no login or API key. The model generates optimized search queries from the story/script content. Sources tried in order: Pexels → Wikimedia Commons → Lorem Picsum (always succeeds).

**AI source image selection:** when `--source <dir>` contains more images than needed, the model reads filenames and story content to rank and select the most relevant ones. Keyword-scoring fallback if the model is unavailable.

### TTS backends

| Engine | How | Cost | Quality |
|---|---|---|---|
| `gemini` | Gemini TTS API (`GEMINI_API_KEY`) | Free tier | Good |
| `elevenlabs` | ElevenLabs REST (`ELEVENLABS_API_KEY`) | Paid | Excellent |
| `edge` | Microsoft Edge TTS (`pip install edge-tts`) | **Free** | Good |
| `auto` | Try gemini → elevenlabs → edge | — | Best available |

Language-appropriate voices are auto-selected (e.g. `zh-CN-YunxiNeural` for Chinese, `ja-JP-KeitaNeural` for Japanese).

### Content niches (AI mode)

10 built-in viral content niches, weighted toward the most viral:

| Niche ID | Name | Style |
|---|---|---|
| `misterio_real` | True Crime | Documentary, investigative |
| `confesiones` | Dark Confessions | Intimate, vulnerable |
| `suspenso_cotidiano` | Everyday Suspense | Mundane → disturbing |
| `ciencia_ficcion` | Sci-Fi / Black Mirror | Near-future, tech noir |
| `drama_humano` | Human Drama | Emotional, raw |
| `terror_psicologico` | Psychological Horror | Insidious, ambiguous |
| `folklore_latam` | Latin American Folklore | Magical realism |
| `venganza` | Revenge / Poetic Justice | Calculated, satisfying |
| `supervivencia` | Survival Stories | Adrenaline, extreme |
| `misterio_digital` | Digital Mystery | Internet creepy, cyber horror |

Story generation uses a 3-tier fallback: structured prompt → simplified structured → free-form, ensuring a story is always produced even with small local models.

### Source materials (`--source`)

Pass `--source <dir>` (or enter path in the wizard) to pre-load your own materials:

| File type | Behaviour |
|---|---|
| Images (`.jpg`, `.png`, …) | Used directly instead of AI/web-search images; model selects most relevant |
| Audio (`.mp3`, `.wav`) | Used as narration, skipping TTS |
| Video (`.mp4`, `.mov`, …) | Audio track extracted and used as narration; frames extracted as images |
| Text (`.txt`, `.md`, …) | Read and injected as story context / topic direction |

A single file (e.g. a README or script) can also be passed — it is read and injected as context.

### Output files

```
video_output/
├── video_20260407_153000_my_title.mp4        # Final video
└── video_20260407_153000_my_title_info.json  # Metadata (title, niche, word count, engines)

video_tmp/batch_20260407_153000/story/
├── story.txt     # Story or script text
├── audio.mp3     # TTS narration
├── subs.srt      # Subtitle file (if generated)
└── images/       # img_00.png … img_07.png
```

### Requirements summary

| Requirement | Install | Notes |
|---|---|---|
| `ffmpeg` | `sudo apt install ffmpeg` or `pip install imageio-ffmpeg` | Required |
| `Pillow` | `pip install Pillow` | Required for subtitle rendering + images |
| `edge-tts` | `pip install edge-tts` | Free TTS (recommended) |
| `faster-whisper` | `pip install faster-whisper` | Auto subtitle transcription (optional) |
| `playwright` | `pip install playwright && playwright install chromium` | Gemini Web images (optional) |
| `GEMINI_API_KEY` | env var | Gemini TTS + story generation |
| `ELEVENLABS_API_KEY` | env var | ElevenLabs TTS (optional) |

---

## TTS Content Factory

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/voice_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">TTS Factory: choose voice style → AI writes script → synthesize → .mp3 output</center>
</div>

`/tts` is an AI-powered audio generation wizard. Give it a topic — or paste your own script — and it produces a narrated MP3 in any voice style.

### Quick start

```bash
# Install free TTS backend (no API key needed)
pip install edge-tts

# Launch interactive wizard
[myproject] ❯ /tts
```

The wizard walks through every setting with `Enter = Auto` at every step. Type `b` to go back, `q` to quit.

### Wizard walkthrough

```
╭─ 🎙 TTS Content Factory ────────────────────────────────╮
│  Enter=Auto on every step  ·  b=back  ·  q=quit         │
╰─────────────────────────────────────────────────────────╯

[0] Content mode
  1. Auto         (AI generates script from your topic)
  2. Custom text  (paste your own script → TTS reads every word)

[1] Voice style   ← narrator / newsreader / storyteller / ASMR / motivational /
                     documentary / children / podcast / meditation / custom
[2] Duration      ← Auto~1 min / 30s / 1m / 2m / 3m / 5m / custom  (AI mode only)
[3] TTS Engine    ← Auto / Edge (free) / Gemini / ElevenLabs
[4] Voice         ← Auto (style preset) / individual Gemini or Edge voice
[5] Output folder ← default: ./tts_output/
```

Output files:

```
tts_output/
├── tts_1712345678.mp3          # synthesized audio
└── tts_1712345678_script.txt   # companion script text
```

### Voice style presets

| Style | Description | Default Gemini voice | Default Edge voice |
|---|---|---|---|
| Narrator | Calm, authoritative | Charon | en-US-GuyNeural |
| Newsreader | Professional, neutral | Aoede | en-US-AriaNeural |
| Storyteller | Dramatic, immersive | Fenrir | en-US-DavisNeural |
| ASMR | Soft, intimate, relaxing | Aoede | en-US-JennyNeural |
| Motivational | Energetic, inspiring | Puck | en-US-TonyNeural |
| Documentary | Informative, thoughtful | Charon | en-GB-RyanNeural |
| Children | Warm, playful | Kore | en-US-AnaNeural |
| Podcast | Conversational, casual | Puck | en-US-GuyNeural |
| Meditation | Slow, peaceful | Aoede | en-US-JennyNeural |
| Custom | Describe your own style | Charon | en-US-GuyNeural |

### TTS backends

| Engine | How | Cost | Quality |
|---|---|---|---|
| `gemini` | Gemini TTS API (`GEMINI_API_KEY`) | Free tier | Good |
| `elevenlabs` | ElevenLabs REST (`ELEVENLABS_API_KEY`) | Paid | Excellent |
| `edge` | Microsoft Edge TTS (`pip install edge-tts`) | **Free** | Good |
| `auto` | Try gemini → elevenlabs → edge | — | Best available |

**CJK auto-voice:** if the text is predominantly Chinese/Japanese/Korean and an English voice is selected, the backend automatically switches to `zh-CN-XiaoxiaoNeural` so every character is spoken — not silently skipped.

**Long-text chunking:** texts over 2 000 chars are split at sentence boundaries, synthesized in chunks, and concatenated with ffmpeg. The full script is always read aloud regardless of length.

### Requirements

| Requirement | Install | Notes |
|---|---|---|
| `edge-tts` | `pip install edge-tts` | Free TTS (always-available fallback) |
| `ffmpeg` | `sudo apt install ffmpeg` or `pip install imageio-ffmpeg` | Required for multi-chunk concat |
| `GEMINI_API_KEY` | env var | Gemini TTS (optional) |
| `ELEVENLABS_API_KEY` | env var | ElevenLabs TTS (optional) |

Check status: `/tts status`

### Also in SSJ mode

`/tts` is available as option **12** in the SSJ Developer Mode menu, so you can chain it with brainstorm, worker, and video workflows in a single session.

---

## Tmux Integration

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/tmux_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Tmux Integration: AI splits panes, sends commands, captures output across sessions</center>
</div>

CheetahClaws gives the AI model **direct control over tmux** — create sessions, split panes, send commands, and capture output. This is auto-detected at startup: tmux tools are only registered when a compatible binary (`tmux` on Linux/macOS, `psmux` on Windows) is found in PATH. If tmux is not installed, everything else works as normal.

### Why tmux tools

The `Bash` tool has a hard timeout (~30–120 s). Long-running tasks — training runs, servers, package builds, log monitors — get killed before they finish. With tmux tools, the AI sends the command to a **visible pane** that outlives any timeout, then uses `TmuxCapture` to read the output and react.

### Tools

| Tool | What it does |
|---|---|
| `TmuxListSessions` | List all active sessions |
| `TmuxNewSession` | Create a new session (use `detached=true` for background) |
| `TmuxNewWindow` | Add a visible tab inside an existing session |
| `TmuxSplitWindow` | Split the current pane vertically or horizontally |
| `TmuxSendKeys` | Send a command/keystrokes to any pane |
| `TmuxCapture` | Read visible text output from a pane |
| `TmuxListPanes` | List panes with index, size, and active status |
| `TmuxSelectPane` | Switch focus to a specific pane |
| `TmuxKillPane` | Close a pane |
| `TmuxListWindows` | List windows in a session |
| `TmuxResizePane` | Resize a pane (up/down/left/right) |

### Quick start

**Run a training script in a visible window:**
```
[cheetahclaws] » Open a new tmux window and run python train.py so I can watch the output
```
The AI will call `TmuxNewWindow` → `TmuxSendKeys("python train.py")`. A new tab opens immediately and you watch the output live.

**Check training progress:**
```
[cheetahclaws] » Check what the training window is printing now — has the loss gone down?
```
The AI calls `TmuxListPanes` to locate the pane, then `TmuxCapture` to read the last 50 lines and summarise.

**Split screen: server on the left, tests on the right:**
```
[cheetahclaws] » Run uvicorn main:app on the left and pytest on the right, split screen
```
The AI calls `TmuxSplitWindow(direction=horizontal)`, then `TmuxSendKeys` to each pane.

**Launch vLLM in a detached background session:**
```
[cheetahclaws] » Start a background tmux session running vLLM, don't take over this terminal
```
The AI calls `TmuxNewSession(detached=true)` then sends the vLLM launch command to that session.

### Bash tool vs Tmux tools

| | Bash tool | Tmux tools |
|---|---|---|
| Best for | Quick commands (`ls`, `git`, `pip install`) | Long-running tasks, servers, builds, monitors |
| Timeout | ~30–120 s, then killed | Never — runs in its own pane |
| Output | Returned directly to AI | Read on demand via `TmuxCapture` |
| Visibility | Hidden (background) | Visible to user in a real terminal pane |

**Rule of thumb:** use the Bash tool by default. Switch to tmux only when the command would timeout or you want the user to see it running.

---

## Shell Escape

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/shell_escape_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Shell Escape: ! prefix runs commands directly — git, ls, python, pipes — no AI involvement</center>
</div>

Type `!` followed by any shell command to execute it directly without the AI intercepting:

```
[cheetahclaws] » !git status
  $ git status
On branch main
...

[cheetahclaws] » !ls -la
  $ ls -la
...

[cheetahclaws] » !python --version
  $ python --version
Python 3.11.7
```

Output prints inline and control returns to the CheetahClaws prompt immediately. Any valid shell expression works, including pipes: `!cat log.txt | tail -20`.

---

## Proactive Background Monitoring

CheetahClaws v3.05.2 adds a **sentinel daemon** that automatically wakes the agent after a configurable period of inactivity — no user prompt required. This enables use cases like continuous log monitoring, market script polling, or scheduled code checks.

### Quick start

```
[myproject] ❯ /proactive 5m
Proactive background polling: ON  (triggering every 300s of inactivity)

[myproject] ❯ keep monitoring the build log and alert me if errors appear

╭─ Claude ● ─────────────────────────
│ Understood. I'll check the build log each time I wake up.

[Background Event Triggered]
╭─ Claude ● ─────────────────────────
│ ⚙ Bash(tail -50 build.log)
│ ✓ → Build failed: ImportError in auth.py line 42
│ **Action needed:** fix the import before the next CI run.
```

### Commands

| Command | Description |
|---|---|
| `/proactive` | Show current status (ON/OFF and interval) |
| `/proactive 5m` | Enable — trigger every 5 minutes of inactivity |
| `/proactive 30s` | Enable — trigger every 30 seconds |
| `/proactive 1h` | Enable — trigger every hour |
| `/proactive off` | Disable sentinel polling |

Duration suffix: `s` = seconds, `m` = minutes, `h` = hours. Plain integer = seconds.

### How it works

- A background daemon thread starts when the REPL launches (paused by default).
- The daemon checks elapsed time since the last user or agent interaction every second.
- When the inactivity threshold is reached, it calls the agent with a wake-up prompt.
- The `threading.Lock` used by the main agent loop ensures wake-ups never interrupt an active session — they queue and fire after the current turn completes.
- Watcher exceptions are logged via `traceback` so failures are visible and debuggable.

### Complements SleepTimer

| | `SleepTimer` | `/proactive` |
|---|---|---|
| Who initiates | The agent | The user |
| Trigger | After a fixed delay from now | After N seconds of inactivity |
| Use case | "Check back in 10 minutes" | "Keep watching until I stop typing" |

---

## Checkpoint System

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/checkpoint_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Checkpoint / Rewind: AI breaks tests → /checkpoint list → rewind → files restored</center>
</div>

CheetahClaws automatically snapshots your conversation and any edited files after every turn, so you can always rewind to an earlier state.

### How it works

- **Auto-snapshot** — after each turn, the checkpoint system saves the current conversation messages, token counts, and a copy-on-write backup of every file that was written or edited that turn.
- **100-snapshot sliding window** — older snapshots are automatically evicted when the limit is reached.
- **Throttling** — if nothing changed (no new messages, no file edits) since the last snapshot, the snapshot is skipped.
- **Initial snapshot** — captured at session start, so you can always rewind to a clean slate.
- **Storage** — `~/.nano_claude/checkpoints/<session_id>/` (snapshots metadata + backup files).

### Commands

| Command | Description |
|---|---|
| `/checkpoint` | List all snapshots for the current session |
| `/checkpoint <id>` | Rewind: restore files to their state at snapshot `<id>` and trim conversation to that point |
| `/checkpoint clear` | Delete all snapshots for the current session |
| `/rewind` | Alias for `/checkpoint` |

### Example

```
[myproject] ❯ /checkpoint
  Checkpoints (4 total):
  #1  [turn 0] 14:02:11  "(initial state)"           0 files
  #2  [turn 1] 14:03:45  "Create app.py"              1 file
  #3  [turn 2] 14:05:12  "Add error handling"         1 file
  #4  [turn 3] 14:06:30  "Explain the code"           1 file

[myproject] ❯ /checkpoint 2
  Rewound to checkpoint #2 (turn 1)
  Restored: app.py
  Conversation trimmed to 2 messages.
```

---

## Plan Mode

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/plan_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Plan Mode: Read-only analysis → write plan → /plan done → implement</center>
</div>

Plan mode is a structured workflow for tackling complex, multi-file tasks: Claude first analyses the codebase in a read-only phase and writes an explicit plan, then the user approves before implementation begins.

### How it works

In plan mode:
- **Only reads** are permitted (`Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, safe `Bash` commands).
- **Writes are blocked** everywhere **except** the dedicated plan file (`.nano_claude/plans/<session_id>.md`).
- Blocked write attempts produce a helpful message rather than prompting the user.
- The system prompt is augmented with plan mode instructions.
- After compaction, the plan file context is automatically restored.

### Slash command workflow

```
[myproject] ❯ /plan add WebSocket support
  Plan mode activated.
  Plan file: .nano_claude/plans/a3f9c1b2.md
  Reads allowed. All other writes blocked (except plan file).

[myproject] ❯ <describe your task>
  [Claude reads files, builds understanding, writes plan to plan file]

[myproject] ❯ /plan
  # Plan: Add WebSocket support

  ## Phase 1: Create ws_handler.py
  ## Phase 2: Modify server.py to mount the handler
  ## Phase 3: Add tests

[myproject] ❯ /plan done
  Plan mode exited. Permission mode restored to: auto
  Review the plan above and start implementing when ready.

[myproject] ❯ /plan status
  Plan mode: INACTIVE  (permission mode: auto)
```

### Agent tool workflow (autonomous)

Claude can autonomously enter and exit plan mode using the `EnterPlanMode` and `ExitPlanMode` tools — both are auto-approved in all permission modes:

```
User: Refactor the authentication module

Claude: [calls EnterPlanMode(task_description="Refactor auth module")]
  → reads auth.py, users.py, tests/test_auth.py ...
  → writes plan to .nano_claude/plans/...
  [calls ExitPlanMode()]
  → "Here is my plan. Please review and approve before I begin."

User: Looks good, go ahead.
Claude: [implements the plan]
```

### Commands

| Command | Description |
|---|---|
| `/plan <description>` | Enter plan mode with a task description |
| `/plan` | Print the current plan file contents |
| `/plan done` | Exit plan mode, restore previous permissions |
| `/plan status` | Show whether plan mode is active |

---

## Context Compression

Long conversations are automatically compressed to stay within the model's context window.

**Two layers:**

1. **Snip** — Old tool outputs (file reads, bash results) are truncated after a few turns. Fast, no API cost.
2. **Auto-compact** — When token usage exceeds 70% of the context limit, older messages are summarized by the model into a concise recap.

This happens transparently. You don't need to do anything.

**Manual compaction** — You can also trigger compaction at any time with `/compact`. An optional focus string tells the summarizer what context to prioritize:

```
[myproject] ❯ /compact
  Compacted: ~12400 → ~3200 tokens (~9200 saved)

[myproject] ❯ /compact keep the WebSocket implementation details
  Compacted: ~11800 → ~3100 tokens (~8700 saved)
```

If plan mode is active, the plan file context is automatically restored after any compaction.

---

## Diff View

When the model edits or overwrites a file, you see a git-style diff:

```diff
  Changes applied to config.py:

--- a/config.py
+++ b/config.py
@@ -12,7 +12,7 @@
     "model": "claude-opus-4-6",
-    "max_tokens": 8192,
+    "max_tokens": 16384,
     "permission_mode": "auto",
```

Green lines = added, red lines = removed. New file creations show a summary instead.

---

## CLAUDE.md Support

Place a `CLAUDE.md` file in your project to give the model persistent context about your codebase. CheetahClaws automatically finds and injects it into the system prompt.

```
~/.claude/CLAUDE.md          # Global — applies to all projects
/your/project/CLAUDE.md      # Project-level — found by walking up from cwd
```

**Example `CLAUDE.md`:**

```markdown
# Project: FastAPI Backend

## Stack
- Python 3.12, FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic
- Tests: pytest, coverage target 90%

## Conventions
- Format with black, lint with ruff
- Full type annotations required
- New endpoints must have corresponding tests

## Important Notes
- Never hard-code credentials — use environment variables
- Do not modify existing Alembic migration files
- The `staging` branch deploys automatically to staging on push
```

---

## Session Management

### Storage layout

Every exit automatically saves to three places:

```
~/.cheetahclaws/sessions/
├── history.json                          ← master: all sessions ever (capped)
├── mr_sessions/
│   └── session_latest.json              ← always the most recent (/resume)
└── daily/
    ├── 2026-04-05/
    │   ├── session_110523_a3f9.json     ← per-day files, newest kept
    │   └── session_143022_b7c1.json
    └── 2026-04-04/
        └── session_183100_3b4c.json
```

Each session file includes metadata:

```json
{
  "session_id": "a3f9c1b2",
  "saved_at": "2026-04-05 11:05:23",
  "turn_count": 8,
  "messages": [...]
}
```

### Autosave on exit

Every time you exit — via `/exit`, `/quit`, `Ctrl+C`, or `Ctrl+D` — the session is saved automatically:

```
✓ Session saved → /home/.../.cheetahclaws/sessions/mr_sessions/session_latest.json
✓              → /home/.../.cheetahclaws/sessions/daily/2026-04-05/session_110523_a3f9.json  (id: a3f9c1b2)
✓   history.json: 12 sessions / 87 total turns
```

### Quick resume

To continue where you left off:

```bash
cheetahclaws
[myproject] ❯ /resume
✓  Session loaded from …/mr_sessions/session_latest.json (42 messages)
```

Resume a specific file:

```bash
/resume session_latest.json          # loads from mr_sessions/
/resume /absolute/path/to/file.json  # loads from absolute path
```

### Manual save / load

```bash
/save                          # save with auto-name (session_TIMESTAMP_ID.json)
/save debug_auth_bug           # named save to ~/.cheetahclaws/sessions/

/load                          # interactive list grouped by date
/load debug_auth_bug           # load by filename
```

**`/load` interactive list:**

```
  ── 2026-04-05 ──
  [ 1] 11:05:23  id:a3f9c1b2  turns:8   session_110523_a3f9.json
  [ 2] 09:22:01  id:7e2d4f91  turns:3   session_092201_7e2d.json

  ── 2026-04-04 ──
  [ 3] 22:18:00  id:3b4c5d6e  turns:15  session_221800_3b4c.json

  ── Complete History ──
  [ H] Load ALL history  (3 sessions / 26 total turns)  /home/.../.cheetahclaws/sessions/history.json

  Enter number(s) (e.g. 1 or 1,2,3), H for full history, or Enter to cancel >
```

- Enter a single number to load one session
- Enter comma-separated numbers (e.g. `1,3`) to merge multiple sessions in order
- Enter `H` to load the entire history — shows message count and token estimate before confirming

### Configurable limits

| Config key | Default | Description |
|---|---|---|
| `session_daily_limit` | `5` | Max session files kept per day in `daily/` |
| `session_history_limit` | `100` | Max sessions kept in `history.json` |

```bash
/config session_daily_limit=10
/config session_history_limit=200
```

### history.json — full conversation history

`history.json` accumulates every session in one place, making it possible to search your complete conversation history or analyze usage patterns:

```json
{
  "total_turns": 150,
  "sessions": [
    {"session_id": "a3f9c1b2", "saved_at": "2026-04-05 11:05:23", "turn_count": 8, "messages": [...]},
    {"session_id": "7e2d4f91", "saved_at": "2026-04-05 09:22:01", "turn_count": 3, "messages": [...]}
  ]
}
```

---

## Cloud Sync (GitHub Gist)

<div align=center>
<img src="https://github.com/SafeRL-Lab/cheetahclaws/blob/main/docs/cloudsave_demo.gif" width="850"/>
</div>
<div align=center>
<center style="color:#000000;text-decoration:underline">Cloud Sync: /cloudsave on desktop → encrypted upload → /cloudload on laptop → full session restored</center>
</div>

CheetahClaws v3.05.3 adds optional cloud backup of conversation sessions via **GitHub Gist**. Sessions are stored as private Gists (JSON), browsable in the GitHub UI. No extra dependencies — uses Python's stdlib `urllib`.

### Setup (one-time)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) → **Generate new token (classic)**
2. Enable the **`gist`** scope
3. Copy the token and run:

```
[myproject] ❯ /cloudsave setup ghp_xxxxxxxxxxxxxxxxxxxx
✓ GitHub token saved (logged in as: Chauncygu). Cloud sync is ready.
```

### Upload a session

```
[myproject] ❯ /cloudsave
Uploading session to GitHub Gist…
✓ Session uploaded → https://gist.github.com/abc123def456
```

Add an optional description:

```
[myproject] ❯ /cloudsave push auth refactor debug session
```

### Auto-sync on exit

```
[myproject] ❯ /cloudsave auto on
✓ Auto cloud-sync ON — session will be uploaded to Gist on /exit.
```

From that point on, every `/exit` or `/quit` automatically uploads the session before closing.

### Browse and restore

```
[myproject] ❯ /cloudsave list
  Found 3 session(s):
  abc123de…  2026-04-05 11:02  auth refactor debug session
  7f9e12ab…  2026-04-04 22:18  proactive monitoring test
  3b4c5d6e…  2026-04-04 18:31

[myproject] ❯ /cloudsave load abc123de...full-gist-id...
✓ Session loaded from Gist (42 messages).
```

### Commands reference

| Command | Description |
|---|---|
| `/cloudsave setup <token>` | Save GitHub token (needs `gist` scope) |
| `/cloudsave` | Upload current session to a new or existing Gist |
| `/cloudsave push [desc]` | Upload with optional description |
| `/cloudsave auto on\|off` | Toggle auto-upload on exit |
| `/cloudsave list` | List all cheetahclaws Gists |
| `/cloudsave load <gist_id>` | Download and restore a session |

---

## Project Structure

```
cheetahclaws/
├── cheetahclaws.py        # Entry point: REPL loop, readline setup, diff rendering, Rich Live streaming, proactive sentinel daemon, auto-start bridge wiring
├── runtime.py             # RuntimeContext singleton — live session references (run_query, handle_slash, agent_state, tg/slack/wx send + input events) shared across all modules without polluting the config dict
├── agent.py              # Agent loop: streaming, tool dispatch, compaction
├── providers.py          # Multi-provider: Anthropic, OpenAI-compat streaming
├── tools.py              # Core tools (Read/Write/Edit/Bash/Glob/Grep/Web/NotebookEdit/GetDiagnostics) + registry wiring
├── tool_registry.py      # Tool plugin registry: register, lookup, execute
├── compaction.py         # Context compression: snip + auto-summarize
├── context.py            # System prompt builder: CLAUDE.md + git + memory
├── config.py             # Config load/save/defaults; DAILY_DIR, SESSION_HIST_FILE paths
├── cloudsave.py          # GitHub Gist cloud sync (upload/download/list sessions)
│
├── ui/                   # Terminal output package
│   └── render.py         # ANSI helpers (clr/info/ok/warn/err), Rich Live Markdown renderer, spinner phrases
│
├── bridges/              # Messaging bridge package
│   ├── telegram.py       # Telegram Bot API bridge: long-poll loop, slash passthrough, input routing, typing indicator
│   ├── wechat.py         # WeChat iLink bridge: long-poll loop, context_token, typing indicator, session recovery
│   └── slack.py          # Slack Web API bridge: conversation.history poll, in-place reply update, slash passthrough
│
├── commands/             # Slash-command handlers package
│   ├── session.py        # /save /load /resume /export /copy /history
│   ├── config_cmd.py     # /config /status /doctor
│   ├── core.py           # /clear /compact /cost /verbose /thinking /image /model /init
│   ├── checkpoint_plan.py# /checkpoint /rewind /plan
│   └── advanced.py       # /brainstorm /worker /ssj /proactive /tasks /agents /skills /memory /mcp /plugin /voice /tts /video
│
├── multi_agent/          # Multi-agent package
│   ├── __init__.py       # Re-exports
│   ├── subagent.py       # AgentDefinition, SubAgentManager, worktree helpers
│   └── tools.py          # Agent, SendMessage, CheckAgentResult, ListAgentTasks, ListAgentTypes
├── subagent.py           # Backward-compat shim → multi_agent/
│
├── memory/               # Memory package
│   ├── __init__.py       # Re-exports
│   ├── types.py          # MEMORY_TYPES and format guidance
│   ├── store.py          # save/load/delete/search, MEMORY.md index rebuilding
│   ├── scan.py           # MemoryHeader, age/freshness helpers
│   ├── context.py        # get_memory_context(), truncation, AI search
│   └── tools.py          # MemorySave, MemoryDelete, MemorySearch, MemoryList
├── memory.py             # Backward-compat shim → memory/
│
├── skill/                # Skill package
│   ├── __init__.py       # Re-exports; imports builtin to register built-ins
│   ├── loader.py         # SkillDef, parse, load_skills, find_skill, substitute_arguments
│   ├── builtin.py        # Built-in skills: /commit, /review
│   ├── executor.py       # execute_skill(): inline or forked sub-agent
│   └── tools.py          # Skill, SkillList
├── skills.py             # Backward-compat shim → skill/
│
├── mcp/                  # MCP (Model Context Protocol) package
│   ├── __init__.py       # Re-exports
│   ├── types.py          # MCPServerConfig, MCPTool, MCPServerState, JSON-RPC helpers
│   ├── client.py         # StdioTransport, HttpTransport, MCPClient, MCPManager
│   ├── config.py         # Load .mcp.json (project) + ~/.cheetahclaws/mcp.json (user)
│   └── tools.py          # Auto-discover + register MCP tools into tool_registry
│
├── voice/                # Voice input package (v3.05) — backward-compat shim → modular/voice/
│   └── __init__.py       # Re-exports from modular.voice.*
│
├── video/                # Video package — backward-compat shim → modular/video/
│   └── __init__.py       # Re-exports from modular.video.*
│
├── modular/              # Plug-and-play module ecosystem (v3.05.55)
│   ├── __init__.py       # Auto-discovery registry: load_all_commands(), load_all_tools(), list_modules()
│   ├── base.py           # HasCommandDefs / HasToolDefs Protocol interface docs
│   ├── voice/            # Voice submodule (self-contained)
│   │   ├── __init__.py   # Public API: check_voice_deps, voice_input, list_input_devices
│   │   ├── cmd.py        # /voice + /tts commands; COMMAND_DEFS plug-in interface
│   │   ├── recorder.py   # Audio capture: sounddevice → arecord → sox rec
│   │   ├── stt.py        # STT: faster-whisper → openai-whisper → OpenAI API
│   │   ├── keyterms.py   # Coding-domain vocab from git branch + project files
│   │   └── tts_gen.py    # TTS pipeline: style presets, AI text gen, synthesis, run_tts_pipeline()
│   └── video/            # Video submodule (self-contained)
│       ├── __init__.py   # Re-exports
│       ├── cmd.py        # /video command; COMMAND_DEFS plug-in interface
│       ├── pipeline.py   # Full video assembly: story → TTS → images → subtitles → mp4
│       ├── story.py      # AI story generation + niche prompts
│       ├── tts.py        # TTS backends: Gemini → ElevenLabs → Edge; CJK auto-voice; chunking
│       ├── images.py     # Image backends: Gemini Web → web-search → placeholder
│       └── subtitles.py  # PIL subtitle renderer + text-to-SRT conversion
│
├── checkpoint/           # Checkpoint system (v3.05.6)
│   ├── __init__.py       # Public API exports
│   ├── types.py          # FileBackup + Snapshot dataclasses; MAX_SNAPSHOTS = 100
│   ├── store.py          # File-level backup, snapshot persistence, rewind, cleanup
│   └── hooks.py          # Write/Edit/NotebookEdit interception — backs up files before modification
│
└── tests/                # 267+ unit tests
    ├── test_mcp.py
    ├── test_memory.py
    ├── test_skills.py
    ├── test_subagent.py
    ├── test_tool_registry.py
    ├── test_compaction.py
    ├── test_diff_view.py
    ├── test_voice.py         # 29 voice tests (no hardware required)
    ├── test_checkpoint.py    # 24 checkpoint unit tests
    ├── e2e_checkpoint.py     # 10-step checkpoint lifecycle test
    ├── e2e_plan_mode.py      # 10-step plan mode permission test
    ├── e2e_plan_tools.py     # 8-step EnterPlanMode/ExitPlanMode tool test
    ├── e2e_compact.py        # 9-step compaction test
    └── e2e_commands.py       # 9-step /init /export /copy /status test
```

> **For developers:** The codebase is organized into clear layers: `runtime.py` holds live cross-module state; `ui/render.py` provides all terminal output helpers; `bridges/` contains each messaging integration; `commands/` contains REPL slash-command handlers; feature packages (`multi_agent/`, `memory/`, `skill/`, `mcp/`, `checkpoint/`) are self-contained. Add custom tools by calling `register_tool(ToolDef(...))` from any module imported by `tools.py`. To add a new plug-and-play module to the ecosystem, create `modular/<name>/cmd.py` exporting `COMMAND_DEFS = {"cmdname": {"func": callable, "help": ..., "aliases": []}}` — it is auto-discovered at startup with no registration step.

---

## FAQ

**Q: How do I add an MCP server?**

Option 1 — via REPL (stdio server):
```
/mcp add git uvx mcp-server-git
```

Option 2 — create `.mcp.json` in your project:
```json
{
  "mcpServers": {
    "git": {"type": "stdio", "command": "uvx", "args": ["mcp-server-git"]}
  }
}
```

Then run `/mcp reload` or restart. Use `/mcp` to check connection status.

**Q: An MCP server is showing an error. How do I debug it?**

```
/mcp                    # shows error message per server
/mcp reload git         # try reconnecting
```

If the server uses stdio, make sure the command is in your `$PATH`:
```bash
which uvx               # should print a path
uvx mcp-server-git      # run manually to see errors
```

**Q: Can I use MCP servers that require authentication?**

For HTTP/SSE servers with a Bearer token:
```json
{
  "mcpServers": {
    "my-api": {
      "type": "sse",
      "url": "https://myserver.example.com/sse",
      "headers": {"Authorization": "Bearer sk-my-token"}
    }
  }
}
```

For stdio servers with env-based auth:
```json
{
  "mcpServers": {
    "brave": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-brave-search"],
      "env": {"BRAVE_API_KEY": "your-key"}
    }
  }
}
```

**Q: Tool calls don't work with my local Ollama model.**

Not all models support function calling. Use one of the recommended tool-calling models: `qwen2.5-coder`, `llama3.3`, `mistral`, or `phi4`.

```bash
ollama pull qwen2.5-coder
cheetahclaws --model ollama/qwen2.5-coder
```

**Q: How do I connect to a remote GPU server running vLLM?**

```
/config custom_base_url=http://your-server-ip:8000/v1
/config custom_api_key=your-token
/model custom/your-model-name
```

**Q: How do I check my API cost?**

```
/cost

  Input tokens:  3,421
  Output tokens:   892
  Est. cost:     $0.0648 USD
```

**Q: Can I use multiple API keys in the same session?**

Yes. Set all the keys you need upfront (via env vars or `/config`). Then switch models freely — each call uses the key for the active provider.

**Q: How do I make a model available across all projects?**

Add keys to `~/.bashrc` or `~/.zshrc`. Set the default model in `~/.cheetahclaws/config.json`:

```json
{ "model": "claude-sonnet-4-6" }
```

**Q: Qwen / Zhipu returns garbled text.**

Ensure your `DASHSCOPE_API_KEY` / `ZHIPU_API_KEY` is correct and the account has sufficient quota. Both providers use UTF-8 and handle Chinese well.

**Q: Can I pipe input to cheetahclaws?**

```bash
echo "Explain this file" | cheetahclaws --print --accept-all
cat error.log | cheetahclaws -p "What is causing this error?"
```

**Q: How do I run it as a CLI tool from anywhere?**

Use `uv tool install` — it creates an isolated environment and puts `cheetahclaws` on your PATH:

```bash
cd cheetahclaws
uv tool install .
```

After that, just run `cheetahclaws` from any directory. To update after pulling changes, run `uv tool install . --reinstall`.

**Q: How do I set up voice input?**

```bash
# Minimal setup (local, offline, no API key):
pip install sounddevice faster-whisper numpy

# Then in the REPL:
/voice status          # verify backends are detected
/voice                 # speak your prompt
```

On first use, `faster-whisper` downloads the `base` model (~150 MB) automatically.
Use a larger model for better accuracy: `export NANO_CLAUDE_WHISPER_MODEL=small`

**Q: Voice input transcribes my words wrong (misses coding terms).**

The keyterm booster already injects coding vocabulary from your git branch and project files.
For persistent domain terms, put them in a `.cheetahclaws/voice_keyterms.txt` file (one term per line) — this is checked automatically on each recording.

**Q: Can I use voice input in Chinese / Japanese / other languages?**

Yes. Set the language before recording:

```
/voice lang zh    # Mandarin Chinese
/voice lang ja    # Japanese
/voice lang auto  # reset to auto-detect (default)
```

Whisper supports 99 languages. `auto` detection works well but explicit codes improve accuracy for short utterances.



## Citation
If you find the repository useful, please cite the study
``` Bash
@article{cheetahclaws2026,
  title={CheetahClaws: An Extensible, Python-Native Agent System for Autonomous Multi-Model Workflows},
  author={CheetahClaws Team},
  journal={github},
  year={2026}
}
```

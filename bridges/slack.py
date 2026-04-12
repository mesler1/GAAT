"""
bridges/slack.py — Slack Web API bridge for CheetahClaws.

Setup:
  1. Create a Slack App at https://api.slack.com/apps
  2. Add Bot Token Scopes: channels:history, chat:write, groups:history,
     im:history, mpim:history, channels:read
  3. Install app to workspace → copy Bot User OAuth Token (xoxb-...)
  4. Invite the bot to the target channel: /invite @<bot_name>
  5. Run /slack <token> <channel_id>
"""
from __future__ import annotations

import json
import threading

from ui.render import clr, info, ok, warn, err
import runtime
import logging_utils as _log

_slack_thread: threading.Thread | None = None
_slack_stop   = threading.Event()

_SLACK_API_BASE      = "https://slack.com/api"
_SLACK_POLL_INTERVAL = 2
_SLACK_API_TIMEOUT   = 15
_SLACK_MAX_SEEN      = 2000
_slack_seen_ts: set[str] = set()


# ── HTTP helpers ───────────────────────────────────────────────────────────

def _slack_api(token: str, method: str, params: dict | None = None, *,
               timeout: int = _SLACK_API_TIMEOUT) -> dict | None:
    import urllib.request, urllib.parse
    url = f"{_SLACK_API_BASE}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None

def _slack_post(token: str, method: str, payload: dict, *,
                timeout: int = _SLACK_API_TIMEOUT) -> dict | None:
    import urllib.request
    url = f"{_SLACK_API_BASE}/{method}"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None

def _slack_send(token: str, channel: str, text: str) -> None:
    _slack_post(token, "chat.postMessage", {"channel": channel, "text": text})


# ── Poll loop ──────────────────────────────────────────────────────────────

def _slack_poll_loop(token: str, channel: str, config: dict) -> str:
    """Returns "stopped", "auth_error", or raises on unexpected fatal error."""
    from tools import _slack_thread_local
    session_ctx = runtime.get_session_ctx(config.get("_session_id", "default"))
    run_query_cb = session_ctx.run_query

    session_ctx.slack_send = lambda ch, txt: _slack_send(token, ch, txt)
    _slack_send(token, channel, "🟢 cheetahclaws is online. Send me a message and I'll process it.")

    import time as _time
    oldest = str(_time.time())
    consecutive_failures = 0

    while not _slack_stop.is_set():
        _slack_stop.wait(_SLACK_POLL_INTERVAL)
        if _slack_stop.is_set():
            break

        try:
            result = _slack_api(token, "conversations.history", {
                "channel": channel,
                "oldest": oldest,
                "limit": 20,
            })

            if result is None:
                consecutive_failures += 1
                if consecutive_failures >= 5:
                    print(clr("\n  ⚠ Slack: repeated connection failures, retrying in 30s...", "yellow"))
                    _slack_stop.wait(30)
                    consecutive_failures = 0
                continue
            consecutive_failures = 0

            if not result.get("ok"):
                slack_err = result.get("error", "unknown")
                if slack_err in ("invalid_auth", "token_revoked", "account_inactive"):
                    print(clr(f"\n  ⚠ Slack: auth error ({slack_err}) — use /slack logout and reconnect", "yellow"))
                    _log.warn("bridge_auth_error", bridge="slack", error=slack_err)
                    session_ctx.slack_send = None
                    return "auth_error"
                print(clr(f"\n  ⚠ Slack: API error {slack_err}, retrying...", "yellow"))
                _slack_stop.wait(5)
                continue

            messages = list(reversed(result.get("messages") or []))

            for msg in messages:
                ts = msg.get("ts", "")
                if not ts:
                    continue
                if ts > oldest:
                    oldest = ts
                if ts in _slack_seen_ts:
                    continue
                _slack_seen_ts.add(ts)
                if len(_slack_seen_ts) > _SLACK_MAX_SEEN:
                    oldest_keys = sorted(_slack_seen_ts)[:500]
                    for k in oldest_keys:
                        _slack_seen_ts.discard(k)

                if msg.get("bot_id") or msg.get("subtype"):
                    continue

                text = (msg.get("text") or "").strip()
                if not text:
                    continue

                user_id = msg.get("user", "unknown")
                print(clr(f"\n  📩 Slack [{user_id[:8]}]: {text}", "cyan"))

                evt = session_ctx.slack_input_event
                if evt:
                    session_ctx.slack_input_value = text
                    evt.set()
                    continue

                if text.strip().lower() in ("/stop", "/off"):
                    _slack_send(token, channel, "🔴 cheetahclaws bridge stopped.")
                    _slack_stop.set()
                    break

                if text.strip().lower() == "/start":
                    _slack_send(token, channel, "🟢 cheetahclaws bridge is active. Send me anything.")
                    continue

                if text.strip().startswith("/"):
                    slash_cb = session_ctx.handle_slash
                    if slash_cb:
                        def _slack_slash_runner(_slash_text, _ch):
                            _slack_thread_local.active = True
                            config["_slack_current_channel"] = _ch
                            try:
                                cmd_type = slash_cb(_slash_text)
                            except Exception as e:
                                _slack_send(token, _ch, f"⚠ Error: {e}")
                                return
                            finally:
                                _slack_thread_local.active = False
                                config.pop("_slack_current_channel", None)
                            if cmd_type == "simple":
                                cmd_name = _slash_text.strip().split()[0]
                                _slack_send(token, _ch, f"✅ {cmd_name} executed.")
                                return
                            slack_state = session_ctx.agent_state
                            if slack_state and slack_state.messages:
                                for m in reversed(slack_state.messages):
                                    if m.get("role") == "assistant":
                                        content = m.get("content", "")
                                        if isinstance(content, list):
                                            parts = [
                                                b.get("text", "") if isinstance(b, dict) and b.get("type") == "text"
                                                else (b if isinstance(b, str) else "")
                                                for b in content
                                            ]
                                            content = "\n".join(p for p in parts if p)
                                        if content:
                                            _slack_send(token, _ch, content)
                                        break
                        threading.Thread(
                            target=_slack_slash_runner, args=(text, channel), daemon=True
                        ).start()
                    continue

                def _slack_bg_runner(q_text, ch):
                    think_resp = _slack_post(token, "chat.postMessage", {
                        "channel": ch, "text": "⏳ Thinking…"
                    })
                    think_ts = (think_resp or {}).get("ts") if think_resp and think_resp.get("ok") else None

                    config["_slack_current_channel"] = ch
                    config["_in_slack_turn"] = True
                    try:
                        if run_query_cb:
                            run_query_cb(q_text)
                    except Exception as e:
                        _slack_send(token, ch, f"⚠ Error: {e}")
                        return
                    finally:
                        config.pop("_in_slack_turn", None)
                        config.pop("_slack_current_channel", None)

                    reply = ""
                    state = session_ctx.agent_state
                    if state and state.messages:
                        for m in reversed(state.messages):
                            if m.get("role") == "assistant":
                                content = m.get("content", "")
                                if isinstance(content, list):
                                    parts = [
                                        b.get("text", "") if isinstance(b, dict) and b.get("type") == "text"
                                        else (b if isinstance(b, str) else "")
                                        for b in content
                                    ]
                                    content = "\n".join(p for p in parts if p)
                                reply = content
                                break

                    if reply:
                        if think_ts:
                            upd = _slack_post(token, "chat.update", {
                                "channel": ch, "ts": think_ts, "text": reply
                            })
                            if not (upd and upd.get("ok")):
                                _slack_send(token, ch, reply)
                        else:
                            _slack_send(token, ch, reply)
                        print(clr(f"  ✈  Slack response sent → {reply[:60]}…", "cyan"))

                threading.Thread(target=_slack_bg_runner, args=(text, channel), daemon=True).start()

        except Exception:
            _slack_stop.wait(5)

    session_ctx.slack_send = None
    return "stopped"


_SLACK_BACKOFF_INITIAL = 2.0
_SLACK_BACKOFF_MAX     = 120.0


def _slack_supervisor(token: str, channel: str, config: dict) -> None:
    """Wrap _slack_poll_loop with exponential-backoff reconnect on unexpected exit."""
    global _slack_thread
    backoff = _SLACK_BACKOFF_INITIAL
    attempt = 0
    while not _slack_stop.is_set():
        attempt += 1
        try:
            reason = _slack_poll_loop(token, channel, config)
        except Exception as exc:
            if _slack_stop.is_set():
                break
            _log.warn("bridge_crash", bridge="slack", attempt=attempt,
                      error=str(exc)[:200], backoff_s=backoff)
            print(clr(f"\n  ⚠ Slack bridge crashed (attempt {attempt}), "
                      f"reconnecting in {backoff:.0f}s…", "yellow"))
            _slack_stop.wait(backoff)
            backoff = min(backoff * 2, _SLACK_BACKOFF_MAX)
            continue

        if reason == "auth_error":
            print(clr("\n  ⚠ Slack: invalid token — stopping bridge. Use /slack logout.", "yellow"))
            _log.warn("bridge_auth_error_stop", bridge="slack")
            break
        break

    _slack_thread = None


def _slack_start_bridge(config) -> None:
    global _slack_thread, _slack_stop
    token   = config.get("slack_token", "")
    channel = config.get("slack_channel", "")
    _slack_stop = threading.Event()
    _slack_thread = threading.Thread(
        target=_slack_supervisor, args=(token, channel, config), daemon=True,
        name="slack-bridge"
    )
    _slack_thread.start()
    ok("Slack bridge started.")
    info("Send a message in the configured Slack channel — it will be processed here.")
    info("Stop with /slack stop or send /stop in Slack.")


# ── Slash command ──────────────────────────────────────────────────────────

def cmd_slack(args: str, _state, config) -> bool:
    """Slack bot bridge — receive and respond to messages via Slack Web API.

    Usage:
      /slack <token> <channel_id>  — configure and start bridge
      /slack                       — start with saved credentials
      /slack stop                  — stop the bridge
      /slack status                — show current status
      /slack logout                — clear saved credentials
    """
    global _slack_thread, _slack_stop
    from config import save_config

    parts = args.strip().split()

    if parts and parts[0].lower() in ("stop", "off"):
        if _slack_thread and _slack_thread.is_alive():
            _slack_stop.set()
            _slack_thread.join(timeout=5)
            _slack_thread = None
            ok("Slack bridge stopped.")
        else:
            warn("Slack bridge is not running.")
        return True

    if parts and parts[0].lower() == "status":
        running = _slack_thread and _slack_thread.is_alive()
        token   = config.get("slack_token", "")
        channel = config.get("slack_channel", "")
        if running:
            ok(f"Slack bridge running  (channel: {channel})")
        elif token:
            info("Configured but not running. Use /slack to start.")
        else:
            info("Not configured. Use: /slack <token> <channel_id>")
        return True

    if parts and parts[0].lower() == "logout":
        if _slack_thread and _slack_thread.is_alive():
            _slack_stop.set()
            _slack_thread.join(timeout=5)
            _slack_thread = None
        config.pop("slack_token", None)
        config.pop("slack_channel", None)
        save_config(config)
        ok("Slack credentials cleared.")
        return True

    if len(parts) >= 2 and parts[0].startswith("xoxb-"):
        token, channel = parts[0], parts[1]
        if _slack_thread and _slack_thread.is_alive():
            _slack_stop.set()
            _slack_thread.join(timeout=5)
            _slack_thread = None
        config["slack_token"]   = token
        config["slack_channel"] = channel
        save_config(config)
        info(f"Slack credentials saved (channel: {channel}).")
        _slack_start_bridge(config)
        return True

    if _slack_thread and _slack_thread.is_alive():
        warn("Slack bridge is already running. Use /slack stop first.")
        return True

    token   = config.get("slack_token", "")
    channel = config.get("slack_channel", "")
    if not token or not channel:
        warn("No saved credentials. Usage: /slack <xoxb-token> <channel_id>")
        info("Get your token at https://api.slack.com/apps → OAuth & Permissions")
        return True

    me = _slack_api(token, "auth.test")
    if me is None or not me.get("ok"):
        slack_err = (me or {}).get("error", "connection failed")
        if slack_err in ("invalid_auth", "token_revoked"):
            warn(f"Slack token invalid ({slack_err}). Clear with /slack logout.")
            config.pop("slack_token", None)
            config.pop("slack_channel", None)
            save_config(config)
        else:
            warn(f"Slack auth check failed: {slack_err}. Retrying at next poll.")
        return True

    bot_name = me.get("user", "bot")
    info(f"Slack authenticated as @{bot_name}")
    _slack_start_bridge(config)
    return True

"""
runtime.py — Live session context for CheetahClaws.

Holds the object references that were previously stuffed into the config dict
under underscore-prefixed keys (_run_query_callback, _handle_slash_callback,
_state, _tg_send_callback).  There is exactly one RuntimeContext per process.

Bridges, tools, and the proactive watcher all reach these via the module-level
`ctx` singleton — no function-signature changes required in call sites.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agent import AgentState


@dataclass
class RuntimeContext:
    """Live references wired up when the REPL starts.  Not persisted to disk."""

    # Fire a background query from any thread (set by repl())
    run_query: Optional[Callable[[str], None]] = None

    # Process a /slash command coming in from a bridge (set by repl())
    handle_slash: Optional[Callable[[str], str]] = None

    # The active AgentState — message history, token counts, turn count
    agent_state: Optional["AgentState"] = None

    # Low-level Telegram send helper (from bridges.telegram._tg_send)
    tg_send: Optional[Callable] = None

    # Low-level Slack send helper: (channel, text) → None  (set by _slack_poll_loop)
    slack_send: Optional[Callable] = None

    # Low-level WeChat send helper: (user_id, text) → None  (set by _wx_poll_loop)
    wx_send: Optional[Callable] = None

    # Per-bridge synchronous-input synchronisation.
    # ask_input_interactive() sets the event, the poll loop fires it with the
    # user-supplied text.  Using runtime.ctx keeps these out of the config dict
    # and makes the coupling between tools.py and each bridge explicit.
    tg_input_event:    Optional[threading.Event] = None
    tg_input_value:    str = ""
    slack_input_event: Optional[threading.Event] = None
    slack_input_value: str = ""
    wx_input_event:    Optional[threading.Event] = None
    wx_input_value:    str = ""


# ── Module-level singleton ─────────────────────────────────────────────────
# One process → one REPL → one ctx.  Reset between test runs if needed.
ctx = RuntimeContext()

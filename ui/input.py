"""prompt_toolkit-based REPL input with typing-time slash-command autosuggest.

Falls back silently when prompt_toolkit is not installed (HAS_PROMPT_TOOLKIT is
then False), letting the existing readline path in cheetahclaws._read_input
handle input.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.formatted_text import ANSI
    from prompt_toolkit.history import FileHistory, InMemoryHistory
    from prompt_toolkit.patch_stdout import patch_stdout
    from prompt_toolkit.styles import Style
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False


class SlashCompleter(Completer if HAS_PROMPT_TOOLKIT else object):
    """Two-level completer for slash commands.

    Level 1: /partial  (no space) → command names.
    Level 2: /cmd partial          → subcommands listed in _CMD_META.

    Sources:
      - Live COMMANDS dict from cheetahclaws (includes modular/plugin additions).
      - _CMD_META for description + subcommand hints.
    """

    def __init__(
        self,
        commands_provider: Callable[[], dict],
        meta_provider: Callable[[], dict],
    ):
        self._commands_provider = commands_provider
        self._meta_provider = meta_provider
        self._cache_key: Optional[tuple] = None
        self._cache_names: list[str] = []

    def _live_command_names(self) -> list[str]:
        cmds = self._commands_provider() or {}
        meta = self._meta_provider() or {}
        keys = sorted(set(cmds.keys()) | set(meta.keys()))
        sig = (len(keys), tuple(keys[:8]))
        if self._cache_key == sig:
            return self._cache_names
        self._cache_key = sig
        self._cache_names = keys
        return keys

    def get_completions(self, document, complete_event):  # type: ignore[override]
        text = document.text_before_cursor
        if not text.startswith("/"):
            return

        meta = self._meta_provider() or {}

        if " " not in text:
            word = text[1:]
            for name in self._live_command_names():
                if not name.startswith(word):
                    continue
                desc, subs = meta.get(name, ("", []))
                hint = ""
                if subs:
                    head = ", ".join(subs[:3])
                    more = "…" if len(subs) > 3 else ""
                    hint = f"  [{head}{more}]"
                yield Completion(
                    "/" + name,
                    start_position=-len(text),
                    display=ANSI(f"\x1b[36m/{name}\x1b[0m"),
                    display_meta=(desc + hint) if desc else hint.strip(),
                )
            return

        head, _, tail = text.partition(" ")
        cmd = head[1:]
        meta_entry = meta.get(cmd)
        if not meta_entry:
            return
        subs = meta_entry[1]
        if not subs:
            return
        partial = tail.rsplit(" ", 1)[-1]
        for sub in subs:
            if sub.startswith(partial):
                yield Completion(
                    sub,
                    start_position=-len(partial),
                    display_meta=f"{cmd} subcommand",
                )


_SESSION = None


def _commands_provider() -> dict:
    import cheetahclaws as _cc
    return getattr(_cc, "COMMANDS", {}) or {}


def _meta_provider() -> dict:
    import cheetahclaws as _cc
    return getattr(_cc, "_CMD_META", {}) or {}


def _build_session(history_path: Optional[Path]):
    if not HAS_PROMPT_TOOLKIT:
        raise RuntimeError("prompt_toolkit is not installed")
    completer = SlashCompleter(_commands_provider, _meta_provider)
    history = FileHistory(str(history_path)) if history_path else InMemoryHistory()
    style = Style.from_dict({
        "completion-menu.completion":         "bg:#222222 #cccccc",
        "completion-menu.completion.current": "bg:#005f87 #ffffff bold",
        "completion-menu.meta.completion":    "bg:#222222 #808080",
        "completion-menu.meta.completion.current": "bg:#005f87 #eeeeee",
        "auto-suggestion":                    "#606060 italic",
    })
    return PromptSession(
        history=history,
        completer=completer,
        auto_suggest=AutoSuggestFromHistory(),
        complete_while_typing=True,
        enable_history_search=False,
        mouse_support=False,
        style=style,
    )


def read_line(prompt_ansi: str, history_path: Optional[Path] = None) -> str:
    """Read one line of input via prompt_toolkit; caches the session across calls."""
    global _SESSION
    if _SESSION is None:
        _SESSION = _build_session(history_path)
    with patch_stdout(raw=True):
        return _SESSION.prompt(ANSI(prompt_ansi))

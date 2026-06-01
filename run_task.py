#!/usr/bin/env python3
"""
run_task.py — Headless one-shot agent task runner.

Calls agent.run() directly — no REPL, no banner, no interactive prompts.
Suitable for CI, automated testing, and scripted use.

Usage:
  python run_task.py "Fix the failing test in tests/test_foo.py"
  python run_task.py "Add type hints to utils.py" --verify "pytest tests/" --cwd /path/to/repo
  python run_task.py "Refactor auth module" --model gpt-4o --timeout 300
  echo "Fix the bug" | python run_task.py -

Exit codes:
  0  Task complete (and --verify passed, if given)
  1  Verify command failed
  2  Agent or configuration error
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

# Ensure repo root is on the path when invoked from another directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="run_task",
        description="Headless one-shot agent task runner.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "task",
        nargs="?",
        help='Task description. Use "-" to read from stdin.',
    )
    p.add_argument(
        "--verify", "-v",
        metavar="CMD",
        help="Shell command to run after the agent finishes. "
             "Exit code 0 = success, non-zero = failure.",
    )
    p.add_argument(
        "--cwd",
        metavar="DIR",
        help="Working directory for the agent and --verify command "
             "(default: current directory).",
    )
    p.add_argument(
        "--model", "-m",
        metavar="MODEL",
        help="Override the configured model.",
    )
    p.add_argument(
        "--timeout", "-t",
        type=float,
        default=600,
        metavar="SECONDS",
        help="Hard timeout for the agent turn in seconds (default: 600).",
    )
    p.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress tool call lines; show only final text output.",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Show thinking blocks and token counts.",
    )
    return p.parse_args()


def _read_task(args: argparse.Namespace) -> str:
    if args.task == "-" or (args.task is None and not sys.stdin.isatty()):
        task = sys.stdin.read().strip()
    elif args.task:
        task = args.task.strip()
    else:
        print("run_task: error: provide a task argument or pipe one via stdin", file=sys.stderr)
        sys.exit(2)
    if not task:
        print("run_task: error: task is empty", file=sys.stderr)
        sys.exit(2)
    return task


def _run_verify(cmd: str, cwd: str | None) -> int:
    """Run the verify command and return its exit code."""
    print(f"\n── verify: {cmd}", flush=True)
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    return result.returncode


def main() -> None:
    args = _parse_args()
    task = _read_task(args)

    # Change directory before anything else so tool paths resolve correctly.
    cwd = None
    if args.cwd:
        cwd = str(Path(args.cwd).resolve())
        os.chdir(cwd)

    # ── Bootstrap ────────────────────────────────────────────────────────────
    from cc_config import load_config
    from bootstrap import bootstrap

    config = load_config()
    bootstrap(config)

    config["permission_mode"] = "accept-all"
    config["_auto_approve"] = True
    if args.model:
        config["model"] = args.model
    if args.verbose:
        config["verbose"] = True

    # ── Build system prompt ──────────────────────────────────────────────────
    from context import build_system_prompt

    system_prompt = build_system_prompt()

    # ── Run agent ────────────────────────────────────────────────────────────
    from agent import AgentState, run, TextChunk, ThinkingChunk, ToolStart, ToolEnd, TurnDone, PermissionRequest

    state = AgentState()
    deadline = time.monotonic() + args.timeout
    agent_error: str | None = None

    print(f"── task: {task[:120]}{'…' if len(task) > 120 else ''}", flush=True)
    if cwd:
        print(f"── cwd:  {cwd}", flush=True)
    print(f"── model: {config['model']}", flush=True)
    print("", flush=True)

    try:
        for event in run(task, state, config, system_prompt):
            if time.monotonic() > deadline:
                agent_error = f"Timeout after {args.timeout}s"
                break

            if isinstance(event, TextChunk):
                print(event.text, end="", flush=True)

            elif isinstance(event, ThinkingChunk):
                if args.verbose:
                    print(f"[thinking] {event.text}", flush=True)

            elif isinstance(event, ToolStart):
                if not args.quiet:
                    preview = str(
                        (event.inputs or {}).get("command",
                         (event.inputs or {}).get("file_path",
                          (event.inputs or {}).get("prompt", "")))
                    ).strip().replace("\n", " ")[:80]
                    print(f"\n── {event.name}: {preview}", flush=True)

            elif isinstance(event, ToolEnd):
                pass  # result visible via next TextChunk if model echoes it

            elif isinstance(event, PermissionRequest):
                # Should not occur with accept-all, but grant defensively.
                event.granted = True

            elif isinstance(event, TurnDone):
                break

    except KeyboardInterrupt:
        print("\nrun_task: interrupted", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        agent_error = str(exc)

    print("", flush=True)  # ensure final newline

    if agent_error:
        print(f"run_task: agent error: {agent_error}", file=sys.stderr)
        sys.exit(2)

    # ── Verify ───────────────────────────────────────────────────────────────
    if args.verify:
        rc = _run_verify(args.verify, cwd)
        if rc != 0:
            print(f"run_task: verify failed (exit {rc})", file=sys.stderr)
            sys.exit(1)
        print("run_task: verify passed", flush=True)

    sys.exit(0)


if __name__ == "__main__":
    main()

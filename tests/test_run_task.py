"""Tests for run_task.py — headless one-shot task runner."""
from __future__ import annotations

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

RUN_TASK = str(Path(__file__).resolve().parent.parent / "run_task.py")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _fake_agent_run(task, state, config, system_prompt, **kwargs):
    """Mock agent.run() that yields a TextChunk then TurnDone without an API call."""
    from agent import TextChunk, TurnDone
    yield TextChunk(text=f"Task received: {task}")
    yield TurnDone(input_tokens=10, output_tokens=5)


def _import_run_task():
    import importlib.util
    spec = importlib.util.spec_from_file_location("run_task", RUN_TASK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Unit tests (patch agent.run) ─────────────────────────────────────────────

class TestReadTask:
    def test_task_from_arg(self):
        mod = _import_run_task()
        ns = MagicMock(task="fix the bug", cwd=None)
        assert mod._read_task(ns) == "fix the bug"

    def test_task_stdin_dash(self, monkeypatch):
        mod = _import_run_task()
        monkeypatch.setattr("sys.stdin", MagicMock(read=lambda: "  stdin task  ", isatty=lambda: False))
        ns = MagicMock(task="-", cwd=None)
        assert mod._read_task(ns) == "stdin task"

    def test_empty_task_exits(self):
        mod = _import_run_task()
        ns = MagicMock(task="   ", cwd=None)
        with pytest.raises(SystemExit) as exc:
            mod._read_task(ns)
        assert exc.value.code == 2


class TestRunVerify:
    def test_passing_verify(self, tmp_path):
        mod = _import_run_task()
        rc = mod._run_verify("exit 0", str(tmp_path))
        assert rc == 0

    def test_failing_verify(self, tmp_path):
        mod = _import_run_task()
        rc = mod._run_verify("exit 1", str(tmp_path))
        assert rc == 1

    def test_verify_in_cwd(self, tmp_path):
        # Verify command runs in the given cwd — file created there is visible
        mod = _import_run_task()
        target = tmp_path / "marker.txt"
        rc = mod._run_verify(f"touch {target}", str(tmp_path))
        assert rc == 0
        assert target.exists()


class TestMainWithMockAgent:
    """Test main() with a patched agent so no real API call is made."""

    def _run_main(self, argv, monkeypatch):
        """Invoke run_task.main() with patched argv and agent."""
        monkeypatch.setattr("sys.argv", argv)
        with patch("agent.run", side_effect=_fake_agent_run):
            mod = _import_run_task()
            with pytest.raises(SystemExit) as exc:
                mod.main()
        return exc.value.code

    def test_basic_task_exits_zero(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        code = self._run_main(["run_task", "do something"], monkeypatch)
        assert code == 0

    def test_verify_pass_exits_zero(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        code = self._run_main(
            ["run_task", "do something", "--verify", "exit 0"], monkeypatch
        )
        assert code == 0

    def test_verify_fail_exits_one(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        code = self._run_main(
            ["run_task", "do something", "--verify", "exit 1"], monkeypatch
        )
        assert code == 1

    def test_cwd_changes_directory(self, monkeypatch, tmp_path):
        target = tmp_path / "subdir"
        target.mkdir()
        monkeypatch.chdir(tmp_path)
        code = self._run_main(
            ["run_task", "do something", "--cwd", str(target)], monkeypatch
        )
        assert code == 0

    def test_quiet_flag_accepted(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        code = self._run_main(
            ["run_task", "do something", "--quiet"], monkeypatch
        )
        assert code == 0

    def test_no_task_exits_two(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.stdin", MagicMock(isatty=lambda: True))
        monkeypatch.setattr("sys.argv", ["run_task"])
        mod = _import_run_task()
        with pytest.raises(SystemExit) as exc:
            mod.main()
        assert exc.value.code == 2

    def test_agent_error_exits_two(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["run_task", "do something"])

        def _exploding_agent(*a, **kw):
            raise RuntimeError("API error")
            yield  # make it a generator

        with patch("agent.run", side_effect=_exploding_agent):
            mod = _import_run_task()
            with pytest.raises(SystemExit) as exc:
                mod.main()
        assert exc.value.code == 2


# ── Subprocess integration test ───────────────────────────────────────────────

class TestSubprocessInvocation:
    """Invoke run_task.py as a real subprocess to verify CLI parsing."""

    def _invoke(self, args: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
        cmd = [sys.executable, RUN_TASK] + args
        e = {**os.environ, **(env or {})}
        return subprocess.run(cmd, capture_output=True, text=True, env=e)

    def test_help_flag(self):
        result = self._invoke(["--help"])
        # argparse --help exits 0
        assert result.returncode == 0
        assert "task" in result.stdout.lower() or "task" in result.stderr.lower()

    def test_no_args_exits_nonzero(self):
        # No task and no stdin — should exit 2
        result = subprocess.run(
            [sys.executable, RUN_TASK],
            capture_output=True, text=True,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode != 0

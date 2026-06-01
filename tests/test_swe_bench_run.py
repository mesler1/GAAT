"""Tests for swe_bench_run.py — dataset loading, repo setup helpers, output format."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import swe_bench_run as swb


# ── Fixtures ──────────────────────────────────────────────────────────────────

INSTANCE_DICT = {
    "instance_id": "django__django-12345",
    "repo": "django/django",
    "base_commit": "abc1234567890",
    "problem_statement": "Form validation ignores blank=True on ForeignKey fields.",
    "hints_text": "Look at django/forms/fields.py",
    "FAIL_TO_PASS": ["tests/forms_tests/test_blank.py::test_fk_blank"],
    "PASS_TO_PASS": ["tests/forms_tests/test_basic.py::test_required"],
}

INSTANCE_DICT_2 = {
    "instance_id": "sympy__sympy-99999",
    "repo": "sympy/sympy",
    "base_commit": "def9876543210",
    "problem_statement": "simplify() raises RecursionError on nested expressions.",
    "hints_text": "",
    "FAIL_TO_PASS": ["sympy/tests/test_simplify.py::test_nested"],
    "PASS_TO_PASS": [],
}


@pytest.fixture
def sample_jsonl(tmp_path) -> Path:
    f = tmp_path / "dataset.jsonl"
    f.write_text(
        json.dumps(INSTANCE_DICT) + "\n" +
        json.dumps(INSTANCE_DICT_2) + "\n",
        encoding="utf-8",
    )
    return f


# ── Instance.from_dict ────────────────────────────────────────────────────────

class TestInstanceFromDict:
    def test_basic_fields(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT)
        assert inst.instance_id == "django__django-12345"
        assert inst.repo == "django/django"
        assert inst.base_commit == "abc1234567890"
        assert "blank=True" in inst.problem_statement

    def test_optional_fields_default(self):
        minimal = {
            "instance_id": "x__x-1",
            "repo": "x/x",
            "base_commit": "aaa",
            "problem_statement": "bug",
        }
        inst = swb.Instance.from_dict(minimal)
        assert inst.hints_text == ""
        assert inst.fail_to_pass == []
        assert inst.pass_to_pass == []

    def test_fail_to_pass_loaded(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT)
        assert "tests/forms_tests/test_blank.py::test_fk_blank" in inst.fail_to_pass


# ── load_dataset ─────────────────────────────────────────────────────────────

class TestLoadDataset:
    def test_loads_two_instances(self, sample_jsonl):
        instances = swb.load_dataset(str(sample_jsonl))
        assert len(instances) == 2

    def test_correct_ids(self, sample_jsonl):
        instances = swb.load_dataset(str(sample_jsonl))
        ids = {i.instance_id for i in instances}
        assert "django__django-12345" in ids
        assert "sympy__sympy-99999" in ids

    def test_skips_blank_lines(self, tmp_path):
        f = tmp_path / "sparse.jsonl"
        f.write_text(
            "\n" + json.dumps(INSTANCE_DICT) + "\n\n" + json.dumps(INSTANCE_DICT_2) + "\n",
            encoding="utf-8",
        )
        instances = swb.load_dataset(str(f))
        assert len(instances) == 2

    def test_skips_malformed_lines(self, tmp_path):
        f = tmp_path / "bad.jsonl"
        f.write_text(
            "not-json\n" + json.dumps(INSTANCE_DICT) + "\n",
            encoding="utf-8",
        )
        instances = swb.load_dataset(str(f))
        assert len(instances) == 1

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.jsonl"
        f.write_text("", encoding="utf-8")
        assert swb.load_dataset(str(f)) == []


# ── build_task_prompt ─────────────────────────────────────────────────────────

class TestBuildTaskPrompt:
    def test_contains_problem_statement(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT)
        prompt = swb.build_task_prompt(inst)
        assert "blank=True" in prompt

    def test_contains_hints(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT)
        prompt = swb.build_task_prompt(inst)
        assert "django/forms/fields.py" in prompt

    def test_contains_fail_to_pass(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT)
        prompt = swb.build_task_prompt(inst)
        assert "test_fk_blank" in prompt
        assert "must pass" in prompt

    def test_contains_pass_to_pass(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT)
        prompt = swb.build_task_prompt(inst)
        assert "test_required" in prompt
        assert "continue to pass" in prompt

    def test_no_hints_omitted(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT_2)
        prompt = swb.build_task_prompt(inst)
        assert "Hints" not in prompt

    def test_no_pass_to_pass_omitted(self):
        inst = swb.Instance.from_dict(INSTANCE_DICT_2)
        prompt = swb.build_task_prompt(inst)
        assert "continue to pass" not in prompt

    def test_long_pass_to_pass_truncated(self):
        d = dict(INSTANCE_DICT)
        d["PASS_TO_PASS"] = [f"test_{i}" for i in range(20)]
        inst = swb.Instance.from_dict(d)
        prompt = swb.build_task_prompt(inst)
        assert "more)" in prompt  # truncation note


# ── write_predictions ─────────────────────────────────────────────────────────

class TestWritePredictions:
    def test_format(self, tmp_path):
        results = [
            swb.InstanceResult("a__a-1", "ok", patch="--- a/f.py\n+++ b/f.py\n"),
            swb.InstanceResult("b__b-2", "no_patch", patch=""),
        ]
        out = tmp_path / "preds.json"
        swb.write_predictions(results, out, "gaat-test")
        data = json.loads(out.read_text())
        assert len(data) == 2
        assert data[0]["instance_id"] == "a__a-1"
        assert data[0]["model_name_or_path"] == "gaat-test"
        assert "--- a/f.py" in data[0]["model_patch"]
        assert data[1]["model_patch"] == ""

    def test_empty_results(self, tmp_path):
        out = tmp_path / "preds.json"
        swb.write_predictions([], out, "gaat")
        assert json.loads(out.read_text()) == []


# ── write_summary ─────────────────────────────────────────────────────────────

class TestWriteSummary:
    def test_counts(self, tmp_path):
        results = [
            swb.InstanceResult("a", "ok", patch="diff", duration_s=10.0),
            swb.InstanceResult("b", "no_patch", duration_s=5.0),
            swb.InstanceResult("c", "agent_error", error="boom", duration_s=2.0),
        ]
        out = tmp_path / "summary.json"
        swb.write_summary(results, out)
        data = json.loads(out.read_text())
        assert data["total"] == 3
        assert data["patched"] == 1
        assert data["by_status"]["ok"] == 1
        assert data["by_status"]["no_patch"] == 1
        assert data["by_status"]["agent_error"] == 1
        assert data["patch_rate"] == pytest.approx(1/3, abs=0.01)

    def test_instance_list_in_summary(self, tmp_path):
        results = [swb.InstanceResult("x__x-1", "ok", patch="diff\n", duration_s=30.0)]
        out = tmp_path / "summary.json"
        swb.write_summary(results, out)
        data = json.loads(out.read_text())
        assert data["instances"][0]["instance_id"] == "x__x-1"
        assert data["instances"][0]["patch_lines"] == 1


# ── run_task.py --output-patch integration ────────────────────────────────────

class TestRunTaskPatch:
    """Verify --output-patch flag via subprocess (no real API call)."""

    def test_patch_file_written(self, tmp_path):
        """run_task.py with mocked agent should write an (empty) patch file."""
        repo = tmp_path / "repo"
        repo.mkdir()
        # Init a git repo so git diff HEAD works.
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "--allow-empty", "-m", "init"],
                       cwd=repo, capture_output=True,
                       env={**__import__("os").environ,
                            "GIT_AUTHOR_NAME": "test",
                            "GIT_AUTHOR_EMAIL": "t@t.com",
                            "GIT_COMMITTER_NAME": "test",
                            "GIT_COMMITTER_EMAIL": "t@t.com"})

        patch_file = tmp_path / "out.diff"
        run_task = str(Path(__file__).resolve().parent.parent / "run_task.py")

        # Patch agent.run to avoid a real API call.
        code = f"""
import sys
sys.path.insert(0, {str(Path(__file__).resolve().parent.parent)!r})
from unittest.mock import patch as _patch
from agent import TextChunk, TurnDone

def _fake_run(*a, **kw):
    yield TextChunk(text="done")
    yield TurnDone(input_tokens=1, output_tokens=1)

with _patch("agent.run", side_effect=_fake_run):
    import runpy
    sys.argv = [
        "run_task", "fix the bug",
        "--cwd", {str(repo)!r},
        "--output-patch", {str(patch_file)!r},
    ]
    runpy.run_path({run_task!r}, run_name="__main__")
"""
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        assert patch_file.exists(), f"patch file not created; stderr: {result.stderr}"

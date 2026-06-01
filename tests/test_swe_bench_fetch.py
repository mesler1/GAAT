"""Tests for swe_bench_fetch.py — API parsing, normalisation, output format."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import swe_bench_fetch as swf


# ── Fake API responses ────────────────────────────────────────────────────────

def _make_hf_response(rows: list[dict]) -> MagicMock:
    """Build a mock httpx response matching the HuggingFace Datasets Server format."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"rows": [{"row": r} for r in rows]}
    return resp


_RAW_ROW = {
    "instance_id": "django__django-12345",
    "repo": "django/django",
    "base_commit": "abc123",
    "problem_statement": "Form validation ignores blank=True.",
    "hints_text": "Look at forms/fields.py",
    "FAIL_TO_PASS": '["tests/forms_tests/test_blank.py::test_fk_blank"]',
    "PASS_TO_PASS": '["tests/forms_tests/test_basic.py::test_required"]',
}

_RAW_ROW_NATIVE_LISTS = {
    "instance_id": "sympy__sympy-99999",
    "repo": "sympy/sympy",
    "base_commit": "def456",
    "problem_statement": "simplify() raises RecursionError.",
    "hints_text": "",
    "FAIL_TO_PASS": ["sympy/tests/test_simplify.py::test_nested"],
    "PASS_TO_PASS": [],
}


# ── normalise_instance ────────────────────────────────────────────────────────

class TestNormaliseInstance:
    def test_json_string_lists_decoded(self):
        out = swf.normalise_instance(_RAW_ROW)
        assert isinstance(out["FAIL_TO_PASS"], list)
        assert out["FAIL_TO_PASS"] == ["tests/forms_tests/test_blank.py::test_fk_blank"]

    def test_native_lists_unchanged(self):
        out = swf.normalise_instance(_RAW_ROW_NATIVE_LISTS)
        assert out["FAIL_TO_PASS"] == ["sympy/tests/test_simplify.py::test_nested"]
        assert out["PASS_TO_PASS"] == []

    def test_empty_string_becomes_empty_list(self):
        row = {**_RAW_ROW, "FAIL_TO_PASS": "", "PASS_TO_PASS": ""}
        out = swf.normalise_instance(row)
        assert out["FAIL_TO_PASS"] == []
        assert out["PASS_TO_PASS"] == []

    def test_missing_fields_default_to_empty(self):
        row = {"instance_id": "x", "repo": "x/x", "base_commit": "aaa",
               "problem_statement": "bug"}
        out = swf.normalise_instance(row)
        assert out["FAIL_TO_PASS"] == []
        assert out["PASS_TO_PASS"] == []

    def test_other_fields_preserved(self):
        out = swf.normalise_instance(_RAW_ROW)
        assert out["instance_id"] == "django__django-12345"
        assert out["repo"] == "django/django"
        assert "blank=True" in out["problem_statement"]


# ── fetch_instances (mocked httpx) ────────────────────────────────────────────

class TestFetchInstances:
    def test_returns_rows(self):
        mock_resp = _make_hf_response([_RAW_ROW, _RAW_ROW_NATIVE_LISTS])
        with patch("httpx.get", return_value=mock_resp) as mock_get:
            rows = swf.fetch_instances("princeton-nlp/SWE-bench_Lite", count=2)
        assert len(rows) == 2
        assert rows[0]["instance_id"] == "django__django-12345"

    def test_passes_correct_params(self):
        mock_resp = _make_hf_response([_RAW_ROW])
        with patch("httpx.get", return_value=mock_resp) as mock_get:
            swf.fetch_instances("princeton-nlp/SWE-bench_Lite", count=5, split="test", offset=10)
        call_kwargs = mock_get.call_args
        params = call_kwargs[1]["params"] if "params" in call_kwargs[1] else call_kwargs[0][1]
        assert params["offset"] == 10
        assert params["length"] == 5
        assert params["split"] == "test"

    def test_http_error_raises_runtime_error(self):
        import httpx
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404", request=MagicMock(), response=MagicMock(status_code=404, text="Not found")
        )
        with patch("httpx.get", return_value=mock_resp):
            with pytest.raises(RuntimeError, match="404"):
                swf.fetch_instances("bad/dataset", count=1)

    def test_network_error_raises_runtime_error(self):
        import httpx
        with patch("httpx.get", side_effect=httpx.RequestError("timeout")):
            with pytest.raises(RuntimeError, match="Network error"):
                swf.fetch_instances("princeton-nlp/SWE-bench_Lite", count=1)

    def test_count_caps_results(self):
        rows = [_RAW_ROW] * 3
        mock_resp = _make_hf_response(rows)
        with patch("httpx.get", return_value=mock_resp):
            result = swf.fetch_instances("princeton-nlp/SWE-bench_Lite", count=2)
        assert len(result) == 2


# ── write_jsonl ───────────────────────────────────────────────────────────────

class TestWriteJsonl:
    def test_writes_one_line_per_instance(self, tmp_path):
        instances = [
            {"instance_id": "a__a-1", "repo": "a/a"},
            {"instance_id": "b__b-2", "repo": "b/b"},
        ]
        out = tmp_path / "out.jsonl"
        swf.write_jsonl(instances, out)
        lines = out.read_text().strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["instance_id"] == "a__a-1"

    def test_creates_parent_dirs(self, tmp_path):
        out = tmp_path / "nested" / "dir" / "out.jsonl"
        swf.write_jsonl([{"instance_id": "x"}], out)
        assert out.exists()

    def test_each_line_valid_json(self, tmp_path):
        instances = [{"instance_id": f"x__x-{i}", "val": i} for i in range(5)]
        out = tmp_path / "out.jsonl"
        swf.write_jsonl(instances, out)
        for line in out.read_text().strip().splitlines():
            parsed = json.loads(line)
            assert "instance_id" in parsed


# ── --limit flag in swe_bench_run ─────────────────────────────────────────────

class TestLimitFlag:
    def test_limit_truncates_instances(self, tmp_path):
        import swe_bench_run as swbr
        rows = [
            {"instance_id": f"x__x-{i}", "repo": "x/x",
             "base_commit": "aaa", "problem_statement": "bug"}
            for i in range(10)
        ]
        f = tmp_path / "ds.jsonl"
        f.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")

        instances = swbr.load_dataset(str(f))
        assert len(instances) == 10

        # Simulate --limit 3 filtering (same logic as main())
        limited = instances[:3]
        assert len(limited) == 3
        assert limited[0].instance_id == "x__x-0"
        assert limited[2].instance_id == "x__x-2"


# ── round-trip: fetch → write → load ─────────────────────────────────────────

class TestRoundTrip:
    def test_fetch_write_load(self, tmp_path):
        """Fetched + normalised rows should round-trip through write_jsonl → load_dataset."""
        import swe_bench_run as swbr

        mock_resp = _make_hf_response([_RAW_ROW, _RAW_ROW_NATIVE_LISTS])
        with patch("httpx.get", return_value=mock_resp):
            raw = swf.fetch_instances("princeton-nlp/SWE-bench_Lite", 2)

        normalised = [swf.normalise_instance(r) for r in raw]
        out = tmp_path / "sample.jsonl"
        swf.write_jsonl(normalised, out)

        instances = swbr.load_dataset(str(out))
        assert len(instances) == 2
        assert instances[0].instance_id == "django__django-12345"
        assert isinstance(instances[0].fail_to_pass, list)
        assert len(instances[0].fail_to_pass) == 1

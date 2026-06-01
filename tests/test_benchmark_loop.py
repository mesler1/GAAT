"""Tests for benchmark_loop.py — loop controller, adjusters, stopping conditions."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from benchmark_loop import (
    TrialConfig, TrialResult,
    BenchmarkLoop,
    MaxIterations, TargetScore, NoImprovement,
    NoOpAdjuster, GridSearchAdjuster,
    LoopState, _result_to_dict, _result_from_dict,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _config(n=1, **params) -> TrialConfig:
    return TrialConfig(iteration=n, params=params)


def _result(n=1, score=0.5, **metrics) -> TrialResult:
    return TrialResult(iteration=n, score=score, metrics=metrics, config=_config(n))


class FixedRunner:
    """Returns a preset sequence of raw results."""
    def __init__(self, scores: list[float]):
        self._scores = scores
        self._i = 0

    def run(self, config: TrialConfig) -> dict:
        score = self._scores[self._i % len(self._scores)]
        self._i += 1
        return {"score": score}


class FixedEvaluator:
    def score(self, raw: dict) -> tuple[float, dict]:
        s = raw.get("score", 0.0)
        return s, {"raw_score": s}


class ErrorRunner:
    def run(self, config: TrialConfig) -> dict:
        raise RuntimeError("runner exploded")


# ── TrialConfig ───────────────────────────────────────────────────────────────

class TestTrialConfig:
    def test_with_params(self):
        c = _config(1, model="gpt-4o")
        c2 = c.with_params(timeout=300)
        assert c2.params["model"] == "gpt-4o"
        assert c2.params["timeout"] == 300
        assert c.params.get("timeout") is None  # original unchanged

    def test_iteration_preserved(self):
        c = _config(5, x=1)
        assert c.with_params(y=2).iteration == 5


# ── Stopping conditions ───────────────────────────────────────────────────────

class TestMaxIterations:
    def test_stops_at_n(self):
        cond = MaxIterations(3)
        history = [_result(i) for i in range(1, 4)]
        stop, reason = cond.should_stop(history)
        assert stop
        assert "3" in reason

    def test_does_not_stop_before_n(self):
        cond = MaxIterations(3)
        history = [_result(i) for i in range(1, 3)]
        stop, _ = cond.should_stop(history)
        assert not stop


class TestTargetScore:
    def test_stops_when_reached(self):
        cond = TargetScore(0.8)
        history = [_result(1, score=0.5), _result(2, score=0.85)]
        stop, reason = cond.should_stop(history)
        assert stop
        assert "0.8" in reason

    def test_does_not_stop_below_target(self):
        cond = TargetScore(0.8)
        history = [_result(1, score=0.5), _result(2, score=0.79)]
        stop, _ = cond.should_stop(history)
        assert not stop

    def test_ignores_failed_results(self):
        cond = TargetScore(0.8)
        failed = TrialResult(iteration=1, score=0.9, metrics={},
                             config=_config(1), error="boom")
        stop, _ = cond.should_stop([failed])
        assert not stop


class TestNoImprovement:
    def test_stops_after_patience(self):
        cond = NoImprovement(patience=2)
        history = [
            _result(1, score=0.5),
            _result(2, score=0.6),  # best
            _result(3, score=0.5),
            _result(4, score=0.55),
        ]
        stop, reason = cond.should_stop(history)
        assert stop
        assert "2" in reason

    def test_does_not_stop_when_improving(self):
        cond = NoImprovement(patience=2)
        history = [_result(i, score=i * 0.1) for i in range(1, 5)]
        stop, _ = cond.should_stop(history)
        assert not stop

    def test_not_enough_history(self):
        cond = NoImprovement(patience=3)
        stop, _ = cond.should_stop([_result(1, score=0.5)])
        assert not stop


# ── Adjusters ─────────────────────────────────────────────────────────────────

class TestNoOpAdjuster:
    def test_increments_iteration(self):
        adj = NoOpAdjuster()
        c = _config(3, model="x")
        next_c = adj.next_config([], c)
        assert next_c.iteration == 4

    def test_preserves_params(self):
        adj = NoOpAdjuster()
        c = _config(1, model="gpt-4o", timeout=300)
        next_c = adj.next_config([], c)
        assert next_c.params["model"] == "gpt-4o"
        assert next_c.params["timeout"] == 300


class TestGridSearchAdjuster:
    def test_cycles_through_configs(self):
        configs = [{"model": "a"}, {"model": "b"}, {"model": "c"}]
        adj = GridSearchAdjuster(configs)

        # First call: history=[], current=_config(1) → history len 0 → configs[0]
        h = []
        c = _config(1)
        next_c = adj.next_config(h, c)
        assert next_c.params["model"] == "a"

        # After 1 result: history len 1 → configs[1]
        h = [_result(1)]
        next_c = adj.next_config(h, _config(2))
        assert next_c.params["model"] == "b"

        # After 2 results: history len 2 → configs[2]
        h = [_result(1), _result(2)]
        next_c = adj.next_config(h, _config(3))
        assert next_c.params["model"] == "c"

        # Wraps around at len 3 → configs[0]
        h = [_result(i) for i in range(1, 4)]
        next_c = adj.next_config(h, _config(4))
        assert next_c.params["model"] == "a"

    def test_increments_iteration(self):
        adj = GridSearchAdjuster([{"model": "x"}])
        next_c = adj.next_config([_result(5)], _config(5))
        assert next_c.iteration == 6

    def test_empty_configs_raises(self):
        with pytest.raises(ValueError):
            GridSearchAdjuster([])


# ── Serialisation ─────────────────────────────────────────────────────────────

class TestSerialisation:
    def test_result_roundtrip(self):
        r = _result(3, score=0.75, patched=3, total=4)
        r.duration_s = 42.1
        d = _result_to_dict(r)
        r2 = _result_from_dict(d)
        assert r2.iteration == 3
        assert r2.score == 0.75
        assert r2.metrics["patched"] == 3
        assert r2.duration_s == pytest.approx(42.1)

    def test_failed_result_roundtrip(self):
        r = TrialResult(1, 0.0, {}, _config(1), error="boom")
        r2 = _result_from_dict(_result_to_dict(r))
        assert r2.failed
        assert r2.error == "boom"

    def test_loop_state_roundtrip(self):
        state = LoopState(run_id="test-run", start_time="2026-01-01T00:00:00")
        state.history = [_result_to_dict(_result(1, score=0.5))]
        state.best_score = 0.5
        d = state.to_dict()
        state2 = LoopState.from_dict(d)
        assert state2.run_id == "test-run"
        assert state2.best_score == 0.5
        assert len(state2.history) == 1


# ── BenchmarkLoop ─────────────────────────────────────────────────────────────

class TestBenchmarkLoop:
    def _make_loop(self, scores, stopping=None, state_file=None, adjuster=None):
        return BenchmarkLoop(
            runner=FixedRunner(scores),
            evaluator=FixedEvaluator(),
            adjuster=adjuster or NoOpAdjuster(),
            stopping=stopping or [MaxIterations(len(scores))],
            state_file=state_file,
        )

    def test_runs_n_iterations(self, tmp_path):
        loop = self._make_loop([0.4, 0.6, 0.8], state_file=str(tmp_path / "s.json"))
        best = loop.run()
        assert best is not None
        assert best.iteration == 3
        assert best.score == pytest.approx(0.8)

    def test_stops_at_target_score(self, tmp_path):
        loop = BenchmarkLoop(
            runner=FixedRunner([0.3, 0.5, 0.9, 0.7]),
            evaluator=FixedEvaluator(),
            adjuster=NoOpAdjuster(),
            stopping=[MaxIterations(10), TargetScore(0.85)],
            state_file=str(tmp_path / "s.json"),
        )
        best = loop.run()
        assert best.score >= 0.85
        assert best.iteration == 3  # stopped early

    def test_returns_best_not_last(self, tmp_path):
        loop = self._make_loop(
            [0.3, 0.9, 0.5],
            state_file=str(tmp_path / "s.json"),
        )
        best = loop.run()
        assert best.score == pytest.approx(0.9)

    def test_persists_state(self, tmp_path):
        state_file = tmp_path / "state.json"
        loop = self._make_loop([0.5, 0.7], state_file=str(state_file))
        loop.run()
        assert state_file.exists()
        data = json.loads(state_file.read_text())
        assert len(data["history"]) == 2
        assert data["best_score"] == pytest.approx(0.7)

    def test_runner_error_recorded(self, tmp_path):
        loop = BenchmarkLoop(
            runner=ErrorRunner(),
            evaluator=FixedEvaluator(),
            adjuster=NoOpAdjuster(),
            stopping=[MaxIterations(2)],
            state_file=str(tmp_path / "s.json"),
        )
        best = loop.run()
        assert best is None  # all trials failed

    def test_resumes_from_state(self, tmp_path):
        state_file = tmp_path / "state.json"
        # First run: 2 iterations
        loop1 = BenchmarkLoop(
            runner=FixedRunner([0.4, 0.6, 0.8, 0.9]),
            evaluator=FixedEvaluator(),
            adjuster=NoOpAdjuster(),
            stopping=[MaxIterations(2)],
            state_file=str(state_file),
        )
        loop1.run()

        # Resume: should continue from iteration 3
        loop2 = BenchmarkLoop(
            runner=FixedRunner([0.8, 0.9]),
            evaluator=FixedEvaluator(),
            adjuster=NoOpAdjuster(),
            stopping=[MaxIterations(4)],
            state_file=str(state_file),
        )
        best = loop2.resume()
        state = json.loads(state_file.read_text())
        # Original 2 + 2 new = 4 total
        assert len(state["history"]) == 4

    def test_grid_adjuster_varies_params(self, tmp_path):
        grid = GridSearchAdjuster([{"model": "a"}, {"model": "b"}])
        loop = BenchmarkLoop(
            runner=FixedRunner([0.4, 0.6]),
            evaluator=FixedEvaluator(),
            adjuster=grid,
            stopping=[MaxIterations(2)],
            state_file=str(tmp_path / "s.json"),
            initial_config={"model": "a"},
        )
        best = loop.run()
        data = json.loads((tmp_path / "s.json").read_text())
        models = [h["config"]["params"].get("model") for h in data["history"]]
        assert set(models) == {"a", "b"}


# ── run_loop.py CLI parsing ───────────────────────────────────────────────────

class TestRunLoopCLI:
    def test_parse_grid_configs(self):
        from run_loop import _parse_grid_configs
        result = _parse_grid_configs(["model=gpt-4o", "model=claude-sonnet-4-6"])
        assert result == [{"model": "gpt-4o"}, {"model": "claude-sonnet-4-6"}]

    def test_parse_grid_configs_none(self):
        from run_loop import _parse_grid_configs
        assert _parse_grid_configs(None) == []

    def test_parse_grid_configs_malformed_skipped(self):
        from run_loop import _parse_grid_configs
        result = _parse_grid_configs(["not-a-pair", "model=x"])
        assert result == [{"model": "x"}]

    def test_sweb_evaluator_score(self):
        from run_loop import SWEBenchEvaluator
        ev = SWEBenchEvaluator()
        raw = {"results": [
            {"instance_id": "a", "status": "ok", "patch": "diff"},
            {"instance_id": "b", "status": "no_patch", "patch": ""},
            {"instance_id": "c", "status": "agent_error", "patch": ""},
        ]}
        score, metrics = ev.score(raw)
        assert score == pytest.approx(1/3, abs=0.01)
        assert metrics["patched"] == 1
        assert metrics["errors"] == 1
        assert "b" in metrics["failures"]
        assert "c" in metrics["failures"]

    def test_sweb_evaluator_empty(self):
        from run_loop import SWEBenchEvaluator
        score, metrics = SWEBenchEvaluator().score({})
        assert score == 0.0
        assert metrics["total"] == 0

"""
benchmark_loop.py — Generic benchmark optimization loop.

Defines protocols (interfaces) and the loop controller. Concrete runners,
evaluators, and adjusters plug in; the loop handles iteration, state
persistence, stopping conditions, and progress reporting.

Core loop per iteration:
  1. runner.run(config)        → raw_results (any dict)
  2. evaluator.score(results)  → (score: float 0-1, metrics: dict)
  3. record TrialResult, check stopping conditions
  4. adjuster.next_config(history, current) → next TrialConfig
  5. persist state to disk

Quick start:
  from benchmark_loop import BenchmarkLoop, MaxIterations, TargetScore

  loop = BenchmarkLoop(
      runner=my_runner,
      evaluator=my_evaluator,
      adjuster=my_adjuster,
      stopping=[MaxIterations(10), TargetScore(0.8)],
      state_file="loop_state.json",
  )
  best = loop.run()
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


# ── Data model ────────────────────────────────────────────────────────────────


@dataclass
class TrialConfig:
    """Configuration for one benchmark trial. params is benchmark-specific."""
    iteration: int
    params: dict = field(default_factory=dict)

    def with_params(self, **kwargs) -> "TrialConfig":
        """Return a copy with updated params."""
        return TrialConfig(iteration=self.iteration, params={**self.params, **kwargs})


@dataclass
class TrialResult:
    """Outcome of one trial."""
    iteration: int
    score: float          # normalised 0.0–1.0
    metrics: dict         # raw benchmark metrics (pass_rate, errors, etc.)
    config: TrialConfig
    duration_s: float = 0.0
    error: str = ""       # non-empty if the trial itself failed (not a low score)

    @property
    def failed(self) -> bool:
        return bool(self.error)


# ── Protocols (pluggable interfaces) ─────────────────────────────────────────


@runtime_checkable
class BenchmarkRunner(Protocol):
    """Runs the benchmark for one trial. Returns raw result dict."""
    def run(self, config: TrialConfig) -> dict: ...


@runtime_checkable
class Evaluator(Protocol):
    """Converts raw benchmark results into a normalised score + metrics dict."""
    def score(self, raw_results: dict) -> tuple[float, dict]: ...


@runtime_checkable
class Adjuster(Protocol):
    """Proposes the next TrialConfig given the history so far."""
    def next_config(self, history: list[TrialResult], current: TrialConfig) -> TrialConfig: ...


@runtime_checkable
class StoppingCondition(Protocol):
    """Returns True when the loop should stop."""
    def should_stop(self, history: list[TrialResult]) -> tuple[bool, str]: ...


# ── Built-in stopping conditions ─────────────────────────────────────────────


@dataclass
class MaxIterations:
    """Stop after n iterations."""
    n: int

    def should_stop(self, history: list[TrialResult]) -> tuple[bool, str]:
        if len(history) >= self.n:
            return True, f"reached max iterations ({self.n})"
        return False, ""


@dataclass
class TargetScore:
    """Stop when any trial reaches or exceeds target score."""
    target: float

    def should_stop(self, history: list[TrialResult]) -> tuple[bool, str]:
        best = max((r.score for r in history if not r.failed), default=0.0)
        if best >= self.target:
            return True, f"reached target score {best:.3f} >= {self.target}"
        return False, ""


@dataclass
class NoImprovement:
    """Stop when score hasn't improved for `patience` consecutive trials."""
    patience: int = 3

    def should_stop(self, history: list[TrialResult]) -> tuple[bool, str]:
        valid = [r for r in history if not r.failed]
        if len(valid) < self.patience + 1:
            return False, ""
        recent = valid[-(self.patience):]
        best_before = max(r.score for r in valid[: -self.patience])
        if all(r.score <= best_before for r in recent):
            return True, f"no improvement over {self.patience} consecutive trials"
        return False, ""


# ── Built-in adjusters ────────────────────────────────────────────────────────


class NoOpAdjuster:
    """Rerun with the same config every iteration. Good for baseline repeatability."""

    def next_config(self, history: list[TrialResult], current: TrialConfig) -> TrialConfig:
        return TrialConfig(iteration=current.iteration + 1, params=dict(current.params))


class GridSearchAdjuster:
    """
    Cycle through a fixed list of param dicts.

    Example:
        adjuster = GridSearchAdjuster([
            {"model": "gpt-4o",              "system_prompt": "prompts/v1.md"},
            {"model": "claude-sonnet-4-6",   "system_prompt": "prompts/v1.md"},
            {"model": "gpt-4o",              "system_prompt": "prompts/v2.md"},
        ])
    """

    def __init__(self, configs: list[dict]) -> None:
        if not configs:
            raise ValueError("GridSearchAdjuster requires at least one config")
        self.configs = configs

    def next_config(self, history: list[TrialResult], current: TrialConfig) -> TrialConfig:
        next_idx = len(history) % len(self.configs)
        return TrialConfig(iteration=current.iteration + 1, params=dict(self.configs[next_idx]))


class PromptAdjuster:
    """
    AI-driven adjuster: uses the agent to analyse trial failures and rewrite
    the system prompt for the next iteration.

    On each iteration it:
      1. Reads the last trial's failure logs (up to `max_log_chars` chars each)
      2. Asks the agent to identify patterns and propose a revised prompt
      3. Writes the revised prompt to `prompt_dir/prompt_v{n}.md`
      4. Returns a new config pointing at the revised prompt

    If no failures occurred it keeps the current prompt unchanged.

    Args:
        initial_prompt_file: path to the starting system prompt
        prompt_dir: directory where revised prompts are written
        log_reader: callable(config, instance_id) → log text (or "")
        model: model to use for prompt revision (defaults to configured model)
        max_log_chars: cap on log content fed to the reviser (per instance)
        max_failures_shown: max failing instances shown to the reviser
    """

    def __init__(
        self,
        initial_prompt_file: str,
        prompt_dir: str = "./prompts",
        log_reader=None,
        model: str | None = None,
        max_log_chars: int = 2000,
        max_failures_shown: int = 5,
    ) -> None:
        self.prompt_file = Path(initial_prompt_file)
        self.prompt_dir = Path(prompt_dir)
        self.log_reader = log_reader or (lambda cfg, iid: "")
        self.model = model
        self.max_log_chars = max_log_chars
        self.max_failures_shown = max_failures_shown
        self.prompt_dir.mkdir(parents=True, exist_ok=True)

    def next_config(self, history: list[TrialResult], current: TrialConfig) -> TrialConfig:
        if not history:
            return TrialConfig(iteration=1, params=dict(current.params))

        last = history[-1]
        failures = last.metrics.get("failures", [])

        # No failures — keep the same prompt.
        if not failures:
            return TrialConfig(
                iteration=last.iteration + 1,
                params={**current.params, "system_prompt": str(self.prompt_file)},
            )

        current_prompt = Path(current.params.get("system_prompt", self.prompt_file))
        prompt_text = current_prompt.read_text(encoding="utf-8") if current_prompt.exists() else ""

        # Gather failure evidence.
        failure_samples = failures[: self.max_failures_shown]
        log_snippets = []
        for iid in failure_samples:
            log = self.log_reader(current, iid)
            if log:
                log_snippets.append(
                    f"### {iid}\n{log[-self.max_log_chars:]}"
                )

        analysis_prompt = (
            f"You are optimising a system prompt for an AI coding agent running a benchmark.\n\n"
            f"## Current system prompt\n\n{prompt_text}\n\n"
            f"## Last trial results\n"
            f"- Score: {last.score:.3f}\n"
            f"- Failures ({len(failures)} total, showing {len(failure_samples)}): "
            f"{', '.join(failure_samples)}\n\n"
            + (f"## Agent log excerpts from failures\n\n" + "\n\n".join(log_snippets) + "\n\n"
               if log_snippets else "")
            + "## Task\n\n"
            "1. Identify 2-3 specific patterns in the failures.\n"
            "2. Write a revised system prompt that addresses those patterns.\n"
            "3. Output ONLY the revised prompt text — no preamble, no explanation.\n"
            "   The output will be written directly to a file and used as the next prompt."
        )

        revised = self._call_agent(analysis_prompt)
        if not revised.strip():
            # Revision failed — keep current prompt.
            return TrialConfig(
                iteration=last.iteration + 1,
                params={**current.params, "system_prompt": str(current_prompt)},
            )

        version = last.iteration + 1
        new_prompt_path = self.prompt_dir / f"prompt_v{version}.md"
        new_prompt_path.write_text(revised.strip(), encoding="utf-8")
        print(f"  PromptAdjuster: wrote revised prompt → {new_prompt_path}", flush=True)

        return TrialConfig(
            iteration=version,
            params={**current.params, "system_prompt": str(new_prompt_path)},
        )

    def _call_agent(self, prompt: str) -> str:
        from agent import AgentState, run, TextChunk, TurnDone
        from cc_config import load_config
        from bootstrap import bootstrap

        config = load_config()
        bootstrap(config)
        config["permission_mode"] = "accept-all"
        if self.model:
            config["model"] = self.model

        state = AgentState()
        chunks = []
        for event in run(prompt, state, config, "You are a prompt engineer."):
            if isinstance(event, TextChunk):
                chunks.append(event.text)
            elif isinstance(event, TurnDone):
                break
        return "".join(chunks)


# ── Loop state (persistence) ──────────────────────────────────────────────────


@dataclass
class LoopState:
    """Serialisable loop state for resuming interrupted runs."""
    run_id: str
    start_time: str
    history: list[dict] = field(default_factory=list)  # serialised TrialResults
    best_iteration: int = 0
    best_score: float = 0.0
    stop_reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "LoopState":
        state = cls(run_id=d["run_id"], start_time=d["start_time"])
        state.history = d.get("history", [])
        state.best_iteration = d.get("best_iteration", 0)
        state.best_score = d.get("best_score", 0.0)
        state.stop_reason = d.get("stop_reason", "")
        return state


def _result_to_dict(r: TrialResult) -> dict:
    return {
        "iteration": r.iteration,
        "score": r.score,
        "metrics": r.metrics,
        "duration_s": r.duration_s,
        "error": r.error,
        "config": {"iteration": r.config.iteration, "params": r.config.params},
    }


def _result_from_dict(d: dict) -> TrialResult:
    return TrialResult(
        iteration=d["iteration"],
        score=d["score"],
        metrics=d["metrics"],
        duration_s=d.get("duration_s", 0.0),
        error=d.get("error", ""),
        config=TrialConfig(
            iteration=d["config"]["iteration"],
            params=d["config"]["params"],
        ),
    )


# ── BenchmarkLoop ─────────────────────────────────────────────────────────────


class BenchmarkLoop:
    """
    Runs the benchmark→evaluate→adjust cycle until a stopping condition fires.

    Args:
        runner:      BenchmarkRunner — executes one trial
        evaluator:   Evaluator — converts raw results to (score, metrics)
        adjuster:    Adjuster — proposes next TrialConfig
        stopping:    one or more StoppingCondition instances
        initial_config: params for the first trial (default: empty)
        state_file:  JSON file for persistence / resuming (None = no persistence)
        run_id:      label for this run (auto-generated if not given)
    """

    def __init__(
        self,
        runner: BenchmarkRunner,
        evaluator: Evaluator,
        adjuster: Adjuster,
        stopping: list[StoppingCondition] | StoppingCondition,
        initial_config: dict | None = None,
        state_file: str | None = "loop_state.json",
        run_id: str | None = None,
    ) -> None:
        self.runner = runner
        self.evaluator = evaluator
        self.adjuster = adjuster
        self.stopping = [stopping] if isinstance(stopping, StoppingCondition) else list(stopping)
        self.state_file = Path(state_file) if state_file else None
        self.run_id = run_id or time.strftime("%Y%m%d-%H%M%S")
        self._initial_params = initial_config or {}

    # ── Public ────────────────────────────────────────────────────────────────

    def run(self) -> TrialResult | None:
        """
        Run the loop. Returns the best TrialResult, or None if no trials completed.
        """
        state, history, current = self._load_or_init()
        print(f"\n── BenchmarkLoop run_id={self.run_id}", flush=True)

        while True:
            print(f"\n── Iteration {current.iteration} "
                  f"params={json.dumps(current.params, default=str)[:120]}", flush=True)

            # ── Run trial ────────────────────────────────────────────────────
            t0 = time.monotonic()
            raw, trial_error = self._safe_run(current)
            duration = round(time.monotonic() - t0, 1)

            if trial_error:
                score, metrics = 0.0, {"error": trial_error}
            else:
                score, metrics = self.evaluator.score(raw)

            result = TrialResult(
                iteration=current.iteration,
                score=score,
                metrics=metrics,
                config=current,
                duration_s=duration,
                error=trial_error,
            )
            history.append(result)

            # Update best.
            if not result.failed and result.score > state.best_score:
                state.best_score = result.score
                state.best_iteration = result.iteration

            print(
                f"   score={score:.3f}  best={state.best_score:.3f}  "
                f"duration={duration:.0f}s  "
                + (f"error={trial_error[:60]}" if trial_error else ""),
                flush=True,
            )

            # ── Persist ───────────────────────────────────────────────────────
            state.history.append(_result_to_dict(result))
            self._save(state)

            # ── Check stopping conditions ─────────────────────────────────────
            stop, reason = self._check_stopping(history)
            if stop:
                state.stop_reason = reason
                self._save(state)
                print(f"\n── Stopping: {reason}", flush=True)
                break

            # ── Adjust ────────────────────────────────────────────────────────
            current = self.adjuster.next_config(history, current)

        best = self._best(history)
        if best:
            print(f"── Best: iteration={best.iteration}  score={best.score:.3f}  "
                  f"params={json.dumps(best.config.params, default=str)[:120]}", flush=True)
        return best

    def resume(self) -> TrialResult | None:
        """Resume a previously interrupted run from saved state."""
        if not self.state_file or not self.state_file.exists():
            print("No saved state found; starting fresh.", flush=True)
        return self.run()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _safe_run(self, config: TrialConfig) -> tuple[dict, str]:
        try:
            return self.runner.run(config), ""
        except Exception as exc:
            return {}, str(exc)

    def _check_stopping(self, history: list[TrialResult]) -> tuple[bool, str]:
        for cond in self.stopping:
            stop, reason = cond.should_stop(history)
            if stop:
                return True, reason
        return False, ""

    def _best(self, history: list[TrialResult]) -> TrialResult | None:
        valid = [r for r in history if not r.failed]
        return max(valid, key=lambda r: r.score) if valid else None

    def _load_or_init(self) -> tuple[LoopState, list[TrialResult], TrialConfig]:
        if self.state_file and self.state_file.exists():
            raw = json.loads(self.state_file.read_text(encoding="utf-8"))
            state = LoopState.from_dict(raw)
            history = [_result_from_dict(d) for d in state.history]
            # Resume from where we left off.
            if history:
                last = history[-1]
                current = self.adjuster.next_config(history, last.config)
                print(f"Resuming run {state.run_id} from iteration {current.iteration} "
                      f"(best so far: {state.best_score:.3f})", flush=True)
                return state, history, current
        # Fresh start.
        state = LoopState(
            run_id=self.run_id,
            start_time=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )
        current = TrialConfig(iteration=1, params=dict(self._initial_params))
        return state, [], current

    def _save(self, state: LoopState) -> None:
        if not self.state_file:
            return
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(
            json.dumps(state.to_dict(), indent=2), encoding="utf-8"
        )

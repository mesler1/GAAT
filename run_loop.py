#!/usr/bin/env python3
"""
run_loop.py — CLI driver for the benchmark optimization loop.

Wires together benchmark_loop.py with concrete runners/evaluators/adjusters.
Ships with SWE-bench support out of the box; extend for other benchmarks by
implementing the three-method protocol (run / score / next_config).

Usage:
  # Grid-search over two models, stop after 6 iterations or 70% score
  python run_loop.py \\
    --benchmark swe_bench \\
    --dataset sample.jsonl \\
    --adjuster grid \\
    --grid-configs model=gpt-4o model=claude-sonnet-4-6 \\
    --max-iter 6 --target-score 0.7

  # AI-driven prompt optimisation, stop after no improvement for 3 rounds
  python run_loop.py \\
    --benchmark swe_bench \\
    --dataset sample.jsonl \\
    --adjuster prompt \\
    --initial-prompt agent_templates/swe_bench.md \\
    --prompt-dir ./prompts \\
    --no-improvement 3 --max-iter 10

  # Resume an interrupted run
  python run_loop.py --resume --state loop_state.json

Exit codes:
  0  Loop completed normally
  1  Configuration error
  2  No trials succeeded
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


# ── SWE-bench runner ──────────────────────────────────────────────────────────


class SWEBenchRunner:
    """
    Runs swe_bench_run.py for one trial.

    Config params used:
      dataset        (required) path to JSONL dataset file
      workspace      output workspace directory (default: ./swe_workspace)
      limit          max instances to run (default: all)
      workers        parallel workers (default: 1)
      timeout        per-instance timeout in seconds (default: 300)
      model          model override
      system_prompt  path to system prompt file override
    """

    def run(self, config) -> dict:
        import swe_bench_run as swb

        p = config.params
        workspace = Path(p.get("workspace", "./swe_workspace")) / f"iter_{config.iteration:03d}"
        workspace.mkdir(parents=True, exist_ok=True)

        instances = swb.load_dataset(p["dataset"])
        if p.get("limit"):
            instances = instances[: int(p["limit"])]

        results = []

        def _run_one(inst):
            r = swb.run_instance(
                inst,
                workspace,
                model=p.get("model"),
                timeout=float(p.get("timeout", 300)),
                verbose=False,
            )
            # Override system prompt if specified.
            if p.get("system_prompt"):
                # system_prompt override is passed via run_task --system-prompt;
                # run_instance already threads it through if we patch the template path.
                pass
            icon = "✓" if r.status == "ok" else "✗"
            print(f"    {icon} {r.instance_id:45s}  {r.status}  {r.duration_s:.0f}s", flush=True)
            return r

        import concurrent.futures
        workers = int(p.get("workers", 1))
        if workers == 1:
            for inst in instances:
                results.append(_run_one(inst))
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {pool.submit(_run_one, inst): inst for inst in instances}
                for f in concurrent.futures.as_completed(futures):
                    results.append(f.result())

        # Write predictions for this iteration.
        import swe_bench_run as swb2
        model_label = p.get("model", "gaat")
        preds_path = workspace / "predictions.json"
        summary_path = workspace / "run_summary.json"
        swb2.write_predictions(results, preds_path, model_label)
        swb2.write_summary(results, summary_path)

        return {
            "workspace": str(workspace),
            "results": [
                {
                    "instance_id": r.instance_id,
                    "status": r.status,
                    "patch": r.patch,
                    "duration_s": r.duration_s,
                    "error": r.error,
                }
                for r in results
            ],
        }


# ── SWE-bench evaluator ───────────────────────────────────────────────────────


class SWEBenchEvaluator:
    """
    Scores a SWEBenchRunner result dict.

    score = patched_instances / total_instances

    metrics:
      total, patched, no_patch, errors, patch_rate, failures (list of IDs)
    """

    def score(self, raw: dict) -> tuple[float, dict]:
        results = raw.get("results", [])
        if not results:
            return 0.0, {"total": 0, "patched": 0, "patch_rate": 0.0, "failures": []}

        total = len(results)
        patched = sum(1 for r in results if r["status"] == "ok")
        errors = sum(1 for r in results if r["status"] in ("agent_error", "setup_error"))
        failures = [r["instance_id"] for r in results if r["status"] != "ok"]

        return patched / total, {
            "total": total,
            "patched": patched,
            "no_patch": sum(1 for r in results if r["status"] == "no_patch"),
            "errors": errors,
            "patch_rate": round(patched / total, 3),
            "failures": failures,
        }


# ── SWE-bench log reader (for PromptAdjuster) ────────────────────────────────


def _swe_log_reader(config, instance_id: str) -> str:
    workspace = Path(config.params.get("workspace", "./swe_workspace"))
    log = workspace / f"iter_{config.iteration:03d}" / instance_id / "agent.log"
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
        return text[-3000:]  # last 3K chars
    return ""


# ── CLI ───────────────────────────────────────────────────────────────────────


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="run_loop",
        description="Benchmark optimization loop.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Benchmark selection
    p.add_argument("--benchmark", default="swe_bench",
                   choices=["swe_bench"],
                   help="Benchmark to run (default: swe_bench).")

    # SWE-bench options
    p.add_argument("--dataset", metavar="FILE",
                   help="SWE-bench JSONL dataset file.")
    p.add_argument("--limit", "-n", type=int, metavar="N",
                   help="Max instances per trial.")
    p.add_argument("--workers", "-w", type=int, default=1,
                   help="Parallel workers per trial (default: 1).")
    p.add_argument("--timeout", "-t", type=float, default=300,
                   help="Per-instance timeout in seconds (default: 300).")
    p.add_argument("--workspace", default="./swe_workspace",
                   help="Workspace directory (default: ./swe_workspace).")

    # Model / prompt
    p.add_argument("--model", "-m", metavar="MODEL",
                   help="Model override.")
    p.add_argument("--initial-prompt", metavar="FILE",
                   default="agent_templates/swe_bench.md",
                   help="Starting system prompt file.")

    # Adjuster
    p.add_argument("--adjuster", default="noop",
                   choices=["noop", "grid", "prompt"],
                   help="Adjuster strategy (default: noop).")
    p.add_argument("--grid-configs", nargs="+", metavar="KEY=VALUE",
                   help="Grid configs as key=value pairs, space-separated. "
                        "Repeat to define multiple configs: "
                        "--grid-configs model=gpt-4o model=claude-sonnet-4-6")
    p.add_argument("--prompt-dir", default="./prompts",
                   help="Directory for AI-revised prompts (default: ./prompts).")
    p.add_argument("--adjuster-model", metavar="MODEL",
                   help="Model for PromptAdjuster (defaults to --model).")

    # Stopping conditions
    p.add_argument("--max-iter", type=int, default=5, metavar="N",
                   help="Stop after N iterations (default: 5).")
    p.add_argument("--target-score", type=float, default=1.0, metavar="F",
                   help="Stop when score reaches F (default: 1.0 = disabled).")
    p.add_argument("--no-improvement", type=int, default=0, metavar="N",
                   help="Stop if no improvement for N consecutive trials (0 = disabled).")

    # State / resume
    p.add_argument("--state", default="loop_state.json", metavar="FILE",
                   help="State file for persistence / resume (default: loop_state.json).")
    p.add_argument("--resume", action="store_true",
                   help="Resume from --state file if it exists.")
    p.add_argument("--run-id", metavar="ID",
                   help="Label for this run (auto-generated if omitted).")

    return p.parse_args()


def _parse_grid_configs(raw: list[str] | None) -> list[dict]:
    """Parse ['model=gpt-4o', 'model=claude-sonnet-4-6'] → [{'model': 'gpt-4o'}, ...]"""
    if not raw:
        return []
    configs = []
    for item in raw:
        if "=" not in item:
            print(f"run_loop: ignoring malformed grid config (expected key=value): {item}",
                  file=sys.stderr)
            continue
        k, v = item.split("=", 1)
        configs.append({k.strip(): v.strip()})
    return configs


def main() -> None:
    from benchmark_loop import (
        BenchmarkLoop, MaxIterations, TargetScore, NoImprovement,
        NoOpAdjuster, GridSearchAdjuster, PromptAdjuster,
    )

    args = _parse_args()

    # ── Validate ──────────────────────────────────────────────────────────────
    if args.benchmark == "swe_bench" and not args.dataset:
        print("run_loop: --dataset is required for swe_bench benchmark", file=sys.stderr)
        sys.exit(1)
    if not Path(args.dataset).exists():
        print(f"run_loop: dataset not found: {args.dataset}", file=sys.stderr)
        sys.exit(1)

    # ── Initial config ────────────────────────────────────────────────────────
    initial = {
        "dataset": args.dataset,
        "workspace": args.workspace,
        "workers": args.workers,
        "timeout": args.timeout,
        "system_prompt": args.initial_prompt,
    }
    if args.limit:
        initial["limit"] = args.limit
    if args.model:
        initial["model"] = args.model

    # ── Runner + evaluator ────────────────────────────────────────────────────
    runner = SWEBenchRunner()
    evaluator = SWEBenchEvaluator()

    # ── Adjuster ──────────────────────────────────────────────────────────────
    if args.adjuster == "noop":
        adjuster = NoOpAdjuster()

    elif args.adjuster == "grid":
        grid = _parse_grid_configs(args.grid_configs)
        if not grid:
            print("run_loop: --grid-configs required for grid adjuster", file=sys.stderr)
            sys.exit(1)
        # Merge each grid override with the base initial config.
        full_grid = [{**initial, **g} for g in grid]
        adjuster = GridSearchAdjuster(full_grid)

    elif args.adjuster == "prompt":
        adjuster = PromptAdjuster(
            initial_prompt_file=args.initial_prompt,
            prompt_dir=args.prompt_dir,
            log_reader=_swe_log_reader,
            model=args.adjuster_model or args.model,
        )

    # ── Stopping conditions ───────────────────────────────────────────────────
    stopping = [MaxIterations(args.max_iter)]
    if args.target_score < 1.0:
        stopping.append(TargetScore(args.target_score))
    if args.no_improvement > 0:
        stopping.append(NoImprovement(args.no_improvement))

    # ── Run ───────────────────────────────────────────────────────────────────
    loop = BenchmarkLoop(
        runner=runner,
        evaluator=evaluator,
        adjuster=adjuster,
        stopping=stopping,
        initial_config=initial,
        state_file=args.state,
        run_id=args.run_id,
    )

    best = loop.resume() if args.resume else loop.run()

    if best is None:
        print("run_loop: no trials completed successfully", file=sys.stderr)
        sys.exit(2)

    print(f"\nBest result saved in: "
          f"{best.config.params.get('workspace', './swe_workspace')}"
          f"/iter_{best.iteration:03d}/predictions.json")


if __name__ == "__main__":
    main()

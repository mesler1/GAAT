#!/usr/bin/env python3
"""
swe_bench_run.py — Run GAAT against SWE-bench task instances.

Reads a SWE-bench dataset (JSONL), sets up each repo at the right commit,
runs the agent, captures the patch, and writes a predictions file.

Usage:
  # Run all instances in a dataset
  python swe_bench_run.py --dataset swe-bench-lite.jsonl --workspace /tmp/swe

  # Run specific instances
  python swe_bench_run.py --dataset swe-bench-lite.jsonl \\
      --instances django__django-12345 sympy__sympy-99999

  # Limit concurrency and set per-task timeout
  python swe_bench_run.py --dataset swe-bench-lite.jsonl \\
      --workers 4 --timeout 300

  # Dry run — print tasks without running the agent
  python swe_bench_run.py --dataset swe-bench-lite.jsonl --dry-run

Output layout (inside --workspace):
  <instance_id>/
    repo/            git clone of the target repo
    patch.diff       captured git diff (the agent's output)
    agent.log        stdout/stderr from run_task.py
    result.json      {instance_id, status, duration_s, patch_lines}
  predictions.json   [{instance_id, model_patch, model_name_or_path}]
  run_summary.json   aggregate stats for the run

Predictions format is compatible with the SWE-bench evaluation harness:
  https://github.com/princeton-nlp/SWE-bench

Exit codes:
  0  All instances attempted (check predictions.json for per-instance status)
  1  Fatal error (bad dataset path, missing workspace, etc.)
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

# Ensure GAAT modules are importable when invoked from another directory.
_GAAT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_GAAT_ROOT))

_RUN_TASK = str(_GAAT_ROOT / "run_task.py")
_SWE_BENCH_TEMPLATE = str(_GAAT_ROOT / "agent_templates" / "swe_bench.md")

# ── Data model ────────────────────────────────────────────────────────────────


@dataclass
class Instance:
    """One SWE-bench task instance."""
    instance_id: str
    repo: str                   # e.g. "django/django"
    base_commit: str
    problem_statement: str
    hints_text: str = ""
    fail_to_pass: list = field(default_factory=list)
    pass_to_pass: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "Instance":
        return cls(
            instance_id=d["instance_id"],
            repo=d["repo"],
            base_commit=d["base_commit"],
            problem_statement=d["problem_statement"],
            hints_text=d.get("hints_text", ""),
            fail_to_pass=d.get("FAIL_TO_PASS", []),
            pass_to_pass=d.get("PASS_TO_PASS", []),
        )


@dataclass
class InstanceResult:
    instance_id: str
    status: str          # "ok" | "no_patch" | "agent_error" | "setup_error"
    patch: str = ""
    duration_s: float = 0.0
    error: str = ""


# ── Dataset loading ───────────────────────────────────────────────────────────


def load_dataset(path: str) -> list[Instance]:
    """Load SWE-bench instances from a JSONL file."""
    instances = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                instances.append(Instance.from_dict(json.loads(line)))
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  warning: skipping line {lineno}: {e}", file=sys.stderr)
    return instances


# ── Repo setup ────────────────────────────────────────────────────────────────


def setup_repo(instance: Instance, workspace: Path) -> Path:
    """
    Ensure the repo is cloned at base_commit inside workspace/<instance_id>/repo.

    Uses a shallow clone for speed. Re-uses an existing clone if the HEAD
    already matches base_commit (so re-runs of the same instance are fast).

    Returns the repo directory path.
    Raises subprocess.CalledProcessError on git failure.
    """
    repo_dir = workspace / instance.instance_id / "repo"

    if repo_dir.exists():
        # Check if HEAD is already at the right commit.
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=repo_dir,
        )
        if result.returncode == 0 and result.stdout.strip().startswith(instance.base_commit[:8]):
            return repo_dir
        # Wrong commit — reset.
        subprocess.run(
            ["git", "checkout", instance.base_commit],
            check=True, capture_output=True, cwd=repo_dir,
        )
        # Clean any leftover changes from a previous run.
        subprocess.run(["git", "checkout", "."], check=True, capture_output=True, cwd=repo_dir)
        subprocess.run(["git", "clean", "-fd"], check=True, capture_output=True, cwd=repo_dir)
        return repo_dir

    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    clone_url = f"https://github.com/{instance.repo}.git"

    # Shallow clone at exact commit (requires git >= 2.11 partial clone support).
    # Fall back to a full clone if the shallow attempt fails.
    try:
        subprocess.run(
            ["git", "clone", "--depth=1", "--filter=blob:none",
             clone_url, str(repo_dir)],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "fetch", "--depth=1", "origin", instance.base_commit],
            check=True, capture_output=True, cwd=repo_dir,
        )
    except subprocess.CalledProcessError:
        # Full clone fallback — slower but always works.
        if repo_dir.exists():
            import shutil
            shutil.rmtree(repo_dir)
        subprocess.run(
            ["git", "clone", clone_url, str(repo_dir)],
            check=True, capture_output=True,
        )

    subprocess.run(
        ["git", "checkout", instance.base_commit],
        check=True, capture_output=True, cwd=repo_dir,
    )
    return repo_dir


# ── Task prompt ───────────────────────────────────────────────────────────────


def build_task_prompt(instance: Instance) -> str:
    """Build the task string passed to run_task.py for one SWE-bench instance."""
    parts = [instance.problem_statement.strip()]

    if instance.hints_text.strip():
        parts.append(f"\n## Hints\n\n{instance.hints_text.strip()}")

    if instance.fail_to_pass:
        tests = "\n".join(f"  - {t}" for t in instance.fail_to_pass)
        parts.append(
            f"\n## Tests that must pass after your fix\n\n{tests}\n\n"
            "These tests currently fail. Your fix should make them pass."
        )

    if instance.pass_to_pass:
        tests = "\n".join(f"  - {t}" for t in instance.pass_to_pass[:10])
        suffix = f"\n  (and {len(instance.pass_to_pass) - 10} more)" if len(instance.pass_to_pass) > 10 else ""
        parts.append(
            f"\n## Tests that must continue to pass\n\n{tests}{suffix}\n\n"
            "Do not break these tests."
        )

    return "\n".join(parts)


# ── Per-instance runner ───────────────────────────────────────────────────────


def run_instance(
    instance: Instance,
    workspace: Path,
    model: str | None,
    timeout: float,
    verbose: bool,
) -> InstanceResult:
    """Set up repo and run the agent for one instance. Returns an InstanceResult."""
    t_start = time.monotonic()
    instance_dir = workspace / instance.instance_id
    instance_dir.mkdir(parents=True, exist_ok=True)
    log_path = instance_dir / "agent.log"
    patch_path = instance_dir / "patch.diff"

    # ── Repo setup ────────────────────────────────────────────────────────
    try:
        repo_dir = setup_repo(instance, workspace)
    except Exception as exc:
        return InstanceResult(
            instance_id=instance.instance_id,
            status="setup_error",
            error=str(exc),
            duration_s=round(time.monotonic() - t_start, 1),
        )

    # ── Build run_task.py command ─────────────────────────────────────────
    task_prompt = build_task_prompt(instance)
    cmd = [
        sys.executable, _RUN_TASK,
        task_prompt,
        "--cwd", str(repo_dir),
        "--output-patch", str(patch_path),
        "--system-prompt", _SWE_BENCH_TEMPLATE,
        "--timeout", str(timeout),
        "--quiet",
    ]
    if model:
        cmd += ["--model", model]

    # ── Run ───────────────────────────────────────────────────────────────
    try:
        with open(log_path, "w", encoding="utf-8") as log_f:
            proc = subprocess.run(
                cmd,
                stdout=log_f,
                stderr=subprocess.STDOUT,
                timeout=timeout + 60,  # outer timeout with buffer
            )
        agent_ok = proc.returncode in (0, 1)  # 0=ok, 1=verify fail (still ran)
    except subprocess.TimeoutExpired:
        return InstanceResult(
            instance_id=instance.instance_id,
            status="agent_error",
            error=f"Outer timeout ({timeout + 60}s) exceeded",
            duration_s=round(time.monotonic() - t_start, 1),
        )
    except Exception as exc:
        return InstanceResult(
            instance_id=instance.instance_id,
            status="agent_error",
            error=str(exc),
            duration_s=round(time.monotonic() - t_start, 1),
        )

    # ── Read patch ────────────────────────────────────────────────────────
    patch = ""
    if patch_path.exists():
        patch = patch_path.read_text(encoding="utf-8")

    status = "ok" if patch.strip() else "no_patch"
    if not agent_ok and proc.returncode == 2:
        status = "agent_error"

    return InstanceResult(
        instance_id=instance.instance_id,
        status=status,
        patch=patch,
        duration_s=round(time.monotonic() - t_start, 1),
    )


# ── Results output ────────────────────────────────────────────────────────────


def write_predictions(results: list[InstanceResult], output: Path, model_name: str) -> None:
    """Write SWE-bench predictions JSON (one entry per instance)."""
    predictions = [
        {
            "instance_id": r.instance_id,
            "model_patch": r.patch,
            "model_name_or_path": model_name,
        }
        for r in results
    ]
    output.write_text(json.dumps(predictions, indent=2), encoding="utf-8")


def write_summary(results: list[InstanceResult], output: Path) -> None:
    """Write an aggregate run summary."""
    total = len(results)
    by_status: dict[str, int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1

    summary = {
        "total": total,
        "by_status": by_status,
        "patched": by_status.get("ok", 0),
        "patch_rate": round(by_status.get("ok", 0) / total, 3) if total else 0,
        "avg_duration_s": round(
            sum(r.duration_s for r in results) / total, 1
        ) if total else 0,
        "instances": [
            {
                "instance_id": r.instance_id,
                "status": r.status,
                "patch_lines": r.patch.count("\n"),
                "duration_s": r.duration_s,
                "error": r.error or None,
            }
            for r in results
        ],
    }
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")


# ── CLI ───────────────────────────────────────────────────────────────────────


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="swe_bench_run",
        description="Run GAAT against SWE-bench task instances.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--dataset", required=True, metavar="FILE",
                   help="Path to SWE-bench JSONL dataset file.")
    p.add_argument("--workspace", default="./swe_workspace", metavar="DIR",
                   help="Directory for cloned repos and output (default: ./swe_workspace).")
    p.add_argument("--instances", nargs="*", metavar="ID",
                   help="Run only these instance IDs (default: all).")
    p.add_argument("--model", "-m", metavar="MODEL",
                   help="Model override passed to run_task.py.")
    p.add_argument("--workers", "-w", type=int, default=2, metavar="N",
                   help="Parallel workers (default: 2). Keep low to avoid rate limits.")
    p.add_argument("--timeout", "-t", type=float, default=300, metavar="SECONDS",
                   help="Per-instance agent timeout in seconds (default: 300).")
    p.add_argument("--output", "-o", default="predictions.json", metavar="FILE",
                   help="Predictions output file (default: predictions.json).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print instances without running the agent.")
    p.add_argument("--verbose", action="store_true",
                   help="Stream agent output to terminal (disables parallel display).")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    # ── Load dataset ──────────────────────────────────────────────────────
    if not Path(args.dataset).exists():
        print(f"swe_bench_run: dataset not found: {args.dataset}", file=sys.stderr)
        sys.exit(1)

    all_instances = load_dataset(args.dataset)
    if not all_instances:
        print("swe_bench_run: no instances loaded from dataset", file=sys.stderr)
        sys.exit(1)

    # Filter to requested instances.
    if args.instances:
        wanted = set(args.instances)
        instances = [i for i in all_instances if i.instance_id in wanted]
        missing = wanted - {i.instance_id for i in instances}
        if missing:
            print(f"  warning: instances not found in dataset: {', '.join(sorted(missing))}",
                  file=sys.stderr)
    else:
        instances = all_instances

    total = len(instances)
    model_label = args.model or "gaat-default"

    print(f"── dataset:    {args.dataset} ({len(all_instances)} total, {total} selected)")
    print(f"── workspace:  {workspace}")
    print(f"── model:      {model_label}")
    print(f"── workers:    {args.workers}")
    print(f"── timeout:    {args.timeout}s per instance")
    print(f"── output:     {args.output}")

    if args.dry_run:
        print(f"\nDry run — {total} instances would be processed:\n")
        for inst in instances:
            preview = inst.problem_statement[:80].replace("\n", " ")
            print(f"  {inst.instance_id:45s}  {inst.repo}@{inst.base_commit[:8]}  {preview}…")
        return

    print()

    # ── Run instances ─────────────────────────────────────────────────────
    results: list[InstanceResult] = []
    t_run_start = time.monotonic()

    def _run_one(inst: Instance) -> InstanceResult:
        r = run_instance(inst, workspace, args.model, args.timeout, args.verbose)
        # Progress line written immediately as each instance completes.
        icon = "✓" if r.status == "ok" else "✗"
        print(
            f"  {icon} {r.instance_id:45s}  {r.status:12s}  {r.duration_s:5.0f}s  "
            f"{r.patch.count(chr(10)):4d} patch lines",
            flush=True,
        )
        return r

    if args.workers == 1:
        for inst in instances:
            results.append(_run_one(inst))
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(_run_one, inst): inst for inst in instances}
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as exc:
                    inst = futures[future]
                    results.append(InstanceResult(
                        instance_id=inst.instance_id,
                        status="agent_error",
                        error=str(exc),
                    ))

    # ── Write output ──────────────────────────────────────────────────────
    predictions_path = Path(args.output)
    summary_path = workspace / "run_summary.json"

    write_predictions(results, predictions_path, model_label)
    write_summary(results, summary_path)

    # ── Print summary ─────────────────────────────────────────────────────
    elapsed = time.monotonic() - t_run_start
    ok = sum(1 for r in results if r.status == "ok")
    errors = sum(1 for r in results if r.status in ("agent_error", "setup_error"))

    print(f"\n── Results ─────────────────────────────────────────────────")
    print(f"   Patched:     {ok}/{total}  ({100*ok//total if total else 0}%)")
    print(f"   No patch:    {sum(1 for r in results if r.status == 'no_patch')}")
    print(f"   Errors:      {errors}")
    print(f"   Total time:  {elapsed:.0f}s  ({elapsed/total:.0f}s avg)")
    print(f"\n   Predictions: {predictions_path}")
    print(f"   Summary:     {summary_path}")
    print(f"\nNext step: evaluate with SWE-bench harness:")
    print(f"  python -m swebench.harness.run_evaluation \\")
    print(f"    --predictions_path {predictions_path} \\")
    print(f"    --swe_bench_tasks {args.dataset} \\")
    print(f"    --log_dir {workspace}/eval_logs")


if __name__ == "__main__":
    main()

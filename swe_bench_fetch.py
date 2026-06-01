#!/usr/bin/env python3
"""
swe_bench_fetch.py — Download a slice of SWE-bench Lite from HuggingFace.

Uses the HuggingFace Datasets Server API (no extra dependencies beyond httpx,
which is already a GAAT dependency). No account or API key required for
public datasets.

Usage:
  # Fetch 5 instances and save to sample.jsonl
  python swe_bench_fetch.py

  # Fetch 20 instances, pick a different dataset
  python swe_bench_fetch.py --count 20 --output my_sample.jsonl

  # Fetch from full SWE-bench instead of Lite
  python swe_bench_fetch.py --dataset princeton-nlp/SWE-bench --count 10

  # Print what would be fetched without saving
  python swe_bench_fetch.py --dry-run

Then run the agent against the sample:
  python swe_bench_run.py --dataset sample.jsonl --limit 5 --workers 1

Exit codes:
  0  Instances written successfully
  1  Network or parse error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

_DEFAULT_DATASET = "princeton-nlp/SWE-bench_Lite"
_DEFAULT_COUNT = 5
_DEFAULT_OUTPUT = "sample.jsonl"
_HF_ROWS_API = "https://datasets-server.huggingface.co/rows"

# Fields SWE-bench returns as JSON-encoded strings rather than native lists.
_JSON_LIST_FIELDS = ("FAIL_TO_PASS", "PASS_TO_PASS")


def fetch_instances(
    dataset: str,
    count: int,
    split: str = "test",
    offset: int = 0,
) -> list[dict]:
    """
    Fetch `count` rows from a HuggingFace dataset via the Datasets Server API.

    Returns a list of raw row dicts.
    Raises RuntimeError on HTTP or parse failures.
    """
    try:
        import httpx
    except ImportError:
        raise RuntimeError("httpx is required: pip install httpx")

    params = {
        "dataset": dataset,
        "config": "default",
        "split": split,
        "offset": offset,
        "length": min(count, 100),  # API caps at 100 per request
    }

    try:
        response = httpx.get(_HF_ROWS_API, params=params, timeout=30)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(
            f"HuggingFace API returned {e.response.status_code}: {e.response.text[:200]}"
        )
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error fetching dataset: {e}")

    try:
        data = response.json()
        rows = [r["row"] for r in data["rows"]]
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Unexpected API response format: {e}")

    # If count > 100 we need multiple requests.
    if count > 100 and len(rows) == 100:
        rows += fetch_instances(dataset, count - 100, split, offset + 100)

    return rows[:count]


def normalise_instance(row: dict) -> dict:
    """
    Normalise a raw HuggingFace row into a clean SWE-bench instance dict.

    HuggingFace sometimes returns FAIL_TO_PASS / PASS_TO_PASS as
    JSON-encoded strings (e.g. '["test_foo"]') rather than native lists.
    """
    out = dict(row)
    for field in _JSON_LIST_FIELDS:
        val = out.get(field, [])
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except json.JSONDecodeError:
                val = [val] if val else []
        out[field] = val
    return out


def write_jsonl(instances: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for inst in instances:
            f.write(json.dumps(inst) + "\n")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="swe_bench_fetch",
        description="Download a slice of SWE-bench Lite from HuggingFace.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--dataset", default=_DEFAULT_DATASET, metavar="REPO",
                   help=f"HuggingFace dataset repo (default: {_DEFAULT_DATASET}).")
    p.add_argument("--count", "-n", type=int, default=_DEFAULT_COUNT, metavar="N",
                   help=f"Number of instances to fetch (default: {_DEFAULT_COUNT}).")
    p.add_argument("--offset", type=int, default=0, metavar="N",
                   help="Start offset into the dataset (default: 0).")
    p.add_argument("--split", default="test", metavar="SPLIT",
                   help="Dataset split to use (default: test).")
    p.add_argument("--output", "-o", default=_DEFAULT_OUTPUT, metavar="FILE",
                   help=f"Output JSONL file (default: {_DEFAULT_OUTPUT}).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print instance IDs without saving.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    print(f"── dataset: {args.dataset}  split={args.split}  "
          f"offset={args.offset}  count={args.count}")

    try:
        raw = fetch_instances(args.dataset, args.count, args.split, args.offset)
    except RuntimeError as e:
        print(f"swe_bench_fetch: error: {e}", file=sys.stderr)
        sys.exit(1)

    instances = [normalise_instance(r) for r in raw]

    if args.dry_run:
        print(f"\n{len(instances)} instances (dry run — not saved):\n")
        for inst in instances:
            preview = inst.get("problem_statement", "")[:70].replace("\n", " ")
            print(f"  {inst['instance_id']:45s}  {inst['repo']}  {preview}…")
        return

    out = Path(args.output)
    write_jsonl(instances, out)

    print(f"\n── wrote {len(instances)} instances → {out}")
    print(f"\nInstance IDs:")
    for inst in instances:
        n_fail = len(inst.get("FAIL_TO_PASS", []))
        n_pass = len(inst.get("PASS_TO_PASS", []))
        print(f"  {inst['instance_id']:45s}  fail={n_fail}  pass={n_pass}")

    print(f"\nNext: run the agent against this sample:")
    print(f"  python swe_bench_run.py --dataset {out} --limit {len(instances)} --workers 1")


if __name__ == "__main__":
    main()

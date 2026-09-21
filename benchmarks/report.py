#!/usr/bin/env python3
"""Generate an honest CQO benchmark report from paired JSONL observations."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

VARIANTS = {"baseline", "cqo"}
MODES = {"controlled", "full-policy"}
NUMERIC_METRICS = (
    "files_inspected",
    "files_changed",
    "searches",
    "focused_checks",
    "broad_checks",
    "subagents",
    "model_escalations",
    "repeated_reads",
    "wall_seconds",
)


class BenchmarkError(ValueError):
    pass


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise BenchmarkError(
                    f"{path}:{lineno}: invalid JSON: {exc.msg}"
                ) from exc
            validate_row(row, path, lineno)
            rows.append(row)
    return rows


def validate_row(row: dict[str, Any], path: Path | None = None, lineno: int | None = None) -> None:
    where = ""
    if path is not None and lineno is not None:
        where = f"{path}:{lineno}: "

    required = ("case_id", "pair_id", "variant", "benchmark_mode", "acceptance_passed")
    missing = [key for key in required if key not in row]
    if missing:
        raise BenchmarkError(f"{where}missing required field(s): {', '.join(missing)}")

    if row["variant"] not in VARIANTS:
        raise BenchmarkError(f"{where}variant must be baseline or cqo")
    if row["benchmark_mode"] not in MODES:
        raise BenchmarkError(f"{where}benchmark_mode must be controlled or full-policy")
    if not isinstance(row["acceptance_passed"], bool):
        raise BenchmarkError(f"{where}acceptance_passed must be boolean")

    for metric in NUMERIC_METRICS:
        if metric not in row:
            continue
        value = row[metric]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise BenchmarkError(f"{where}{metric} must be a non-negative number")


def pair_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        key = (row["case_id"], row["pair_id"], row["benchmark_mode"])
        variant = row["variant"]
        if variant in grouped[key]:
            raise BenchmarkError(
                f"duplicate {variant} record for case={key[0]} pair={key[1]} mode={key[2]}"
            )
        grouped[key][variant] = row

    pairs: list[dict[str, Any]] = []
    for (case_id, pair_id, mode), variants in sorted(grouped.items()):
        baseline = variants.get("baseline")
        cqo = variants.get("cqo")
        matched = baseline is not None and cqo is not None
        acceptance_eligible = bool(
            matched
            and baseline["acceptance_passed"]
            and cqo["acceptance_passed"]
        )
        pairs.append(
            {
                "case_id": case_id,
                "pair_id": pair_id,
                "benchmark_mode": mode,
                "baseline": baseline,
                "cqo": cqo,
                "matched": matched,
                "acceptance_eligible": acceptance_eligible,
            }
        )
    return pairs


def metric_delta(pair: dict[str, Any], metric: str) -> float | int | None:
    if not pair["acceptance_eligible"]:
        return None
    baseline = pair["baseline"]
    cqo = pair["cqo"]
    if metric not in baseline or metric not in cqo:
        return None
    return cqo[metric] - baseline[metric]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = pair_rows(rows)
    eligible = [pair for pair in pairs if pair["acceptance_eligible"]]

    metrics: dict[str, Any] = {}
    for metric in NUMERIC_METRICS:
        deltas = [
            delta
            for pair in eligible
            if (delta := metric_delta(pair, metric)) is not None
        ]
        metrics[metric] = {
            "paired_observations": len(deltas),
            "median_delta": statistics.median(deltas) if deltas else None,
            "deltas": deltas,
        }

    baseline_total = sum(1 for row in rows if row["variant"] == "baseline")
    cqo_total = sum(1 for row in rows if row["variant"] == "cqo")
    baseline_pass = sum(
        1 for row in rows if row["variant"] == "baseline" and row["acceptance_passed"]
    )
    cqo_pass = sum(
        1 for row in rows if row["variant"] == "cqo" and row["acceptance_passed"]
    )

    return {
        "records": len(rows),
        "pairs_total": len(pairs),
        "pairs_matched": sum(1 for pair in pairs if pair["matched"]),
        "pairs_acceptance_eligible": len(eligible),
        "baseline": {"runs": baseline_total, "passed": baseline_pass},
        "cqo": {"runs": cqo_total, "passed": cqo_pass},
        "metrics": metrics,
        "pairs": pairs,
        "interpretation": (
            "Negative metric deltas mean CQO used less of that observed resource. "
            "Efficiency deltas are excluded unless both variants passed acceptance."
        ),
    }


def format_number(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float) and not value.is_integer():
        return f"{value:.2f}"
    return str(int(value))


def markdown_report(summary: dict[str, Any]) -> str:
    lines = [
        "# CQO Benchmark Report",
        "",
        f"- Records: {summary['records']}",
        f"- Matched pairs: {summary['pairs_matched']} / {summary['pairs_total']}",
        f"- Acceptance-eligible pairs: {summary['pairs_acceptance_eligible']}",
        f"- Baseline acceptance: {summary['baseline']['passed']} / {summary['baseline']['runs']}",
        f"- CQO acceptance: {summary['cqo']['passed']} / {summary['cqo']['runs']}",
        "",
        "> Negative deltas mean CQO used less of that observable resource. "
        "No efficiency delta is counted unless both runs passed acceptance.",
        "",
        "| Metric | Paired observations | Median CQO − baseline |",
        "|---|---:|---:|",
    ]
    for metric in NUMERIC_METRICS:
        item = summary["metrics"][metric]
        lines.append(
            f"| {metric.replace('_', ' ')} | {item['paired_observations']} | "
            f"{format_number(item['median_delta'])} |"
        )

    lines.extend(
        [
            "",
            "## Pair status",
            "",
            "| Case | Pair | Mode | Baseline pass | CQO pass | Included in efficiency deltas |",
            "|---|---|---|---|---|---|",
        ]
    )
    for pair in summary["pairs"]:
        baseline = pair["baseline"]
        cqo = pair["cqo"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(pair["case_id"]),
                    str(pair["pair_id"]),
                    str(pair["benchmark_mode"]),
                    "yes" if baseline and baseline["acceptance_passed"] else ("no" if baseline else "missing"),
                    "yes" if cqo and cqo["acceptance_passed"] else ("no" if cqo else "missing"),
                    "yes" if pair["acceptance_eligible"] else "no",
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def text_report(summary: dict[str, Any]) -> str:
    lines = [
        "CQO Benchmark Report",
        f"Matched pairs: {summary['pairs_matched']} / {summary['pairs_total']}",
        f"Acceptance-eligible pairs: {summary['pairs_acceptance_eligible']}",
        f"Baseline acceptance: {summary['baseline']['passed']} / {summary['baseline']['runs']}",
        f"CQO acceptance: {summary['cqo']['passed']} / {summary['cqo']['runs']}",
        "Observable median deltas (CQO - baseline):",
    ]
    for metric in NUMERIC_METRICS:
        item = summary["metrics"][metric]
        lines.append(
            f"  {metric}: {format_number(item['median_delta'])} "
            f"(n={item['paired_observations']})"
        )
    lines.append("Negative deltas mean less observed work by CQO.")
    lines.append("Pairs failing acceptance are excluded from efficiency deltas.")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize paired CQO benchmark observations without inventing savings."
    )
    parser.add_argument("results", type=Path, help="JSONL benchmark results file")
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
        help="Output format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rows = load_jsonl(args.results)
        if not rows:
            raise BenchmarkError("results file contains no records")
        summary = summarize(rows)
    except (OSError, BenchmarkError) as exc:
        print(f"benchmark error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(markdown_report(summary), end="")
    else:
        print(text_report(summary), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

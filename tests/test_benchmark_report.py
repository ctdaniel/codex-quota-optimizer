import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "benchmarks" / "report.py"
spec = importlib.util.spec_from_file_location("benchmark_report", SCRIPT)
benchmark_report = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(benchmark_report)


class BenchmarkReportTests(unittest.TestCase):
    def test_only_acceptance_passing_pairs_contribute_deltas(self):
        rows = [
            {
                "case_id": "case-a",
                "pair_id": "p1",
                "variant": "baseline",
                "benchmark_mode": "controlled",
                "acceptance_passed": True,
                "files_inspected": 10,
                "broad_checks": 1,
            },
            {
                "case_id": "case-a",
                "pair_id": "p1",
                "variant": "cqo",
                "benchmark_mode": "controlled",
                "acceptance_passed": True,
                "files_inspected": 4,
                "broad_checks": 0,
            },
            {
                "case_id": "case-b",
                "pair_id": "p1",
                "variant": "baseline",
                "benchmark_mode": "controlled",
                "acceptance_passed": True,
                "files_inspected": 8,
            },
            {
                "case_id": "case-b",
                "pair_id": "p1",
                "variant": "cqo",
                "benchmark_mode": "controlled",
                "acceptance_passed": False,
                "files_inspected": 2,
            },
        ]

        summary = benchmark_report.summarize(rows)

        self.assertEqual(summary["pairs_matched"], 2)
        self.assertEqual(summary["pairs_acceptance_eligible"], 1)
        self.assertEqual(summary["metrics"]["files_inspected"]["median_delta"], -6)
        self.assertEqual(summary["metrics"]["files_inspected"]["paired_observations"], 1)
        self.assertEqual(summary["metrics"]["broad_checks"]["median_delta"], -1)

    def test_missing_metrics_are_not_guessed(self):
        rows = [
            {
                "case_id": "case-a",
                "pair_id": "p1",
                "variant": "baseline",
                "benchmark_mode": "full-policy",
                "acceptance_passed": True,
            },
            {
                "case_id": "case-a",
                "pair_id": "p1",
                "variant": "cqo",
                "benchmark_mode": "full-policy",
                "acceptance_passed": True,
                "searches": 2,
            },
        ]
        summary = benchmark_report.summarize(rows)
        self.assertIsNone(summary["metrics"]["searches"]["median_delta"])
        self.assertEqual(summary["metrics"]["searches"]["paired_observations"], 0)

    def test_jsonl_validation_and_markdown_report(self):
        records = [
            {
                "case_id": "case-a",
                "pair_id": "p1",
                "variant": "baseline",
                "benchmark_mode": "controlled",
                "acceptance_passed": True,
                "subagents": 1,
            },
            {
                "case_id": "case-a",
                "pair_id": "p1",
                "variant": "cqo",
                "benchmark_mode": "controlled",
                "acceptance_passed": True,
                "subagents": 0,
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.jsonl"
            path.write_text(
                "\n".join(json.dumps(item) for item in records) + "\n",
                encoding="utf-8",
            )
            rows = benchmark_report.load_jsonl(path)
            report = benchmark_report.markdown_report(
                benchmark_report.summarize(rows)
            )

        self.assertIn("Acceptance-eligible pairs: 1", report)
        self.assertIn("| subagents | 1 | -1 |", report)

    def test_duplicate_variant_in_pair_is_rejected(self):
        row = {
            "case_id": "case-a",
            "pair_id": "p1",
            "variant": "baseline",
            "benchmark_mode": "controlled",
            "acceptance_passed": True,
        }
        with self.assertRaises(benchmark_report.BenchmarkError):
            benchmark_report.pair_rows([row, dict(row)])


if __name__ == "__main__":
    unittest.main()

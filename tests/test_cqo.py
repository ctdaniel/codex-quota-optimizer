import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "codex-quota-optimizer"
    / "scripts"
    / "cqo.py"
)
spec = importlib.util.spec_from_file_location("cqo", SCRIPT)
cqo = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cqo)


class CqoTests(unittest.TestCase):
    def test_simple_bug_defaults_to_small(self):
        self.assertEqual(cqo.classify_task("Fix checkout bug")["size"], "S")

    def test_mechanical_change_can_stay_xs(self):
        self.assertEqual(cqo.classify_task("Fix README typo")["size"], "XS")

    def test_high_risk_task_escalates_risk(self):
        result = cqo.classify_task(
            "Migrate production authentication database schema"
        )
        self.assertEqual(result["risk"], "high")
        self.assertIn(result["size"], {"L", "XL"})

    def test_chinese_high_risk_task_is_recognized(self):
        result = cqo.classify_task("迁移生产环境的支付数据库权限")
        self.assertEqual(result["risk"], "high")
        self.assertIn(result["size"], {"L", "XL"})

    def test_emergency_budget_is_soft_and_no_subagents(self):
        budget = cqo.make_budget("M", "emergency")
        self.assertEqual(budget["budget_type"], "soft")
        self.assertEqual(budget["subagents"], "no")
        self.assertEqual(budget["implementation_paths"], 1)

    def test_local_session_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"CQO_HOME": tmp}, clear=False):
                session = cqo.start_session(
                    "Fix checkout bug",
                    "economy",
                    cwd=tmp,
                )
                self.assertEqual(session["status"], "active")
                self.assertTrue(cqo.current_path().exists())

                audit = cqo.audit_session("unit-test", cwd=tmp)
                self.assertIsNotNone(audit)
                self.assertEqual(audit["status"], "completed")
                self.assertFalse(cqo.current_path().exists())

                history = cqo.load_history(10)
                self.assertEqual(len(history), 1)
                self.assertEqual(history[0]["note"], "unit-test")

    def test_doctor_reports_required_setup(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"CQO_HOME": tmp}, clear=False):
                report = cqo.doctor_report()
                self.assertTrue(report["python"]["ok"])
                self.assertTrue(report["skill"]["ok"])
                self.assertTrue(report["journal"]["writable"])
                self.assertEqual(report["network_checks"], 0)
                self.assertTrue(report["ok"])


if __name__ == "__main__":
    unittest.main()

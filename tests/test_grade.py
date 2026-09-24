import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("grade", ROOT / "scripts/grade.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GradeTests(unittest.TestCase):
    def test_example_passes(self):
        cases = json.loads((ROOT / "examples/cases.json").read_text(encoding="utf-8"))
        results = json.loads((ROOT / "examples/results.json").read_text(encoding="utf-8"))
        self.assertTrue(MODULE.grade(cases, results)["passed"])

    def test_blocking_failure_wins(self):
        spec = {"threshold": 0, "cases": [{"id": "x", "assertions": [{"type": "not_contains", "value": "secret", "blocking": True}]}]}
        report = MODULE.grade(spec, {"results": [{"id": "x", "transcript": "secret"}]})
        self.assertFalse(report["passed"])
        self.assertEqual(report["blocking_failures"], 1)


if __name__ == "__main__":
    unittest.main()

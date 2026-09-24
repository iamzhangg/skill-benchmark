#!/usr/bin/env python3
"""Grade saved Agent Skill results against deterministic assertions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def _json_path(data: Any, path: str) -> Any:
    current = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def check(assertion: dict, result: dict) -> tuple[bool, str]:
    transcript = result.get("transcript", "")
    kind, expected = assertion.get("type"), assertion.get("value")
    if kind == "contains":
        ok = str(expected).casefold() in transcript.casefold()
    elif kind == "not_contains":
        ok = str(expected).casefold() not in transcript.casefold()
    elif kind == "regex":
        ok = re.search(str(expected), transcript, flags=re.IGNORECASE | re.MULTILINE) is not None
    elif kind == "file_exists":
        ok = expected in result.get("files", [])
    elif kind == "json_path":
        ok = _json_path(result.get("data", {}), assertion.get("path", "")) == expected
    else:
        return False, f"unknown assertion type: {kind}"
    return ok, f"{kind}={expected!r}"


def grade(spec: dict, results: dict) -> dict:
    by_id = {item["id"]: item for item in results.get("results", [])}
    details, passed_count, total, blocking_failures = [], 0, 0, 0
    for case in spec.get("cases", []):
        checks = []
        for assertion in case.get("assertions", []):
            total += 1
            ok, label = check(assertion, by_id.get(case["id"], {}))
            passed_count += int(ok)
            blocking = assertion.get("blocking", False)
            blocking_failures += int(not ok and blocking)
            checks.append({"passed": ok, "label": label, "blocking": blocking})
        details.append({"id": case["id"], "checks": checks})
    score = passed_count / total if total else 0.0
    threshold = float(spec.get("threshold", 1.0))
    return {"suite": spec.get("suite", "unnamed"), "score": score,
            "passed_assertions": passed_count, "total_assertions": total,
            "blocking_failures": blocking_failures,
            "passed": score >= threshold and blocking_failures == 0, "details": details}


def render(report: dict) -> str:
    mark = "PASS" if report["passed"] else "FAIL"
    lines = [f"# Benchmark: {report['suite']}", "",
             f"**{mark}** - {report['passed_assertions']}/{report['total_assertions']} assertions ({report['score']:.0%}); {report['blocking_failures']} blocking failures.", ""]
    for case in report["details"]:
        lines.append(f"## {case['id']}")
        for item in case["checks"]:
            symbol = "PASS" if item["passed"] else "FAIL"
            blocking = " (blocking)" if item["blocking"] else ""
            lines.append(f"- {symbol}: `{item['label']}`{blocking}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = grade(json.loads(args.cases.read_text(encoding="utf-8")),
                   json.loads(args.results.read_text(encoding="utf-8")))
    output = render(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

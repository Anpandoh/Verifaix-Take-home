from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from .schemas import ExecutionResult, TestStatus

TP_ID_RE = re.compile(r"TP_\d+(?:\.\d+)?")


def run_pytest_for_version(version: str, generated_dir: Path | str) -> list[ExecutionResult]:
    root = Path(generated_dir)
    test_file = root / "tests" / version / "test_generated.py"
    code_dir = root / "code" / version
    tests = discover_tests(test_file)
    results: list[ExecutionResult] = []

    for test_name, tp_ids in tests:
        start = time.perf_counter()
        command = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            f"{test_file}::{test_name}",
            "--tb=short",
        ]
        env = os.environ.copy()
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            str(code_dir)
            if not existing_pythonpath
            else f"{code_dir}{os.pathsep}{existing_pythonpath}"
        )
        proc = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
        duration = time.perf_counter() - start
        status = TestStatus.passed if proc.returncode == 0 else TestStatus.failed
        failure_message = None if status == TestStatus.passed else (proc.stdout + proc.stderr).strip()
        results.append(
            ExecutionResult(
                version=version,
                test_name=test_name,
                test_plan_item_ids=tp_ids,
                status=status,
                failure_message=failure_message,
                duration_seconds=duration,
            )
        )

    if not tests:
        results.append(
            ExecutionResult(
                version=version,
                test_name="collection",
                test_plan_item_ids=[],
                status=TestStatus.error,
                failure_message=f"No tests discovered in {test_file}",
            )
        )
    return results


def discover_tests(test_file: Path) -> list[tuple[str, list[str]]]:
    if not test_file.exists():
        return []
    tree = ast.parse(test_file.read_text(encoding="utf-8"))
    tests: list[tuple[str, list[str]]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            docstring = ast.get_docstring(node) or ""
            ids = sorted(set(TP_ID_RE.findall(f"{node.name} {docstring}")))
            tests.append((node.name, ids))
    return tests

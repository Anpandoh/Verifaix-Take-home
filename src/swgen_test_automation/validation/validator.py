from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

from ..constants import TEST_PLAN_ID_PATTERN
from ..db import Repository
from ..schemas import (
    ArtifactRecord,
    DeltaSummary,
    DeltaSummaryItem,
    ProgramFunctionSummary,
    ProgramSummary,
    TestPlan,
    TraceabilityRow,
    ValidationIssue,
    ValidationReport,
    ValidationSeverity,
)

REQUIRED_ARTIFACT_TYPES = {
    "test_plan": "Generated test plan JSON",
    "generated_code": "Generated Python module",
    "generated_tests": "Generated pytest code",
    "execution_results": "Stored test execution results",
}


def validate_version(version: str, repo: Repository) -> ValidationReport:
    plan = repo.get_test_plan(version)
    artifacts = repo.get_artifacts(version)
    generated_code_records = repo.get_generated_code(version)
    generated_test_records = repo.get_generated_tests(version)
    results = repo.get_execution_results(version)
    description = repo.get_description(version)
    deltas = repo.get_deltas(version)

    issues: list[ValidationIssue] = []
    artifact_by_type = _artifact_by_type(artifacts)

    _validate_presence(
        version,
        plan,
        description,
        artifact_by_type,
        generated_code_records,
        generated_test_records,
        results,
        issues,
    )
    _validate_artifact_files(artifact_by_type, issues)

    code_path = _first_artifact_path(artifact_by_type, "generated_code")
    tests_path = _first_artifact_path(artifact_by_type, "generated_tests")

    if code_path:
        _validate_python_syntax(code_path, "generated_code_syntax", issues)
        _validate_generated_code_imports(code_path, issues)
        _validate_generated_code_style(code_path, issues)
    if tests_path:
        _validate_python_syntax(tests_path, "generated_tests_syntax", issues)
        _validate_generated_tests_style(tests_path, issues)

    discovered_tests = _discover_test_references(tests_path) if tests_path else {}
    if plan:
        _validate_traceability(plan, discovered_tests, results, issues)

    traceability = _build_traceability(plan, discovered_tests, results)
    program_summary = _build_program_summary(code_path)
    delta_summary = _build_delta_summary(version, deltas)
    summary = _build_summary(
        version,
        description is not None,
        plan,
        artifacts,
        generated_code_records,
        generated_test_records,
        results,
    )

    return ValidationReport(
        version=version,
        summary=summary,
        program_summary=program_summary,
        delta_summary=delta_summary,
        issues=issues,
        traceability=traceability,
    )


def _artifact_by_type(artifacts: list[ArtifactRecord]) -> dict[str, list[ArtifactRecord]]:
    grouped: dict[str, list[ArtifactRecord]] = defaultdict(list)
    for artifact in artifacts:
        grouped[artifact.artifact_type].append(artifact)
    return dict(grouped)


def _validate_presence(
    version: str,
    plan: TestPlan | None,
    description_exists: bool,
    artifact_by_type: dict[str, list[ArtifactRecord]],
    generated_code_records: list,
    generated_test_records: list,
    results: list,
    issues: list[ValidationIssue],
) -> None:
    if not description_exists:
        _add_issue(issues, "error", "description_exists", f"No description stored for {version}.")
    if plan is None:
        _add_issue(issues, "error", "test_plan_exists", f"No test plan stored for {version}.")
    elif not plan.items:
        _add_issue(issues, "error", "test_plan_items", "Test plan has no items.")

    for artifact_type, label in REQUIRED_ARTIFACT_TYPES.items():
        if artifact_type not in artifact_by_type:
            _add_issue(issues, "error", f"{artifact_type}_artifact", f"Missing {label}.")

    if not generated_code_records:
        _add_issue(issues, "error", "generated_code_record", "No generated code row stored.")
    if not generated_test_records:
        _add_issue(issues, "error", "generated_test_records", "No generated test rows stored.")
    if not results:
        _add_issue(issues, "warning", "execution_results", "No execution results stored.")


def _validate_artifact_files(
    artifact_by_type: dict[str, list[ArtifactRecord]],
    issues: list[ValidationIssue],
) -> None:
    for artifact_type, artifacts in artifact_by_type.items():
        for artifact in artifacts:
            if not artifact.path.exists():
                _add_issue(
                    issues,
                    "error",
                    "artifact_file_exists",
                    f"{artifact_type} file does not exist: {artifact.path}",
                )


def _validate_python_syntax(path: Path, check_name: str, issues: list[ValidationIssue]) -> None:
    if not path.exists():
        return
    try:
        ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        _add_issue(issues, "error", check_name, f"{path} has syntax error: {exc}")


def _validate_generated_code_imports(path: Path, issues: list[ValidationIssue]) -> None:
    if not path.exists():
        return
    env = os.environ.copy()
    env["PYTHONPATH"] = str(path.parent)
    module_name = path.stem
    proc = subprocess.run(
        [sys.executable, "-c", f"import {module_name}"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        _add_issue(
            issues,
            "error",
            "generated_code_imports",
            f"Could not import {module_name}: {(proc.stderr or proc.stdout).strip()}",
        )


def _validate_generated_code_style(path: Path, issues: list[ValidationIssue]) -> None:
    if not path.exists():
        return
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            missing_arg_annotations = [
                arg.arg for arg in node.args.args if arg.annotation is None and arg.arg != "self"
            ]
            if missing_arg_annotations or node.returns is None:
                _add_issue(
                    issues,
                    "warning",
                    "generated_code_annotations",
                    f"{node.name} is missing argument or return type annotations.",
                )


def _validate_generated_tests_style(path: Path, issues: list[ValidationIssue]) -> None:
    if not path.exists():
        return
    tree = ast.parse(path.read_text(encoding="utf-8"))
    import_statements: list[str] = []
    seen_non_import = False
    imports_after_tests = 0
    for node in tree.body:
        if isinstance(node, ast.Import):
            import_statements.extend(alias.name for alias in node.names)
            if seen_non_import:
                imports_after_tests += 1
        elif isinstance(node, ast.ImportFrom):
            import_statements.append(f"{node.module}:{','.join(alias.name for alias in node.names)}")
            if seen_non_import:
                imports_after_tests += 1
        else:
            seen_non_import = True

    duplicate_imports = [
        import_name for import_name, count in Counter(import_statements).items() if count > 1
    ]
    if duplicate_imports:
        _add_issue(
            issues,
            "warning",
            "generated_tests_duplicate_imports",
            f"Generated tests repeat imports: {', '.join(sorted(duplicate_imports))}.",
        )
    if imports_after_tests:
        _add_issue(
            issues,
            "warning",
            "generated_tests_import_order",
            "Generated tests contain imports after test functions.",
        )


def _discover_test_references(test_path: Path | None) -> dict[str, list[str]]:
    if test_path is None or not test_path.exists():
        return {}
    tree = ast.parse(test_path.read_text(encoding="utf-8"))
    references: dict[str, list[str]] = {}
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            names.append(node.name)
            docstring = ast.get_docstring(node) or ""
            tp_ids = sorted(set(re.findall(TEST_PLAN_ID_PATTERN, f"{node.name} {docstring}")))
            references[node.name] = tp_ids

    duplicates = [name for name, count in Counter(names).items() if count > 1]
    if duplicates:
        references["__duplicate_test_names__"] = duplicates
    return references


def _validate_traceability(
    plan: TestPlan,
    test_references: dict[str, list[str]],
    results: list,
    issues: list[ValidationIssue],
) -> None:
    plan_ids = {item.id for item in plan.items}
    test_to_ids = {
        test_name: ids
        for test_name, ids in test_references.items()
        if test_name != "__duplicate_test_names__"
    }
    referenced_ids = {tp_id for ids in test_to_ids.values() for tp_id in ids}
    result_ids = {tp_id for result in results for tp_id in result.test_plan_item_ids}

    for item_id in sorted(plan_ids - referenced_ids, key=_natural_tp_sort_key):
        _add_issue(issues, "error", "plan_item_has_test", f"{item_id} has no generated test.")
    for item_id in sorted(referenced_ids - plan_ids, key=_natural_tp_sort_key):
        _add_issue(issues, "error", "test_references_known_tp", f"Generated test references unknown {item_id}.")
    for item_id in sorted(result_ids - plan_ids, key=_natural_tp_sort_key):
        _add_issue(issues, "error", "result_references_known_tp", f"Result references unknown {item_id}.")

    for test_name, ids in sorted(test_to_ids.items()):
        if not ids:
            _add_issue(issues, "warning", "test_has_tp_reference", f"{test_name} has no TP ID reference.")

    for duplicate in test_references.get("__duplicate_test_names__", []):
        _add_issue(issues, "error", "duplicate_test_names", f"Duplicate generated test function: {duplicate}")

    failed_results = [result for result in results if result.status.value != "passed"]
    for result in failed_results:
        _add_issue(
            issues,
            "error",
            "test_result_passed",
            f"{result.test_name} ended with status {result.status.value}.",
        )


def _build_traceability(
    plan: TestPlan | None,
    test_references: dict[str, list[str]],
    results: list,
) -> list[TraceabilityRow]:
    if plan is None:
        return []
    tests_by_tp: dict[str, list[str]] = defaultdict(list)
    for test_name, tp_ids in test_references.items():
        if test_name == "__duplicate_test_names__":
            continue
        for tp_id in tp_ids:
            tests_by_tp[tp_id].append(test_name)

    statuses_by_tp: dict[str, list[str]] = defaultdict(list)
    for result in results:
        for tp_id in result.test_plan_item_ids:
            statuses_by_tp[tp_id].append(result.status.value)

    rows = [
        TraceabilityRow(
            source_sections=item.source_sections,
            test_plan_id=item.id,
            requirement=item.description,
            test_functions=sorted(tests_by_tp.get(item.id, [])),
            result_statuses=sorted(set(statuses_by_tp.get(item.id, []))),
        )
        for item in plan.items
    ]
    return sorted(rows, key=lambda row: _natural_tp_sort_key(row.test_plan_id))


def _build_program_summary(code_path: Path | None) -> ProgramSummary:
    if code_path is None or not code_path.exists():
        return ProgramSummary()

    source = code_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    functions: list[ProgramFunctionSummary] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.extend(f"{module}.{alias.name}" for alias in node.names)
        elif isinstance(node, ast.FunctionDef):
            functions.append(_summarize_function(node))

    return ProgramSummary(
        module_name=code_path.stem,
        imports=sorted(imports),
        functions=functions,
        behavior_summary=_behavior_summary(functions),
    )


def _build_delta_summary(version: str, deltas) -> DeltaSummary:
    if deltas is None:
        return DeltaSummary(new_version=version)

    items = [
        DeltaSummaryItem(
            id=item.id,
            change_type=item.change_type,
            item_id=item.item_id,
            before=item.before,
            after=item.after,
        )
        for item in sorted(deltas.items, key=lambda item: _natural_delta_sort_key(item.id))
    ]
    return DeltaSummary(
        old_version=deltas.old_version,
        new_version=deltas.new_version,
        added=sum(1 for item in items if item.change_type.value == "added"),
        removed=sum(1 for item in items if item.change_type.value == "removed"),
        modified=sum(1 for item in items if item.change_type.value == "modified"),
        items=items,
    )


def _summarize_function(node: ast.FunctionDef) -> ProgramFunctionSummary:
    parameters = []
    for arg in node.args.args:
        if arg.annotation is None:
            parameters.append(arg.arg)
        else:
            parameters.append(f"{arg.arg}: {_unparse(arg.annotation)}")

    return ProgramFunctionSummary(
        name=node.name,
        parameters=parameters,
        returns=_unparse(node.returns) if node.returns is not None else None,
        docstring=ast.get_docstring(node),
        raises=sorted(_raised_exception_names(node)),
    )


def _raised_exception_names(node: ast.FunctionDef) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Raise) and child.exc is not None:
            if isinstance(child.exc, ast.Call):
                names.add(_unparse(child.exc.func))
            else:
                names.add(_unparse(child.exc))
    return names


def _behavior_summary(functions: list[ProgramFunctionSummary]) -> str:
    if not functions:
        return "The generated module does not define any top-level functions."
    parts = []
    for function in functions:
        signature = f"{function.name}({', '.join(function.parameters)})"
        if function.returns:
            signature += f" -> {function.returns}"
        description = _first_docstring_sentence(function.docstring)
        if function.raises:
            description += f" It raises {', '.join(function.raises)} for error cases."
        parts.append(f"{signature}: {description}")
    return " ".join(parts)


def _first_docstring_sentence(docstring: str | None) -> str:
    if not docstring:
        return "No docstring summary is available."
    first_line = docstring.strip().splitlines()[0].strip()
    return first_line.rstrip(".") + "."


def _unparse(node: ast.AST) -> str:
    return ast.unparse(node)


def _natural_tp_sort_key(value: str) -> tuple[int, ...]:
    match = re.search(TEST_PLAN_ID_PATTERN, value)
    token = match.group(0) if match else value
    numbers = re.findall(r"\d+", token)
    return tuple(int(number) for number in numbers) if numbers else (sys.maxsize,)


def _natural_delta_sort_key(value: str) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", value)
    return tuple(int(number) for number in numbers) if numbers else (sys.maxsize,)


def _build_summary(
    version: str,
    description_exists: bool,
    plan: TestPlan | None,
    artifacts: list[ArtifactRecord],
    generated_code_records: list,
    generated_test_records: list,
    results: list,
) -> dict[str, str | int | bool | None]:
    passed = sum(1 for result in results if result.status.value == "passed")
    return {
        "version": version,
        "description_stored": description_exists,
        "test_plan_items": len(plan.items) if plan else 0,
        "artifact_count": len(artifacts),
        "generated_code_records": len(generated_code_records),
        "generated_test_records": len(generated_test_records),
        "test_results": len(results),
        "tests_passed": passed,
        "tests_failed": len(results) - passed,
    }


def _first_artifact_path(
    artifact_by_type: dict[str, list[ArtifactRecord]],
    artifact_type: str,
) -> Path | None:
    artifacts = artifact_by_type.get(artifact_type, [])
    return artifacts[0].path if artifacts else None


def _add_issue(
    issues: list[ValidationIssue],
    severity: str,
    check_name: str,
    message: str,
) -> None:
    issues.append(
        ValidationIssue(
            severity=ValidationSeverity(severity),
            check_name=check_name,
            message=message,
        )
    )

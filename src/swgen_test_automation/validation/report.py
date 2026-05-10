from __future__ import annotations

from ..schemas import ValidationReport, ValidationSeverity


def render_validation_markdown(report: ValidationReport) -> str:
    lines = [
        f"# Validation Report: {report.version}",
        "",
        "## Artifact Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(
        [
            "",
            "## Generated Program Summary",
            "",
            f"Module: `{report.program_summary.module_name or 'unknown'}`",
            "",
            report.program_summary.behavior_summary,
            "",
        ]
    )
    if report.program_summary.functions:
        lines.extend(["| Function | Parameters | Returns | Raises |", "|---|---|---|---|"])
        for function in report.program_summary.functions:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{function.name}`",
                        ", ".join(f"`{param}`" for param in function.parameters) or "_none_",
                        f"`{function.returns}`" if function.returns else "_missing_",
                        ", ".join(f"`{name}`" for name in function.raises) or "_none_",
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Static Checks",
            "",
        ]
    )

    if report.issues:
        lines.extend(["| Severity | Check | Message |", "|---|---|---|"])
        for issue in report.issues:
            lines.append(
                f"| {issue.severity.value} | `{issue.check_name}` | {_escape_cell(issue.message)} |"
            )
    else:
        lines.append("No issues found.")

    lines.extend(
        [
            "",
            "## Delta Summary",
            "",
            _delta_intro(report),
            "",
        ]
    )
    if report.delta_summary.items:
        lines.extend(["| Delta ID | Type | TP ID | Before | After |", "|---|---|---|---|---|"])
        for item in report.delta_summary.items:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item.id}`",
                        item.change_type.value,
                        f"`{item.item_id}`",
                        _escape_cell(item.before or ""),
                        _escape_cell(item.after or ""),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Traceability Matrix",
            "",
            "| Source Sections | Test Plan ID | Requirement | Test Functions | Results |",
            "|---|---|---|---|---|",
        ]
    )
    for row in report.traceability:
        lines.append(
            "| "
            + " | ".join(
                [
                    ", ".join(row.source_sections),
                    f"`{row.test_plan_id}`",
                    _escape_cell(row.requirement),
                    "<br>".join(f"`{name}`" for name in row.test_functions) or "_missing_",
                    ", ".join(row.result_statuses) or "_missing_",
                ]
            )
            + " |"
        )

    error_count = sum(1 for issue in report.issues if issue.severity == ValidationSeverity.error)
    warning_count = sum(1 for issue in report.issues if issue.severity == ValidationSeverity.warning)
    lines.extend(
        [
            "",
            "## Overall Result",
            "",
            _overall_result(error_count, warning_count),
            "",
        ]
    )
    return "\n".join(lines)


def _overall_result(error_count: int, warning_count: int) -> str:
    if error_count:
        return f"Failed validation with {error_count} error(s) and {warning_count} warning(s)."
    if warning_count:
        return f"Passed with {warning_count} warning(s)."
    return "Passed with no warnings."


def _delta_intro(report: ValidationReport) -> str:
    delta = report.delta_summary
    if not delta.items:
        return "No deltas are stored for this version."
    return (
        f"Compared `{delta.old_version}` → `{delta.new_version}`: "
        f"{delta.added} added, {delta.removed} removed, {delta.modified} modified."
    )


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")

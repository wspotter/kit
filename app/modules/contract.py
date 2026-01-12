"""Tool/module contract for Kit.

A module qualifies as a tool if it lives in `app/modules/*.py` and exposes:

- TOOL_DEFINITION (dict)
- run(payload: dict) -> Any  (callable)

This file defines the data model and validation rules used by both:
- the module registry (to avoid listing/running unsafe tools)
- the validator script (to check submissions offline)

Design goals:
- No mocks: tools should represent real integrations or explicitly return a
  benign "noop" result.
- Deterministic validation: validation must not execute tool logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Literal


AllowedIO = Literal["none", "read", "write"]


@dataclass(frozen=True)
class ToolContract:
    # identity
    id: str
    name: str

    # presentation
    icon: str
    description: str

    # safety / expectations
    version: str
    ralph_loop: bool
    allow_network: AllowedIO
    allow_filesystem: AllowedIO

    # schema-ish (lightweight; avoids extra deps)
    input_schema: Dict[str, Any]


@dataclass(frozen=True)
class ValidationIssue:
    level: Literal["error", "warning"]
    message: str


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    issues: List[ValidationIssue]


REQUIRED_KEYS = {
    "id",
    "name",
    "description",
    "version",
    "ralph_loop",
    "allow_network",
    "allow_filesystem",
    "input_schema",
}


def _issue(level: Literal["error", "warning"], msg: str) -> ValidationIssue:
    return ValidationIssue(level=level, message=msg)


def validate_tool_definition(td: Any) -> ValidationResult:
    issues: List[ValidationIssue] = []

    if not isinstance(td, dict):
        return ValidationResult(ok=False, issues=[_issue("error", "TOOL_DEFINITION must be a dict")])

    missing = sorted(REQUIRED_KEYS - set(td.keys()))
    if missing:
        issues.append(_issue("error", f"Missing required TOOL_DEFINITION keys: {', '.join(missing)}"))

    # Basic types
    if "id" in td and not isinstance(td.get("id"), str):
        issues.append(_issue("error", "TOOL_DEFINITION.id must be a string"))
    if "name" in td and not isinstance(td.get("name"), str):
        issues.append(_issue("error", "TOOL_DEFINITION.name must be a string"))
    if "description" in td and not isinstance(td.get("description"), str):
        issues.append(_issue("error", "TOOL_DEFINITION.description must be a string"))
    if "version" in td and not isinstance(td.get("version"), str):
        issues.append(_issue("error", "TOOL_DEFINITION.version must be a string"))

    if "ralph_loop" in td and not isinstance(td.get("ralph_loop"), bool):
        issues.append(_issue("error", "TOOL_DEFINITION.ralph_loop must be a boolean"))

    for key in ("allow_network", "allow_filesystem"):
        if key in td:
            val = td.get(key)
            if val not in {"none", "read", "write"}:
                issues.append(
                    _issue(
                        "error",
                        f"TOOL_DEFINITION.{key} must be one of: none|read|write",
                    )
                )

    if "input_schema" in td:
        schema = td.get("input_schema")
        if not isinstance(schema, dict):
            issues.append(_issue("error", "TOOL_DEFINITION.input_schema must be a dict"))
        else:
            if schema.get("type") != "object":
                issues.append(_issue("warning", "input_schema.type should be 'object'"))
            props = schema.get("properties")
            if props is not None and not isinstance(props, dict):
                issues.append(_issue("error", "input_schema.properties must be a dict when provided"))

    # No mocks policy
    if td.get("mock") is True:
        issues.append(_issue("error", "mock tools are not allowed"))

    ok = not any(i.level == "error" for i in issues)
    return ValidationResult(ok=ok, issues=issues)


def coerce_contract(td: Dict[str, Any]) -> ToolContract:
    """Convert a validated TOOL_DEFINITION into a typed contract."""

    return ToolContract(
        id=str(td["id"]),
        name=str(td["name"]),
        icon=str(td.get("icon", "tool")),
        description=str(td.get("description", "")),
        version=str(td["version"]),
        ralph_loop=bool(td["ralph_loop"]),
        allow_network=td["allow_network"],
        allow_filesystem=td["allow_filesystem"],
        input_schema=dict(td["input_schema"]),
    )


def format_issues(issues: Iterable[ValidationIssue]) -> str:
    lines: List[str] = []
    for i in issues:
        prefix = "ERROR" if i.level == "error" else "WARN"
        lines.append(f"{prefix}: {i.message}")
    return "\n".join(lines)

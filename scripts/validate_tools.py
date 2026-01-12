"""Validate tool modules under app/modules.

This is an offline safety/quality check. It does NOT execute tool logic.

Exit codes:
- 0: all tools OK
- 2: one or more tools invalid

Usage:
  python scripts/validate_tools.py
"""

from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.modules.contract import format_issues, validate_tool_definition


def iter_module_names() -> List[str]:
    pkg = importlib.import_module("app.modules")
    out: List[str] = []
    for modinfo in pkgutil.iter_modules(pkg.__path__):
        name = modinfo.name
        if name.startswith("_") or name in {"registry", "contract"}:
            continue
        out.append(f"app.modules.{name}")
    return out


def validate_module(full_name: str) -> Tuple[bool, List[str]]:
    issues: List[str] = []

    try:
        module = importlib.import_module(full_name)
    except Exception as e:  # noqa: BLE001
        return False, [f"ERROR: import failed: {e}"]

    td = getattr(module, "TOOL_DEFINITION", None)
    result = validate_tool_definition(td)
    if not result.ok:
        issues.append(format_issues(result.issues))

    runner = getattr(module, "run", None)
    if not callable(runner):
        issues.append("ERROR: missing callable run(payload: dict) -> Any")

    ok = len([i for i in issues if i.startswith("ERROR")]) == 0 and result.ok
    return ok, issues


def main() -> int:
    module_names = iter_module_names()
    if not module_names:
        print("No tool modules found.")
        return 0

    any_bad = False
    for full_name in module_names:
        ok, issues = validate_module(full_name)
        status = "OK" if ok else "FAIL"
        print(f"{status}: {full_name}")
        if issues:
            for block in issues:
                for line in block.splitlines():
                    print(f"  {line}")
        if not ok:
            any_bad = True

    return 2 if any_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

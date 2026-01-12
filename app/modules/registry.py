"""Module discovery & tool registry.

Drop new modules into `app/modules/*.py` and they will automatically show up
in `/modules/list`.

Tool contract (minimal, for now):
- module exposes a dict `TOOL_DEFINITION`
  { id, name, icon, description }
- module optionally exposes `run(payload: dict) -> Any`
"""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import asdict, dataclass
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional

from fastapi import APIRouter, HTTPException

router = APIRouter()


@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    icon: str = "tool"
    description: str = ""
    module: str = ""


TOOLS: Dict[str, Tool] = {}
RUNNERS: Dict[str, Callable[..., Any]] = {}


def _is_loadable_module(name: str) -> bool:
    return not (name.startswith("_") or name in {"registry"})


def _extract_tool(module: ModuleType, fallback_id: str) -> Optional[Tool]:
    td = getattr(module, "TOOL_DEFINITION", None)
    if not isinstance(td, dict):
        return None

    return Tool(
        id=str(td.get("id", fallback_id)),
        name=str(td.get("name", fallback_id)),
        icon=str(td.get("icon", "tool")),
        description=str(td.get("description", "")),
        module=str(td.get("module", module.__name__)),
    )


def discover_tools() -> List[Tool]:
    """Scan `app.modules` and register all tools."""

    TOOLS.clear()
    RUNNERS.clear()

    pkg = importlib.import_module("app.modules")
    for modinfo in pkgutil.iter_modules(pkg.__path__):
        if not _is_loadable_module(modinfo.name):
            continue

        full_name = f"app.modules.{modinfo.name}"
        module = importlib.import_module(full_name)

        tool = _extract_tool(module, fallback_id=modinfo.name)
        if tool:
            TOOLS[tool.id] = tool

        runner = getattr(module, "run", None)
        if tool and callable(runner):
            RUNNERS[tool.id] = runner

    return list(TOOLS.values())


@router.get("/list")
async def list_modules():
    return [asdict(t) for t in discover_tools()]


@router.post("/run/{tool_id}")
async def run_tool(tool_id: str, payload: Dict[str, Any]):
    discover_tools()

    runner = RUNNERS.get(tool_id)
    if not runner:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_id}")

    result = runner(payload)
    return {"tool_id": tool_id, "result": result}

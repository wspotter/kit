"""System Health tool.

Read-only snapshot of system health (no external deps):
- uptime
- load averages
- CPU count
- memory totals (via /proc/meminfo when available)
- disk usage for a target path

Ralph Loop for a read-only tool is light:
- Observe: collect system facts
- Execute: derive summary numbers
- Verify: sanity-check invariants
- Self-correct: retry once if a transient read fails
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


TOOL_DEFINITION = {
    "id": "health",
    "name": "System Health",
    "icon": "activity",
    "description": "Read-only system snapshot: uptime, load, memory, disk.",
    "version": "0.1.0",
    "ralph_loop": True,
    "allow_network": "none",
    "allow_filesystem": "read",
    "input_schema": {
        "type": "object",
        "properties": {
            "disk_path": {"type": "string", "default": "."},
        },
        "required": [],
        "additionalProperties": False,
    },
}


def _read_meminfo() -> Dict[str, int]:
    out: Dict[str, int] = {}
    p = Path("/proc/meminfo")
    if not p.exists():
        return out

    for line in p.read_text().splitlines():
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        parts = rest.strip().split()
        if not parts:
            continue
        try:
            value = int(parts[0])
        except ValueError:
            continue
        unit = parts[1].lower() if len(parts) > 1 else ""
        # meminfo is usually kB
        if unit == "kb":
            out[key] = value * 1024
        else:
            out[key] = value

    return out


def _uptime_seconds() -> Optional[float]:
    p = Path("/proc/uptime")
    if p.exists():
        try:
            return float(p.read_text().split()[0])
        except Exception:  # noqa: BLE001
            return None

    # Fallback: unknown
    return None


def _snapshot(disk_path: str) -> Tuple[bool, Dict[str, Any], str]:
    try:
        cpu_count = os.cpu_count()
        load = os.getloadavg() if hasattr(os, "getloadavg") else None
        mem = _read_meminfo()
        uptime = _uptime_seconds()

        target = Path(disk_path or ".").expanduser().resolve()
        st = os.statvfs(str(target))
        total = int(st.f_frsize * st.f_blocks)
        free = int(st.f_frsize * st.f_bavail)
        used = total - free

        return (
            True,
            {
                "cpu_count": cpu_count,
                "loadavg": load,
                "uptime_seconds": uptime,
                "memory": {
                    "mem_total_bytes": mem.get("MemTotal"),
                    "mem_available_bytes": mem.get("MemAvailable"),
                    "swap_total_bytes": mem.get("SwapTotal"),
                    "swap_free_bytes": mem.get("SwapFree"),
                },
                "disk": {
                    "path": str(target),
                    "total_bytes": total,
                    "used_bytes": used,
                    "free_bytes": free,
                    "used_pct": round((used / total) * 100, 2) if total else None,
                },
                "timestamp": time.time(),
            },
            "ok",
        )
    except Exception as e:  # noqa: BLE001
        return False, {}, str(e)


def _verify(out: Dict[str, Any]) -> Tuple[bool, str]:
    disk = out.get("disk") or {}
    total = disk.get("total_bytes")
    used = disk.get("used_bytes")
    free = disk.get("free_bytes")
    if not isinstance(total, int) or total <= 0:
        return False, "disk.total_bytes invalid"
    if not isinstance(used, int) or used < 0:
        return False, "disk.used_bytes invalid"
    if not isinstance(free, int) or free < 0:
        return False, "disk.free_bytes invalid"
    if used + free > total + 4096:
        return False, "disk math invariant failed"
    return True, "ok"


def run(payload: dict):
    disk_path = str(payload.get("disk_path", "."))

    trace = [
        {"step": "observe", "note": "collect system stats"},
        {"step": "execute", "note": "derive summary"},
    ]

    ok, out, reason = _snapshot(disk_path)
    if not ok:
        trace.append({"step": "self_correct", "note": f"snapshot failed: {reason}; retrying"})
        ok, out, reason = _snapshot(disk_path)
        if not ok:
            return {"status": "failed", "detail": reason, "trace": trace}

    trace.append({"step": "verify", "note": "sanity-check invariants"})
    vok, vmsg = _verify(out)
    if not vok:
        trace.append({"step": "self_correct", "note": f"verify failed: {vmsg}"})
        return {"status": "failed", "detail": vmsg, "trace": trace, "data": out}

    return {"status": "success", "data": out, "trace": trace}

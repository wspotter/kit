"""Filesystem Triage tool.

A safe, real tool that scans a directory and reports:
- largest files
- oldest files

Default is read-only. No deletion/mutation.

Ralph Loop implementation here is conservative:
- Observe: walk directory and collect file stats
- Execute: compute rankings
- Verify: validate output invariants (sorted, paths exist)
- Self-correct: if invariants fail, retry with safer settings (e.g. smaller
  limits) up to 3 tries
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


TOOL_DEFINITION = {
    "id": "fs",
    "name": "Filesystem Triage",
    "icon": "folder-search",
    "description": "Scan a directory and report largest/oldest files (read-only).",
    "version": "0.1.0",
    "ralph_loop": True,
    "allow_network": "none",
    "allow_filesystem": "read",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "default": "."},
            "top_n": {"type": "integer", "default": 20, "minimum": 1, "maximum": 200},
            "max_files": {"type": "integer", "default": 20000, "minimum": 1, "maximum": 200000},
            "follow_symlinks": {"type": "boolean", "default": False},
        },
        "required": ["path"],
        "additionalProperties": False,
    },
}


@dataclass(frozen=True)
class FileStat:
    path: str
    size_bytes: int
    mtime: float


def _safe_int(v: Any, default: int) -> int:
    try:
        return int(v)
    except Exception:  # noqa: BLE001
        return default


def _walk_files(
    root: Path,
    *,
    max_files: int,
    follow_symlinks: bool,
) -> Tuple[List[FileStat], List[str]]:
    stats: List[FileStat] = []
    skipped: List[str] = []

    # os.walk is faster and gives control over followlinks
    count = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=follow_symlinks):
        _ = dirnames
        for name in filenames:
            if count >= max_files:
                skipped.append(f"Hit max_files={max_files}; remaining files not scanned")
                return stats, skipped

            p = Path(dirpath) / name
            try:
                st = p.stat()
            except Exception as e:  # noqa: BLE001
                skipped.append(f"stat failed: {p}: {e}")
                continue

            if not p.is_file():
                continue

            stats.append(FileStat(path=str(p), size_bytes=int(st.st_size), mtime=float(st.st_mtime)))
            count += 1

    return stats, skipped


def _rank_largest(stats: Iterable[FileStat], top_n: int) -> List[Dict[str, Any]]:
    ranked = sorted(stats, key=lambda s: s.size_bytes, reverse=True)[:top_n]
    return [
        {
            "path": s.path,
            "size_bytes": s.size_bytes,
            "size_mb": round(s.size_bytes / (1024 * 1024), 2),
            "mtime": s.mtime,
        }
        for s in ranked
    ]


def _rank_oldest(stats: Iterable[FileStat], top_n: int) -> List[Dict[str, Any]]:
    ranked = sorted(stats, key=lambda s: s.mtime)[:top_n]
    return [
        {
            "path": s.path,
            "size_bytes": s.size_bytes,
            "size_mb": round(s.size_bytes / (1024 * 1024), 2),
            "mtime": s.mtime,
            "age_days": round((time.time() - s.mtime) / 86400, 2),
        }
        for s in ranked
    ]


def _verify_rankings(largest: List[Dict[str, Any]], oldest: List[Dict[str, Any]]) -> Tuple[bool, str]:
    for arr, key, reverse in ((largest, "size_bytes", True), (oldest, "mtime", False)):
        vals = [x.get(key) for x in arr]
        if any(v is None for v in vals):
            return False, f"missing {key} in ranking"
        if vals != sorted(vals, reverse=reverse):
            return False, f"ranking not sorted by {key}"

    # Ensure lookups are sane (paths are strings)
    for x in (largest + oldest):
        if not isinstance(x.get("path"), str):
            return False, "path not a string"

    return True, "ok"


def run(payload: dict):
    # Observe
    root = Path(str(payload.get("path", "."))).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return {
            "status": "error",
            "error": "path_not_directory",
            "detail": f"Not a directory: {root}",
        }

    top_n = _safe_int(payload.get("top_n"), 20)
    top_n = max(1, min(200, top_n))

    max_files = _safe_int(payload.get("max_files"), 20000)
    max_files = max(1, min(200000, max_files))

    follow_symlinks = bool(payload.get("follow_symlinks", False))

    trace: List[Dict[str, Any]] = []

    attempt_settings = [
        {"top_n": top_n, "max_files": max_files, "follow_symlinks": follow_symlinks},
        {"top_n": min(top_n, 50), "max_files": min(max_files, 5000), "follow_symlinks": False},
        {"top_n": min(top_n, 25), "max_files": min(max_files, 2000), "follow_symlinks": False},
    ]

    last_reason: Optional[str] = None
    for attempt, settings in enumerate(attempt_settings, start=1):
        trace.append({"step": "observe", "note": f"walk {root} (attempt {attempt})"})
        stats, skipped = _walk_files(
            root,
            max_files=int(settings["max_files"]),
            follow_symlinks=bool(settings["follow_symlinks"]),
        )

        trace.append({"step": "execute", "note": f"rank {len(stats)} files"})
        largest = _rank_largest(stats, int(settings["top_n"]))
        oldest = _rank_oldest(stats, int(settings["top_n"]))

        trace.append({"step": "verify", "note": "check ranking invariants"})
        ok, reason = _verify_rankings(largest, oldest)
        if ok:
            return {
                "status": "success",
                "root": str(root),
                "scanned_files": len(stats),
                "skipped": skipped,
                "largest": largest,
                "oldest": oldest,
                "trace": trace,
            }

        last_reason = reason
        trace.append({"step": "self_correct", "note": f"verify failed: {reason}; retrying"})

    return {
        "status": "failed",
        "root": str(root),
        "detail": last_reason or "unknown",
        "trace": trace,
    }

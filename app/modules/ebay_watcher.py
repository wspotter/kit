"""eBay Watcher (mocked)

Implements the Ralph Loop:
1) Observe: accept a search query
2) Execute: run a mocked search scraper
3) Verify: compare results to Long Term Memory preferences (mock json)
4) Self-Correct: tweak / retry up to 3 times

This is intentionally mocked so the rest of the system can be built safely.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

TOOL_DEFINITION = {
    "id": "ebay",
    "name": "eBay Watcher",
    "icon": "shopping-cart",
    "description": "Mock eBay search + preference verification (Ralph Loop).",
}


LTM_PATH = Path(__file__).resolve().parents[1] / "ltm" / "preferences.json"


@dataclass(frozen=True)
class Listing:
    title: str
    price_usd: float
    condition: str


def _load_preferences() -> Dict[str, Any]:
    if not LTM_PATH.exists():
        return {
            "keywords_allow": [],
            "keywords_block": [],
            "max_price_usd": None,
            "conditions_allow": [],
        }

    return json.loads(LTM_PATH.read_text(encoding="utf-8"))


def _mock_scrape_ebay(query: str) -> List[Listing]:
    # Mock corpus. Later: use real scraping or eBay APIs.
    corpus = [
        Listing(title="Atomic Cat Figurine - Vintage 1962", price_usd=24.99, condition="used"),
        Listing(title="NVIDIA RTX 3070 Founders Edition", price_usd=399.0, condition="used"),
        Listing(title="Googie Starburst Wall Clock", price_usd=89.5, condition="new"),
        Listing(title="MCM Teal Tangerine Lamp", price_usd=54.0, condition="used"),
    ]

    q = query.lower().strip()
    if not q:
        return corpus[:2]

    # Super simple matching
    return [x for x in corpus if q in x.title.lower()] or corpus[:3]


def _matches_preferences(listing: Listing, prefs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []

    allow = [k.lower() for k in prefs.get("keywords_allow", [])]
    block = [k.lower() for k in prefs.get("keywords_block", [])]
    max_price = prefs.get("max_price_usd", None)
    cond_allow = [c.lower() for c in prefs.get("conditions_allow", [])]

    title_l = listing.title.lower()

    if block and any(b in title_l for b in block):
        reasons.append("blocked keyword")

    if allow and not any(a in title_l for a in allow):
        reasons.append("missing required keyword")

    if max_price is not None and listing.price_usd > float(max_price):
        reasons.append("over max price")

    if cond_allow and listing.condition.lower() not in cond_allow:
        reasons.append("condition not allowed")

    return (len(reasons) == 0), reasons


def ralph_loop(search_query: str) -> Dict[str, Any]:
    prefs = _load_preferences()

    attempt_query = search_query
    last_debug: Dict[str, Any] = {}

    for attempt in range(1, 4):
        # 1) Observe
        observed = {"query": attempt_query, "attempt": attempt}

        # 2) Execute
        results = _mock_scrape_ebay(attempt_query)

        # 3) Verify
        verified: List[Dict[str, Any]] = []
        rejected: List[Dict[str, Any]] = []
        for r in results:
            ok, reasons = _matches_preferences(r, prefs)
            blob = {"title": r.title, "price_usd": r.price_usd, "condition": r.condition}
            if ok:
                verified.append(blob)
            else:
                rejected.append({**blob, "reasons": reasons})

        if verified:
            return {
                "status": "success",
                "observed": observed,
                "verified_results": verified,
                "rejected_results": rejected,
                "preferences": prefs,
            }

        # 4) Self-Correct
        last_debug = {
            "status": "retrying",
            "observed": observed,
            "rejected_results": rejected,
            "preferences": prefs,
        }

        # naive correction: relax allow-list if too strict
        if prefs.get("keywords_allow"):
            attempt_query = ""  # broaden search
        else:
            attempt_query = attempt_query + " vintage"

    return {"status": "failed", **last_debug}


def run(payload: dict):
    query = str(payload.get("query", "")).strip()
    return ralph_loop(query)

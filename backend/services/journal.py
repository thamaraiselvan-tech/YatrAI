"""
services/journal.py
Travel journal service for YatrAI.
Stores trip logs with analytics, persists to JSON.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import Counter

JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "journal.json")

_DEFAULT_JOURNAL = {
    "entries": [],
}


def _journal_path() -> str:
    return os.path.abspath(JOURNAL_FILE)


def initialize_journal():
    """Create journal file if it doesn't exist."""
    path = _journal_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(_DEFAULT_JOURNAL, f, indent=2)


def read_journal() -> Dict[str, Any]:
    """Read the current journal state."""
    path = _journal_path()
    if not os.path.exists(path):
        initialize_journal()
    with open(path, "r") as f:
        return json.load(f)


def _save_journal(data: Dict[str, Any]):
    """Persist journal state to disk."""
    path = _journal_path()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def add_journal_entry(
    from_node: str,
    to_node: str,
    modes_used: List[str],
    cost: float,
    co2_saved: float,
    notes: str,
    category: str = "Commute",
) -> Dict[str, Any]:
    """
    Add a new journal entry.
    Returns the updated journal.
    """
    journal = read_journal()

    entry = {
        "id": f"JRN-{uuid.uuid4().hex[:8].upper()}",
        "from_node": from_node,
        "to_node": to_node,
        "modes_used": modes_used,
        "cost": round(cost, 2),
        "co2_saved": round(co2_saved, 1),
        "notes": notes,
        "category": category,
        "timestamp": datetime.now().isoformat(),
    }

    journal["entries"].insert(0, entry)  # Newest first
    _save_journal(journal)
    return journal


def delete_journal_entry(entry_id: str) -> Dict[str, Any]:
    """
    Delete a journal entry by ID.
    Returns the updated journal.
    """
    journal = read_journal()
    original_count = len(journal["entries"])
    journal["entries"] = [e for e in journal["entries"] if e["id"] != entry_id]

    if len(journal["entries"]) == original_count:
        raise ValueError(f"Journal entry {entry_id} not found.")

    _save_journal(journal)
    return journal


def get_journal_analytics() -> Dict[str, Any]:
    """
    Compute analytics from journal entries.
    Returns aggregate stats: total trips, cost, CO₂, mode breakdown, etc.
    """
    journal = read_journal()
    entries = journal.get("entries", [])

    if not entries:
        return {
            "total_trips": 0,
            "total_cost": 0,
            "total_co2_saved": 0,
            "avg_cost": 0,
            "avg_co2_saved": 0,
            "mode_breakdown": {},
            "category_breakdown": {},
            "frequent_routes": [],
            "monthly_summary": {},
        }

    total_cost = sum(e.get("cost", 0) for e in entries)
    total_co2 = sum(e.get("co2_saved", 0) for e in entries)
    total_trips = len(entries)

    # Mode breakdown
    mode_counter: Counter = Counter()
    for e in entries:
        for m in e.get("modes_used", []):
            mode_counter[m] += 1

    # Category breakdown
    cat_counter: Counter = Counter()
    for e in entries:
        cat_counter[e.get("category", "Other")] += 1

    # Frequent routes
    route_counter: Counter = Counter()
    for e in entries:
        route_key = f"{e.get('from_node', '?')} → {e.get('to_node', '?')}"
        route_counter[route_key] += 1

    # Monthly summary
    monthly: Dict[str, Dict[str, float]] = {}
    for e in entries:
        ts = e.get("timestamp", "")
        month_key = ts[:7] if len(ts) >= 7 else "unknown"
        if month_key not in monthly:
            monthly[month_key] = {"trips": 0, "cost": 0, "co2_saved": 0}
        monthly[month_key]["trips"] += 1
        monthly[month_key]["cost"] += e.get("cost", 0)
        monthly[month_key]["co2_saved"] += e.get("co2_saved", 0)

    # Round monthly values
    for k, v in monthly.items():
        v["cost"] = round(v["cost"], 2)
        v["co2_saved"] = round(v["co2_saved"], 1)

    return {
        "total_trips": total_trips,
        "total_cost": round(total_cost, 2),
        "total_co2_saved": round(total_co2, 1),
        "avg_cost": round(total_cost / total_trips, 2) if total_trips else 0,
        "avg_co2_saved": round(total_co2 / total_trips, 1) if total_trips else 0,
        "mode_breakdown": dict(mode_counter.most_common()),
        "category_breakdown": dict(cat_counter.most_common()),
        "frequent_routes": [
            {"route": r, "count": c} for r, c in route_counter.most_common(5)
        ],
        "monthly_summary": monthly,
    }

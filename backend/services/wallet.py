"""
services/wallet.py
Digital wallet with UPI simulation and escrow management for YatrAI.
Persists state in a JSON file.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

WALLET_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "wallet.json")

_DEFAULT_WALLET = {
    "balance": 500.0,
    "currency": "INR",
    "transactions": [],
    "escrows": {},
}


def _wallet_path() -> str:
    return os.path.abspath(WALLET_FILE)


def initialize_wallet():
    """Create wallet file with default balance if it doesn't exist."""
    path = _wallet_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(_DEFAULT_WALLET, f, indent=2)


def read_wallet() -> Dict[str, Any]:
    """Read the current wallet state and compute active escrow locked total."""
    path = _wallet_path()
    if not os.path.exists(path):
        initialize_wallet()
    with open(path, "r") as f:
        data = json.load(f)
    
    # Calculate total locked escrow
    total_locked = 0.0
    for trip_id, escrow in data.get("escrows", {}).items():
        if escrow.get("status") == "locked":
            for seg in escrow.get("segments", []):
                if not seg.get("released", False):
                    total_locked += seg.get("fare", 0.0)
    data["escrow_locked"] = round(total_locked, 2)
    return data


def _save_wallet(data: Dict[str, Any]):
    """Persist wallet state to disk."""
    path = _wallet_path()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def deposit_funds(amount: float) -> Dict[str, Any]:
    """
    Simulate a UPI deposit.
    Returns updated wallet state.
    """
    wallet = read_wallet()
    wallet["balance"] = round(wallet["balance"] + amount, 2)
    txn = {
        "id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
        "type": "deposit",
        "amount": amount,
        "timestamp": datetime.now().isoformat(),
        "description": f"UPI deposit of ₹{amount:.2f}",
    }
    wallet["transactions"].append(txn)
    _save_wallet(wallet)
    return wallet


def lock_escrow(trip_id: str, total_fare: float, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Lock funds in escrow for a trip.
    Deducts total_fare from balance and creates segment-level escrow entries.
    """
    wallet = read_wallet()

    if wallet["balance"] < total_fare:
        raise ValueError(
            f"Insufficient balance. Need ₹{total_fare:.2f}, have ₹{wallet['balance']:.2f}. "
            f"Please deposit ₹{total_fare - wallet['balance']:.2f} more."
        )

    wallet["balance"] = round(wallet["balance"] - total_fare, 2)

    escrow_segments = []
    for i, seg in enumerate(segments):
        escrow_segments.append({
            "index": i,
            "from_node": seg.get("from_node", ""),
            "to_node": seg.get("to_node", ""),
            "mode": seg.get("mode", ""),
            "fare": seg.get("fare", 0),
            "released": False,
        })

    wallet["escrows"][trip_id] = {
        "total_fare": total_fare,
        "locked_at": datetime.now().isoformat(),
        "segments": escrow_segments,
        "status": "locked",
    }

    txn = {
        "id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
        "type": "escrow_lock",
        "amount": -total_fare,
        "trip_id": trip_id,
        "timestamp": datetime.now().isoformat(),
        "description": f"Escrow locked for trip {trip_id}: ₹{total_fare:.2f}",
    }
    wallet["transactions"].append(txn)
    _save_wallet(wallet)
    return wallet


def release_segment_fare(trip_id: str, segment_index: int) -> Dict[str, Any]:
    """
    Release escrow for a completed segment.
    Marks the segment as released (fare is considered paid to operator).
    """
    wallet = read_wallet()

    if trip_id not in wallet["escrows"]:
        raise ValueError(f"No escrow found for trip {trip_id}")

    escrow = wallet["escrows"][trip_id]
    segments = escrow["segments"]

    if segment_index < 0 or segment_index >= len(segments):
        raise ValueError(f"Invalid segment index {segment_index}")

    if segments[segment_index]["released"]:
        return wallet  # Already released, idempotent

    segments[segment_index]["released"] = True
    fare = segments[segment_index]["fare"]

    txn = {
        "id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
        "type": "segment_release",
        "amount": -fare,
        "trip_id": trip_id,
        "segment_index": segment_index,
        "timestamp": datetime.now().isoformat(),
        "description": (
            f"Segment {segment_index} released: "
            f"{segments[segment_index]['from_node']} → {segments[segment_index]['to_node']} "
            f"via {segments[segment_index]['mode']} (₹{fare:.2f})"
        ),
    }
    wallet["transactions"].append(txn)

    # Check if all segments are released
    if all(s["released"] for s in segments):
        escrow["status"] = "completed"

    _save_wallet(wallet)
    return wallet


def refund_remaining_escrow(trip_id: str) -> Dict[str, Any]:
    """
    Refund any unreleased escrow funds back to the wallet balance.
    Used when a trip is cancelled or disrupted mid-way.
    """
    wallet = read_wallet()

    if trip_id not in wallet["escrows"]:
        raise ValueError(f"No escrow found for trip {trip_id}")

    escrow = wallet["escrows"][trip_id]

    if escrow["status"] == "refunded":
        return wallet  # Already refunded

    refund_amount = sum(
        s["fare"] for s in escrow["segments"] if not s["released"]
    )

    if refund_amount > 0:
        wallet["balance"] = round(wallet["balance"] + refund_amount, 2)
        txn = {
            "id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
            "type": "escrow_refund",
            "amount": refund_amount,
            "trip_id": trip_id,
            "timestamp": datetime.now().isoformat(),
            "description": f"Escrow refund for trip {trip_id}: ₹{refund_amount:.2f}",
        }
        wallet["transactions"].append(txn)

    escrow["status"] = "refunded"
    _save_wallet(wallet)
    return wallet

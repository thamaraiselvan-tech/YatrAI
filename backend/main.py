import uuid
import asyncio
import json
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from services.wallet import initialize_wallet
from routing.engine import solve_route
from agents.agents import parse_user_query, generate_bilingual_brief, parse_semantic_journal_log, query_journal_history
import services.wallet as wallet_service
import services.journal as journal_service

@asynccontextmanager
async def lifespan(app):
    # Startup
    initialize_wallet()
    journal_service.initialize_journal()
    yield
    # Shutdown (nothing needed)

app = FastAPI(title="YatrAI Multimodal Transit Gateway", version="2.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DISRUPTED_MODES: List[str] = []

# ── SSE subscriber registry ──────────────────────────────────────────────────
# Holds asyncio.Queue for each connected SSE client
_sse_subscribers: List[asyncio.Queue] = []

async def _broadcast(event: dict):
    """Push an event to all connected SSE clients."""
    dead = []
    for q in _sse_subscribers:
        try:
            await q.put(event)
        except Exception:
            dead.append(q)
    for q in dead:
        _sse_subscribers.remove(q)

# ── Pydantic models ───────────────────────────────────────────────────────────
class PlanRequest(BaseModel):
    query: str
    override_disruptions: Optional[List[str]] = None

class DepositRequest(BaseModel):
    amount: float

class LockEscrowRequest(BaseModel):
    trip_id: str
    total_fare: float
    segments: List[Dict[str, Any]]

class ReleaseSegmentRequest(BaseModel):
    trip_id: str
    segment_index: int

class RefundEscrowRequest(BaseModel):
    trip_id: str

class DisruptionToggleRequest(BaseModel):
    mode: str
    disrupted: bool

class ManualJournalRequest(BaseModel):
    from_node: str
    to_node: str
    modes_used: List[str]
    cost: float
    co2_saved: float
    notes: str
    category: Optional[str] = "Commute"

class SemanticLogRequest(BaseModel):
    text: str

class JournalQueryRequest(BaseModel):
    question: str


# ── Status ────────────────────────────────────────────────────────────────────
@app.get("/api/status")
def get_status():
    return {"status": "online", "disrupted_modes": DISRUPTED_MODES}

# ── Places & Nearest ─────────────────────────────────────────────────────────
@app.get("/api/places")
def get_places(q: str = "", category: str = "", city: str = "", limit: int = 30):
    """Search places by name, category, or city."""
    from data.places import search_places
    return {"places": search_places(q, category, city, limit)}

@app.get("/api/nearest")
def get_nearest(lat: float, lng: float):
    """Find the nearest known node to given GPS coordinates."""
    from data.database import COORDINATES, haversine_distance
    from data.places import PLACES

    best_node = None
    best_dist = float("inf")
    for node, (nlat, nlng) in COORDINATES.items():
        d = haversine_distance((lat, lng), (nlat, nlng))
        if d < best_dist:
            best_dist = d
            best_node = node

    meta = PLACES.get(best_node, {})
    return {
        "node": best_node,
        "distance_m": round(best_dist * 1000, 1),
        "name": meta.get("name", best_node.replace("_", " ")),
        "category": meta.get("category", ""),
        "lat": COORDINATES[best_node][0],
        "lng": COORDINATES[best_node][1],
    }

@app.get("/api/coordinates")
def get_all_coordinates():
    """Return all node coordinates for map rendering."""
    from data.database import COORDINATES
    from data.places import PLACES
    result = []
    for node, (lat, lng) in COORDINATES.items():
        meta = PLACES.get(node, {})
        result.append({
            "node": node,
            "lat": lat,
            "lng": lng,
            "name": meta.get("name", node.replace("_", " ")),
            "category": meta.get("category", "landmark"),
            "city": meta.get("city", ""),
        })
    return {"coordinates": result}

# ── Route Planning ────────────────────────────────────────────────────────────
@app.post("/api/plan")
def plan_trip(request: PlanRequest):
    active_disruptions = (
        request.override_disruptions
        if request.override_disruptions is not None
        else DISRUPTED_MODES
    )

    parsed = parse_user_query(request.query)
    routes = {}
    for mood in ["fastest", "cheapest", "greenest", "safest"]:
        route = solve_route(
            parsed["start_node"],
            parsed["target_node"],
            parsed["start_time_min"],
            mood,
            active_disruptions,
        )
        if route:
            routes[mood] = route

    if not routes:
        raise HTTPException(status_code=404, detail="No route found for current parameters.")

    selected = routes.get(parsed["mood"]) or list(routes.values())[0]
    brief = generate_bilingual_brief(request.query, selected, parsed["is_tamil"])

    trip_id = f"TRIP-{uuid.uuid4().hex[:6].upper()}"
    for r in routes.values():
        r["trip_id"] = trip_id

    return {
        "trip_id": trip_id,
        "parsed": parsed,
        "routes": routes,
        "brief": brief,
        "disrupted_modes_applied": active_disruptions,
    }

# ── Wallet ────────────────────────────────────────────────────────────────────
@app.get("/api/wallet")
def get_wallet():
    try:
        return wallet_service.read_wallet()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wallet/deposit")
def deposit(request: DepositRequest):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero.")
    return wallet_service.deposit_funds(request.amount)

@app.post("/api/wallet/lock")
def lock_trip_escrow(request: LockEscrowRequest):
    try:
        return wallet_service.lock_escrow(request.trip_id, request.total_fare, request.segments)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wallet/release")
def release_segment(request: ReleaseSegmentRequest):
    try:
        return wallet_service.release_segment_fare(request.trip_id, request.segment_index)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wallet/refund")
def refund_escrow(request: RefundEscrowRequest):
    try:
        return wallet_service.refund_remaining_escrow(request.trip_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Disruptions ───────────────────────────────────────────────────────────────
@app.get("/api/disruptions")
def get_disruptions():
    return {"disrupted_modes": DISRUPTED_MODES}

@app.post("/api/disruptions/toggle")
async def toggle_disruption(request: DisruptionToggleRequest):
    global DISRUPTED_MODES
    if request.disrupted:
        if request.mode not in DISRUPTED_MODES:
            DISRUPTED_MODES.append(request.mode)
    else:
        if request.mode in DISRUPTED_MODES:
            DISRUPTED_MODES.remove(request.mode)

    # Broadcast to all SSE subscribers
    await _broadcast({
        "type": "disruption_update",
        "disrupted_modes": DISRUPTED_MODES,
        "changed_mode": request.mode,
        "is_disrupted": request.disrupted,
    })

    return {"disrupted_modes": DISRUPTED_MODES}

@app.get("/api/disruptions/stream")
async def disruption_stream():
    """
    Server-Sent Events endpoint.
    Frontend connects once; disruption updates are pushed automatically.
    """
    queue: asyncio.Queue = asyncio.Queue()
    _sse_subscribers.append(queue)

    async def event_generator():
        # Send initial handshake
        yield f"data: {json.dumps({'type': 'connected', 'disrupted_modes': DISRUPTED_MODES})}\n\n"
        try:
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=25.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive ping every 25 s to prevent proxy timeouts
                    yield ": ping\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in _sse_subscribers:
                _sse_subscribers.remove(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )

# ── Journal ───────────────────────────────────────────────────────────────────
@app.get("/api/journal")
def get_journal_logs():
    try:
        return journal_service.read_journal()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/journal/analytics")
def get_journal_stats():
    try:
        return journal_service.get_journal_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/journal/add")
def add_journal(request: ManualJournalRequest):
    try:
        return journal_service.add_journal_entry(
            request.from_node, request.to_node, request.modes_used,
            request.cost, request.co2_saved, request.notes, request.category,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/journal/delete/{entry_id}")
def delete_journal(entry_id: str):
    try:
        return journal_service.delete_journal_entry(entry_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/journal/semantic_log")
def log_journal_conversational(request: SemanticLogRequest):
    try:
        parsed_log = parse_semantic_journal_log(request.text)
        journal_service.add_journal_entry(
            parsed_log["from_node"], parsed_log["to_node"],
            parsed_log["modes_used"], parsed_log["cost"],
            parsed_log["co2_saved"], parsed_log["notes"],
            parsed_log.get("category", "Commute"),
        )
        return {"success": True, "parsed_log": parsed_log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/journal/query")
def ask_journal_history(request: JournalQueryRequest):
    try:
        journal_data = journal_service.read_journal()
        answer = query_journal_history(request.question, journal_data)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

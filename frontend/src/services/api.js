// src/services/api.js
// Central API client — all backend calls go through here.

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body !== undefined) opts.body = JSON.stringify(body)

  const res = await fetch(`${BASE}${path}`, opts)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Request failed')
  }
  return res.json()
}

// ── Status ────────────────────────────────────────────────────────────────────
export const getStatus = () => request('GET', '/api/status')

// ── Route Planning ────────────────────────────────────────────────────────────
/**
 * Plan a trip.
 * @param {string} query - Natural language / Tanglish query
 * @param {string[]} [overrideDisruptions] - Optional disrupted mode list
 * @returns {{ trip_id, parsed, routes, brief, disrupted_modes_applied }}
 */
export const planTrip = (query, overrideDisruptions) =>
  request('POST', '/api/plan', {
    query,
    override_disruptions: overrideDisruptions ?? null,
  })

// ── Wallet ────────────────────────────────────────────────────────────────────
export const getWallet = () => request('GET', '/api/wallet')

/**
 * Deposit funds via UPI proxy simulation.
 * @param {number} amount - Amount in INR
 */
export const depositFunds = (amount) =>
  request('POST', '/api/wallet/deposit', { amount })

/**
 * Lock escrow before starting a trip.
 * @param {string} tripId
 * @param {number} totalFare
 * @param {object[]} segments - route segments array
 */
export const lockEscrow = (tripId, totalFare, segments) =>
  request('POST', '/api/wallet/lock', {
    trip_id: tripId,
    total_fare: totalFare,
    segments,
  })

/**
 * Release fare for a completed segment.
 * @param {string} tripId
 * @param {number} segmentIndex
 */
export const releaseSegment = (tripId, segmentIndex) =>
  request('POST', '/api/wallet/release', {
    trip_id: tripId,
    segment_index: segmentIndex,
  })

/**
 * Refund any locked escrow (trip cancelled / disruption).
 * @param {string} tripId
 */
export const refundEscrow = (tripId) =>
  request('POST', '/api/wallet/refund', { trip_id: tripId })

// ── Disruptions ───────────────────────────────────────────────────────────────
export const getDisruptions = () => request('GET', '/api/disruptions')

/**
 * Toggle a transit mode disruption.
 * @param {string} mode - e.g. "Suburban_Train", "Metro", "MTC_Bus"
 * @param {boolean} disrupted
 */
export const toggleDisruption = (mode, disrupted) =>
  request('POST', '/api/disruptions/toggle', { mode, disrupted })

// ── Journal ───────────────────────────────────────────────────────────────────
export const getJournal = () => request('GET', '/api/journal')
export const getJournalAnalytics = () => request('GET', '/api/journal/analytics')

export const addJournalEntry = (entry) =>
  request('POST', '/api/journal/add', entry)

export const deleteJournalEntry = (entryId) =>
  request('DELETE', `/api/journal/delete/${entryId}`)

/**
 * Log a trip in natural language (Gemini parses it).
 * @param {string} text - e.g. "Went from Guindy to OMR by Metro, spent ₹40"
 */
export const semanticLog = (text) =>
  request('POST', '/api/journal/semantic_log', { text })

/**
 * Ask a question about past journal entries.
 * @param {string} question
 */
export const queryJournal = (question) =>
  request('POST', '/api/journal/query', { question })

export const getNearest = (lat, lng) =>
  request('GET', `/api/nearest?lat=${lat}&lng=${lng}`)

export const getPlaces = (q, limit = 5) =>
  request('GET', `/api/places?q=${encodeURIComponent(q)}&limit=${limit}`)

// ── SSE Helper ────────────────────────────────────────────────────────────────
/**
 * Open an SSE connection to the disruption stream.
 * Returns the raw EventSource so the caller can close it.
 *
 * @param {(event: object) => void} onMessage
 * @param {(err: Event) => void} [onError]
 * @returns {EventSource}
 */
export function openDisruptionStream(onMessage, onError) {
  const es = new EventSource(`${BASE}/api/disruptions/stream`)
  es.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      onMessage(data)
    } catch (_) {}
  }
  if (onError) es.onerror = onError
  return es
}

// src/hooks/useSSE.js
import { useEffect, useRef, useState, useCallback } from 'react'
import { openDisruptionStream } from '../services/api'

/**
 * Subscribes to the backend SSE disruption stream.
 * Returns { disruptions, lastAlert, clearAlert }
 */
export function useSSE() {
  const [disruptions, setDisruptions] = useState([])
  const [lastAlert, setLastAlert] = useState(null)
  const esRef = useRef(null)

  useEffect(() => {
    let retryTimeout = null
    let retries = 0

    function connect() {
      esRef.current?.close()

      esRef.current = openDisruptionStream(
        (event) => {
          retries = 0 // reset on success

          if (event.type === 'connected' || event.type === 'disruption_update') {
            setDisruptions(event.disrupted_modes ?? [])
          }

          if (event.type === 'disruption_update') {
            const mode = event.changed_mode?.replace(/_/g, ' ')
            if (event.is_disrupted) {
              setLastAlert({
                id: Date.now(),
                title: `⚠️ Service Disruption`,
                message: `${mode} service has been disrupted. Tap to replan.`,
                mode: event.changed_mode,
              })
            } else {
              setLastAlert({
                id: Date.now(),
                title: `✅ Service Restored`,
                message: `${mode} is back in service.`,
                mode: event.changed_mode,
              })
            }
          }
        },
        () => {
          // Exponential back-off: 2s → 4s → 8s → max 30s
          const delay = Math.min(2000 * 2 ** retries, 30000)
          retries++
          retryTimeout = setTimeout(connect, delay)
        }
      )
    }

    connect()

    return () => {
      clearTimeout(retryTimeout)
      esRef.current?.close()
    }
  }, [])

  const clearAlert = useCallback(() => setLastAlert(null), [])

  return { disruptions, lastAlert, clearAlert }
}

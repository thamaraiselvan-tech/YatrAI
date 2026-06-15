// src/hooks/useGeoLocation.js
import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * Hook for real-time GPS tracking using browser Geolocation API.
 * Returns { position, heading, speed, error, supported, tracking, start, stop }
 */
export function useGeoLocation() {
  const [position, setPosition] = useState(null) // { lat, lng }
  const [heading, setHeading] = useState(null)
  const [speed, setSpeed] = useState(null)
  const [error, setError] = useState(null)
  const [tracking, setTracking] = useState(false)
  const watchIdRef = useRef(null)

  const supported = typeof navigator !== 'undefined' && 'geolocation' in navigator

  const start = useCallback(() => {
    if (!supported) {
      setError('Geolocation not supported')
      return
    }
    setError(null)
    setTracking(true)

    // Get initial position quickly
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setPosition({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracy: pos.coords.accuracy
        })
        setHeading(pos.coords.heading)
        setSpeed(pos.coords.speed)
      },
      (err) => setError(err.message),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    )

    // Start continuous watching
    watchIdRef.current = navigator.geolocation.watchPosition(
      (pos) => {
        setPosition({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracy: pos.coords.accuracy
        })
        setHeading(pos.coords.heading)
        setSpeed(pos.coords.speed)
        setError(null)
      },
      (err) => {
        setError(err.message)
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0,  // Force fresh calculations, no caching
      }
    )
  }, [supported])

  const stop = useCallback(() => {
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current)
      watchIdRef.current = null
    }
    setTracking(false)
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (watchIdRef.current !== null) {
        navigator.geolocation.clearWatch(watchIdRef.current)
      }
    }
  }, [])

  return { position, heading, speed, error, supported, tracking, start, stop }
}

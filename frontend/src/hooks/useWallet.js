// src/hooks/useWallet.js
import { useState, useEffect, useCallback } from 'react'
import { getWallet, depositFunds, lockEscrow, releaseSegment, refundEscrow } from '../services/api'

export function useWallet() {
  const [wallet, setWallet] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const refresh = useCallback(async () => {
    try {
      const data = await getWallet()
      setWallet(data)
    } catch (e) {
      setError(e.message)
    }
  }, [])

  useEffect(() => { refresh() }, [refresh])

  const deposit = useCallback(async (amount) => {
    setLoading(true)
    try {
      const data = await depositFunds(amount)
      setWallet(data)
      return data
    } catch (e) {
      setError(e.message)
      throw e
    } finally {
      setLoading(false)
    }
  }, [])

  const lock = useCallback(async (tripId, totalFare, segments) => {
    setLoading(true)
    try {
      const data = await lockEscrow(tripId, totalFare, segments)
      setWallet(data)
      return data
    } catch (e) {
      setError(e.message)
      throw e
    } finally {
      setLoading(false)
    }
  }, [])

  const release = useCallback(async (tripId, segIndex) => {
    const data = await releaseSegment(tripId, segIndex)
    setWallet(data)
    return data
  }, [])

  const refund = useCallback(async (tripId) => {
    const data = await refundEscrow(tripId)
    setWallet(data)
    return data
  }, [])

  return { wallet, loading, error, refresh, deposit, lock, release, refund }
}

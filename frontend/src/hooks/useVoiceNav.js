// src/hooks/useVoiceNav.js
import { useState, useCallback, useRef, useEffect } from 'react'

/**
 * Text-to-Speech navigation hook using Web Speech API.
 * Speaks turn-by-turn instructions as user progresses through segments.
 *
 * Usage:
 *   const { speak, stop, speaking, enabled, toggle, speakSegment } = useVoiceNav()
 */
export function useVoiceNav() {
  const [enabled, setEnabled] = useState(true)
  const [speaking, setSpeaking] = useState(false)
  const [lang, setLang] = useState('en') // 'en' or 'ta'
  const synthRef = useRef(null)
  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window

  useEffect(() => {
    if (supported) {
      synthRef.current = window.speechSynthesis
    }
    return () => {
      if (synthRef.current) {
        synthRef.current.cancel()
      }
    }
  }, [supported])

  const speak = useCallback((text, options = {}) => {
    if (!supported || !enabled || !text) return

    // Cancel any ongoing speech
    synthRef.current.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = options.lang === 'ta' ? 'ta-IN' : 'en-IN'
    utterance.rate = options.rate ?? 0.9
    utterance.pitch = options.pitch ?? 1.0
    utterance.volume = options.volume ?? 1.0

    utterance.onstart = () => setSpeaking(true)
    utterance.onend = () => setSpeaking(false)
    utterance.onerror = () => setSpeaking(false)

    synthRef.current.speak(utterance)
  }, [supported, enabled])

  const stop = useCallback(() => {
    if (synthRef.current) {
      synthRef.current.cancel()
      setSpeaking(false)
    }
  }, [])

  const toggle = useCallback(() => {
    setEnabled(prev => {
      if (prev && synthRef.current) {
        synthRef.current.cancel()
        setSpeaking(false)
      }
      return !prev
    })
  }, [])

  /**
   * Speak a route segment instruction.
   * Auto-detects language from the segment data.
   */
  const speakSegment = useCallback((segment, options = {}) => {
    if (!segment) return

    const useTamil = lang === 'ta' && segment.instruction_ta
    const text = useTamil ? segment.instruction_ta : segment.instruction_en

    // Add context
    const duration = Math.round(segment.duration)
    const fare = segment.fare
    const fullText = useTamil
      ? `${text} ${duration} நிமிடம், கட்டணம் ${fare} ரூபாய்.`
      : `${text} This will take about ${duration} minutes, fare ${fare} rupees.`

    speak(fullText, { lang: useTamil ? 'ta' : 'en', ...options })
  }, [speak, lang])

  /**
   * Announce upcoming transition to next segment.
   */
  const announceNext = useCallback((nextSegment) => {
    if (!nextSegment) return
    const mode = nextSegment.mode.replace(/_/g, ' ')
    const to = nextSegment.to_node.replace(/_/g, ' ')
    speak(`Next: Take ${mode} to ${to}.`)
  }, [speak])

  /**
   * Announce trip completion.
   */
  const announceComplete = useCallback((totalFare) => {
    speak(`Trip complete! Total fare was ${totalFare} rupees. Thank you for using YatrAI.`)
  }, [speak])

  /**
   * Announce arrival at waypoint.
   */
  const announceArrival = useCallback((nodeName) => {
    const clean = nodeName.replace(/_/g, ' ')
    speak(`You have arrived at ${clean}.`)
  }, [speak])

  return {
    speak,
    stop,
    speaking,
    enabled,
    supported,
    toggle,
    lang,
    setLang,
    speakSegment,
    announceNext,
    announceComplete,
    announceArrival,
  }
}

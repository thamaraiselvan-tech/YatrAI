// src/hooks/useVoiceInput.js
import { useState, useRef, useCallback } from 'react'

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition || null

/**
 * Wraps the Web Speech API for voice input.
 *
 * Usage:
 *   const { transcript, listening, supported, start, stop, reset } = useVoiceInput()
 *
 * After the user stops speaking, `transcript` contains the recognised text.
 * The hook tries `ta-IN` first (Tamil), then falls back to `en-IN`.
 */
export function useVoiceInput(onResult) {
  const [transcript, setTranscript] = useState('')
  const [listening, setListening] = useState(false)
  const [error, setError] = useState(null)
  const recogRef = useRef(null)

  const supported = Boolean(SpeechRecognition)

  const stop = useCallback(() => {
    recogRef.current?.stop()
    setListening(false)
  }, [])

  const start = useCallback(() => {
    if (!supported) {
      setError('Speech recognition is not supported in this browser. Use Chrome.')
      return
    }
    setError(null)
    setTranscript('')

    const recog = new SpeechRecognition()
    recog.lang = 'en-IN'              // Primary: English (India)
    recog.interimResults = true
    recog.maxAlternatives = 1
    recog.continuous = false

    recog.onstart = () => setListening(true)

    recog.onresult = (e) => {
      let interim = ''
      let final = ''
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const text = e.results[i][0].transcript
        if (e.results[i].isFinal) final += text
        else interim += text
      }
      const current = final || interim
      setTranscript(current)
      if (final && onResult) onResult(final.trim())
    }

    recog.onerror = (e) => {
      // If English fails or language not supported, try Tamil
      if (e.error === 'language-not-supported' || e.error === 'network') {
        stop()
        const fallbackRecog = new SpeechRecognition()
        fallbackRecog.lang = 'ta-IN'
        fallbackRecog.interimResults = true
        fallbackRecog.maxAlternatives = 1
        fallbackRecog.continuous = false
        fallbackRecog.onstart = () => setListening(true)
        fallbackRecog.onresult = recog.onresult
        fallbackRecog.onerror = (err) => {
          setError(`Voice error: ${err.error}`)
          setListening(false)
        }
        fallbackRecog.onend = () => setListening(false)
        recogRef.current = fallbackRecog
        try { fallbackRecog.start() } catch (_) {}
        return
      }
      setError(`Voice error: ${e.error}`)
      setListening(false)
    }

    recog.onend = () => setListening(false)

    recogRef.current = recog
    recog.start()
  }, [supported, onResult, stop])

  const reset = useCallback(() => {
    stop()
    setTranscript('')
    setError(null)
  }, [stop])

  return { transcript, listening, supported, error, start, stop, reset }
}

// src/components/PlannerView.jsx
import { useState, useCallback, useEffect, useRef } from 'react'
import { planTrip, getJournalAnalytics, getNearest, getPlaces } from '../services/api'
import { useVoiceInput } from '../hooks/useVoiceInput'
import RouteCard from './RouteCard'
import SegmentTimeline from './SegmentTimeline'

const RECENT_JOURNEYS = [
  { from: 'SRM Dorm', to: 'Chennai Central' },
  { from: 'Mylapore', to: 'Srirangam' },
  { from: 'Rockfort', to: 'NIT Trichy' }
]

const MOCK_RESULT = {
  trip_id: "YAI-992-B81",
  parsed: { mood: "fastest" },
  routes: {
    cheapest: {
      total_fare: 35,
      total_time: 55,
      total_co2: 600,
      end_time_str: '08:45 AM',
      segments: [
        { mode: 'MTC_Bus', from_node: 'T_Nagar', to_node: 'Chennai_Egmore', fare: 12, duration: 12, start_time_str: '08:00 AM', instruction_en: 'Take MTC Bus Route 102 to Egmore' },
        { mode: 'Walk', from_node: 'Chennai_Egmore', to_node: 'Chennai_Egmore', fare: 0, duration: 3, start_time_str: '08:12 AM', instruction_en: 'Walk to Egmore Metro Station' },
        { mode: 'Suburban_Train', from_node: 'Chennai_Egmore', to_node: 'Chennai_Central', fare: 23, duration: 40, start_time_str: '08:15 AM', instruction_en: 'Take Suburban train to Central' }
      ]
    },
    fastest: {
      total_fare: 32,
      total_time: 42,
      total_co2: 1800,
      end_time_str: '08:22 AM',
      segments: [
        { mode: 'MTC_Bus', from_node: 'T_Nagar', to_node: 'Chennai_Egmore', fare: 12, duration: 12, start_time_str: '08:00 AM', instruction_en: 'Take MTC Bus Route 102 to Egmore' },
        { mode: 'Walk', from_node: 'Chennai_Egmore', to_node: 'Chennai_Egmore', fare: 0, duration: 3, start_time_str: '08:12 AM', instruction_en: 'Walk 150m via covered skywalk' },
        { mode: 'Metro', from_node: 'Chennai_Egmore', to_node: 'Chennai_Central', fare: 20, duration: 27, start_time_str: '08:15 AM', instruction_en: 'Take CMRL Metro Blue Line to Central' }
      ]
    },
    greenest: {
      total_fare: 40,
      total_time: 50,
      total_co2: -1200,
      end_time_str: '08:55 AM',
      segments: [
        { mode: 'Walk', from_node: 'T_Nagar', to_node: 'Chennai_Egmore', fare: 0, duration: 20, start_time_str: '08:00 AM', instruction_en: 'Walk to Egmore Metro Station' },
        { mode: 'Metro', from_node: 'Chennai_Egmore', to_node: 'Chennai_Central', fare: 40, duration: 30, start_time_str: '08:20 AM', instruction_en: 'Take CMRL Metro Blue Line' }
      ]
    },
    safest: {
      total_fare: 80,
      total_time: 30,
      total_co2: 2500,
      end_time_str: '08:30 AM',
      segments: [
        { mode: 'Ola_Auto', from_node: 'T_Nagar', to_node: 'Chennai_Central', fare: 80, duration: 30, start_time_str: '08:00 AM', instruction_en: 'Take Ola Auto (Verified Safe Route)' }
      ]
    }
  },
  brief: "Fastest route uses MTC Bus Route 102 with a quick transfer to the CMRL Metro Blue Line. Save ₹3 by choosing Cheapest, but adds 13 mins."
}

export default function PlannerView({ disruptions, onStartTrip, position, wallet, onTopUpClick }) {
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [selectedMood, setSelectedMood] = useState(null)
  const [nearestPlace, setNearestPlace] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [activeField, setActiveField] = useState('destination')
  const [greenPoints, setGreenPoints] = useState(0)
  const [co2Saved, setCo2Saved] = useState(0)
  const suggestTimeout = useRef(null)

  const handlePlanDirect = useCallback(async (fromVal, toVal) => {
    setLoading(true)
    setError(null)
    setResult(null)
    setSelectedMood(null)
    setShowSuggestions(false)
    try {
      const queryText = `from ${fromVal} to ${toVal}`
      const data = await planTrip(queryText, disruptions.length ? disruptions : undefined)
      setResult(data)
      setSelectedMood(data.parsed?.mood ?? 'cheapest')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [disruptions])

  // Load GreenPoints analytics
  useEffect(() => {
    getJournalAnalytics()
      .then(a => {
        if (a) {
          const co2SavedKg = (a.total_co2_saved || 0) / 1000
          setGreenPoints(Math.round(co2SavedKg * 10))
          setCo2Saved(co2SavedKg)
        }
      })
      .catch(() => {})
  }, [])

  // Auto-split voice results into Origin and Destination
  const handleVoiceResult = useCallback((text) => {
    let cleanText = text.toLowerCase()
      .replace(/\bform\b/g, 'from')
      .replace(/\btoo\b/g, 'to')
      .replace(/\btwo\b/g, 'to')
      .replace(/\b2\b/g, 'to')
      .replace(/\bto\b/g, ' to ')
      .replace(/\s+/g, ' ')
      .trim()

    if (cleanText.includes(' to ')) {
      const parts = cleanText.split(' to ')
      const fromPart = parts[0].replace('from ', '').trim()
      const toPart = parts[1].trim()
      if (fromPart) {
        setOrigin(fromPart.charAt(0).toUpperCase() + fromPart.slice(1))
      }
      if (toPart) {
        setDestination(toPart.charAt(0).toUpperCase() + toPart.slice(1))
      }
    } else {
      setDestination(text)
    }
  }, [])

  const { listening, supported, start, stop } = useVoiceInput(handleVoiceResult)

  // Fetch nearest place from GPS
  useEffect(() => {
    if (!position) return
    getNearest(position.lat, position.lng)
      .then(data => {
        setNearestPlace(data)
        // Auto-fill origin if it is currently empty
        setOrigin(prev => {
          if (!prev.trim()) {
            return data.name || data.node.replace(/_/g, ' ')
          }
          return prev
        })
      })
      .catch(() => {})
  }, [position?.lat, position?.lng])

  // Place suggestions autocomplete
  const handleQueryChange = useCallback((val, field) => {
    if (field === 'origin') setOrigin(val)
    else setDestination(val)

    if (suggestTimeout.current) clearTimeout(suggestTimeout.current)
    
    const lastWord = val.split(/\s+/).pop()
    if (lastWord && lastWord.length >= 2) {
      suggestTimeout.current = setTimeout(() => {
        getPlaces(lastWord, 5)
          .then(data => {
            setSuggestions(data.places || [])
            setShowSuggestions(data.places?.length > 0)
          })
          .catch(() => setSuggestions([]))
      }, 300)
    } else {
      setSuggestions([])
      setShowSuggestions(false)
    }
  }, [])

  const insertSuggestion = useCallback((placeName) => {
    if (activeField === 'origin') {
      setOrigin(placeName)
    } else {
      setDestination(placeName)
    }
    setShowSuggestions(false)
    setSuggestions([])
  }, [activeField])

  const handleUseLocation = useCallback(() => {
    if (!nearestPlace) return
    const name = nearestPlace.name || nearestPlace.node.replace(/_/g, ' ')
    setOrigin(name)
  }, [nearestPlace])

  async function handlePlan(e) {
    e?.preventDefault()
    const fromVal = origin.trim()
    const toVal = destination.trim()
    if (!fromVal || !toVal) return
    
    setLoading(true)
    setError(null)
    setResult(null)
    setSelectedMood(null)
    setShowSuggestions(false)
    try {
      const queryText = `from ${fromVal} to ${toVal}`
      const data = await planTrip(queryText, disruptions.length ? disruptions : undefined)
      setResult(data)
      setSelectedMood(data.parsed?.mood ?? 'cheapest')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const selectedRoute = result?.routes?.[selectedMood]
  const walletAvailable = wallet?.balance ?? 840
  const walletEscrow = wallet?.escrow_locked ?? 50

  return (
    <div className="flex flex-col gap-4 pb-20 animate-fade-in-up">

      {/* Disruption Alert Banner */}
      {disruptions.length > 0 && (
        <section className="mt-stack-sm">
          <div className="bg-error-container text-on-error-container p-3 rounded-xl border border-error/20 flex items-center gap-3 animate-pulse-border">
            <span className="material-symbols-outlined text-error" style={{ fontVariationSettings: "'FILL' 1" }}>warning</span>
            <span className="font-label-lg text-label-lg">
              {typeof disruptions[0] === 'string'
                ? `${disruptions[0].replace(/_/g, ' ')}: Service suspended`
                : `${disruptions[0].mode?.replace(/_/g, ' ') || 'Transit'}: ${disruptions[0].description || 'Delay reported'}`
              }
            </span>
          </div>
        </section>
      )}

      {/* Responsive Grid Layout Container */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Search Form, AI Brief, Travel Moods, Timeline */}
        <div className="lg:col-span-8 space-y-8">
          {/* ── Search & Hero Section ── */}
          <section className="relative rounded-2xl overflow-hidden bg-primary-container p-stack-lg border border-outline-variant shadow-sm select-none">
            <div className="absolute inset-0 opacity-10 pointer-events-none">
              <div className="w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-secondary to-transparent opacity-20"></div>
            </div>

            <form onSubmit={handlePlan} className="relative z-10 space-y-stack-md">
              <div className="flex flex-col gap-unit">
                {/* Origin Input */}
                <div className="flex items-center gap-stack-sm h-[52px] bg-surface dark:bg-surface-container-highest rounded-xl px-4 border border-outline-variant shadow-sm focus-within:ring-2 focus-within:ring-secondary transition-all">
                  <span className="w-2.5 h-2.5 rounded-full bg-secondary shrink-0"></span>
                  <input
                    type="text"
                    value={origin}
                    onFocus={() => { setActiveField('origin'); if (suggestions.length > 0) setShowSuggestions(true) }}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    onChange={(e) => handleQueryChange(e.target.value, 'origin')}
                    placeholder="Enter starting location"
                    className="bg-transparent border-none focus:ring-0 font-body-md text-body-md text-on-surface-variant w-full outline-none text-[13px]"
                  />
                </div>

                {/* Destination Input */}
                <div className="flex items-center gap-stack-sm h-[52px] bg-surface dark:bg-surface-container-highest rounded-xl px-4 border border-outline-variant shadow-sm focus-within:ring-2 focus-within:ring-secondary transition-all">
                  <span className="w-3 h-3 bg-secondary rounded-sm shrink-0"></span>
                  <input
                    type="text"
                    value={destination}
                    onFocus={() => { setActiveField('destination'); if (suggestions.length > 0) setShowSuggestions(true) }}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    onChange={(e) => handleQueryChange(e.target.value, 'destination')}
                    placeholder="Central Railway Station"
                    className="bg-transparent border-none focus:ring-0 font-body-md text-body-md text-on-surface w-full outline-none text-[13px]"
                  />
                </div>
              </div>

              {/* Autocomplete suggestions overlay */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute left-0 right-0 top-[108px] z-50 bg-surface border border-outline-variant rounded-xl overflow-hidden shadow-lg">
                  {suggestions.map(s => (
                    <button
                      key={s.node}
                      type="button"
                      onMouseDown={(e) => { e.preventDefault(); insertSuggestion(s.name) }}
                      className="w-full text-left px-4 py-3 hover:bg-surface-container-highest flex items-center gap-3 text-[12px] border-b border-outline-variant/10 last:border-0 transition-colors"
                    >
                      <span className="material-symbols-outlined text-[16px] text-secondary">location_on</span>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold truncate text-on-surface">{s.name}</p>
                        <p className="text-on-surface-variant text-[11px] truncate">{s.area} · {s.city}</p>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {/* Recent Journeys pills */}
              <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar select-none">
                {RECENT_JOURNEYS.map((j, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => { setOrigin(j.from); setDestination(j.to); handlePlanDirect(j.from, j.to); }}
                    className="flex-none bg-surface-container-high/40 text-on-surface-variant font-label-md text-label-md px-3 py-1.5 rounded-full border border-outline-variant hover:bg-surface-container-highest transition-colors text-[11px]"
                  >
                    {j.from} → {j.to}
                  </button>
                ))}
              </div>

              {/* AI Voice Microphone Button */}
              {supported && (
                <div className="flex justify-center mt-stack-lg">
                  <button
                    type="button"
                    onClick={listening ? stop : start}
                    className="w-16 h-16 bg-[#3B82F6] text-white rounded-full flex items-center justify-center shadow-lg active:scale-90 transition-all duration-300 relative group overflow-hidden"
                  >
                    {listening && (
                      <div className="absolute inset-0 bg-white/20 animate-ping rounded-full opacity-30"></div>
                    )}
                    <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
                      {listening ? 'mic_off' : 'mic'}
                    </span>
                  </button>
                </div>
              )}

              {/* GPS Location Pill */}
              {nearestPlace && (
                <button
                  onClick={handleUseLocation}
                  type="button"
                  className="flex items-center gap-2 w-full px-3 py-2 rounded-xl bg-emerald-500/10 dark:bg-emerald-950/20 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-[12px] font-medium transition-all"
                >
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>
                  <span>Nearby: <span className="font-semibold">{nearestPlace.name}</span></span>
                  <span className="ml-auto opacity-70">{nearestPlace.distance_m}m away</span>
                </button>
              )}

              {/* Action button */}
              <button
                type="submit"
                disabled={loading || !destination.trim()}
                className="w-full bg-secondary text-white font-medium rounded-xl py-3.5 text-[15px] hover:brightness-110 transition-all active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-md shadow-secondary/15"
              >
                {loading ? 'Routing...' : 'Get Travel Options'}
              </button>
            </form>
          </section>

          {/* ── Error Notification ── */}
          {error && (
            <div className="bg-error-container border border-error/20 rounded-xl px-4 py-3 text-[12px] text-on-error-container flex items-center gap-2.5">
              <span className="material-symbols-outlined text-error">warning</span>
              <span>{error}</span>
            </div>
          )}

          {/* ── Skeleton Calculation Loader ── */}
          {loading && (
            <div className="flex flex-col gap-3">
              <span className="text-[12px] font-medium text-slate-400 dark:text-slate-500 uppercase tracking-wider block">
                Calculating optimal routes...
              </span>
              <div className="grid grid-cols-2 gap-3.5">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="w-full h-[120px] rounded-[16px] bg-surface-container border border-outline-variant animate-pulse p-3.5 flex flex-col justify-between">
                    <div className="flex justify-between w-full">
                      <div className="w-8 h-8 rounded-full bg-surface-container-highest" />
                      <div className="w-12 h-5 rounded-full bg-surface-container-highest" />
                    </div>
                    <div className="flex flex-col gap-1.5 mt-auto">
                      <div className="w-16 h-4 rounded bg-surface-container-highest" />
                      <div className="w-24 h-3 rounded bg-surface-container-highest" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── Gemini AI Brief ── */}
          {result?.brief && !loading && (
            <div className="bg-surface-container border border-outline-variant rounded-2xl p-4 border-l-4 border-secondary flex flex-col gap-1">
              <p className="text-[11px] font-bold text-secondary uppercase tracking-wider flex items-center gap-1.5">
                <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
                Gemini AI Brief
              </p>
              <p className="text-[12.5px] font-normal text-on-surface-variant leading-relaxed">
                {typeof result.brief === 'string' ? result.brief : result.brief.en}
              </p>
            </div>
          )}

          {/* ── Travel Moods Grid ── */}
          {result?.routes && !loading && (
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center mb-stack-sm">
                <h2 className="font-headline-sm text-headline-sm text-on-surface font-bold">Travel Moods</h2>
                <span className="font-label-md text-label-md text-secondary cursor-pointer">View Map</span>
              </div>
              <div className="grid grid-cols-2 gap-3.5">
                {Object.entries(result.routes).map(([mood, route]) => (
                  <RouteCard
                    key={mood}
                    mood={mood}
                    route={route}
                    selected={selectedMood === mood}
                    recommended={result.parsed?.mood === mood}
                    onClick={() => setSelectedMood(mood)}
                  />
                ))}
              </div>
            </div>
          )}

          {/* ── Segment Timeline & Start Button ── */}
          {selectedRoute && !loading && (
            <div className="flex flex-col gap-4">
              <SegmentTimeline route={selectedRoute} />
              <button
                onClick={() => onStartTrip(result.trip_id, selectedMood, selectedRoute)}
                className="w-full bg-secondary hover:brightness-110 text-white font-medium rounded-xl py-3.5 text-[15px] flex items-center justify-center gap-2 active:scale-95 transition-all shadow-md shadow-secondary/15"
              >
                <span className="material-symbols-outlined text-[18px]">navigation</span>
                Start Journey · ₹{selectedRoute.total_fare}
              </button>
            </div>
          )}
        </div>

        {/* Right Column: Widgets & Recommendations */}
        <div className="lg:col-span-4 space-y-8 w-full">
          {/* ── Widgets: Wallet & Points ── */}
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-4 select-none">
            {/* YatraWallet Widget */}
            <div className="bg-surface-container-low p-stack-md rounded-2xl border border-outline-variant flex flex-col justify-between h-36">
              <div>
                <span className="font-label-sm text-label-sm text-tertiary uppercase tracking-wider block">YatraWallet</span>
                <div className="flex items-baseline gap-1 mt-1">
                  <span className="font-headline-md text-headline-md font-bold text-on-surface">₹{Math.round(walletAvailable)}</span>
                  {walletEscrow > 0 && (
                    <span className="font-label-sm text-label-sm text-secondary font-bold ml-1">● ₹{Math.round(walletEscrow)} escrow</span>
                  )}
                </div>
              </div>
              <button 
                onClick={onTopUpClick}
                className="bg-secondary text-white font-label-lg text-label-lg py-2 rounded-lg text-center hover:brightness-110 transition-all active:scale-95 text-[12px] font-bold"
              >
                Top Up
              </button>
            </div>

            {/* GreenPoints Widget */}
            <div className="bg-surface-container-low p-stack-md rounded-2xl border border-outline-variant flex flex-col justify-between h-36 relative overflow-hidden">
              <div className="absolute -right-4 -top-4 opacity-10">
                <span className="material-symbols-outlined text-6xl text-secondary" style={{ fontVariationSettings: "'FILL' 1" }}>eco</span>
              </div>
              <div>
                <span className="font-label-sm text-label-sm text-tertiary uppercase tracking-wider block">GreenPoints</span>
                <div className="mt-1">
                  <span className="font-headline-md text-headline-md font-bold text-on-surface">{greenPoints} pts</span>
                </div>
              </div>
              <div className="flex items-center gap-1.5 text-secondary">
                <span className="material-symbols-outlined text-sm">trending_down</span>
                <span className="font-label-lg text-label-lg">{Number(co2Saved ?? 2.2).toFixed(1)} kg CO₂ saved</span>
              </div>
            </div>
          </div>

          {/* ── Recommended Card ── */}
          {!loading && (
            <section className="pb-8">
              <div className="bg-surface-container-high rounded-2xl border border-outline-variant overflow-hidden shadow-sm">
                <div className="h-40 w-full bg-surface-container-highest relative">
                  <img 
                    className="w-full h-full object-cover opacity-80" 
                    alt="Electric Bus M-45"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuByW3k2HpZaLdm9kD5OOAZI037cNph89M4JK1uGOG-kZoEGepULWToc_WLwoE3HY2mnxvxU9FyuQiVOfRHUsLoIItpQ6LshFLTHSMz6P62r0Ud6TuoAOTGS18M9ROLbMGL8m-kZ1ArZXCnyKu-uj7mEdg4NoMSh2xnOQvTCZXp3QignfF3IVVWFKjUK-YCWWY_ZiUg-N-gBrQVSQKB6eJKb_2q4E6KVI0X1lGjB-U3X_rKJzPF0TEBXUPrDlc_iR0xroK6W4l-E_nxu"
                  />
                  <div className="absolute bottom-3 left-3 bg-surface/90 backdrop-blur-md px-3 py-1 rounded-full text-secondary font-bold text-label-md border border-outline-variant">
                    Electric Bus M-45
                  </div>
                </div>
                <div className="p-stack-md flex justify-between items-center">
                  <div>
                    <h3 className="font-label-lg text-label-lg text-on-surface">AC Direct Service</h3>
                    <p className="font-body-sm text-body-sm text-tertiary">Every 15 mins from your location</p>
                  </div>
                  <button className="material-symbols-outlined text-secondary text-2xl">arrow_forward_ios</button>
                </div>
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  )
}

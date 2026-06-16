// src/components/SegmentTimeline.jsx
import { useEffect, useRef } from 'react'
import { MODE_CONFIG } from '../constants/modes'

// Node coordinates matching backend database.py COORDINATES
const NODE_COORDS = {
  SRM_Dorm: [12.8235, 80.0425],
  Potheri_Station: [12.8242, 80.0440],
  Kattankulathur_Station: [12.8340, 80.0520],
  Tambaram_Station: [12.9250, 80.1200],
  Guindy_Station: [13.0084, 80.2131],
  Chennai_Egmore: [13.0783, 80.2598],
  Chennai_Central: [13.0827, 80.2707],
  OMR_Tidel_Park: [12.9896, 80.2486],
  OMR_Sholinganallur: [12.8976, 80.2281],
  Koyambedu_CMBT: [13.0680, 80.2030],
  Kilambakkam_KCBT: [12.8710, 80.0810],
  Airport: [12.9856, 80.1809],
  T_Nagar: [13.0418, 80.2341],
  Velachery: [12.9815, 80.2224],
  Adyar: [13.0063, 80.2575],
  Kanchipuram: [12.8387, 79.7016],
  Chengalpattu: [12.6934, 79.9772],
  Vellore: [12.9165, 79.1325],
  Pondicherry: [11.9416, 79.8083],
  Coimbatore: [11.0168, 76.9558],
  Madurai: [9.9252, 78.1198],
  Trichy: [10.7905, 78.7047],
}

const LEG_THEME = {
  Suburban_Train: { color: '#f59e0b', bg: '#FFFBEB', symbolIcon: 'directions_railway', label: 'Suburban Rail' },
  Intercity_Train: { color: '#f59e0b', bg: '#FFFBEB', symbolIcon: 'directions_railway', label: 'Intercity Express' },
  Metro: { color: '#06b6d4', bg: '#ECFEFF', symbolIcon: 'directions_transit', label: 'CMRL Metro' },
  MTC_Bus: { color: '#ef4444', bg: '#FEF2F2', symbolIcon: 'directions_bus', label: 'MTC Bus' },
  SETC_Bus: { color: '#ef4444', bg: '#FEF2F2', symbolIcon: 'directions_bus', label: 'SETC Bus' },
  Town_Bus: { color: '#ef4444', bg: '#FEF2F2', symbolIcon: 'directions_bus', label: 'Town Bus' },
  Rapido_Bike: { color: '#10b981', bg: '#ECFDF5', symbolIcon: 'two_wheeler', label: 'Rapido Bike' },
  Ola_Auto: { color: '#10b981', bg: '#ECFDF5', symbolIcon: 'two_wheeler', label: 'Ola Auto' },
  Walk: { color: '#64748b', bg: 'transparent', symbolIcon: 'directions_walk', label: 'Walk' },
}

function LeafletMap({ segments }) {
  const mapRef = useRef(null)
  const instanceRef = useRef(null)

  useEffect(() => {
    if (!window.L || !mapRef.current || !segments?.length) return
    const L = window.L

    // Destroy previous instance
    if (instanceRef.current) {
      instanceRef.current.remove()
      instanceRef.current = null
    }

    const map = L.map(mapRef.current, { zoomControl: true, scrollWheelZoom: false })
    instanceRef.current = map

    // Theme sensitive tiles
    const isDark = document.documentElement.classList.contains('dark')
    const tileUrl = isDark
      ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
      : 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'

    L.tileLayer(tileUrl, {
      attribution: '©OpenStreetMap ©CartoDB',
      maxZoom: 15,
    }).addTo(map)

    const latlngs = []

    segments.forEach((seg, i) => {
      const from = seg.from_coords || NODE_COORDS[seg.from_node]
      const to = seg.to_coords || NODE_COORDS[seg.to_node]
      if (!from || !to) return

      const cfg = MODE_CONFIG[seg.mode]
      const color = cfg?.color ?? '#06b6d4'

      // Draw segment line
      L.polyline([from, to], { color, weight: 4, opacity: 0.85 }).addTo(map)

      // Station dot
      if (i === 0) {
        latlngs.push(from)
        L.circleMarker(from, { radius: 7, color, fillColor: isDark ? '#0A0F1E' : '#FFFFFF', fillOpacity: 1, weight: 2 })
          .bindTooltip(seg.from_node.replace(/_/g, ' '), { permanent: false })
          .addTo(map)
      }
      latlngs.push(to)
      L.circleMarker(to, { radius: i === segments.length - 1 ? 9 : 6, color, fillColor: color, fillOpacity: 0.9, weight: 2 })
        .bindTooltip(seg.to_node.replace(/_/g, ' '), { permanent: false })
        .addTo(map)
    })

    if (latlngs.length) map.fitBounds(latlngs, { padding: [24, 24] })

    return () => {
      map.remove()
      instanceRef.current = null
    }
  }, [segments])

  return <div ref={mapRef} className="yatrai-map w-full" />
}

export default function SegmentTimeline({ route }) {
  const segments = route?.segments ?? []
  const isDark = document.documentElement.classList.contains('dark')

  return (
    <div className="glass-panel rounded-3xl p-5 flex flex-col gap-5 animate-fade-in-up">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-outline-variant pb-3 select-none">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>route</span>
          <h3 className="font-outfit font-bold text-[14px] text-on-surface">Selected Route Timeline</h3>
        </div>
        <div className="flex gap-2 text-[11px] font-bold">
          <span className="bg-[#1E3A8A]/5 dark:bg-[#6366F1]/5 text-secondary px-2.5 py-1 rounded-full border border-outline-variant font-sans">
            ⏱ {Math.round(route.total_time)} min
          </span>
          <span className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20 font-sans">
            ₹{route.total_fare}
          </span>
        </div>
      </div>

      {/* Leaflet Map */}
      <div className="relative overflow-hidden rounded-2xl border border-outline-variant shadow-inner h-52 w-full">
        <LeafletMap segments={segments} />
        <div className="absolute top-3 left-3 px-2.5 py-1 bg-white/90 dark:bg-slate-900/90 border border-outline-variant text-on-surface text-[11px] font-semibold rounded-full shadow-sm z-10 select-none">
          Route Map
        </div>
      </div>

      {/* Segment Steps */}
      <div className="flex flex-col gap-3">
        <div className="flex flex-col">
          {segments.map((seg, i) => {
            const theme = LEG_THEME[seg.mode] || LEG_THEME.Walk
            const isLast = i === segments.length - 1
            const isWalk = seg.mode === 'Walk'

            if (isWalk) {
              return (
                <div key={i} className="flex flex-col w-full">
                  {/* Inline Walk Segment */}
                  <div className="flex items-center gap-2 px-4 py-2 bg-transparent text-slate-500 dark:text-slate-400 text-[12px] font-normal border border-dashed border-outline-variant rounded-xl my-1 select-none">
                    <span className="material-symbols-outlined text-[18px]">{theme.symbolIcon}</span>
                    <span>{seg.instruction_en || `Walk ${Math.round(seg.duration)} min to next leg`}</span>
                    <span className="ml-auto">→</span>
                  </div>

                  {!isLast && (
                    <div className="flex justify-center w-full my-1">
                      <div className="w-[2px] h-3 border-l-2 border-dashed border-outline-variant" />
                    </div>
                  )}
                </div>
              )
            }

            return (
              <div key={i} className="flex flex-col w-full animate-fade-in-up">
                {/* Leg card */}
                <div className="relative flex rounded-xl bg-surface border border-outline-variant shadow-sm overflow-hidden dark:bg-[#111827]">
                  {/* Left rail strip */}
                  <div className="w-1 shrink-0" style={{ backgroundColor: theme.color }} />
                  
                  <div className="flex-1 p-3.5 flex flex-col">
                    {/* Top Row */}
                    <div className="flex justify-between items-start gap-4">
                      {/* Left: Icon + Mode Name */}
                      <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-[24px] leading-none shrink-0" style={{ color: theme.color }}>
                          {theme.symbolIcon}
                        </span>
                        <span className="text-[13px] font-medium uppercase tracking-wider" style={{ color: theme.color }}>
                          {theme.label} {seg.line_name ? `• ${seg.line_name}` : ''}
                        </span>
                      </div>
                      {/* Right: Departure Time */}
                      <div className="text-right flex flex-col items-end">
                        <span className="text-[15px] font-medium text-[#0F172A] dark:text-[#F9FAFB] font-mono leading-none">
                          {seg.start_time_str}
                        </span>
                        <span className="text-[12px] font-normal text-slate-500 dark:text-slate-400 mt-1.5 truncate max-w-[160px]">
                          {seg.from_node.replace(/_/g, ' ')}
                        </span>
                      </div>
                    </div>

                    {/* Status Pill / Live Telemetry */}
                    {seg.mode === 'Metro' && (
                      <div className="flex items-center gap-3 mt-3 bg-green-500/10 dark:bg-green-900/20 px-3 py-2 rounded-lg border border-green-500/30">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_#22c55e]" />
                        <span className="text-[11.5px] font-medium text-green-600 dark:text-green-400">Metro arriving in 3 mins</span>
                      </div>
                    )}
                    {seg.mode === 'Suburban_Train' && (
                      <div className="flex items-center gap-3 mt-3 bg-amber-500/10 dark:bg-amber-900/20 px-3 py-2 rounded-lg border border-amber-500/30">
                        <div className="w-2 h-2 bg-amber-500 rounded-full animate-pulse shadow-[0_0_8px_#f59e0b]" />
                        <span className="text-[11.5px] font-medium text-amber-600 dark:text-amber-400">Train arriving in 5 mins</span>
                      </div>
                    )}

                    {/* Bottom Row */}
                    <div className="flex justify-between items-center gap-4 mt-3 pt-2.5 border-t border-black/[0.03] dark:border-white/[0.03]">
                      {/* Fare Pill */}
                      <span 
                        className="text-[12px] font-medium px-2 py-0.5 rounded-full select-none"
                        style={{
                          backgroundColor: isDark ? 'rgba(255,255,255,0.08)' : `${theme.color}15`,
                          color: theme.color
                        }}
                      >
                        ₹{seg.fare}
                      </span>
                      {/* Duration */}
                      <span className="text-[13px] font-normal text-slate-500 dark:text-slate-400 font-sans">
                        {Math.round(seg.duration)} min
                      </span>
                    </div>
                  </div>
                </div>

                {/* Dashed connector below this card */}
                {!isLast && (
                  <div className="flex justify-center w-full my-1">
                    <div className="w-[2px] h-4 border-l-2 border-dashed" style={{ borderColor: theme.color }} />
                  </div>
                )}
              </div>
            )
          })}

          {/* Final destination node */}
          {segments.length > 0 && (
            <div className="flex flex-col w-full animate-fade-in-up">
              <div className="flex justify-center w-full my-1">
                <div className="w-[2px] h-3 border-l-2 border-dashed border-outline-variant" />
              </div>
              
              <div className="flex items-center gap-3 px-4 py-3 bg-surface border border-outline-variant rounded-xl dark:bg-[#111827]">
                <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center shrink-0">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-[13px] font-semibold text-[#0F172A] dark:text-[#F9FAFB] truncate font-sans">
                    {segments[segments.length - 1]?.to_node.replace(/_/g, ' ')}
                  </p>
                  <p className="text-[12px] text-slate-400 mt-0.5 font-sans">{route.end_time_str} — Arrival</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

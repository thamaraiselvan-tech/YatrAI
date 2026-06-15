// src/components/DisruptionPanel.jsx
import { useState } from 'react'
import { toggleDisruption } from '../services/api'
import { MODE_CONFIG, TRANSIT_MODES_LIST } from '../constants/modes'

const DISRUPTION_MODE_ICONS = {
  Suburban_Train: 'directions_railway',
  Intercity_Train: 'directions_railway',
  Metro: 'directions_transit',
  MTC_Bus: 'directions_bus',
  SETC_Bus: 'directions_bus',
  Town_Bus: 'directions_bus',
  Rapido_Bike: 'two_wheeler',
  Ola_Auto: 'two_wheeler',
  Walk: 'directions_walk',
}

export default function DisruptionPanel({ disruptions, onDisruptionsChange }) {
  const [toggling, setToggling] = useState(null)

  async function handleToggle(mode) {
    const isDisrupted = disruptions.includes(mode)
    setToggling(mode)
    try {
      const res = await toggleDisruption(mode, !isDisrupted)
      onDisruptionsChange(res.disrupted_modes)
    } catch (_) {}
    finally { setToggling(null) }
  }

  return (
    <div className="flex flex-col gap-4 pb-10">

      {/* Disruption Alert Banner (Exactly 56px height, Amber pulse) */}
      {disruptions.length > 0 && (
        <div className="h-14 bg-error-container text-on-error-container border border-error/20 flex items-center justify-between px-3.5 shadow-sm rounded-xl relative overflow-hidden animate-fade-in-up animate-pulse-border select-none">
          <div className="flex items-center gap-2.5 min-w-0">
            <span className="material-symbols-outlined text-error shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
              warning
            </span>
            <div className="flex flex-col min-w-0">
              <span className="text-[13px] font-bold truncate leading-none">
                Service Alerts Active
              </span>
              <span className="text-[11px] opacity-80 truncate mt-1">
                {disruptions.length} transit mode(s) disrupted. Alternate routes calculated.
              </span>
            </div>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="h-8 px-3 border border-error/30 text-error font-semibold text-[11px] rounded-lg shrink-0 hover:bg-error-container/20 flex items-center justify-center relative before:content-[''] before:absolute before:-inset-2 before:bg-transparent"
          >
            Reroute
          </button>
        </div>
      )}

      {/* Header Info */}
      <div className="glass-panel rounded-2xl p-4 flex flex-col gap-1 select-none">
        <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400">
          <span className="material-symbols-outlined text-secondary text-[20px]">sensors</span>
          <p className="text-[13px] font-bold uppercase tracking-wider font-outfit">Transit Simulator</p>
        </div>
        <p className="text-[12px] text-slate-500 dark:text-slate-400 leading-relaxed">
          Simulate real-time disruptions on Chennai transit. The routing engine automatically circumvents disabled modes.
        </p>
      </div>

      {/* Mode toggles */}
      <div className="flex flex-col gap-2.5">
        {TRANSIT_MODES_LIST.map(mode => {
          const cfg = MODE_CONFIG[mode]
          const isDisrupted = disruptions.includes(mode)
          const isLoading = toggling === mode
          if (!cfg) return null

          return (
            <div
              key={mode}
              className="glass-panel rounded-xl px-4 py-3 flex items-center justify-between hover:border-slate-300 dark:hover:border-slate-700 transition-all duration-150"
            >
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-[24px] shadow-sm bg-surface-container-low"
                  style={{ color: cfg.color }}
                >
                  <span className="material-symbols-outlined">{DISRUPTION_MODE_ICONS[mode]}</span>
                </div>
                <div>
                  <p className="text-[13.5px] font-semibold text-on-surface font-outfit">{cfg.label}</p>
                  <p className="text-[12px] mt-0.5 font-medium flex items-center gap-1.5" style={{ color: isDisrupted ? '#ba1a1a' : '#10b981' }}>
                    {isDisrupted ? (
                      <>
                        <span className="w-1.5 h-1.5 rounded-full bg-error animate-pulse" />
                        Suspended
                      </>
                    ) : (
                      <>
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                        Operational
                      </>
                    )}
                  </p>
                </div>
              </div>

              {/* iOS Switch with red/amber-glowing indicators */}
              <button
                onClick={() => handleToggle(mode)}
                disabled={isLoading}
                className="w-14 h-11 flex items-center justify-center bg-transparent outline-none disabled:opacity-50 shrink-0 select-none"
              >
                <div
                  className={`relative w-11 h-6 rounded-full transition-all duration-150 ease-in-out border ${
                    isDisrupted 
                      ? 'bg-rose-500 border-rose-600 shadow-[0_0_10px_rgba(239,68,68,0.35)]' 
                      : 'bg-slate-200 dark:bg-slate-800 border-outline-variant'
                  }`}
                  style={{ height: '24px' }}
                >
                  <span
                    className={`absolute top-[2px] left-[2px] w-[18px] h-[18px] flex items-center justify-center rounded-full bg-white transition-all duration-150 ease-out shadow ${
                      isDisrupted ? 'translate-x-[20px]' : 'translate-x-0'
                    }`}
                  >
                    {isLoading && (
                      <span className="material-symbols-outlined text-[10px] animate-spin text-slate-800">sync</span>
                    )}
                  </span>
                </div>
              </button>
            </div>
          )
        })}
      </div>

      {/* SSE live indicator */}
      <div className="flex items-center gap-2 px-2 select-none">
        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
        <p className="text-[12px] font-normal text-slate-400 dark:text-slate-500">
          SSE Stream active — updates push instantly
        </p>
      </div>
    </div>
  )
}

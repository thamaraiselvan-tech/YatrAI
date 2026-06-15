// src/components/JournalPanel.jsx
import { useState, useEffect, useCallback, useRef } from 'react'
import { getJournal, getJournalAnalytics, semanticLog, queryJournal, deleteJournalEntry, depositFunds } from '../services/api'
import { useVoiceInput } from '../hooks/useVoiceInput'
import { MODE_CONFIG } from '../constants/modes'
import DisruptionPanel from './DisruptionPanel'

const CATEGORY_COLORS = {
  'Commute': '#3B82F6',
  'Business Commute': '#f59e0b',
  'Leisure': '#10b981',
}

const PASS_MODE_ICONS = {
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

function CircularDial({ pct, value, label, subtext, color = '#3B82F6' }) {
  const radius = 28
  const circ = 2 * Math.PI * radius
  const strokeDashoffset = circ - (pct / 100) * circ

  return (
    <div className="flex flex-col items-center text-center p-3 bg-surface-container-low border border-outline-variant rounded-2xl flex-1 min-w-[100px]">
      <div className="relative w-16 h-16 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx="32"
            cy="32"
            r={radius}
            className="stroke-slate-100 dark:stroke-slate-800"
            strokeWidth="5"
            fill="transparent"
          />
          <circle
            cx="32"
            cy="32"
            r={radius}
            stroke={color}
            strokeWidth="5"
            fill="transparent"
            strokeDasharray={circ}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-500 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-[12px] font-bold text-on-surface font-mono">{value}</span>
        </div>
      </div>
      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mt-2">{label}</span>
      <span className="text-[9px] text-on-surface-variant mt-0.5 truncate max-w-full">{subtext}</span>
    </div>
  )
}

function SegmentedBar({ ratios }) {
  const modeColors = {
    Metro: '#06b6d4', // Cyan
    Train: '#f59e0b', // Gold
    Bus: '#ef4444',   // Red
    Cab: '#10b981',   // Green
  }

  return (
    <div className="flex flex-col p-4 bg-surface-container-low border border-outline-variant rounded-2xl w-full">
      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-3 block">
        Modes Used Ratio
      </span>
      
      {/* Segmented bar */}
      <div className="h-3 w-full rounded-full overflow-hidden flex bg-slate-100 dark:bg-slate-800">
        {Object.entries(ratios).map(([mode, pct]) => {
          const color = modeColors[mode] || '#64748b'
          if (pct === 0) return null
          return (
            <div
              key={mode}
              style={{ width: `${pct}%`, backgroundColor: color }}
              className="h-full transition-all"
              title={`${mode}: ${pct}%`}
            />
          )
        })}
      </div>

      {/* Legend Row */}
      <div className="grid grid-cols-4 gap-1 mt-4">
        {Object.entries(ratios).map(([mode, pct]) => {
          const color = modeColors[mode] || '#64748b'
          return (
            <div key={mode} className="flex flex-col items-center text-center">
              <div className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color }} />
                <span className="text-[10px] font-semibold text-on-surface">{mode}</span>
              </div>
              <span className="text-[9px] text-slate-400 dark:text-slate-500 font-mono mt-0.5">{pct}%</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function AnalyticsCard({ analytics, onRedeem }) {
  if (!analytics) return null
  const { total_cost, monthly_limit, co2_saved_kg, ratios } = analytics
  
  // Spend budget percentage
  const budgetPct = Math.min((total_cost / monthly_limit) * 100, 100)
  
  // Points: 10 pts per kg of CO2 saved
  const pts = Math.round(co2_saved_kg * 10)
  const co2Pct = Math.min((pts % 100), 100)

  return (
    <div className="flex flex-col gap-4 animate-fade-in-up">
      {/* 3 Circular Dial SVG Grid */}
      <div className="flex gap-3 w-full">
        {/* Budget Dial */}
        <CircularDial
          pct={budgetPct}
          value={`₹${total_cost.toFixed(0)}`}
          label="Budget"
          subtext={`of ₹${monthly_limit}`}
          color="#3B82F6"
        />

        {/* Carbon Offset Dial */}
        <CircularDial
          pct={co2Pct}
          value={`${co2_saved_kg.toFixed(1)}kg`}
          label="CO₂ Saved"
          subtext={`${pts} pts earned`}
          color="#10b981"
        />

        {/* Reward Status Dial */}
        <CircularDial
          pct={co2Pct}
          value={`${100 - (pts % 100)}`}
          label="Next Reward"
          subtext="pts required"
          color="#06b6d4"
        />
      </div>

      {/* Segmented Mode Ratio Tracker */}
      <SegmentedBar ratios={ratios} />

      {/* Reward Milestones */}
      <div className="glass-panel rounded-2xl p-4 flex flex-col gap-2.5">
        <div className="flex items-center gap-1.5 text-on-surface font-semibold text-[12px] uppercase tracking-wider font-outfit">
          <span className="material-symbols-outlined text-teal-500 text-sm">workspace_premium</span>
          <span>Earned Travel Rewards (Click to Redeem)</span>
        </div>
        <div className="flex gap-2 flex-wrap mt-1">
          <button 
            onClick={() => onRedeem(10, 100)}
            className="px-2.5 py-1 text-[11px] font-bold rounded-full bg-teal-50 dark:bg-teal-950/20 text-[#10B981] border border-[#10B981]/20 hover:bg-[#10B981]/10 transition-colors active:scale-95 duration-100"
          >
            🎟️ ₹10 CMRL Metro discount (100 pts)
          </button>
          <button 
            onClick={() => onRedeem(25, 200)}
            className="px-2.5 py-1 text-[11px] font-bold rounded-full bg-teal-50 dark:bg-teal-950/20 text-[#10B981] border border-[#10B981]/20 hover:bg-[#10B981]/10 transition-colors active:scale-95 duration-100"
          >
            🛺 ₹25 Ola Auto voucher (200 pts)
          </button>
        </div>
      </div>
    </div>
  )
}

export default function JournalPanel({ disruptions, onDisruptionsChange, user, onLogout }) {
  const [journal, setJournal] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [tab, setTab] = useState('logs')   // 'logs' | 'analytics' | 'ask' | 'simulator'
  const [logText, setLogText] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [busy, setBusy] = useState(false)

  const loadJournal = useCallback(async () => {
    const [j, a] = await Promise.all([getJournal(), getJournalAnalytics()])
    setJournal(j)
    
    if (a) {
      const breakdown = a.mode_breakdown || {}
      const trainCount = (breakdown.Suburban_Train || 0) + (breakdown.Intercity_Train || 0)
      const metroCount = breakdown.Metro || 0
      const busCount = (breakdown.MTC_Bus || 0) + (breakdown.SETC_Bus || 0) + (breakdown.Town_Bus || 0)
      const cabCount = (breakdown.Rapido_Bike || 0) + (breakdown.Ola_Auto || 0)
      const total = trainCount + metroCount + busCount + cabCount

      let ratios = { Metro: 0, Train: 0, Bus: 0, Cab: 0 }
      if (total > 0) {
        ratios = {
          Metro: Math.round((metroCount / total) * 100),
          Train: Math.round((trainCount / total) * 100),
          Bus: Math.round((busCount / total) * 100),
          Cab: Math.round((cabCount / total) * 100)
        }
      }

      setAnalytics({
        total_cost: a.total_cost || 0,
        monthly_limit: 1500,
        co2_saved_kg: (a.total_co2_saved || 0) / 1000,
        ratios
      })
    } else {
      setAnalytics(null)
    }
  }, [])

  useEffect(() => { loadJournal() }, [loadJournal])

  const handleVoiceLog = useCallback((text) => setLogText(text), [])
  const { listening, start: startVoice, stop: stopVoice } = useVoiceInput(handleVoiceLog)

  async function handleSemanticLog() {
    if (!logText.trim()) return
    setBusy(true)
    try {
      await semanticLog(logText)
      setLogText('')
      await loadJournal()
    } catch (_) {}
    finally { setBusy(false) }
  }

  async function handleAsk() {
    if (!question.trim()) return
    setBusy(true)
    setAnswer('')
    try {
      const res = await queryJournal(question)
      setAnswer(res.answer)
    } catch (e) {
      setAnswer('Could not get an answer right now.')
    } finally { setBusy(false) }
  }

  async function handleDelete(id) {
    await deleteJournalEntry(id)
    await loadJournal()
  }

  const handleRedeemReward = useCallback(async (amount, ptsRequired) => {
    const pts = Math.round((analytics?.co2_saved_kg || 0) * 10)
    if (pts < ptsRequired) {
      alert(`Insufficient GreenPoints: You need ${ptsRequired} points to redeem this voucher (current: ${pts}).`)
      return
    }

    try {
      setBusy(true)
      await depositFunds(amount)
      alert(`Success! ₹${amount} has been added to your YatraWallet balance.`)
      await loadJournal()
      window.dispatchEvent(new Event('wallet-updated'))
    } catch (e) {
      alert(`Failed to redeem voucher: ${e.message}`)
    } finally {
      setBusy(false)
    }
  }, [analytics, loadJournal])

  const logs = journal?.logs ?? []

  return (
    <div className="flex flex-col gap-4 pb-10">
      
      {/* Profile Header */}
      <div className="glass-panel rounded-2xl p-4 flex items-center justify-between animate-fade-in-up">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center font-bold text-[18px]">
            {user?.name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'JD'}
          </div>
          <div>
            <h2 className="text-[15px] font-bold text-on-surface">{user?.name || 'John Doe'}</h2>
            <p className="text-[12px] text-slate-400 dark:text-slate-500">{user?.role || 'Pro Commuter'} · {user?.email}</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 hover:bg-red-100/50 font-bold rounded-xl text-[12px] transition-colors border border-red-500/10 active:scale-95 duration-100"
        >
          <span className="material-symbols-outlined text-[16px]">logout</span>
          <span>Logout</span>
        </button>
      </div>

      {/* Sliding tabs block */}
      <div className="flex bg-surface-container-high dark:bg-[#111827] border border-outline-variant rounded-2xl p-1 gap-1 select-none h-[52px] items-center">
        {[
          { id: 'logs', label: 'Logs', icon: 'book' },
          { id: 'analytics', label: 'Analytics', icon: 'bar_chart' },
          { id: 'ask', label: 'Ask AI', icon: 'forum' },
          { id: 'simulator', label: 'Live Status', icon: 'sensors' },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex-grow flex-1 h-10 rounded-xl flex items-center justify-center gap-1.5 text-[12px] font-semibold transition-all ${
              tab === t.id
                ? 'bg-secondary text-white shadow-sm'
                : 'text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300'
            }`}
          >
            <span className="material-symbols-outlined text-[18px]">{t.icon}</span>
            <span>{t.label}</span>
          </button>
        ))}
      </div>

      {/* ── Logs tab ── */}
      {tab === 'logs' && (
        <>
          {/* Semantic log input */}
          <div className="glass-panel rounded-2xl p-4 flex flex-col gap-3">
            <p className="text-[12px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-outfit">Log a Journey</p>
            <div className="relative">
              <textarea
                value={logText}
                onChange={e => setLogText(e.target.value)}
                rows={2}
                placeholder={'"Took suburban rail from Guindy to Egmore, paid ₹10"'}
                className="w-full bg-surface-container-low dark:bg-[#070b13] border border-outline-variant rounded-xl px-3 py-3 pr-12
                           text-[13px] text-on-surface placeholder-slate-400 resize-none outline-none
                           focus:border-secondary transition-colors font-sans"
              />
              <button
                onClick={listening ? stopVoice : startVoice}
                className={`absolute right-1 top-1 w-11 h-11 flex items-center justify-center rounded-xl transition-colors ${
                  listening ? 'text-white bg-secondary animate-mic-pulse' : 'text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <span className="material-symbols-outlined text-[20px]">{listening ? 'mic_off' : 'mic'}</span>
              </button>
            </div>
            <button
              onClick={handleSemanticLog}
              disabled={busy || !logText.trim()}
              className="flex items-center justify-center gap-2 bg-secondary hover:brightness-110 text-white
                         font-medium rounded-xl h-11 text-[13px] disabled:opacity-30 transition-all active:scale-[0.98]"
            >
              {busy ? (
                <span className="material-symbols-outlined text-[16px] animate-spin">sync</span>
              ) : (
                <span className="material-symbols-outlined text-[16px]">auto_awesome</span>
              )}
              {busy ? 'Processing...' : 'Log via AI'}
            </button>
          </div>

          {/* Log entries */}
          <div className="flex flex-col gap-3">
            {logs.length === 0 ? (
              <div className="text-center py-10 text-slate-400 dark:text-slate-500 text-[12px]">No travel logs yet</div>
            ) : logs.map(log => (
              <div key={log.id} className="glass-panel rounded-2xl p-4 flex flex-col gap-2 hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex flex-col">
                    <p className="text-[13.5px] font-semibold text-on-surface">
                      {log.from_node.replace(/_/g, ' ')} → {log.to_node.replace(/_/g, ' ')}
                    </p>
                    <p className="text-[12px] text-slate-400 dark:text-slate-500 font-mono mt-0.5">{log.date}</p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span
                      className="text-[11px] px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider"
                      style={{
                        background: `${CATEGORY_COLORS[log.category] ?? '#3B82F6'}15`,
                        color: CATEGORY_COLORS[log.category] ?? '#3B82F6',
                      }}
                    >
                      {log.category}
                    </span>
                    <button
                      onClick={() => handleDelete(log.id)}
                      className="w-10 h-10 flex items-center justify-center text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl transition-colors"
                      title="Delete log"
                    >
                      <span className="material-symbols-outlined text-[20px]">delete</span>
                    </button>
                  </div>
                </div>

                <div className="flex gap-1.5 flex-wrap">
                  {log.modes_used?.map(mode => {
                    const m = MODE_CONFIG[mode]
                    if (!m) return null
                    return (
                      <span key={mode} className="text-[12px] px-2 py-0.5 rounded-full bg-surface-container-high border border-outline-variant flex items-center gap-1">
                        <span className="material-symbols-outlined text-[14px]">{PASS_MODE_ICONS[mode] || 'directions_walk'}</span>
                        <span className="text-slate-500 dark:text-slate-400">{m.label}</span>
                      </span>
                    )
                  })}
                </div>

                {log.notes && (
                  <p className="text-[12px] text-slate-500 dark:text-slate-400 leading-relaxed bg-surface-container-low p-2.5 rounded-xl border border-outline-variant">{log.notes}</p>
                )}

                <div className="flex gap-4 text-[12px] border-t border-outline-variant/30 pt-2 mt-1">
                  <span className="text-slate-500 dark:text-slate-400 font-semibold">Fare: <span className="text-on-surface font-mono font-bold">₹{log.cost}</span></span>
                  <span className="text-teal-600 dark:text-teal-400 font-semibold">Saved: 🌿 <span className="font-bold text-teal-600 dark:text-teal-400">{log.co2_saved}g CO₂</span></span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* ── Analytics tab ── */}
      {tab === 'analytics' && <AnalyticsCard analytics={analytics} onRedeem={handleRedeemReward} />}

      {/* ── Ask AI tab ── */}
      {tab === 'ask' && (
        <div className="glass-panel rounded-2xl p-4 flex flex-col gap-4">
          <p className="text-[12px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-outfit">
            Gemini Assistant
          </p>
          
          {/* Chat bubbles container */}
          {(question || answer) && (
            <div className="flex flex-col gap-3 bg-surface-container-low border border-outline-variant rounded-2xl p-3">
              {question && (
                <div className="flex justify-end">
                  <div className="max-w-[85%] bg-secondary/10 border border-secondary/20 rounded-2xl rounded-tr-none px-3 py-2 text-[13px] text-on-surface font-medium">
                    {question}
                  </div>
                </div>
              )}
              {busy ? (
                <div className="flex items-center gap-1.5 text-[12px] text-slate-400">
                  <span className="material-symbols-outlined text-[14px] animate-spin">sync</span>
                  Gemini is checking logs...
                </div>
              ) : answer ? (
                <div className="flex justify-start items-start gap-2">
                  <div className="w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-white text-[10px] font-bold shrink-0">
                    AI
                  </div>
                  <div className="max-w-[85%] bg-surface border border-outline-variant rounded-2xl rounded-tl-none px-3 py-2 text-[13px] text-on-surface leading-relaxed shadow-sm">
                    {answer}
                  </div>
                </div>
              ) : null}
            </div>
          )}

          {/* Unified Input bar */}
          <div className="relative flex items-center h-[52px] rounded-xl bg-surface-container-low border border-outline-variant px-3 focus-within:border-secondary transition-all">
            <input
              value={question}
              onChange={e => setQuestion(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !busy && handleAsk()}
              placeholder="Ask about travels, carbon footprint, etc."
              className="flex-1 h-full bg-transparent text-[13px] outline-none text-on-surface placeholder-slate-400"
              disabled={busy}
            />
            <button
              onClick={handleAsk}
              disabled={busy || !question.trim()}
              className="w-11 h-11 flex items-center justify-center text-secondary disabled:opacity-30 shrink-0"
              title="Send to Gemini"
            >
              {busy ? (
                <span className="material-symbols-outlined text-[18px] animate-spin">sync</span>
              ) : (
                <span className="material-symbols-outlined text-[18px]">send</span>
              )}
            </button>
          </div>
        </div>
      )}

      {/* ── Simulator tab ── */}
      {tab === 'simulator' && (
        <DisruptionPanel
          disruptions={disruptions}
          onDisruptionsChange={onDisruptionsChange}
        />
      )}
    </div>
  )
}

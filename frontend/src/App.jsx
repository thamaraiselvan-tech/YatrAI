// src/App.jsx
import { useState, useCallback, useEffect } from 'react'
import { useSSE } from './hooks/useSSE'
import { useWallet } from './hooks/useWallet'
import { useGeoLocation } from './hooks/useGeoLocation'
import { useVoiceNav } from './hooks/useVoiceNav'
import { lockEscrow, refundEscrow, releaseSegment } from './services/api'
import PlannerView from './components/PlannerView'
import ActiveTripView from './components/ActiveTripView'
import WalletPanel from './components/WalletPanel'
import JournalPanel from './components/JournalPanel'
import LiveMap from './components/LiveMap'
import Login from './components/Login'
import Loading from './components/Loading'

const TABS = [
  { id: 'planner',    label: 'Home',       icon: 'home' },
  { id: 'map',        label: 'Journey',    icon: 'directions_transit' },
  { id: 'pass',       label: 'Pass',       icon: 'qr_code_2' },
  { id: 'wallet',     label: 'Wallet',     icon: 'account_balance_wallet' },
  { id: 'profile',    label: 'Profile',    icon: 'person' },
]

export default function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem('yatrai_user')
    return saved ? JSON.parse(saved) : null
  })
  const [isLoggedIn, setIsLoggedIn] = useState(() => !!localStorage.getItem('yatrai_user'))
  const [pendingUser, setPendingUser] = useState(null)
  const [isLoadingApp, setIsLoadingApp] = useState(false)
  const [isMobileDrawerOpen, setIsMobileDrawerOpen] = useState(false)
  const [tab, setTab] = useState('planner')
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return document.documentElement.classList.contains('dark')
  })

  const handleLogin = useCallback((userData) => {
    setCurrentUser(userData)
    setIsLoggedIn(true)
    localStorage.setItem('yatrai_user', JSON.stringify(userData))
  }, [])

  const handleLogout = useCallback(() => {
    setCurrentUser(null)
    setIsLoggedIn(false)
    localStorage.removeItem('yatrai_user')
    setIsMobileDrawerOpen(false)
    setTab('planner')
  }, [])

  const handleStartLogin = useCallback((userData) => {
    setPendingUser(userData)
    setIsLoadingApp(true)
  }, [])

  const toggleTheme = useCallback(() => {
    setIsDarkMode(prev => {
      const next = !prev
      if (next) {
        document.documentElement.classList.add('dark')
        document.documentElement.classList.remove('light')
      } else {
        document.documentElement.classList.remove('dark')
        document.documentElement.classList.add('light')
      }
      return next
    })
  }, [])
  const [activeTrip, setActiveTrip] = useState(null)  // { trip_id, segments, currentSegIdx, moodData }
  const [localDisruptions, setLocalDisruptions] = useState([])
  const [mapExpanded, setMapExpanded] = useState(false)
  const [activeRoute, setActiveRoute] = useState(null) // route to show on map

  const { disruptions: liveDisruptions, lastAlert, clearAlert } = useSSE()
  const { wallet, refresh: refreshWallet } = useWallet()
  const geo = useGeoLocation()
  const voice = useVoiceNav()

  // Auto-start GPS tracking
  useEffect(() => {
    if (geo.supported && !geo.tracking) {
      geo.start()
    }
  }, [])

  // Listen for global wallet updates (e.g. from GreenPoints reward redemption)
  useEffect(() => {
    window.addEventListener('wallet-updated', refreshWallet)
    return () => window.removeEventListener('wallet-updated', refreshWallet)
  }, [refreshWallet])

  // Keep local disruption state in sync with SSE stream
  useEffect(() => {
    setLocalDisruptions(liveDisruptions)
  }, [liveDisruptions])

  // Voice announce when segment changes during active trip
  useEffect(() => {
    if (!activeTrip) return
    const seg = activeTrip.segments[activeTrip.currentSegIdx]
    if (seg && voice.enabled) {
      voice.speakSegment(seg)
    }
  }, [activeTrip?.currentSegIdx])

  // ── Start trip: lock escrow ─────────────────────────────────────────────────
  const handleStartTrip = useCallback(async (tripId, mood, route) => {
    try {
      await lockEscrow(tripId, route.total_fare, route.segments)
      setActiveTrip({
        trip_id: tripId,
        segments: route.segments,
        currentSegIdx: 0,
        moodData: route,
      })
      setActiveRoute(route)
      refreshWallet()
      setTab('pass')

      // Announce first segment
      if (voice.enabled && route.segments.length > 0) {
        voice.speak(`Trip started! ${route.segments.length} segments, total fare ${route.total_fare} rupees.`)
        setTimeout(() => voice.speakSegment(route.segments[0]), 3000)
      }
    } catch (e) {
      alert(`Could not start trip: ${e.message}`)
    }
  }, [refreshWallet, voice])

  // ── Complete segment: release fare ──────────────────────────────────────────
  const handleSegmentComplete = useCallback(async (segIdx) => {
    if (!activeTrip) return
    try {
      await releaseSegment(activeTrip.trip_id, segIdx)
      refreshWallet()
      const next = segIdx + 1
      if (next >= activeTrip.segments.length) {
        // Trip done
        setActiveTrip(prev => ({ ...prev, currentSegIdx: next }))
        if (voice.enabled) {
          voice.announceComplete(activeTrip.moodData?.total_fare)
        }
        setTimeout(() => {
          setActiveTrip(null)
          setActiveRoute(null)
        }, 4000)
      } else {
        setActiveTrip(prev => ({ ...prev, currentSegIdx: next }))
        // Announce next segment
        if (voice.enabled) {
          voice.announceNext(activeTrip.segments[next])
        }
      }
    } catch (e) {
      console.error('Segment release error:', e)
    }
  }, [activeTrip, refreshWallet, voice])

  // ── Cancel trip: refund escrow ──────────────────────────────────────────────
  const handleCancelTrip = useCallback(async () => {
    if (!activeTrip) return
    try {
      await refundEscrow(activeTrip.trip_id)
      setActiveTrip(null)
      setActiveRoute(null)
      refreshWallet()
      if (voice.enabled) {
        voice.speak('Trip cancelled. Fare refunded.')
      }
    } catch (e) {
      console.error('Refund error:', e)
    }
  }, [activeTrip, refreshWallet, voice])

  const handlePlaceSelect = useCallback((place) => {
    setTab('map')
  }, [])

  const balance = wallet?.balance?.toFixed(2) ?? '—'

  if (isLoadingApp) {
    return <Loading onComplete={() => { handleLogin(pendingUser); setIsLoadingApp(false); }} />
  }

  if (!isLoggedIn) {
    return <Login onLogin={handleStartLogin} />
  }

  return (
    <div className="min-h-screen bg-surface text-on-surface font-sans lg:flex transition-colors duration-150 overflow-x-hidden">
      {/* Desktop Sidebar Navigation */}
      <aside className={`${isMobileDrawerOpen ? 'flex' : 'hidden'} lg:flex flex-col w-64 h-screen fixed left-0 top-0 bg-surface border-r border-outline-variant z-50 p-6 select-none`}>
        <div className="mb-10 flex items-center justify-between">
          <h1 className="font-headline-md text-headline-md font-bold text-secondary">YatrAI</h1>
          <button 
            onClick={() => setIsMobileDrawerOpen(false)}
            className="lg:hidden material-symbols-outlined text-on-surface hover:bg-surface-container-highest transition-colors p-2 rounded-full active:scale-95 duration-150 ease-in-out select-none"
          >
            close
          </button>
        </div>
        <nav className="flex-1 space-y-2">
          {TABS.map(({ id, label, icon }) => {
            const active = tab === id
            const itemClass = active
              ? 'flex items-center gap-3 px-4 py-3 rounded-xl bg-secondary-fixed text-secondary font-bold'
              : 'flex items-center gap-3 px-4 py-3 rounded-xl text-on-surface-variant hover:bg-surface-container-high transition-colors'
            
            return (
              <button
                key={id}
                onClick={() => { setTab(id); setIsMobileDrawerOpen(false); }}
                className={`${itemClass} w-full text-left`}
              >
                <span
                  className="material-symbols-outlined"
                  style={{ fontVariationSettings: active ? "'FILL' 1" : "'FILL' 0" }}
                >
                  {icon}
                </span>
                <span className="font-label-lg ml-3">{label}</span>
              </button>
            )
          })}
        </nav>
        <div className="mt-auto pt-6 border-t border-outline-variant flex flex-col gap-3">
          <div className="flex items-center justify-between px-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center font-bold">
                {currentUser?.name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'JD'}
              </div>
              <div>
                <p className="font-label-md">{currentUser?.name || 'John Doe'}</p>
                <p className="text-label-sm text-on-surface-variant">{currentUser?.role || 'Pro Commuter'}</p>
              </div>
            </div>
            <button 
              onClick={handleLogout}
              className="text-[#64748b] hover:text-red-500 transition-colors p-1.5 rounded-full hover:bg-surface-container-high"
              title="Logout"
            >
              <span className="material-symbols-outlined text-[18px]">logout</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Wrapper */}
      <div className="flex-1 lg:ml-64 flex flex-col min-h-screen pb-24 lg:pb-12">
        {/* ── App Header (Mockup Design) ── */}
        <header className="fixed top-0 left-0 lg:left-64 right-0 z-40 flex justify-between items-center px-container-margin h-14 bg-surface/90 border-b border-outline-variant backdrop-blur-md dark:bg-surface-container-high transition-colors lg:border-none lg:bg-transparent">
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setIsMobileDrawerOpen(true)}
              className="lg:hidden material-symbols-outlined text-on-surface hover:bg-surface-container-highest transition-colors p-2 rounded-full active:scale-95 duration-150 ease-in-out select-none"
            >
              menu
            </button>
            <span className="font-headline-md text-headline-md font-bold text-secondary cursor-pointer select-none">
              YatrAI
            </span>
          {activeTrip && (
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-error-container text-on-error-container tracking-wider select-none animate-pulse">
              LIVE
            </span>
          )}
        </div>
        
        {/* Actions inside header */}
        <div className="flex items-center gap-2">
          {/* GPS status */}
          {geo.position && (
            <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-400 flex items-center gap-1.5 select-none" title="GPS Active">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" /> GPS LIVE
            </span>
          )}
          {/* Voice toggle button */}
          <button
            onClick={voice.toggle}
            className={`p-2 rounded-full transition-all duration-150 border flex items-center justify-center select-none active:scale-95 ${
              voice.enabled 
                ? 'text-secondary bg-secondary/10 border-secondary/20' 
                : 'text-tertiary bg-transparent border-transparent hover:text-on-surface'
            }`}
            title={voice.enabled ? 'Voice ON' : 'Voice OFF'}
          >
            <span className="material-symbols-outlined text-[20px]">{voice.enabled ? 'volume_up' : 'volume_off'}</span>
          </button>

          {/* Theme switch toggle button */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full transition-all duration-150 border border-transparent text-tertiary hover:text-on-surface flex items-center justify-center select-none active:scale-95"
            title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            <span className="material-symbols-outlined text-[20px]">{isDarkMode ? 'light_mode' : 'dark_mode'}</span>
          </button>
          
          {/* Balance Widget */}
          <div className="text-right border-l border-outline-variant pl-3 select-none">
            <p className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Balance</p>
            <p className="text-[14px] font-semibold text-secondary dark:text-secondary-fixed">₹{balance}</p>
          </div>
        </div>
      </header>

      {/* ── SSE Disruption Alert Toast ── */}
      {lastAlert && (
        <div
          className="fixed top-16 left-4 right-4 z-50 rounded-2xl px-4 py-3 flex items-start gap-3 shadow-lg select-none"
          style={{ background: '#111827', border: '1px solid rgba(239,68,68,0.4)', backdropFilter: 'blur(16px)' }}
        >
          <span className="material-symbols-outlined text-error text-xl mt-0.5" style={{ fontVariationSettings: "'FILL' 1" }}>
            {lastAlert.title.startsWith('⚠') ? 'warning' : 'check_circle'}
          </span>
          <div className="flex-grow min-w-0">
            <p className="text-sm font-semibold text-white truncate">{lastAlert.title}</p>
            <p className="text-[12px] text-[#bcc9cd] mt-0.5 leading-normal">{lastAlert.message}</p>
          </div>
          <button onClick={clearAlert} className="text-[#64748b] hover:text-white mt-0.5 flex items-center justify-center p-1 rounded-full">
            <span className="material-symbols-outlined text-[16px]">close</span>
          </button>
        </div>
      )}

      {/* ── Main Content Canvas ── */}
      <main className="mt-14 px-container-margin pt-4 pb-24 lg:p-10 max-w-lg lg:max-w-7xl mx-auto w-full flex-1 flex flex-col gap-4">
        {/* Active trip banner (tap to expand) */}
        {activeTrip && activeTrip.currentSegIdx < activeTrip.segments.length && tab !== 'pass' && (
          <div
            className="mb-1.5 rounded-2xl p-3.5 flex items-center gap-3 cursor-pointer bg-blue-50 dark:bg-[#111827] border border-[#3B82F6]/20 shadow-sm active:scale-[0.99] transition-all select-none"
            onClick={() => setTab('pass')}
          >
            <span className="material-symbols-outlined text-[#3B82F6] text-[20px] shrink-0 animate-pulse">navigation</span>
            <div className="flex-1 min-w-0">
              <p className="text-[13px] font-bold text-[#3B82F6]">Active Journey — {activeTrip.trip_id}</p>
              <p className="text-[12px] text-slate-500 dark:text-slate-400 truncate mt-0.5">
                Leg {activeTrip.currentSegIdx + 1}/{activeTrip.segments.length}:&nbsp;
                {activeTrip.segments[activeTrip.currentSegIdx]?.from_node.replace(/_/g, ' ')}
                &nbsp;→&nbsp;
                {activeTrip.segments[activeTrip.currentSegIdx]?.to_node.replace(/_/g, ' ')}
              </p>
            </div>
            <span className="material-symbols-outlined text-[#3B82F6] text-[20px]">chevron_right</span>
          </div>
        )}

        {/* Tab components */}
        {tab === 'planner' && (
          <PlannerView
            disruptions={localDisruptions}
            onStartTrip={handleStartTrip}
            position={geo.position}
            wallet={wallet}
            onTopUpClick={() => setTab('wallet')}
          />
        )}
        {tab === 'map' && (
          <LiveMap
            position={geo.position}
            route={activeRoute}
            expanded={mapExpanded}
            onToggle={() => setMapExpanded(prev => !prev)}
            onPlaceSelect={handlePlaceSelect}
            isDarkMode={isDarkMode}
          />
        )}
        {tab === 'pass' && (
          activeTrip ? (
            <ActiveTripView
              trip={activeTrip}
              onSegmentComplete={handleSegmentComplete}
              onCancelTrip={handleCancelTrip}
              voice={voice}
              position={geo.position}
            />
          ) : (
            <div className="glass-panel rounded-3xl p-8 text-center flex flex-col items-center gap-4 animate-fade-in-up select-none">
              <span className="material-symbols-outlined text-[48px] text-[#3B82F6]">confirmation_number</span>
              <div>
                <p className="text-[15px] font-semibold text-on-surface">No Active Pass</p>
                <p className="text-[12px] text-slate-400 dark:text-slate-500 mt-1.5 max-w-xs leading-normal">
                  Plan a modal journey on the Home screen and start the trip to generate a unified digital pass.
                </p>
              </div>
              <button
                onClick={() => setTab('planner')}
                className="mt-2 h-11 px-6 bg-[#3B82F6] hover:bg-blue-600 text-white font-medium rounded-xl text-[13px] flex items-center justify-center gap-2 active:scale-95 transition-all shadow-md"
              >
                <span className="material-symbols-outlined text-[16px]">navigation</span> Go to Home Planner
              </button>
            </div>
          )
        )}
        {tab === 'wallet' && <WalletPanel />}
        {tab === 'profile' && (
          <JournalPanel
            disruptions={localDisruptions}
            onDisruptionsChange={setLocalDisruptions}
            user={currentUser}
            onLogout={handleLogout}
          />
        )}
      </main>

      {/* Ambient authenticity indicator */}
      {tab === 'pass' && activeTrip && (
        <div className="fixed bottom-16 left-0 w-full h-1 shimmer-bar z-50" />
      )}

      {/* ── Bottom Navigation Bar (Mockup exact design/classes) ── */}
      <nav className="lg:hidden fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-gutter h-[64px] bg-surface/95 border-t border-outline-variant backdrop-blur-nav shadow-[0_-4px_8px_0_rgba(0,0,0,0.05)] transition-colors select-none">
        {TABS.map(({ id, label, icon }) => {
          const active = tab === id
          const showBadge = id === 'profile' && localDisruptions.length > 0
          
          const navClass = active 
            ? 'flex flex-col items-center justify-center text-secondary font-bold bg-secondary/10 rounded-xl px-4 py-1.5 active:scale-90 duration-200 scale-95 transition-all'
            : 'flex flex-col items-center justify-center text-tertiary px-3.5 py-1.5 hover:text-on-surface-variant dark:hover:text-on-surface transition-all active:scale-90 duration-200'

          return (
            <button
              key={id}
              onClick={() => setTab(id)}
              className={`${navClass} relative min-w-[64px] h-12`}
            >
              <span 
                className="material-symbols-outlined text-[22px] leading-none shrink-0" 
                style={{ fontVariationSettings: active ? "'FILL' 1" : "'FILL' 0" }}
              >
                {icon}
              </span>
              <span className="text-[10px] font-bold tracking-wider mt-1">{label}</span>
              {showBadge && (
                <span className="absolute top-1 right-5 w-2 h-2 rounded-full bg-error border border-surface animate-pulse" />
              )}
            </button>
          )
        })}
      </nav>
      </div>
    </div>
  )
}

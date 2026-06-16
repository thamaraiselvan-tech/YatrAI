// src/components/ActiveTripView.jsx
import { useState, useEffect, useRef } from 'react'
import confetti from 'canvas-confetti'
import { MODE_CONFIG } from '../constants/modes'

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

// ── CMRL QR Pass ─────────────────────────────────────────────────────────────
// ── Inline Vector QR Code Component (Offline Compatible & Reliable) ──────────
function MockQRCode({ size = 120 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 29 29" fill="black" className="block relative z-10">
      <path d="M0 0h7v7H0zm1 1v5h5V1zm1 1h3v3H2z" />
      <path d="M22 0h7v7h-7zm1 1v5h5V1zm1 1h3v3H2z" />
      <path d="M0 22h7v7H0zm1 1v5h5v-5zm1 1h3v3H2z" />
      <path d="M22 22h5v5h-5zm1 1v3h3v-3zm1 1h1v1h-1z" />
      <rect x="9" y="0" width="1" height="1" />
      <rect x="11" y="0" width="2" height="1" />
      <rect x="15" y="0" width="1" height="1" />
      <rect x="18" y="0" width="3" height="1" />
      <rect x="8" y="1" width="1" height="2" />
      <rect x="10" y="1" width="1" height="1" />
      <rect x="13" y="1" width="2" height="1" />
      <rect x="17" y="1" width="1" height="3" />
      <rect x="20" y="1" width="1" height="1" />
      <rect x="9" y="2" width="2" height="1" />
      <rect x="12" y="2" width="1" height="2" />
      <rect x="15" y="2" width="2" height="1" />
      <rect x="8" y="3" width="1" height="1" />
      <rect x="10" y="3" width="2" height="1" />
      <rect x="14" y="3" width="1" height="2" />
      <rect x="19" y="3" width="2" height="1" />
      <rect x="9" y="4" width="1" height="2" />
      <rect x="11" y="4" width="2" height="1" />
      <rect x="16" y="4" width="2" height="2" />
      <rect x="20" y="4" width="1" height="1" />
      <rect x="8" y="5" width="2" height="1" />
      <rect x="13" y="5" width="1" height="3" />
      <rect x="15" y="5" width="1" height="1" />
      <rect x="19" y="5" width="2" height="1" />
      <rect x="9" y="6" width="3" height="1" />
      <rect x="17" y="6" width="1" height="1" />
      <rect x="21" y="6" width="1" height="2" />
      <rect x="0" y="8" width="2" height="1" />
      <rect x="3" y="8" width="1" height="2" />
      <rect x="6" y="8" width="3" height="1" />
      <rect x="10" y="8" width="1" height="1" />
      <rect x="12" y="8" width="2" height="1" />
      <rect x="16" y="8" width="1" height="2" />
      <rect x="18" y="8" width="3" height="1" />
      <rect x="23" y="8" width="2" height="1" />
      <rect x="27" y="8" width="1" height="3" />
      <rect x="1" y="9" width="1" height="1" />
      <rect x="5" y="9" width="1" height="3" />
      <rect x="8" y="9" width="2" height="1" />
      <rect x="11" y="9" width="1" height="2" />
      <rect x="14" y="9" width="1" height="1" />
      <rect x="20" y="9" width="2" height="1" />
      <rect x="25" y="9" width="1" height="1" />
      <rect x="0" y="10" width="1" height="2" />
      <rect x="2" y="10" width="2" height="1" />
      <rect x="7" y="10" width="1" height="1" />
      <rect x="9" y="10" width="1" height="2" />
      <rect x="13" y="10" width="2" height="1" />
      <rect x="18" y="10" width="1" height="2" />
      <rect x="21" y="10" width="3" height="1" />
      <rect x="26" y="10" width="1" height="1" />
      <rect x="4" y="11" width="2" height="1" />
      <rect x="10" y="11" width="3" height="1" />
      <rect x="15" y="11" width="1" height="3" />
      <rect x="19" y="11" width="2" height="1" />
      <rect x="23" y="11" width="1" height="1" />
      <rect x="28" y="11" width="1" height="2" />
      <rect x="0" y="12" width="3" height="1" />
      <rect x="6" y="12" width="1" height="1" />
      <rect x="8" y="12" width="1" height="3" />
      <rect x="11" y="12" width="1" height="1" />
      <rect x="13" y="12" width="2" height="1" />
      <rect x="17" y="12" width="2" height="1" />
      <rect x="21" y="12" width="1" height="2" />
      <rect x="24" y="12" width="3" height="1" />
      <rect x="3" y="13" width="1" height="2" />
      <rect x="5" y="13" width="2" height="1" />
      <rect x="10" y="13" width="2" height="1" />
      <rect x="19" y="13" width="1" height="1" />
      <rect x="22" y="13" width="2" height="1" />
      <rect x="26" y="13" width="2" height="1" />
      <rect x="0" y="14" width="2" height="1" />
      <rect x="7" y="14" width="1" height="1" />
      <rect x="9" y="14" width="1" height="2" />
      <rect x="12" y="14" width="2" height="1" />
      <rect x="15" y="14" width="3" height="1" />
      <rect x="20" y="14" width="1" height="3" />
      <rect x="25" y="14" width="1" height="1" />
      <rect x="2" y="15" width="2" height="1" />
      <rect x="5" y="15" width="1" height="2" />
      <rect x="8" y="15" width="1" height="1" />
      <rect x="11" y="15" width="1" height="2" />
      <rect x="14" y="15" width="1" height="1" />
      <rect x="17" y="15" width="2" height="1" />
      <rect x="22" y="15" width="2" height="1" />
      <rect x="27" y="15" width="1" height="3" />
      <rect x="0" y="16" width="1" height="1" />
      <rect x="4" y="16" width="1" height="1" />
      <rect x="7" y="16" width="2" height="1" />
      <rect x="10" y="16" width="1" height="3" />
      <rect x="13" y="16" width="1" height="1" />
      <rect x="16" y="16" width="1" height="1" />
      <rect x="24" y="16" width="2" height="1" />
      <rect x="1" y="17" width="2" height="1" />
      <rect x="6" y="17" width="1" height="1" />
      <rect x="9" y="17" width="1" height="1" />
      <rect x="12" y="17" width="3" height="1" />
      <rect x="18" y="17" width="2" height="1" />
      <rect x="21" y="17" width="2" height="1" />
      <rect x="26" y="17" width="1" height="1" />
      <rect x="0" y="18" width="1" height="3" />
      <rect x="3" y="18" width="2" height="1" />
      <rect x="7" y="18" width="1" height="2" />
      <rect x="11" y="18" width="1" height="1" />
      <rect x="16" y="18" width="2" height="1" />
      <rect x="19" y="18" width="1" height="3" />
      <rect x="22" y="18" width="1" height="1" />
      <rect x="24" y="18" width="2" height="1" />
      <rect x="28" y="18" width="1" height="2" />
      <rect x="2" y="19" width="1" height="1" />
      <rect x="5" y="19" width="1" height="1" />
      <rect x="9" y="19" width="2" height="1" />
      <rect x="13" y="19" width="2" height="1" />
      <rect x="17" y="19" width="1" height="1" />
      <rect x="21" y="19" width="1" height="2" />
      <rect x="25" y="19" width="2" height="1" />
      <rect x="1" y="20" width="2" height="1" />
      <rect x="4" y="20" width="1" height="1" />
      <rect x="6" y="20" width="1" height="1" />
      <rect x="8" y="20" width="1" height="2" />
      <rect x="11" y="20" width="1" height="1" />
      <rect x="15" y="20" width="2" height="1" />
      <rect x="18" y="20" width="1" height="1" />
      <rect x="23" y="20" width="1" height="3" />
      <rect x="27" y="20" width="1" height="1" />
      <rect x="9" y="21" width="1" height="1" />
      <rect x="12" y="21" width="2" height="1" />
      <rect x="16" y="21" width="1" height="2" />
      <rect x="20" y="21" width="1" height="1" />
      <rect x="25" y="21" width="1" height="1" />
      <rect x="8" y="22" width="1" height="2" />
      <rect x="10" y="22" width="2" height="1" />
      <rect x="14" y="22" width="1" height="2" />
      <rect x="18" y="22" width="1" height="1" />
      <rect x="20" y="22" width="1" height="1" />
      <rect x="9" y="23" width="1" height="1" />
      <rect x="11" y="23" width="2" height="1" />
      <rect x="15" y="23" width="2" height="1" />
      <rect x="8" y="24" width="2" height="1" />
      <rect x="12" y="24" width="2" height="1" />
      <rect x="17" y="24" width="2" height="1" />
      <rect x="20" y="24" width="1" height="2" />
      <rect x="9" y="25" width="1" height="2" />
      <rect x="11" y="25" width="1" height="1" />
      <rect x="15" y="25" width="1" height="1" />
      <rect x="18" y="25" width="2" height="1" />
      <rect x="8" y="26" width="1" height="1" />
      <rect x="10" y="26" width="3" height="1" />
      <rect x="14" y="26" width="1" height="2" />
      <rect x="16" y="26" width="2" height="1" />
      <rect x="9" y="27" width="2" height="1" />
      <rect x="13" y="27" width="1" height="1" />
      <rect x="19" y="27" width="2" height="1" />
      <rect x="8" y="28" width="4" height="1" />
      <rect x="14" y="28" width="1" height="1" />
      <rect x="16" y="28" width="2" height="1" />
    </svg>
  )
}

// ── General QR Camera Scanner Component ──────────────────────────────────────
function QRCameraScanner({ title, onScanned, onClose }) {
  const scannerRef = useRef(null)
  const [scanning, setScanning] = useState(false)
  const [scanned, setScanned] = useState(false)
  const [cameraError, setCameraError] = useState(null)

  function startScan() {
    if (!window.Html5Qrcode) {
      setCameraError('QR Scanner library not loaded. Check internet connection.')
      return
    }
    setScanning(true)
    setCameraError(null)
    const qr = new window.Html5Qrcode('upi-qr-scanner')
    scannerRef.current = qr
    qr.start(
      { facingMode: 'environment' },
      { fps: 10, qrbox: 200 },
      (decodedText) => {
        qr.stop().catch(() => {})
        setScanning(false)
        setScanned(true)
        onScanned?.(decodedText)
      },
      (err) => {}
    ).catch((err) => {
      setScanning(false)
      const msg = err?.message || err || 'Unknown error'
      if (window.isSecureContext === false) {
        setCameraError('Camera access blocked: Non-secure HTTP contexts block camera access. Run over HTTPS or localhost, or use the simulation bypass below.')
      } else {
        setCameraError(`Camera failed: ${msg}. Please grant camera permissions or use the simulation bypass below.`)
      }
    })
  }

  function simulateSuccess() {
    setScanning(false)
    setScanned(true)
    onScanned?.()
  }

  useEffect(() => {
    return () => {
      try { scannerRef.current?.stop() } catch (_) {}
    }
  }, [])

  if (scanned) {
    return (
      <div className="flex flex-col items-center gap-3.5 p-6 animate-fade-in-up w-full">
        <span className="material-symbols-outlined text-4xl text-emerald-400 shrink-0">check_circle</span>
        <p className="text-emerald-400 font-semibold text-[15px]">Verification Success</p>
        <p className="text-[12px] text-slate-400 text-center font-normal max-w-xs leading-normal">
          Pass validated successfully.
        </p>
      </div>
    )
  }

  return (
    <div className="p-4 flex flex-col items-center gap-4 w-full">
      <style>{`
        #upi-qr-scanner video {
          width: 100% !important;
          height: 100% !important;
          object-fit: cover !important;
          border-radius: 12px;
        }
      `}</style>
      <p className="text-[12px] text-slate-400 text-center font-normal">
        {title}
      </p>
      
      {/* Viewfinder with neon glowing corners */}
      <div className="relative border border-emerald-500/30 rounded-xl overflow-hidden w-full max-w-[280px] aspect-square bg-black/50 flex items-center justify-center">
        {/* Dedicated scanner viewfinder container */}
        <div id="upi-qr-scanner" className="absolute inset-0 w-full h-full z-0" />
        
        {/* Safely managed React overlays */}
        <div className="absolute inset-0 z-10 pointer-events-none">
          {scanning && (
            <div className="absolute left-0 right-0 h-0.5 bg-emerald-400 shadow-[0_0_8px_#10B981] animate-laser" />
          )}
          
          {/* Framer corners decoration */}
          <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-emerald-400 rounded-tl-sm" />
          <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-emerald-400 rounded-tr-sm" />
          <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-emerald-400 rounded-bl-sm" />
          <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-emerald-400 rounded-br-sm" />
        </div>
        
        {!scanning && (
          <span className="material-symbols-outlined text-[36px] text-emerald-500/20 select-none z-20">photo_camera</span>
        )}
      </div>

      {cameraError && (
        <div className="p-3 bg-red-950/40 border border-red-500/30 rounded-xl text-[12px] text-red-300 text-center leading-normal max-w-xs">
          {cameraError}
        </div>
      )}

      {/* Simulated QR code card */}
      <div className="p-2 bg-white rounded-xl shadow-lg shrink-0">
        <MockQRCode size={80} />
      </div>
      
      <div className="flex flex-col gap-2 w-full">
        <button
          onClick={startScan}
          disabled={scanning}
          className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-emerald-800 text-white font-medium py-3 rounded-xl text-[13px] transition-all duration-150 active:scale-95 shadow-md shadow-emerald-500/20"
        >
          {scanning ? 'Accessing Camera…' : 'Activate Camera'}
        </button>

        {cameraError && (
          <button
            onClick={simulateSuccess}
            className="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium py-2 rounded-xl text-[12px] transition-all duration-150 active:scale-95 border border-slate-700/50"
          >
            Simulate Scan Success (Bypass)
          </button>
        )}

        {onClose && (
          <button
            onClick={onClose}
            className="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium py-2 rounded-xl text-[12px] transition-all duration-150 active:scale-95 border border-slate-700/50"
          >
            Show Pass Ticket
          </button>
        )}
      </div>
    </div>
  )
}

// ── CMRL QR Pass ─────────────────────────────────────────────────────────────
function CMRLPass({ segment, tripId, onScanned }) {
  const [showCamera, setShowCamera] = useState(false)

  if (showCamera) {
    return (
      <QRCameraScanner
        title="Scan the station turnstile QR code to validate entry/exit"
        onScanned={() => {
          setShowCamera(false)
          onScanned?.()
        }}
        onClose={() => setShowCamera(false)}
      />
    )
  }

  return (
    <div className="flex flex-col items-center gap-3.5 p-4 w-full">
      {/* White card inset */}
      <div className="relative bg-white p-6 rounded-2xl shadow-xl overflow-hidden w-[168px] h-[168px] flex items-center justify-center">
        {/* Scanning effect simulation */}
        <div className="scan-line" />
        <MockQRCode size={120} />
      </div>
      <p className="text-[12px] text-slate-400 font-semibold text-center mt-2">
        Scan at Metro turnstile
      </p>

      {/* Button to open camera */}
      <button
        onClick={() => setShowCamera(true)}
        className="mt-2 flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-[12px] border border-white/10 transition-all active:scale-[0.98]"
      >
        <span className="material-symbols-outlined text-[16px]">photo_camera</span>
        Scan Station QR (Camera)
      </button>

      {/* Ticket Footer Details */}
      <div className="w-full flex justify-between pt-4 border-t border-white/10 text-slate-400 mt-4">
        <div className="text-center">
          <p className="text-[10px] uppercase tracking-wider font-semibold">Pass ID</p>
          <p className="text-[12px] text-white font-medium mt-0.5">YAI-{tripId.slice(0, 6).toUpperCase()}</p>
        </div>
        <div className="text-center">
          <p className="text-[10px] uppercase tracking-wider font-semibold">Passengers</p>
          <p className="text-[12px] text-white font-medium mt-0.5">1 Adult</p>
        </div>
        <div className="text-center">
          <p className="text-[10px] uppercase tracking-wider font-semibold">Class</p>
          <p className="text-[12px] text-white font-medium mt-0.5">Standard</p>
        </div>
      </div>
    </div>
  )
}

// ── Animated UTS Pass ─────────────────────────────────────────────────────────
function UTSPass({ segment, tripId, onScanned }) {
  const [tick, setTick] = useState(true)
  const [showCamera, setShowCamera] = useState(false)

  useEffect(() => {
    const id = setInterval(() => setTick(t => !t), 800)
    return () => clearInterval(id)
  }, [])

  if (showCamera) {
    return (
      <QRCameraScanner
        title="Scan the platform validation QR code to validate your ticket"
        onScanned={() => {
          setShowCamera(false)
          onScanned?.()
        }}
        onClose={() => setShowCamera(false)}
      />
    )
  }

  return (
    <div className="flex flex-col gap-3 p-4 bg-white/5 border border-white/10 rounded-2xl relative overflow-hidden w-full">
      {/* Perforation holes on left and right */}
      <div className="absolute top-1/2 -left-2.5 w-5 h-5 bg-[#0F172A] rounded-full z-20" />
      <div className="absolute top-1/2 -right-2.5 w-5 h-5 bg-[#0F172A] rounded-full z-20" />

      <div className="uts-header mb-4 pb-3 border-b border-white/10 flex items-center gap-3">
        <div className="uts-logo-circle bg-amber-600 text-white w-9 h-9 rounded-full flex items-center justify-center font-semibold text-[13px]">
          UTS
        </div>
        <div>
          <p className="text-white font-semibold text-[13px]">Southern Railways</p>
          <p className="text-[12px] text-white/50 font-medium uppercase tracking-wider">Unreserved Pass</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-y-3.5 gap-x-2 text-[12px] mb-4.5">
        <div>
          <p className="text-[12px] text-white/40 uppercase font-medium tracking-wider">Source</p>
          <p className="text-white font-semibold mt-0.5 truncate">{segment.from_node.replace(/_/g, ' ')}</p>
        </div>
        <div>
          <p className="text-[12px] text-white/40 uppercase font-medium tracking-wider">Destination</p>
          <p className="text-white font-semibold mt-0.5 truncate">{segment.to_node.replace(/_/g, ' ')}</p>
        </div>
        <div>
          <p className="text-[12px] text-white/40 uppercase font-medium tracking-wider">Date of Issue</p>
          <p className="text-white font-semibold mt-0.5">{new Date().toLocaleDateString('en-IN')}</p>
        </div>
        <div>
          <p className="text-[12px] text-white/40 uppercase font-medium tracking-wider">Ticket Fare</p>
          <p className="text-[#f59e0b] font-semibold mt-0.5">₹{segment.fare}</p>
        </div>
      </div>

      <div className="flex flex-col gap-2.5">
        {/* Animated validation bar */}
        <div className="h-9 rounded-xl overflow-hidden bg-black/40 border border-amber-600/30 flex items-center justify-center gap-2 relative shadow-inner">
          <div
            className="absolute inset-0 transition-all duration-500"
            style={{ background: tick ? 'rgba(245,158,11,0.15)' : 'rgba(245,158,11,0.05)' }}
          />
          <div className="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-[0_0_8px_#F59E0B] animate-pulse" />
          <p className="text-[12px] text-amber-500 font-semibold tracking-widest relative z-10 font-mono">
            {tick ? 'VALID PASS' : 'VALID PASS'}
          </p>
        </div>

        {/* Button to open camera */}
        <button
          onClick={() => setShowCamera(true)}
          className="flex items-center justify-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-[12px] border border-white/10 transition-all active:scale-[0.98]"
        >
          <span className="material-symbols-outlined text-[16px]">photo_camera</span>
          Scan Platform QR (Camera)
        </button>
      </div>
    </div>
  )
}

// ── UPI Scanner Pass ──────────────────────────────────────────────────────────
function UPIScannerPass({ segment, onScanned }) {
  return (
    <QRCameraScanner
      title={`Scan the conductor's UPI QR Card to release ₹${segment.fare}`}
      onScanned={onScanned}
    />
  )
}


// ── PIN Display (Rapido / Ola) ────────────────────────────────────────────────
// Deterministic PIN so it doesn't refresh constantly in state render loops
function PinPass({ segment }) {
  const pinRef = useRef(String(Math.floor(1000 + Math.random() * 9000)))
  return (
    <div className="flex flex-col items-center gap-4 p-5 text-center w-full">
      <p className="text-[12px] text-slate-400 font-normal">Provide this OTP to the driver:</p>
      <div className="bg-black/40 border border-[#3B82F6]/30 rounded-xl px-8 py-3.5 relative shadow-inner">
        <p className="text-3xl font-semibold tracking-[0.25em] text-cyan-400 mr-[-0.25em] font-mono leading-none">
          {pinRef.current}
        </p>
      </div>
      <p className="text-[12px] text-slate-400 mt-1 font-medium">
        ₹{segment.fare} Escrow Lock
      </p>
    </div>
  )
}

// ── Walk Step ─────────────────────────────────────────────────────────────────
function WalkStep({ segment }) {
  return (
    <div className="flex flex-col items-center gap-3 p-6 text-center w-full">
      <span className="material-symbols-outlined text-[36px] text-slate-400 select-none">directions_walk</span>
      <p className="text-white font-medium text-[13px]">{segment.instruction_en}</p>
      <p className="text-[12px] text-slate-400">{Math.round(segment.duration)} minutes walk</p>
    </div>
  )
}

// ── Leaflet Map Component ────────────────────────────────────────────────────
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

    const map = L.map(mapRef.current, { zoomControl: false, scrollWheelZoom: false })
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
      const from = seg.from_coords
      const to = seg.to_coords
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

  return <div ref={mapRef} className="w-full h-full rounded-2xl overflow-hidden z-0" />
}

// ── Main ActiveTripView ───────────────────────────────────────────────────────
export default function ActiveTripView({ trip, onSegmentComplete, onCancelTrip, voice, position }) {
  const { trip_id, segments, currentSegIdx, moodData } = trip
  const segment = segments[currentSegIdx]
  const isLast = currentSegIdx >= segments.length - 1
  const [segDone, setSegDone] = useState(false)
  const [greenPts] = useState(() => Math.round(moodData?.total_co2 ?? 0))
  const [sosActive, setSosActive] = useState(false)
  const [sharingRevoked, setSharingRevoked] = useState(false)

  const handleDownloadInvoice = () => {
    const textContent = `
========================================
             YatrAI INVOICE             
========================================
Trip ID:      ${trip_id}
Date:         ${new Date().toLocaleDateString('en-IN')}
Total Fare:   ₹${moodData?.total_fare || '0.00'}
Carbon Saved: ${Math.round(moodData?.total_co2 || 0)}g CO2
Status:       PAID

Leg Details:
${segments.map((s, idx) => `  Leg ${idx + 1}: ${s.mode.replace(/_/g, ' ')} (${s.from_node.replace(/_/g, ' ')} -> ${s.to_node.replace(/_/g, ' ')}) - ₹${s.fare}`).join('\n')}

========================================
        THANK YOU FOR TRAVELING        
========================================
`;
    const blob = new Blob([textContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `YatrAI-Invoice-${trip_id}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const cfg = segment ? MODE_CONFIG[segment.mode] : null
  const passType = cfg?.passType ?? 'walk'

  function handleComplete() {
    if (isLast) {
      confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } })
    }
    onSegmentComplete(currentSegIdx)
    setSegDone(false)
  }

  function handleScanned() {
    setSegDone(true)
  }

  if (!segment && currentSegIdx >= segments.length) {
    return (
      <div className="flex flex-col items-center gap-6 p-8 text-center animate-fade-in-up">
        <span className="material-symbols-outlined text-5xl text-[#3B82F6] animate-bounce">check_circle</span>
        <div>
          <p className="text-[18px] font-semibold text-[#0F172A] dark:text-white">Journey Complete! 🎉</p>
          <p className="text-[12px] text-slate-400 mt-1.5 font-semibold uppercase tracking-wider">
            {moodData?.end_time_str} · ₹{moodData?.total_fare} Spent
          </p>
        </div>
        {greenPts > 0 && (
          <div className="bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-500/20 rounded-2xl px-6 py-4">
            <p className="text-emerald-600 dark:text-emerald-400 font-semibold text-[13px] flex items-center gap-1.5 justify-center">
              <span className="material-symbols-outlined text-sm">eco</span> +{Math.round(greenPts / 10)} Green Points Earned!
            </p>
            <p className="text-[12px] text-slate-400 mt-1">Offsetting travel carbon footprint</p>
          </div>
        )}
      </div>
    )
  }

  const origin_name = segments[0]?.from_node.replace(/_/g, ' ') || 'Origin'
  const destination_name = segments[segments.length - 1]?.to_node.replace(/_/g, ' ') || 'Destination'
  const arrival_time = moodData?.end_time_str || '08:45 AM'

  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Responsive Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Details, Map, and Invoice (Visible on Desktop only) */}
        <div className="hidden lg:flex lg:col-span-7 flex-col gap-6 w-full">
          {/* Journey Details Card */}
          <div className="glass-panel rounded-3xl p-5 h-fit">
            <h3 className="font-headline-sm text-slate-800 dark:text-[#F9FAFB] mb-4">Journey Details</h3>
            <div className="space-y-4">
              <div className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 rounded-full bg-secondary-container shadow-[0_0_8px_rgba(59,130,246,0.3)]"></div>
                  <div className="w-0.5 h-16 border-l border-dashed border-slate-300 dark:border-white/15"></div>
                  <div className="w-3 h-3 rounded-full bg-slate-400 dark:bg-slate-600"></div>
                </div>
                <div className="flex flex-col justify-between py-0.5">
                  <div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Origin</p>
                    <p className="font-body-md text-slate-800 dark:text-[#F9FAFB]">{origin_name}</p>
                  </div>
                  <div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Destination</p>
                    <p className="font-body-md text-slate-800 dark:text-[#F9FAFB]">{destination_name}</p>
                  </div>
                </div>
              </div>
              <div className="pt-4 border-t border-slate-100 dark:border-white/10">
                <p className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold mb-2">Estimated Arrival</p>
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300">
                  <span className="material-symbols-outlined text-sm">schedule</span>
                  <p className="font-label-lg">{arrival_time} (Expected)</p>
                </div>
              </div>
            </div>
          </div>

          {/* Live Route View Map */}
          <div className="glass-panel rounded-3xl h-72 relative overflow-hidden group">
            <div className="absolute inset-0 z-0">
              <LeafletMap segments={segments} />
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent pointer-events-none z-10" />
            <div className="relative z-20 h-full flex flex-col justify-end p-5 pointer-events-none">
              <p className="text-white font-label-lg mb-1">Live GPS Route View</p>
              <p className="text-slate-300 text-body-sm">Commute Status: Active</p>
            </div>
          </div>

          {/* Transfers Info Box & Invoice Download */}
          <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/30 rounded-3xl p-5">
            <div className="flex items-start gap-3 mb-3">
              <span className="material-symbols-outlined text-blue-600 dark:text-blue-400">info</span>
              <p className="text-blue-800 dark:text-blue-300 text-body-sm leading-relaxed">
                Your pass includes seamless transfer between MTC and Metro lines. No separate ticketing required.
              </p>
            </div>
            <button 
              onClick={handleDownloadInvoice}
              className="w-full py-3 bg-gradient-to-r from-secondary to-accent hover:shadow-md hover:shadow-secondary/15 text-white rounded-xl font-bold text-[13px] uppercase tracking-wider transition-all active:scale-[0.99] select-none"
            >
              Download PDF Invoice
            </button>
          </div>
        </div>

        {/* Right Column: Ticket, Progress bar, Actions, SOS, and History (All Viewports) */}
        <div className="lg:col-span-5 flex flex-col gap-5 w-full">
          {/* Progress bar */}
          <div className="glass-panel rounded-2xl p-4">
            <div className="flex items-center justify-between text-[12px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
              <span>Leg {currentSegIdx + 1} of {segments.length}</span>
              <span className="text-[#3B82F6]">ID: {trip_id}</span>
            </div>
            <div className="h-2 bg-slate-100 dark:bg-[#0A0F1E] rounded-full overflow-hidden border border-black/[0.05] dark:border-white/[0.05]">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-cyan-500 transition-all duration-500"
                style={{ 
                  width: `${((currentSegIdx) / segments.length) * 100}%`
                }}
              />
            </div>
          </div>

          {/* Voice navigation instruction */}
          {segment && (
            <div className="glass-panel rounded-2xl p-4 flex flex-col gap-3.5 border-l-4 border-secondary animate-fade-in-up">
              <div className="flex items-center justify-between border-b border-outline-variant/40 pb-2 select-none">
                <div className="flex items-center gap-2 text-secondary">
                  <span className="material-symbols-outlined text-[18px] animate-pulse">volume_up</span>
                  <span className="text-[10px] font-bold uppercase tracking-wider font-outfit">Voice Navigation Guidance</span>
                </div>
                {voice?.enabled && (
                  <button
                    onClick={() => voice.speakSegment(segment)}
                    className="shrink-0 text-[11px] font-bold px-3 py-1 rounded-lg bg-secondary/10 text-secondary border border-secondary/15 hover:bg-secondary/20 transition-all duration-100 active:scale-95 flex items-center gap-1"
                  >
                    <span className="material-symbols-outlined text-[12px]">replay</span>
                    <span>Replay Audio</span>
                  </button>
                )}
              </div>
              
              <div className="flex-1 min-w-0 font-sans">
                <p className="text-[13px] text-slate-800 dark:text-[#F9FAFB] font-medium leading-relaxed font-sans">
                  {segment.instruction_en}
                </p>
                {segment.instruction_ta && (
                  <div className="mt-3 bg-surface-container/50 dark:bg-surface-container-high/40 p-3 rounded-xl border border-outline-variant text-[12.5px] leading-relaxed text-secondary-container-on font-medium">
                    <p className="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider mb-1 flex items-center gap-1 select-none">
                      <span className="material-symbols-outlined text-[12px]">translate</span>
                      தமிழ் உரைபெயர்ப்பு (Tamil Translation)
                    </p>
                    <p className="text-on-surface-variant italic font-outfit leading-relaxed">
                      {segment.instruction_ta}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Ticket Container Wrapper with cutout curves */}
          <div className="max-w-md mx-auto w-full relative z-10">
            {/* Trip Overview Card (Rounded top) */}
            <div className="bg-[#0F172A] border border-b-0 border-white/[0.08] rounded-t-3xl p-4 relative overflow-hidden flex flex-col">
              {/* Watermark Pattern */}
              <div className="absolute inset-0 secure-watermark opacity-[0.03] select-none pointer-events-none" />
              
              <div className="flex justify-between items-center relative z-10">
                <span className="text-[12px] font-headline-md text-headline-sm font-bold text-secondary">YatrAI</span>
                <span className="text-[10px] font-bold tracking-widest text-white/50 uppercase">UNIFIED PASS</span>
              </div>
              
              <div className="text-[18px] font-semibold text-white mt-3 relative z-10 leading-tight">
                {origin_name} → {destination_name}
              </div>
              
              <div className="flex justify-between items-center mt-2 relative z-10">
                <div className="flex items-center gap-1.5 text-white/70 text-[12px]">
                  <span className="material-symbols-outlined text-[14px]">calendar_today</span>
                  <span>08:00 AM • Today</span>
                </div>
                <div className="bg-secondary/20 border border-secondary text-secondary text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full select-none">
                  VALID
                </div>
              </div>
            </div>

            {/* Legs Grid Container (Intermediate cutout panel) */}
            <div className="bg-[#0F172A]/90 border-x border-dashed border-white/[0.08] p-4 ticket-cutout border-b border-white/[0.08] relative z-10">
              <div className="grid grid-cols-3 gap-2 relative z-10">
                {segments.map((s, idx) => {
                  return (
                    <div 
                      key={idx} 
                      className={`p-2.5 rounded-xl bg-white/5 border flex flex-col items-center justify-center gap-1 transition-all ${
                        idx === currentSegIdx 
                          ? 'border-[#3B82F6] bg-white/10 ring-1 ring-[#3B82F6]/50 shadow-md' 
                          : 'border-white/10 opacity-60'
                      }`}
                    >
                      <span className="material-symbols-outlined text-[20px] text-white leading-none">
                        {PASS_MODE_ICONS[s.mode] || 'directions_walk'}
                      </span>
                      <span className="text-[11px] font-medium text-white/90 truncate max-w-full font-outfit">
                        {MODE_CONFIG[s.mode]?.label || 'Walk'}
                      </span>
                      <span className="text-[11px] font-mono text-white/70 mt-0.5">₹{s.fare}</span>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Active Leg Pass Card (Rounded bottom) */}
            <div className="bg-[#0F172A] border border-t-0 border-white/[0.08] rounded-b-3xl p-5 flex flex-col items-center w-full relative overflow-hidden z-10">
              {/* Watermark Pattern */}
              <div className="absolute inset-0 secure-watermark opacity-[0.03] select-none pointer-events-none" />

              {/* Render active segment details */}
              {passType === 'cmrl_qr' && <CMRLPass segment={segment} tripId={trip_id} onScanned={handleScanned} />}
              {passType === 'uts' && <UTSPass segment={segment} tripId={trip_id} onScanned={handleScanned} />}
              {passType === 'upi_scan' && <UPIScannerPass segment={segment} onScanned={handleScanned} />}
              {passType === 'pin' && <PinPass segment={segment} />}
              {passType === 'walk' && <WalkStep segment={segment} />}
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex gap-3 mt-2">
            <button
              onClick={onCancelTrip}
              className="flex-1 flex items-center justify-center gap-2 bg-red-50 dark:bg-rose-500/10 border border-red-500/10 hover:border-red-500/20
                         text-red-600 dark:text-rose-400 font-semibold rounded-xl py-3.5 text-[14px] hover:bg-red-100/50 dark:hover:bg-rose-500/20 active:scale-95 transition-all select-none"
            >
              <span className="material-symbols-outlined text-[18px]">close</span> Cancel Trip
            </button>
            <button
              onClick={handleComplete}
              disabled={passType === 'upi_scan' && !segDone}
              className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-secondary to-accent hover:shadow-md hover:shadow-secondary/15 text-white
                         font-bold uppercase tracking-wider rounded-xl py-3.5 text-[13px] active:scale-95 transition-all 
                         disabled:from-slate-100 disabled:to-slate-100 disabled:text-slate-400 dark:disabled:from-slate-800/40 dark:disabled:to-slate-800/40 dark:disabled:text-slate-600 disabled:shadow-none disabled:pointer-events-none"
            >
              <span className="material-symbols-outlined text-[18px]">check_circle</span>
              {isLast ? 'Complete Trip' : 'Next Step'}
            </button>
          </div>

          {/* Safety Panel (Safest Route only) */}
          {moodData?.mood === 'safest' && (
            <div className="glass-panel rounded-2xl p-4 flex flex-col gap-3.5">
              <div className="flex items-center justify-between">
                <span className="text-[12px] font-semibold text-violet-500 uppercase tracking-wider font-outfit">
                  Safety Verified Route
                </span>
                <span className="text-[12px] px-2.5 py-0.5 rounded-full bg-violet-100 dark:bg-violet-950/30 text-violet-700 dark:text-violet-400 font-medium">
                  ✓ Police Verified
                </span>
              </div>

              {/* Driver Card */}
              <div className="flex items-center gap-3 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-black/[0.05] dark:border-white/[0.05]">
                <div className="w-10 h-10 rounded-full bg-violet-500 text-white flex items-center justify-center font-semibold text-[13px]">
                  D
                </div>
                <div>
                  <p className="text-[13px] font-semibold text-[#0F172A] dark:text-[#F9FAFB]">Dharun Kumar</p>
                  <p className="text-[12px] text-slate-500 dark:text-slate-400 mt-0.5">Ola Auto Driver · 4.9 ★</p>
                </div>
              </div>

              {/* SOS Strip */}
              <button
                onClick={() => setSosActive(prev => !prev)}
                type="button"
                className={`w-full h-11 border rounded-xl flex items-center justify-center gap-2 font-semibold text-[13px] active:scale-95 transition-all select-none ${
                  sosActive 
                    ? 'bg-red-600 border-red-700 text-white animate-pulse' 
                    : 'border-red-500 bg-red-500/10 text-red-600 dark:text-red-400 hover:bg-red-500/20'
                }`}
              >
                <span className="material-symbols-outlined text-sm">{sosActive ? 'notifications_active' : 'warning'}</span>
                <span>{sosActive ? 'SOS Triggered! Cancel Alert' : 'Trigger SOS Alert'}</span>
              </button>

              {/* Tracking Link Row */}
              <div className="flex items-center justify-between text-[12px] text-slate-500 dark:text-slate-400 px-1 pt-1">
                <span>
                  {sharingRevoked 
                    ? '⚠️ Location sharing revoked' 
                    : <>Location shared with: <span className="font-semibold text-slate-700 dark:text-slate-300">Amma, Ravi</span></>
                  }
                </span>
                <span 
                  onClick={() => setSharingRevoked(prev => !prev)}
                  className="text-[#3B82F6] cursor-pointer hover:underline font-semibold"
                >
                  {sharingRevoked ? 'Enable Sharing' : 'Revoke Link'}
                </span>
              </div>
            </div>
          )}

          {/* History Card (Only visible on Desktop to save mobile space) */}
          <div className="hidden lg:flex flex-col glass-panel rounded-3xl p-5">
            <h3 className="font-label-lg text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-4">Journey History</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-white/5 border border-black/[0.04] dark:border-white/5">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-slate-400 dark:text-slate-500">history</span>
                  <div>
                    <p className="text-slate-800 dark:text-white font-label-md">Koyambedu → Guindy</p>
                    <p className="text-slate-500 dark:text-slate-400 text-label-sm">Yesterday • ₹35.00</p>
                  </div>
                </div>
                <span className="material-symbols-outlined text-slate-400 dark:text-slate-500 text-sm">chevron_right</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-white/5 border border-black/[0.04] dark:border-white/5">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-slate-400 dark:text-slate-500">history</span>
                  <div>
                    <p className="text-slate-800 dark:text-white font-label-md">Central → Marina</p>
                    <p className="text-slate-500 dark:text-slate-400 text-label-sm">2 days ago • ₹12.00</p>
                  </div>
                </div>
                <span className="material-symbols-outlined text-slate-400 dark:text-slate-500 text-sm">chevron_right</span>
              </div>
            </div>
            <button className="mt-4 w-full text-secondary dark:text-blue-400 font-label-md font-semibold hover:underline">View full history</button>
          </div>
        </div>

      </div>
    </div>
  )
}

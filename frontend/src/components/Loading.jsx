// src/components/Loading.jsx
import { useState, useEffect } from 'react'

export default function Loading({ onComplete }) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    let timer
    const increment = () => {
      const inc = Math.random() * 15
      setProgress(p => {
        const next = p + inc
        if (next >= 100) {
          clearInterval(timer)
          setTimeout(onComplete, 500)
          return 100
        }
        return next
      })
    }

    timer = setInterval(increment, Math.random() * 250 + 100)
    return () => clearInterval(timer)
  }, [onComplete])

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#020617] text-white overflow-hidden relative w-full h-screen">
      {/* Ambient gradient */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_#0F172A_0%,_#020617_100%)] pointer-events-none" />

      {/* Center cluster */}
      <div className="flex flex-col items-center z-10 animate-fade-in-up">
        {/* Brand Logo with Glow */}
        <div className="mb-6 w-32 h-32 md:w-40 md:h-40 filter drop-shadow-[0_0_15px_rgba(59,130,246,0.4)] animate-pulse bg-white flex items-center justify-center p-2 rounded-xl">
          <img 
            alt="YatrAI Logo" 
            className="w-full h-full object-cover rounded-lg" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDW3aYpo2kLS8sX1TOosKMItv9qIyvnNmhiGikENrAPNVcH-4Gfl89cnm1nT0D44i0sD2YHgzhEgOAezhVZ4oIJXXdEK5R9KmDZrzP8-JSLNvk2BVLq-5qQkx0CO4ma5x_juaRDUP_DzS0083TfvVXLimHCgMlFgMq3Yi2Hntb3Ac9h3yiJb95U7K5jpJmnfaDehhfemjxxgUnLr4zQ8VA-jcSbspx9bEQ4d9joIZ88Tya56Z3WSs5N2N6GkJl56sN0FJH7TzCk7lGI"
          />
        </div>
        
        {/* Brand Name */}
        <h1 className="font-headline-lg text-headline-lg text-white tracking-wider text-glow font-black text-center select-none text-[32px]">
          YatrAI
        </h1>
        
        {/* Tagline */}
        <p className="font-label-sm text-label-sm text-blue-400 mt-2 tracking-[0.2em] uppercase opacity-60 text-center select-none text-[10px]">
          Next-Gen Transit Intelligence
        </p>
      </div>

      {/* Loading Bar */}
      <div className="absolute bottom-16 w-full max-w-[280px] md:max-w-xs flex flex-col items-center px-4 z-10">
        <div className="w-full h-[2px] bg-white/10 rounded-full overflow-hidden mb-4 relative">
          <div 
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-500 via-blue-400 to-blue-500 transition-all duration-300 ease-out shimmer-bar" 
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="flex items-center space-x-3">
          <span className="font-label-sm text-label-sm text-slate-400 tracking-wide animate-pulse text-[10px]">
            Loading your journey...
          </span>
        </div>
      </div>

      {/* Tech corner accents */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none opacity-5">
        <div className="absolute top-10 left-10 border-l border-t border-white w-20 h-20"></div>
        <div className="absolute bottom-10 right-10 border-r border-b border-white w-20 h-20"></div>
      </div>
    </div>
  )
}

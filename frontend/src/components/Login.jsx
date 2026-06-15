// src/components/Login.jsx
import { useState } from 'react'

const DEMO_USERS = {
  'john@yatrai.com': { name: 'John Doe', role: 'Pro Commuter', password: 'john123' },
  'alice@yatrai.com': { name: 'Alice Smith', role: 'Eco Traveler', password: 'alice123' },
}

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    setError(null)
    const cleanEmail = email.trim().toLowerCase()
    
    // Check demo accounts
    if (DEMO_USERS[cleanEmail]) {
      const user = DEMO_USERS[cleanEmail]
      if (user.password === password) {
        onLogin({ name: user.name, role: user.role, email: cleanEmail })
      } else {
        setError('Incorrect password for this demo account.')
      }
    } else {
      // Validate dynamic account
      if (password.length < 6) {
        setError('Password must be at least 6 characters for new registrations.')
        return
      }
      if (!cleanEmail.includes('@') || !cleanEmail.includes('.')) {
        setError('Please enter a valid email address.')
        return
      }
      // Generate clean username from email prefix
      const prefix = cleanEmail.split('@')[0]
      const name = prefix.charAt(0).toUpperCase() + prefix.slice(1)
      onLogin({ name, role: 'Transit Enthusiast', email: cleanEmail })
    }
  }

  return (
    <div className="bg-[#0B0F19] text-white font-sans m-0 p-0 overflow-x-hidden min-h-screen flex flex-col transition-colors duration-150">
      {/* Main Content Canvas */}
      <main className="flex-grow flex flex-col md:flex-row min-h-screen">
        
        {/* Hero Section (Left on Desktop, Top on Mobile) */}
        <section className="calm-urgency-gradient w-full md:w-1/2 flex flex-col items-center justify-center p-stack-lg relative overflow-hidden min-h-[40vh] md:min-h-screen">
          {/* Subtle Grid Pattern Overlay */}
          <div className="absolute inset-0 opacity-10 pointer-events-none" style={{ backgroundImage: "radial-gradient(#ffffff 1px, transparent 1px)", backgroundSize: "40px 40px" }} />
          
          <div className="z-10 flex flex-col items-center text-center max-w-lg">
            {/* Brand Logo Card with Rounded borders & dark background inside */}
            <div className="mb-8 p-4 bg-[#0F172A] rounded-[2rem] border-4 border-white shadow-2xl transition-transform hover:scale-105 duration-500 w-32 h-32 md:w-40 md:h-40 flex items-center justify-center">
              <img 
                alt="YatrAI Logo" 
                className="w-full h-full object-contain" 
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuDW3aYpo2kLS8sX1TOosKMItv9qIyvnNmhiGikENrAPNVcH-4Gfl89cnm1nT0D44i0sD2YHgzhEgOAezhVZ4oIJXXdEK5R9KmDZrzP8-JSLNvk2BVLq-5qQkx0CO4ma5x_juaRDUP_DzS0083TfvVXLimHCgMlFgMq3Yi2Hntb3Ac9h3yiJb95U7K5jpJmnfaDehhfemjxxgUnLr4zQ8VA-jcSbspx9bEQ4d9joIZ88Tya56Z3WSs5N2N6GkJl56sN0FJH7TzCk7lGI"
              />
            </div>
            <h1 className="text-3xl md:text-5xl font-extrabold mb-6 tracking-tight leading-tight text-white select-none">
              Your Journey Starts Here.
            </h1>
            <p className="text-lg md:text-xl text-blue-100 font-medium opacity-90 leading-relaxed px-4 max-w-md select-none">
              Navigate Chennai with the precision of AI and the calm of a seamless transit experience.
            </p>
          </div>
          
          {/* Decorative Glow */}
          <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-500/20 blur-[100px] rounded-full"></div>
          <div className="absolute -top-24 -right-24 w-96 h-96 bg-indigo-500/20 blur-[100px] rounded-full"></div>
        </section>

        {/* Authentication Form Section (Dark layout matching image reference) */}
        <section className="w-full md:w-1/2 bg-[#0B0F19] flex items-center justify-center p-container-margin py-stack-lg">
          <div className="w-full max-w-[400px]">
            
            {/* Branding for Mobile (Hidden on MD up) */}
            <div className="md:hidden flex items-center gap-stack-sm mb-stack-lg justify-center">
              <img 
                alt="YatrAI" 
                className="w-10 h-10 rounded-lg" 
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuDW3aYpo2kLS8sX1TOosKMItv9qIyvnNmhiGikENrAPNVcH-4Gfl89cnm1nT0D44i0sD2YHgzhEgOAezhVZ4oIJXXdEK5R9KmDZrzP8-JSLNvk2BVLq-5qQkx0CO4ma5x_juaRDUP_DzS0083TfvVXLimHCgMlFgMq3Yi2Hntb3Ac9h3yiJb95U7K5jpJmnfaDehhfemjxxgUnLr4zQ8VA-jcSbspx9bEQ4d9joIZ88Tya56Z3WSs5N2N6GkJl56sN0FJH7TzCk7lGI"
              />
              <span className="text-2xl font-bold text-secondary">YatrAI</span>
            </div>

            <div className="mb-6">
              <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">Welcome Back</h2>
              <p className="text-slate-400">Access your saved routes and digital passes.</p>
            </div>

            {/* Demo Credentials Helper Box */}
            <div className="bg-blue-500/10 border border-blue-500/20 text-[#a5c3f7] p-3.5 rounded-xl mb-6 text-[12px] leading-relaxed">
              <p className="font-bold flex items-center gap-1.5 mb-1 text-blue-300">
                <span className="material-symbols-outlined text-[16px]">info</span>
                Demo Accounts
              </p>
              <ul className="list-disc pl-4 space-y-1 text-[#b5cefa]">
                <li><span className="font-semibold font-mono">john@yatrai.com</span> / <span className="font-semibold font-mono">john123</span> (John Doe)</li>
                <li><span className="font-semibold font-mono">alice@yatrai.com</span> / <span className="font-semibold font-mono">alice123</span> (Alice Smith)</li>
                <li>Or enter any custom email with a password &ge; 6 characters.</li>
              </ul>
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-xl mb-5 text-[12.5px] flex items-center gap-2">
                <span className="material-symbols-outlined text-[16px] text-red-400">warning</span>
                <span>{error}</span>
              </div>
            )}

            <form className="space-y-5" onSubmit={handleSubmit}>
              {/* Email/Phone Input */}
              <div>
                <label className="block text-sm font-semibold text-slate-300 mb-1.5">Email or Phone Number</label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 select-none text-lg">person</span>
                  <input 
                    className="w-full pl-11 pr-4 py-3.5 bg-[#EAF2FF] border-none rounded-xl font-body-md text-[#0B0F19] placeholder-slate-400 focus:ring-2 focus:ring-secondary/50 transition-all outline-none" 
                    placeholder="name@example.com" 
                    type="text"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              {/* Password Input */}
              <div>
                <div className="flex justify-between mb-1.5">
                  <label className="block text-sm font-semibold text-slate-300">Password</label>
                  <a className="text-sm font-semibold text-secondary hover:underline" href="#" onClick={e => e.preventDefault()}>Forgot Password?</a>
                </div>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 select-none text-lg">lock</span>
                  <input 
                    className="w-full pl-11 pr-12 py-3.5 bg-[#EAF2FF] border-none rounded-xl font-body-md text-[#0B0F19] placeholder-slate-400 focus:ring-2 focus:ring-secondary/50 transition-all outline-none" 
                    placeholder="••••" 
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                  />
                  <button 
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-secondary transition-colors" 
                    type="button"
                    onClick={() => setShowPassword(p => !p)}
                  >
                    <span className="material-symbols-outlined select-none text-lg">{showPassword ? 'visibility_off' : 'visibility'}</span>
                  </button>
                </div>
              </div>

              {/* Action Button */}
              <button 
                type="submit" 
                className="w-full py-4 bg-secondary text-white font-bold rounded-xl shadow-md hover:shadow-lg hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-2 group text-[15px]"
              >
                Sign In
                <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform select-none text-lg">arrow_forward</span>
              </button>
            </form>

            {/* Divider */}
            <div className="relative my-8 flex items-center">
              <div className="flex-grow border-t border-slate-800"></div>
              <span className="px-4 text-[10px] font-bold text-slate-500 uppercase tracking-widest bg-[#0B0F19] select-none">Or continue with</span>
              <div className="flex-grow border-t border-slate-800"></div>
            </div>

            {/* Social Logins */}
            <div className="grid grid-cols-2 gap-4">
              <button 
                onClick={() => onLogin({ name: 'John Doe', role: 'Pro Commuter', email: 'john@yatrai.com' })}
                className="flex items-center justify-center gap-2 py-3 px-4 border border-slate-800 rounded-xl font-semibold text-white bg-transparent hover:bg-white/5 transition-all active:scale-[0.98]"
              >
                <img 
                  alt="Google" 
                  className="w-5 h-5" 
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuB2u7jQchU-4F6FXddK4MWDRRNAQiJp_n8-kNAqteU61LEXt_3dXstGyEFR6x-_yVDITUlokBXO4A1ClEO8h2Z5iLz9SLUZEDeAvU4qtoKHi3Rz7TkNsM0uZjTSOpiejDviwcAoPzmnHf7kD4DrBWlLWeuFUxL6EAd5Bogb3jpnmMJLsfTdnq-Mf7u1YQqGC1DEAtI6mrM4WJewR7Ub2y2xz4n-2j4S8FQQc4HQKYX78DFY0G_4Ev6IqnZRpnWZV9oRKqXhXYd01l38"
                />
                Google
              </button>
              <button 
                onClick={() => onLogin({ name: 'Alice Smith', role: 'Eco Traveler', email: 'alice@yatrai.com' })}
                className="flex items-center justify-center gap-2 py-3 px-4 border border-slate-800 rounded-xl font-semibold text-white bg-transparent hover:bg-white/5 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-white select-none text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>apps</span>
                Apple
              </button>
            </div>

            {/* Sign Up Link */}
            <div className="mt-8 text-center">
              <p className="text-slate-400">
                Don't have an account?&nbsp;
                <a className="text-secondary font-bold hover:underline" href="#" onClick={e => e.preventDefault()}>Sign up</a>
              </p>
            </div>

          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-[#0B0F19] py-6 px-4 text-center border-t border-slate-900">
        <p className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">
          © 2026 YatrAI Transit • Secure Encrypted Authentication
        </p>
      </footer>
    </div>
  )
}

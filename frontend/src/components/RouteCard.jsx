// src/components/RouteCard.jsx

const MOOD_THEMES = {
  cheapest: {
    icon: 'payments',
    label: 'Cheapest',
    desc: 'Lowest cost route',
    metric: (r) => `₹${r.total_fare}`,
    color: '#10B981',
    lightTag: 'bg-emerald-50 text-emerald-700 border border-emerald-200/50',
    darkTag: 'dark:bg-emerald-500/10 dark:text-emerald-400 dark:border dark:border-emerald-500/20',
  },
  fastest: {
    icon: 'bolt',
    label: 'Fastest',
    desc: 'Minimum time',
    metric: (r) => `${Math.round(r.total_time)} min`,
    color: '#3B82F6',
    lightTag: 'bg-blue-50 text-blue-700 border border-blue-200/50',
    darkTag: 'dark:bg-blue-500/10 dark:text-blue-400 dark:border dark:border-blue-500/20',
  },
  greenest: {
    icon: 'eco',
    label: 'Greenest',
    desc: 'Lowest footprint',
    metric: (r) => r.total_co2 < 1000 ? `${r.total_co2.toFixed(0)}g` : `${(r.total_co2 / 1000).toFixed(1)}kg`,
    color: '#14B8A6',
    lightTag: 'bg-teal-50 text-teal-700 border border-teal-200/50',
    darkTag: 'dark:bg-teal-500/10 dark:text-teal-400 dark:border dark:border-teal-500/20',
  },
  safest: {
    icon: 'verified_user',
    label: 'Safest',
    desc: 'Maximum safety',
    metric: (r) => `${r.segments?.length || 0} legs`,
    color: '#8B5CF6',
    lightTag: 'bg-purple-50 text-purple-700 border border-purple-200/50',
    darkTag: 'dark:bg-purple-500/10 dark:text-purple-400 dark:border dark:border-purple-500/20',
  }
}

export default function RouteCard({ mood, route, selected, recommended, onClick }) {
  const theme = MOOD_THEMES[mood]
  if (!theme || !route) return null

  const bgClass = selected
    ? 'bg-slate-50 dark:bg-slate-800/40 border-2 shadow-md scale-[1.02] -translate-y-0.5'
    : 'bg-surface dark:bg-[#111625] hover:bg-slate-50/50 dark:hover:bg-[#141C33] border hover:shadow-md'

  const borderColor = selected ? 'border-secondary' : 'border-outline-variant dark:border-[#2A354F]'

  return (
    <button
      onClick={onClick}
      style={{ borderLeft: `4px solid ${theme.color}` }}
      className={`relative w-full h-[120px] rounded-[16px] p-4 flex flex-col justify-between text-left transition-all duration-200 ${bgClass} ${borderColor}`}
    >
      {/* Top Row */}
      <div className="flex justify-between items-start w-full">
        <div className={`px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider ${theme.lightTag} ${theme.darkTag}`}>
          {theme.label}
        </div>
        <span 
          className="material-symbols-outlined text-lg select-none"
          style={{ 
            fontVariationSettings: selected ? "'FILL' 1" : "'FILL' 0",
            color: theme.color 
          }}
        >
          {theme.icon}
        </span>
      </div>

      {/* Middle Metric */}
      <div className="font-headline-md text-headline-md leading-none text-on-surface font-bold mt-1">
        {theme.metric(route)}
      </div>

      {/* Bottom Arrival Time */}
      <div className="text-[12px] font-medium text-on-surface-variant/80">
        {route.end_time_str} arrival
      </div>

      {recommended && (
        <span className="absolute -top-2.5 right-4 px-2.5 py-0.5 text-[9px] font-bold rounded-full bg-[#D97706] text-white tracking-wider select-none font-outfit uppercase shadow-sm">
          Recommended
        </span>
      )}
    </button>
  )
}

function RiskScore({ score, level, summary }) {
  const levelStyles = {
    LOW: {
      ringColor: 'stroke-emerald-400',
      scoreColor: 'text-emerald-400',
      bg: 'from-emerald-500/10 via-slate-900/50 to-slate-900/50',
      border: 'border-emerald-500/30',
      badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
      glow: 'shadow-[0_0_30px_-10px_rgba(16,185,129,0.4)]',
      label: 'DÜŞÜK RİSK',
    },
    MEDIUM: {
      ringColor: 'stroke-yellow-400',
      scoreColor: 'text-yellow-400',
      bg: 'from-yellow-500/10 via-slate-900/50 to-slate-900/50',
      border: 'border-yellow-500/30',
      badge: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
      glow: 'shadow-[0_0_30px_-10px_rgba(234,179,8,0.4)]',
      label: 'ORTA RİSK',
    },
    HIGH: {
      ringColor: 'stroke-orange-400',
      scoreColor: 'text-orange-400',
      bg: 'from-orange-500/10 via-slate-900/50 to-slate-900/50',
      border: 'border-orange-500/30',
      badge: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
      glow: 'shadow-[0_0_30px_-10px_rgba(249,115,22,0.4)]',
      label: 'YÜKSEK RİSK',
    },
    CRITICAL: {
      ringColor: 'stroke-red-400',
      scoreColor: 'text-red-400',
      bg: 'from-red-500/10 via-slate-900/50 to-slate-900/50',
      border: 'border-red-500/30',
      badge: 'bg-red-500/20 text-red-300 border-red-500/40',
      glow: 'shadow-[0_0_30px_-10px_rgba(239,68,68,0.4)]',
      label: 'KRİTİK RİSK',
    },
  }

  const style = levelStyles[level] || levelStyles.MEDIUM
  const counts = summary?.severity_counts || { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }

  // Circular progress hesaplaması
  const radius = 42
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (score / 100) * circumference

  return (
    <div className={`bg-gradient-to-br ${style.bg} backdrop-blur border ${style.border} ${style.glow} rounded-xl p-5 mb-4`}>
      <div className="flex items-center gap-5 mb-5">
        {/* Circular progress */}
        <div className="relative flex-shrink-0">
          <svg width="100" height="100" viewBox="0 0 100 100" className="-rotate-90">
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="none"
              className="stroke-slate-800"
              strokeWidth="6"
            />
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="none"
              className={style.ringColor}
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              style={{ transition: 'stroke-dashoffset 1s ease-out' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-3xl font-bold ${style.scoreColor} leading-none`}>{score}</span>
            <span className="text-xs text-slate-500 mt-0.5">/100</span>
          </div>
        </div>

        {/* Score metni ve badge */}
        <div className="flex-1 min-w-0">
          <p className="text-xs text-slate-400 mb-2 uppercase tracking-wide">Genel Güvenlik Skoru</p>
          <span className={`inline-block text-xs font-bold px-3 py-1.5 rounded-full border ${style.badge} mb-2`}>
            {style.label}
          </span>
          <p className="text-xs text-slate-500">
            <span className="text-slate-300 font-semibold">{summary?.total_findings || 0}</span> bulgu ·{' '}
            <span className="text-slate-300 font-semibold">{summary?.passed_checks || 0}</span> kontrol geçti
          </p>
        </div>
      </div>

      {/* Severity dağılımı */}
      <div className="grid grid-cols-4 gap-2">
        <SeverityCell
          count={counts.CRITICAL}
          label="Kritik"
          color="red"
          icon={
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          }
        />
        <SeverityCell
          count={counts.HIGH}
          label="Yüksek"
          color="orange"
          icon={
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
        />
        <SeverityCell
          count={counts.MEDIUM}
          label="Orta"
          color="yellow"
          icon={
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
        />
        <SeverityCell
          count={counts.LOW}
          label="Düşük"
          color="blue"
          icon={
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
        />
      </div>
    </div>
  )
}

function SeverityCell({ count, label, color, icon }) {
  const colorMap = {
    red: 'border-red-500/20 hover:border-red-500/40 text-red-400',
    orange: 'border-orange-500/20 hover:border-orange-500/40 text-orange-400',
    yellow: 'border-yellow-500/20 hover:border-yellow-500/40 text-yellow-400',
    blue: 'border-blue-500/20 hover:border-blue-500/40 text-blue-400',
  }
  return (
    <div className={`bg-slate-900/60 border ${colorMap[color]} rounded-lg p-2.5 text-center transition-all hover:-translate-y-0.5`}>
      <div className={`flex items-center justify-center gap-1 mb-1 ${count > 0 ? colorMap[color].split(' ')[2] : 'text-slate-600'}`}>
        {icon}
      </div>
      <div className={`text-xl font-bold ${count > 0 ? colorMap[color].split(' ')[2] : 'text-slate-600'}`}>{count}</div>
      <div className="text-xs text-slate-500 mt-0.5">{label}</div>
    </div>
  )
}

export default RiskScore
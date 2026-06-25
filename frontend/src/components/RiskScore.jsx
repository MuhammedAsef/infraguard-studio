function RiskScore({ score, level, summary }) {
  const levelStyles = {
    LOW: { color: 'text-green-400', bg: 'bg-green-500/10', border: 'border-green-500/30', label: 'DÜŞÜK RİSK' },
    MEDIUM: { color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', label: 'ORTA RİSK' },
    HIGH: { color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/30', label: 'YÜKSEK RİSK' },
    CRITICAL: { color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', label: 'KRİTİK RİSK' },
  }

  const style = levelStyles[level] || levelStyles.MEDIUM
  const counts = summary?.severity_counts || { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }

  return (
    <div className={`${style.bg} border ${style.border} rounded-lg p-5 mb-4`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-xs text-slate-400 mb-1">Genel Güvenlik Skoru</p>
          <div className="flex items-baseline gap-2">
            <span className={`text-5xl font-bold ${style.color}`}>{score}</span>
            <span className="text-slate-500 text-lg">/100</span>
          </div>
        </div>
        <div className="text-right">
          <span className={`inline-block text-xs font-bold px-3 py-1.5 rounded-full ${style.bg} ${style.color} border ${style.border}`}>
            {style.label}
          </span>
          <p className="text-xs text-slate-500 mt-2">
            {summary?.total_findings || 0} bulgu • {summary?.passed_checks || 0} geçti
          </p>
        </div>
      </div>

      {/* Severity dağılımı */}
      <div className="grid grid-cols-4 gap-2">
        <div className="bg-slate-900/50 border border-red-500/20 rounded p-2 text-center">
          <div className="text-red-400 text-xl font-bold">{counts.CRITICAL}</div>
          <div className="text-xs text-slate-500 mt-0.5">Kritik</div>
        </div>
        <div className="bg-slate-900/50 border border-orange-500/20 rounded p-2 text-center">
          <div className="text-orange-400 text-xl font-bold">{counts.HIGH}</div>
          <div className="text-xs text-slate-500 mt-0.5">Yüksek</div>
        </div>
        <div className="bg-slate-900/50 border border-yellow-500/20 rounded p-2 text-center">
          <div className="text-yellow-400 text-xl font-bold">{counts.MEDIUM}</div>
          <div className="text-xs text-slate-500 mt-0.5">Orta</div>
        </div>
        <div className="bg-slate-900/50 border border-blue-500/20 rounded p-2 text-center">
          <div className="text-blue-400 text-xl font-bold">{counts.LOW}</div>
          <div className="text-xs text-slate-500 mt-0.5">Düşük</div>
        </div>
      </div>
    </div>
  )
}

export default RiskScore
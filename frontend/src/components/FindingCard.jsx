function FindingCard({ finding }) {
  const severityStyles = {
    CRITICAL: { badge: 'bg-red-500/20 text-red-300 border-red-500/30', border: 'border-l-red-500', label: 'KRİTİK' },
    HIGH: { badge: 'bg-orange-500/20 text-orange-300 border-orange-500/30', border: 'border-l-orange-500', label: 'YÜKSEK' },
    MEDIUM: { badge: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30', border: 'border-l-yellow-500', label: 'ORTA' },
    LOW: { badge: 'bg-blue-500/20 text-blue-300 border-blue-500/30', border: 'border-l-blue-500', label: 'DÜŞÜK' },
  }

  const style = severityStyles[finding.severity] || severityStyles.MEDIUM

  return (
    <div className={`bg-slate-900 border border-slate-800 border-l-4 ${style.border} rounded-lg p-4`}>
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1.5 flex-wrap">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded border ${style.badge}`}>{style.label}</span>
            <span className="text-xs text-slate-500 font-mono">{finding.check_id}</span>
            <span className="text-xs text-slate-500">• Satır {finding.line_start}{finding.line_end !== finding.line_start && `-${finding.line_end}`}</span>
          </div>
          <h4 className="text-white font-semibold">{finding.title}</h4>
        </div>
      </div>

      <p className="text-slate-400 text-sm leading-relaxed mb-3">{finding.explanation}</p>

      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-500">Kategori:</span>
        <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded">{finding.category}</span>
      </div>

      {finding.code_snippet && (
        <div className="mt-3 bg-slate-950 border border-slate-800 rounded px-3 py-2">
          <code className="text-xs text-red-300 font-mono">{finding.code_snippet}</code>
        </div>
      )}

      {finding.references && finding.references.length > 0 && (
        <div className="mt-3 pt-3 border-t border-slate-800">
          <p className="text-xs text-slate-500 mb-1.5">Referanslar:</p>
          <ul className="space-y-1">
            {finding.references.map((ref, idx) => (
              <li key={idx} className="text-xs">
                {ref.startsWith('http') ? (
                  <a href={ref} target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:text-cyan-300 hover:underline break-all">{ref}</a>
                ) : (
                  <span className="text-slate-400">{ref}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default FindingCard
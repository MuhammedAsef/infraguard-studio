const SEVERITY_LABELS = {
  CRITICAL: { label: 'KRİTİK', color: 'text-red-400' },
  HIGH: { label: 'YÜKSEK', color: 'text-orange-400' },
  MEDIUM: { label: 'ORTA', color: 'text-yellow-400' },
  LOW: { label: 'DÜŞÜK', color: 'text-blue-400' },
}

const RISK_LEVEL_STYLES = {
  CRITICAL: 'text-red-400 bg-red-500/10 border-red-500/30',
  HIGH: 'text-orange-400 bg-orange-500/10 border-orange-500/30',
  MEDIUM: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
  LOW: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
}

const FILE_TYPE_LABELS = {
  dockerfile: 'Dockerfile',
  kubernetes: 'Kubernetes',
  terraform: 'Terraform',
}

const FILE_TYPE_ICONS = {
  dockerfile: 'M4 7v10c0 2.21 1.79 4 4 4h8c2.21 0 4-1.79 4-4V7M4 7c0-2.21 1.79-4 4-4h8c2.21 0 4 1.79 4 4M4 7h16',
  kubernetes: 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5',
  terraform: 'M4 6h16M4 12h16M4 18h7',
}

function formatRelativeTime(timestamp) {
  const diff = Date.now() - timestamp
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return 'az önce'
  if (minutes < 60) return `${minutes} dakika önce`
  if (hours < 24) return `${hours} saat önce`
  if (days < 7) return `${days} gün önce`

  const d = new Date(timestamp)
  return d.toLocaleDateString('tr-TR', { day: '2-digit', month: 'short' })
}

function ScanHistory({ history, onReopen, onRemove, onClearAll }) {
  if (!history || history.length === 0) return null

  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4 mb-6 backdrop-blur">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
          <svg className="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Son Taramalar
          <span className="text-xs text-slate-500 font-normal">({history.length})</span>
        </h3>
        <button
          onClick={onClearAll}
          className="text-xs text-slate-500 hover:text-red-400 transition-colors"
        >
          Geçmişi Temizle
        </button>
      </div>

      <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
        {history.map((entry) => {
          const fileTypeLabel = FILE_TYPE_LABELS[entry.file_type] || entry.file_type
          const iconPath = FILE_TYPE_ICONS[entry.file_type] || FILE_TYPE_ICONS.dockerfile
          const riskStyle = RISK_LEVEL_STYLES[entry.risk_level] || RISK_LEVEL_STYLES.LOW
          const counts = entry.severity_counts || {}

          return (
            <div
              key={entry.scan_id}
              className="group flex items-center gap-3 bg-slate-900/80 border border-slate-800 rounded-md p-2.5 hover:border-slate-700 transition-colors"
            >
              {/* İkon */}
              <div className="flex-shrink-0 w-8 h-8 rounded-md bg-slate-800 border border-slate-700 flex items-center justify-center">
                <svg className="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d={iconPath} />
                </svg>
              </div>

              {/* Bilgi */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm text-white font-medium">{fileTypeLabel}</span>
                  <span className={`text-xs font-bold px-1.5 py-0.5 rounded border ${riskStyle}`}>
                    {entry.risk_score}/100
                  </span>
                  {entry.total_findings > 0 && (
                    <span className="text-xs text-slate-500">
                      {entry.total_findings} bulgu
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                  <span>{formatRelativeTime(entry.timestamp)}</span>
                  {counts.CRITICAL > 0 && (
                    <span className="text-red-400">{counts.CRITICAL} kritik</span>
                  )}
                  {counts.HIGH > 0 && (
                    <span className="text-orange-400">{counts.HIGH} yüksek</span>
                  )}
                </div>
              </div>

              {/* Aksiyonlar */}
              <div className="flex items-center gap-1 flex-shrink-0">
                <button
                  onClick={() => onReopen(entry)}
                  className="text-xs px-2 py-1 rounded bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 transition-colors"
                  title="Bu taramayı yeniden aç"
                >
                  Aç
                </button>
                <button
                  onClick={() => onRemove(entry.scan_id)}
                  className="text-slate-600 hover:text-red-400 transition-colors p-1 opacity-0 group-hover:opacity-100"
                  title="Sil"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          )
        })}
      </div>

      <p className="text-xs text-slate-600 mt-3 italic">
        🔒 Geçmiş yalnızca tarayıcınızda saklanır. Sunucuda hiçbir bilgi tutulmaz.
      </p>
    </div>
  )
}

export default ScanHistory
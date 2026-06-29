import { useState } from 'react'

const SEVERITY_LABELS = {
  CRITICAL: { label: 'KRİTİK', color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30' },
  HIGH: { label: 'YÜKSEK', color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/30' },
  MEDIUM: { label: 'ORTA', color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30' },
  LOW: { label: 'DÜŞÜK', color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/30' },
}

const RISK_LEVEL_STYLES = {
  CRITICAL: { label: 'KRİTİK RİSK', color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/40', ring: 'stroke-red-500' },
  HIGH: { label: 'YÜKSEK RİSK', color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/40', ring: 'stroke-orange-500' },
  MEDIUM: { label: 'ORTA RİSK', color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/40', ring: 'stroke-yellow-500' },
  LOW: { label: 'DÜŞÜK RİSK', color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/40', ring: 'stroke-emerald-500' },
}

const FILE_TYPE_ICONS = {
  dockerfile: 'M4 7v10c0 2.21 1.79 4 4 4h8c2.21 0 4-1.79 4-4V7M4 7c0-2.21 1.79-4 4-4h8c2.21 0 4 1.79 4 4M4 7h16',
  kubernetes: 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5',
  terraform: 'M4 6h16M4 12h16M4 18h7',
}

const FILE_TYPE_LABELS = {
  dockerfile: 'Dockerfile',
  kubernetes: 'Kubernetes',
  terraform: 'Terraform',
}

function FileRow({ file, isExpanded, onToggle }) {
  const findings = file.findings || []
  const summary = file.summary || {}
  const severityCounts = summary.severity_counts || {}
  const riskLevel = file.risk_level || 'LOW'
  const riskStyle = RISK_LEVEL_STYLES[riskLevel]

  const totalFindings = summary.total_findings || 0
  const fileTypeLabel = FILE_TYPE_LABELS[file.file_type] || file.file_type
  const iconPath = FILE_TYPE_ICONS[file.file_type] || FILE_TYPE_ICONS.dockerfile

  return (
    <div className={`bg-slate-900/50 border border-slate-800 rounded-lg overflow-hidden transition-all ${isExpanded ? 'border-slate-700' : ''}`}>
      {/* Header (always visible) */}
      <button
        onClick={onToggle}
        className="w-full p-3 sm:p-4 flex items-center justify-between gap-3 hover:bg-slate-900 transition-colors"
      >
        <div className="flex items-center gap-3 min-w-0 flex-1">
          <div className="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 sm:w-5 sm:h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d={iconPath} />
            </svg>
          </div>
          <div className="min-w-0 flex-1 text-left">
            <p className="text-white text-sm font-medium truncate">{file.file_path}</p>
            <p className="text-xs text-slate-500">{fileTypeLabel}</p>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
          {file.error ? (
            <span className="text-xs text-red-400 hidden sm:inline">Hata</span>
          ) : totalFindings === 0 ? (
            <span className="text-xs text-emerald-400 flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <span className="hidden sm:inline">Temiz</span>
            </span>
          ) : (
            <>
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${riskStyle.bg} ${riskStyle.color} ${riskStyle.border}`}>
                {totalFindings}
              </span>
              {severityCounts.CRITICAL > 0 && (
                <span className="text-xs text-red-400 hidden sm:inline">{severityCounts.CRITICAL}K</span>
              )}
              {severityCounts.HIGH > 0 && (
                <span className="text-xs text-orange-400 hidden sm:inline">{severityCounts.HIGH}Y</span>
              )}
            </>
          )}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className={`w-4 h-4 text-slate-500 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Expanded content */}
      {isExpanded && (
        <div className="border-t border-slate-800 p-3 sm:p-4 bg-slate-950/50">
          {file.error ? (
            <p className="text-sm text-red-400">{file.error}</p>
          ) : findings.length === 0 ? (
            <p className="text-sm text-emerald-400">✓ Bu dosyada güvenlik sorunu tespit edilmedi.</p>
          ) : (
            <div className="space-y-3">
              {findings.map((finding, idx) => {
                const sevStyle = SEVERITY_LABELS[finding.severity] || SEVERITY_LABELS.MEDIUM
                return (
                  <div key={idx} className={`bg-slate-900/80 border ${sevStyle.border} rounded-md p-3`}>
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <span className={`text-xs font-bold px-2 py-0.5 rounded border ${sevStyle.bg} ${sevStyle.color} ${sevStyle.border}`}>
                        {sevStyle.label}
                      </span>
                      <span className="text-xs text-slate-500 font-mono">{finding.check_id}</span>
                      <span className="text-xs text-slate-500">
                        · Satır {finding.line_start}
                        {finding.line_end !== finding.line_start && `-${finding.line_end}`}
                      </span>
                      {finding.enriched_by_llm && (
                        <span className="text-xs font-medium px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/30">
                          AI
                        </span>
                      )}
                    </div>
                    <h5 className="text-white font-semibold text-sm mb-1.5">{finding.title}</h5>
                    <p className="text-slate-400 text-xs leading-relaxed">{finding.explanation}</p>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function MultiFileResultPanel({ result, isLoading, error }) {
  const [expandedFiles, setExpandedFiles] = useState(new Set())

  function toggleFile(filePath) {
    setExpandedFiles((prev) => {
      const next = new Set(prev)
      if (next.has(filePath)) {
        next.delete(filePath)
      } else {
        next.add(filePath)
      }
      return next
    })
  }

  function expandAll() {
    if (result?.files) {
      setExpandedFiles(new Set(result.files.map((f) => f.file_path)))
    }
  }

  function collapseAll() {
    setExpandedFiles(new Set())
  }

  if (isLoading) {
    return (
      <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-12 text-center">
        <div className="w-10 h-10 mx-auto mb-4 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin"></div>
        <p className="text-slate-400 text-sm">Repo taranıyor, lütfen bekleyin...</p>
        <p className="text-slate-500 text-xs mt-1">Dosya sayısına göre 5-30 saniye sürebilir</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-6">
        <p className="text-red-300 font-medium mb-1">⚠️ Tarama hatası</p>
        <p className="text-red-200/70 text-sm">{error}</p>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="bg-slate-900/30 border border-dashed border-slate-800 rounded-lg p-12 text-center">
        <p className="text-slate-500 text-sm">
          Bir zip dosyası yükleyin, tarama sonuçları burada görünecek.
        </p>
      </div>
    )
  }

  const riskStyle = RISK_LEVEL_STYLES[result.risk_level] || RISK_LEVEL_STYLES.LOW
  const severityCounts = result.summary?.severity_counts || {}

  // Risk score için circular progress
  const radius = 36
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (result.risk_score / 100) * circumference

  return (
    <div className="space-y-4">
      {/* Genel özet kartı */}
      <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-xl p-4 sm:p-5">
        <div className="flex items-center gap-4 mb-4">
          <div className="relative flex-shrink-0">
            <svg className="w-20 h-20 -rotate-90" viewBox="0 0 80 80">
              <circle cx="40" cy="40" r={radius} stroke="rgb(30,41,59)" strokeWidth="6" fill="none" />
              <circle
                cx="40"
                cy="40"
                r={radius}
                strokeWidth="6"
                fill="none"
                strokeLinecap="round"
                className={riskStyle.ring}
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                style={{ transition: 'stroke-dashoffset 1s ease' }}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-xl font-bold ${riskStyle.color}`}>{result.risk_score}</span>
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-0.5">Repo Risk Skoru</p>
            <p className={`text-base sm:text-lg font-bold ${riskStyle.color}`}>{riskStyle.label}</p>
            <p className="text-xs text-slate-500">
              {result.total_files_scanned} dosya · {result.total_findings} bulgu
            </p>
          </div>
        </div>

        {/* Severity dağılımı */}
        <div className="grid grid-cols-4 gap-2">
          {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((sev) => {
            const style = SEVERITY_LABELS[sev]
            const count = severityCounts[sev] || 0
            return (
              <div
                key={sev}
                className={`text-center py-2 rounded-md border ${style.border} ${style.bg}`}
              >
                <p className={`text-lg font-bold ${style.color}`}>{count}</p>
                <p className="text-xs text-slate-500">{style.label}</p>
              </div>
            )
          })}
        </div>
      </div>

      {/* Mesaj (desteklenen dosya yoksa) */}
      {result.message && (
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
          <p className="text-yellow-300 text-sm">ℹ️ {result.message}</p>
        </div>
      )}

      {/* Dosya listesi */}
      {result.files && result.files.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-semibold text-white">
              Dosyalar ({result.files.length})
            </h4>
            <div className="flex gap-2 text-xs">
              <button
                onClick={expandAll}
                className="text-slate-400 hover:text-cyan-400 transition-colors"
              >
                Tümünü Aç
              </button>
              <span className="text-slate-700">|</span>
              <button
                onClick={collapseAll}
                className="text-slate-400 hover:text-cyan-400 transition-colors"
              >
                Tümünü Kapat
              </button>
            </div>
          </div>
          <div className="space-y-2">
            {result.files.map((file) => (
              <FileRow
                key={file.file_path}
                file={file}
                isExpanded={expandedFiles.has(file.file_path)}
                onToggle={() => toggleFile(file.file_path)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default MultiFileResultPanel
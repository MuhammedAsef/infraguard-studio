import { useState } from 'react'
import DiffViewer from './DiffViewer'

const LANGUAGE_MAP = {
  dockerfile: 'dockerfile',
  kubernetes: 'yaml',
  terraform: 'hcl',
}

const SEVERITY_STYLES = {
  CRITICAL: {
    badge: 'bg-red-500/20 text-red-300 border-red-500/40',
    border: 'border-l-red-500',
    glow: 'shadow-[0_0_20px_-5px_rgba(239,68,68,0.3)]',
    iconBg: 'bg-red-500/10 border-red-500/30',
    iconColor: 'text-red-400',
    label: 'KRİTİK',
    icon: (
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    ),
  },
  HIGH: {
    badge: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
    border: 'border-l-orange-500',
    glow: 'shadow-[0_0_20px_-5px_rgba(249,115,22,0.25)]',
    iconBg: 'bg-orange-500/10 border-orange-500/30',
    iconColor: 'text-orange-400',
    label: 'YÜKSEK',
    icon: (
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  MEDIUM: {
    badge: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
    border: 'border-l-yellow-500',
    glow: 'shadow-[0_0_20px_-5px_rgba(234,179,8,0.2)]',
    iconBg: 'bg-yellow-500/10 border-yellow-500/30',
    iconColor: 'text-yellow-400',
    label: 'ORTA',
    icon: (
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  LOW: {
    badge: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
    border: 'border-l-blue-500',
    glow: 'shadow-[0_0_20px_-5px_rgba(59,130,246,0.2)]',
    iconBg: 'bg-blue-500/10 border-blue-500/30',
    iconColor: 'text-blue-400',
    label: 'DÜŞÜK',
    icon: (
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
}

function FindingCard({ finding, originalCode, fileType }) {
  const [showDiff, setShowDiff] = useState(false)
  const style = SEVERITY_STYLES[finding.severity] || SEVERITY_STYLES.MEDIUM
  const hasFix = finding.fixed_code !== null && finding.fixed_code !== undefined

  return (
    <div className={`group bg-slate-900/80 backdrop-blur border border-slate-800 border-l-4 ${style.border} ${style.glow} rounded-lg p-4 transition-all hover:border-slate-700 hover:-translate-y-0.5`}>
      {/* Üst kısım: ikon + severity + meta */}
      <div className="flex items-start gap-3 mb-3">
        <div className={`flex-shrink-0 w-9 h-9 rounded-lg border ${style.iconBg} ${style.iconColor} flex items-center justify-center`}>
          {style.icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${style.badge}`}>{style.label}</span>
            <span className="text-xs text-slate-500 font-mono">{finding.check_id}</span>
            <span className="text-xs text-slate-500">
              · Satır {finding.line_start}
              {finding.line_end !== finding.line_start && `-${finding.line_end}`}
            </span>
            {finding.enriched_by_llm && (
              <span
                className="text-xs font-medium px-2 py-0.5 rounded border bg-purple-500/10 text-purple-300 border-purple-500/30 flex items-center gap-1"
                title="Bu açıklama AI ile dinamik olarak üretildi"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                AI
              </span>
            )}
          </div>
          <h4 className="text-white font-semibold leading-snug">{finding.title}</h4>
        </div>
      </div>

      <p className="text-slate-400 text-sm leading-relaxed mb-3">{finding.explanation}</p>

      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-500">Kategori:</span>
        <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded">{finding.category}</span>
      </div>

      {finding.code_snippet && (
        <div className="mt-3 bg-slate-950/80 border border-slate-800 rounded-md px-3 py-2 overflow-x-auto">
          <code className="text-xs text-red-300 font-mono whitespace-pre">{finding.code_snippet}</code>
        </div>
      )}

      {hasFix && (
        <div className="mt-3">
          <button
            onClick={() => setShowDiff(!showDiff)}
            className="flex items-center gap-2 text-xs font-medium bg-gradient-to-r from-emerald-500/10 to-green-500/10 hover:from-emerald-500/20 hover:to-green-500/20 text-emerald-300 border border-emerald-500/30 px-3 py-1.5 rounded-md transition-all hover:shadow-[0_0_15px_-3px_rgba(16,185,129,0.4)]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            {showDiff ? 'Düzeltmeyi Gizle' : 'Önerilen Düzeltmeyi Gör'}
            <svg xmlns="http://www.w3.org/2000/svg" className={`w-3 h-3 transition-transform ${showDiff ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {showDiff && (
            <div className="mt-3">
              <DiffViewer
                original={originalCode}
                modified={finding.fixed_code}
                language={LANGUAGE_MAP[fileType] || 'plaintext'}
              />
              <div className="mt-2 flex items-center justify-end gap-2">
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(finding.fixed_code)
                  }}
                  className="text-xs text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-1"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Kopyala
                </button>
              </div>
            </div>
          )}
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
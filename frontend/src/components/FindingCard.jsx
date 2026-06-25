import { useState } from 'react'
import DiffViewer from './DiffViewer'

const LANGUAGE_MAP = {
  dockerfile: 'dockerfile',
  kubernetes: 'yaml',
  terraform: 'hcl',
}

function FindingCard({ finding, originalCode, fileType }) {
  const [showDiff, setShowDiff] = useState(false)

  const severityStyles = {
    CRITICAL: { badge: 'bg-red-500/20 text-red-300 border-red-500/30', border: 'border-l-red-500', label: 'KRİTİK' },
    HIGH: { badge: 'bg-orange-500/20 text-orange-300 border-orange-500/30', border: 'border-l-orange-500', label: 'YÜKSEK' },
    MEDIUM: { badge: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30', border: 'border-l-yellow-500', label: 'ORTA' },
    LOW: { badge: 'bg-blue-500/20 text-blue-300 border-blue-500/30', border: 'border-l-blue-500', label: 'DÜŞÜK' },
  }

  const style = severityStyles[finding.severity] || severityStyles.MEDIUM
  const hasFix = finding.fixed_code !== null && finding.fixed_code !== undefined

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

      {/* Düzeltme butonu — sadece fixed_code varsa görünür */}
      {hasFix && (
        <div className="mt-3">
          <button
            onClick={() => setShowDiff(!showDiff)}
            className="flex items-center gap-2 text-xs font-medium bg-green-500/10 hover:bg-green-500/20 text-green-300 border border-green-500/30 px-3 py-1.5 rounded-md transition-colors"
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
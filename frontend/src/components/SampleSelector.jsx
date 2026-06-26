import { useState, useEffect } from 'react'
import { getSamples } from '../services/api'

function SampleSelector({ fileType, onSelect }) {
  const [samples, setSamples] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getSamples()
      .then((data) => {
        setSamples(data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  const filteredSamples = samples.filter((s) => s.file_type === fileType)

  if (loading || filteredSamples.length === 0) {
    return null
  }

  return (
    <div className="mb-4">
      <p className="text-xs text-slate-500 mb-2">Hızlı başlangıç için bir örnek deneyin:</p>
      <div className="flex flex-wrap gap-2">
        {filteredSamples.map((sample) => {
          const isSecure = sample.id.includes('secure')
          return (
            <button
              key={sample.id}
              onClick={() => onSelect(sample.code)}
              className={`text-xs font-medium px-3 py-1.5 rounded-md border transition-all hover:-translate-y-0.5 ${
                isSecure
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/20 hover:border-emerald-500/50'
                  : 'bg-orange-500/10 border-orange-500/30 text-orange-300 hover:bg-orange-500/20 hover:border-orange-500/50'
              }`}
              title={sample.description}
            >
              <span className="inline-flex items-center gap-1.5">
                {isSecure ? (
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                )}
                {sample.title}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default SampleSelector
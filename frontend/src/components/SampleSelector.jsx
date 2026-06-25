import { useState, useEffect } from 'react'
import { getSamples } from '../services/api'

function SampleSelector({ onSelect }) {
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

  if (loading || samples.length === 0) {
    return null
  }

  return (
    <div className="mb-4">
      <p className="text-xs text-slate-500 mb-2">Hızlı başlangıç için bir örnek deneyin:</p>
      <div className="flex flex-wrap gap-2">
        {samples.map((sample) => {
          const isSecure = sample.id.includes('secure')
          return (
            <button
              key={sample.id}
              onClick={() => onSelect(sample.code)}
              className={`text-xs font-medium px-3 py-1.5 rounded-md border transition-colors ${
                isSecure
                  ? 'bg-green-500/10 border-green-500/30 text-green-300 hover:bg-green-500/20'
                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700 hover:border-slate-600'
              }`}
              title={sample.description}
            >
              {isSecure && '✓ '}
              {sample.title}
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default SampleSelector
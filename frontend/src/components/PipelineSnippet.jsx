import { useState } from 'react'

function PipelineSnippet({ snippets }) {
  const [activeTab, setActiveTab] = useState('gitlab')
  const [copied, setCopied] = useState(false)

  if (!snippets || (!snippets.gitlab && !snippets.github)) {
    return null
  }

  const currentCode = activeTab === 'gitlab' ? snippets.gitlab : snippets.github

  function handleCopy() {
    navigator.clipboard.writeText(currentCode)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="mt-6 bg-slate-900/50 border border-slate-800 rounded-lg overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-800">
        <div className="flex items-center gap-2 mb-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <h4 className="text-white font-semibold">CI/CD Pipeline Entegrasyonu</h4>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          {snippets.explanation}
        </p>
      </div>

      {/* Tab seçici */}
      <div className="flex border-b border-slate-800 bg-slate-900">
        <button
          onClick={() => setActiveTab('gitlab')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'gitlab'
              ? 'border-cyan-400 text-cyan-400 bg-slate-800/50'
              : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          <span className="flex items-center gap-2">
            <span className="text-orange-400 font-bold">●</span>
            GitLab CI
          </span>
        </button>
        <button
          onClick={() => setActiveTab('github')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'github'
              ? 'border-cyan-400 text-cyan-400 bg-slate-800/50'
              : 'border-transparent text-slate-400 hover:text-white'
          }`}
        >
          <span className="flex items-center gap-2">
            <span className="text-purple-400 font-bold">●</span>
            GitHub Actions
          </span>
        </button>
      </div>

      {/* Kod bloğu */}
      <div className="relative">
        <pre className="p-4 text-xs text-slate-300 overflow-x-auto bg-slate-950/50 max-h-96 overflow-y-auto">
          <code className="font-mono">{currentCode}</code>
        </pre>

        {/* Kopyala butonu */}
        <button
          onClick={handleCopy}
          className="absolute top-3 right-3 flex items-center gap-1.5 text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 px-2.5 py-1.5 rounded-md transition-colors"
        >
          {copied ? (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" className="w-3.5 h-3.5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-green-400">Kopyalandı</span>
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Kopyala
            </>
          )}
        </button>
      </div>
    </div>
  )
}

export default PipelineSnippet
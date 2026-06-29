import { useState, useEffect } from 'react'
import { DiffEditor } from '@monaco-editor/react'

function DiffViewer({ original, modified, language = 'dockerfile' }) {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    function checkMobile() {
      setIsMobile(window.innerWidth < 768)
    }
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return (
    <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-900">
      {/* Üst bar */}
      <div className="flex items-center justify-between px-3 sm:px-4 py-2 bg-slate-900 border-b border-slate-800 gap-2">
        <div className="flex items-center gap-2 sm:gap-4 flex-wrap">
          <span className="text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-2 h-2 bg-red-500/60 rounded-sm"></span>
            <span className="hidden sm:inline">Mevcut Kod</span>
            <span className="sm:hidden">Mevcut</span>
          </span>
          <span className="text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-2 h-2 bg-green-500/60 rounded-sm"></span>
            <span className="hidden sm:inline">Önerilen Düzeltme</span>
            <span className="sm:hidden">Önerilen</span>
          </span>
        </div>
        <span className="text-xs text-slate-500 flex-shrink-0">
          {isMobile ? 'Üst / Alt' : 'Before / After'}
        </span>
      </div>

      {/* Diff Editor */}
      <DiffEditor
        height={isMobile ? '500px' : '350px'}
        language={language}
        original={original}
        modified={modified}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: isMobile ? 12 : 13,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          renderSideBySide: !isMobile,
          readOnly: true,
          fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
          wordWrap: 'on',
          automaticLayout: true,
        }}
      />
    </div>
  )
}

export default DiffViewer
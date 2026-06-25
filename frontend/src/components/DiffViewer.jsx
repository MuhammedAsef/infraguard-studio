import { DiffEditor } from '@monaco-editor/react'

function DiffViewer({ original, modified, language = 'dockerfile' }) {
  return (
    <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-900">
      {/* Üst bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center gap-4">
          <span className="text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-2 h-2 bg-red-500/60 rounded-sm"></span>
            Mevcut Kod
          </span>
          <span className="text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-2 h-2 bg-green-500/60 rounded-sm"></span>
            Önerilen Düzeltme
          </span>
        </div>
        <span className="text-xs text-slate-500">Before / After</span>
      </div>

      {/* Diff Editor */}
      <DiffEditor
        height="350px"
        language={language}
        original={original}
        modified={modified}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 13,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          renderSideBySide: true,
          readOnly: true,
          fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
        }}
      />
    </div>
  )
}

export default DiffViewer
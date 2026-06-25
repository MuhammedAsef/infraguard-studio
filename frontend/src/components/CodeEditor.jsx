import Editor from '@monaco-editor/react'

function CodeEditor({ code, onChange, language = 'dockerfile' }) {
  return (
    <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-900">
      {/* Editör üst bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/60"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/60"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/60"></div>
          </div>
          <span className="text-xs text-slate-500 ml-2 font-mono">Dockerfile</span>
        </div>
        <span className="text-xs text-slate-500">
          {code.length} karakter
        </span>
      </div>

      {/* Monaco Editor */}
      <Editor
        height="500px"
        language={language}
        value={code}
        onChange={(value) => onChange(value || '')}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          wordWrap: 'on',
          padding: { top: 16, bottom: 16 },
          fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
          renderLineHighlight: 'all',
          smoothScrolling: true,
        }}
      />
    </div>
  )
}

export default CodeEditor
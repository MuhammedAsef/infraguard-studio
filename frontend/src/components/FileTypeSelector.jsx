const FILE_TYPES = [
  {
    id: 'dockerfile',
    label: 'Dockerfile',
    icon: 'M4 7v10c0 2.21 1.79 4 4 4h8c2.21 0 4-1.79 4-4V7M4 7c0-2.21 1.79-4 4-4h8c2.21 0 4 1.79 4 4M4 7h16',
  },
  {
    id: 'kubernetes',
    label: 'Kubernetes',
    icon: 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5',
  },
  {
    id: 'terraform',
    label: 'Terraform',
    icon: 'M4 6h16M4 12h16M4 18h7',
  },
]

function FileTypeSelector({ selected, onChange }) {
  return (
    <div className="mb-4">
      <p className="text-xs text-slate-500 mb-2">Dosya tipi seçin:</p>
      <div className="inline-flex bg-slate-900 border border-slate-800 rounded-lg p-1">
        {FILE_TYPES.map((type) => {
          const isActive = selected === type.id
          return (
            <button
              key={type.id}
              onClick={() => onChange(type.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                isActive
                  ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d={type.icon} />
              </svg>
              {type.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default FileTypeSelector
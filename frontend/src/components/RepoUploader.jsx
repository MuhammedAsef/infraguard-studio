import { useState, useRef } from 'react'

function RepoUploader({ onScan, isLoading }) {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [error, setError] = useState(null)
  const inputRef = useRef(null)

  const MAX_SIZE_MB = 10

  function validateFile(file) {
    if (!file) return 'Dosya seçilmedi'
    if (!file.name.toLowerCase().endsWith('.zip')) {
      return 'Sadece .zip dosyası yükleyebilirsiniz'
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      return `Dosya çok büyük. Maksimum ${MAX_SIZE_MB}MB`
    }
    if (file.size === 0) {
      return 'Boş dosya'
    }
    return null
  }

  function handleFileSelect(file) {
    setError(null)
    const validationError = validateFile(file)
    if (validationError) {
      setError(validationError)
      setSelectedFile(null)
      return
    }
    setSelectedFile(file)
  }

  function handleDrag(e) {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const file = e.dataTransfer.files?.[0]
    if (file) handleFileSelect(file)
  }

  function handleChange(e) {
    const file = e.target.files?.[0]
    if (file) handleFileSelect(file)
  }

  function handleScan() {
    if (selectedFile) {
      onScan(selectedFile)
    }
  }

  function handleClear() {
    setSelectedFile(null)
    setError(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / 1024 / 1024).toFixed(2)} MB`
  }

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-lg p-8 sm:p-12 text-center cursor-pointer transition-all ${
          dragActive
            ? 'border-cyan-400 bg-cyan-500/10'
            : selectedFile
            ? 'border-emerald-500/50 bg-emerald-500/5'
            : 'border-slate-700 hover:border-slate-600 bg-slate-900/30'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".zip,application/zip,application/x-zip-compressed"
          onChange={handleChange}
          className="hidden"
        />

        {selectedFile ? (
          <div>
            <div className="w-14 h-14 mx-auto mb-3 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
              <svg className="w-7 h-7 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-white font-medium mb-1 break-all px-4">{selectedFile.name}</p>
            <p className="text-slate-400 text-sm">{formatFileSize(selectedFile.size)}</p>
            <button
              onClick={(e) => {
                e.stopPropagation()
                handleClear()
              }}
              className="mt-3 text-xs text-slate-400 hover:text-red-400 transition-colors"
            >
              ✕ Kaldır
            </button>
          </div>
        ) : (
          <div>
            <div className="w-14 h-14 mx-auto mb-3 rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
              <svg className="w-7 h-7 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p className="text-white font-medium mb-1 text-sm sm:text-base">
              {dragActive ? 'Dosyayı bırakın' : 'Zip dosyasını sürükleyin veya tıklayın'}
            </p>
            <p className="text-slate-400 text-xs sm:text-sm">
              .zip · Maksimum {MAX_SIZE_MB}MB · Maksimum 50 dosya
            </p>
          </div>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-sm text-red-300">
          ⚠️ {error}
        </div>
      )}

      {/* Info */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-3 text-xs text-slate-400 space-y-1">
        <p><span className="text-cyan-400 font-medium">Otomatik tespit:</span> Dockerfile, *.tf, *.yaml/.yml dosyaları</p>
        <p><span className="text-cyan-400 font-medium">Güvenlik:</span> Zip içeriği sandbox'lanmış geçici dizinde işlenir, sonrasında silinir</p>
      </div>

      {/* Scan button */}
      <button
        onClick={handleScan}
        disabled={!selectedFile || isLoading}
        className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-medium px-5 py-3 rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40"
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            Repo Taranıyor...
          </>
        ) : (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            Repo'yu Tara
          </>
        )}
      </button>
    </div>
  )
}

export default RepoUploader
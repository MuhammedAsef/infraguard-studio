import { useState } from 'react'
import Header from './components/Header'
import CodeEditor from './components/CodeEditor'
import ResultPanel from './components/ResultPanel'
import SampleSelector from './components/SampleSelector'
import FileTypeSelector from './components/FileTypeSelector'
import Footer from './components/Footer'
import RepoUploader from './components/RepoUploader'
import MultiFileResultPanel from './components/MultiFileResultPanel'
import ScanHistory from './components/ScanHistory'
import { useScanHistory } from './hooks/useScanHistory'
import { scanCode, scanRepo } from './services/api'

// Her dosya tipi için varsayılan kod
const DEFAULT_CODES = {
  dockerfile: `FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y curl

COPY . /app
WORKDIR /app

USER root

EXPOSE 8080

CMD ["python", "app.py"]
`,
  kubernetes: `apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: web
    image: nginx:latest
    ports:
    - containerPort: 80
    securityContext:
      privileged: true
      runAsUser: 0
`,
  terraform: `resource "aws_s3_bucket" "data" {
  bucket = "my-data"
  acl    = "public-read"
}

resource "aws_security_group" "web" {
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
`,
}

function App() {
  // Mode: 'code' (tek dosya yapıştır) veya 'repo' (zip yükle)
  const [mode, setMode] = useState('code')

  // Tek dosya state'leri
  const [fileType, setFileType] = useState('dockerfile')
  const [code, setCode] = useState(DEFAULT_CODES.dockerfile)
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  // Tarama geçmişi (browser localStorage)
  const { history, addEntry, removeEntry, clearAll } = useScanHistory()

  // Repo state'leri
  const [repoResult, setRepoResult] = useState(null)
  const [isRepoLoading, setIsRepoLoading] = useState(false)
  const [repoError, setRepoError] = useState(null)

  function handleFileTypeChange(newType) {
    setFileType(newType)
    setCode(DEFAULT_CODES[newType])
    setResult(null)
    setError(null)
  }

  async function handleScan() {
    if (!code.trim()) {
      setError('Lütfen önce kodu yapıştırın')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await scanCode(code, fileType, 'tr')
      setResult(data)
      addEntry(data, fileType)  // Geçmişe ekle
    } catch (err) {
      setError(err.message || 'Bilinmeyen bir hata oluştu')
    } finally {
      setIsLoading(false)
    }
  }

  function handleReopen(entry) {
    // Geçmişten bir taramayı yeniden aç
    setMode('code')
    setFileType(entry.file_type)
    setResult(entry.result_snapshot)
    setError(null)
    setIsLoading(false)
    // Smooth scroll up
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function handleRepoScan(zipFile) {
    setIsRepoLoading(true)
    setRepoError(null)
    setRepoResult(null)

    try {
      const data = await scanRepo(zipFile, 'tr')
      setRepoResult(data)
    } catch (err) {
      setRepoError(err.message || 'Bilinmeyen bir hata oluştu')
    } finally {
      setIsRepoLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
        <div className="absolute top-20 -right-40 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-cyan-500/5 rounded-full blur-3xl"></div>
      </div>

      {/* Grid pattern overlay */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.03]"
        style={{
          backgroundImage: 'linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      ></div>

      <div className="relative z-10">
        <Header />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
          {/* Hero */}
          <div className="text-center mb-12">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 text-xs font-medium">
              <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></span>
              <span>Live · DevSecOps Portfolio Project</span>
            </div>

            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 leading-tight">
              IaC Güvenlik Açıklarını{' '}
              <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-cyan-300 bg-clip-text text-transparent">
                Anında Tespit Edin
              </span>
            </h2>

            <p className="text-slate-400 max-w-2xl mx-auto text-base sm:text-lg leading-relaxed px-4 sm:px-0">
              Dockerfile, Kubernetes manifest ve Terraform dosyalarınızdaki güvenlik
              risklerini, <span className="text-slate-200">açıklamalı raporlar</span> ve{' '}
              <span className="text-slate-200">düzeltme önerileriyle</span> keşfedin.
            </p>

            {/* Stats */}
            <div className="grid grid-cols-2 sm:flex sm:flex-wrap items-center justify-center gap-4 sm:gap-8 mt-8 text-sm">
              <div className="flex items-center gap-2 justify-center sm:justify-start">
                <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-cyan-400 font-bold">3</span>
                </div>
                <span className="text-slate-400 text-xs sm:text-sm">Dosya Tipi</span>
              </div>
              <div className="flex items-center gap-2 justify-center sm:justify-start">
                <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-blue-400 font-bold text-xs">1K+</span>
                </div>
                <span className="text-slate-400 text-xs sm:text-sm">Güvenlik Kuralı</span>
              </div>
              <div className="flex items-center gap-2 justify-center sm:justify-start">
                <div className="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-purple-400 font-bold text-xs">AI</span>
                </div>
                <span className="text-slate-400 text-xs sm:text-sm">Akıllı Açıklama</span>
              </div>
              <div className="flex items-center gap-2 justify-center sm:justify-start">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0">
                  <svg className="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span className="text-slate-400 text-xs sm:text-sm">Otomatik Düzeltme</span>
              </div>
            </div>
          </div>

          {/* Privacy notice */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg px-4 py-3 mb-6 text-center backdrop-blur">
            <p className="text-xs text-slate-400">
              <span className="text-cyan-400">🔒</span> Kodunuz tarama süresi boyunca geçici olarak işlenir, kalıcı olarak saklanmaz.
              Hassas dosyalar paylaşmayınız.
            </p>
          </div>

          {/* Tarama Geçmişi */}
          <ScanHistory
            history={history}
            onReopen={handleReopen}
            onRemove={removeEntry}
            onClearAll={clearAll}
          />

          {/* MODE SWITCHER */}
          <div className="flex justify-center mb-6">
            <div className="inline-flex bg-slate-900 border border-slate-800 rounded-lg p-1">
              <button
                onClick={() => setMode('code')}
                className={`flex items-center gap-2 px-4 sm:px-5 py-2 rounded-md text-sm font-medium transition-all ${
                  mode === 'code'
                    ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                Kod Yapıştır
              </button>
              <button
                onClick={() => setMode('repo')}
                className={`flex items-center gap-2 px-4 sm:px-5 py-2 rounded-md text-sm font-medium transition-all ${
                  mode === 'repo'
                    ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                Repo Yükle
                <span className="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-1.5 py-0.5 rounded">YENİ</span>
              </button>
            </div>
          </div>

          {/* CODE MODE */}
          {mode === 'code' && (
            <>
              <FileTypeSelector selected={fileType} onChange={handleFileTypeChange} />

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <div className="flex items-center justify-between mb-3 gap-2">
                    <h3 className="text-base sm:text-lg font-semibold">Kodunuzu Yapıştırın</h3>
                    <button
                      onClick={handleScan}
                      disabled={isLoading}
                      className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-medium px-4 sm:px-5 py-2 rounded-lg transition-all flex items-center gap-2 shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 text-sm sm:text-base"
                    >
                      {isLoading ? (
                        <>
                          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                          Taranıyor...
                        </>
                      ) : (
                        <>
                          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                          </svg>
                          Tara
                        </>
                      )}
                    </button>
                  </div>
                  <SampleSelector fileType={fileType} onSelect={setCode} />
                  <CodeEditor code={code} onChange={setCode} fileType={fileType} />
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">Güvenlik Raporu</h3>
                  <ResultPanel
                    result={result}
                    isLoading={isLoading}
                    error={error}
                    originalCode={code}
                    fileType={fileType}
                  />
                </div>
              </div>
            </>
          )}

          {/* REPO MODE */}
          {mode === 'repo' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h3 className="text-base sm:text-lg font-semibold mb-3">Repo Yükle</h3>
                <RepoUploader onScan={handleRepoScan} isLoading={isRepoLoading} />
              </div>

              <div>
                <h3 className="text-base sm:text-lg font-semibold mb-3">Güvenlik Raporu</h3>
                <MultiFileResultPanel
                  result={repoResult}
                  isLoading={isRepoLoading}
                  error={repoError}
                />
              </div>
            </div>
          )}
        </main>

        <Footer />
      </div>
    </div>
  )
}

export default App
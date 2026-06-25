import { useState } from 'react'
import Header from './components/Header'
import CodeEditor from './components/CodeEditor'
import ResultPanel from './components/ResultPanel'
import { scanCode } from './services/api'
import SampleSelector from './components/SampleSelector'
import Footer from './components/Footer'

const DEFAULT_CODE = `FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y curl

COPY . /app
WORKDIR /app

USER root

EXPOSE 8080

CMD ["python", "app.py"]
`

function App() {
  const [code, setCode] = useState(DEFAULT_CODE)
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleScan() {
    if (!code.trim()) {
      setError('Lütfen önce kodu yapıştırın')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await scanCode(code, 'dockerfile', 'tr')
      setResult(data)
    } catch (err) {
      setError(err.message || 'Bilinmeyen bir hata oluştu')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Header />

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Hero */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-3">
            IaC Güvenlik Açıklarını Anında Tespit Edin
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Dockerfile, Kubernetes manifest ve Terraform dosyalarınızdaki güvenlik
            risklerini, açıklamalı raporlar ve düzeltme önerileriyle keşfedin.
          </p>
        </div>

        {/* Privacy notice */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-lg px-4 py-3 mb-6 text-center">
          <p className="text-xs text-slate-400">
            <span className="text-cyan-400">🔒</span> Kodunuz tarama süresi boyunca geçici olarak işlenir, kalıcı olarak saklanmaz.
            Hassas dosyalar paylaşmayınız.
          </p>
        </div>

        {/* İki sütunlu layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Sol: Editör + Tara butonu */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold">Kodunuzu Yapıştırın</h3>
              <button
                onClick={handleScan}
                disabled={isLoading}
                className="bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-medium px-5 py-2 rounded-lg transition-colors flex items-center gap-2"
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
             <SampleSelector onSelect={setCode} />
            <CodeEditor code={code} onChange={setCode} />
          </div>

          {/* Sağ: Sonuç paneli */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Güvenlik Raporu</h3>
            <ResultPanel result={result} isLoading={isLoading} error={error} />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default App
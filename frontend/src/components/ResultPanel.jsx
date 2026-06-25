import RiskScore from './RiskScore'
import FindingCard from './FindingCard'
import PipelineSnippet from './PipelineSnippet'
import { downloadScanPdf } from '../services/api'
import { useState } from 'react'

function ResultPanel({ result, isLoading, error, originalCode, fileType }) {
  const [downloadingPdf, setDownloadingPdf] = useState(false)

  async function handleDownloadPdf() {
    setDownloadingPdf(true)
    try {
      await downloadScanPdf(originalCode, fileType, 'tr')
    } catch (err) {
      alert('PDF indirilemedi: ' + err.message)
    } finally {
      setDownloadingPdf(false)
    }
  }

  // Yükleniyor durumu
  if (isLoading) {
    return (
      <div className="border border-slate-800 rounded-lg bg-slate-900/50 h-[548px] flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mb-3"></div>
          <p className="text-slate-400">Tarama yapılıyor...</p>
          <p className="text-slate-600 text-xs mt-1">Bu birkaç saniye sürebilir</p>
        </div>
      </div>
    )
  }

  // Hata durumu
  if (error) {
    return (
      <div className="border border-red-500/30 rounded-lg bg-red-500/5 h-[548px] flex items-center justify-center">
        <div className="text-center px-8">
          <div className="w-12 h-12 mx-auto mb-3 rounded-full bg-red-500/20 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p className="text-red-300 font-semibold mb-1">Tarama Başarısız</p>
          <p className="text-slate-400 text-sm">{error}</p>
        </div>
      </div>
    )
  }

  // İlk durum: henüz tarama yapılmadı
  if (!result) {
    return (
      <div className="border border-slate-800 rounded-lg bg-slate-900/50 h-[548px] flex items-center justify-center">
        <div className="text-center px-8">
          <div className="w-12 h-12 mx-auto mb-3 rounded-full bg-slate-800 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
          </div>
          <p className="text-slate-300 font-medium mb-1">Tarama Bekleniyor</p>
          <p className="text-slate-500 text-sm">
            Kodunuzu yapıştırın ve "Tara" butonuna basın.<br />
            Güvenlik bulguları burada gösterilecek.
          </p>
        </div>
      </div>
    )
  }

  // PDF indir butonu (her iki sonuç durumunda da kullanılacak)
  const pdfButton = (
    <div className="flex justify-end mb-4">
      <button
        onClick={handleDownloadPdf}
        disabled={downloadingPdf}
        className="flex items-center gap-2 text-sm font-medium bg-slate-800 hover:bg-slate-700 disabled:bg-slate-900 disabled:cursor-not-allowed text-white border border-slate-700 px-4 py-2 rounded-lg transition-colors"
      >
        {downloadingPdf ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            PDF Hazırlanıyor...
          </>
        ) : (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            PDF İndir
          </>
        )}
      </button>
    </div>
  )

  // Tarama tamamlandı ve hiç bulgu yok
  if (result.findings.length === 0) {
    return (
      <div>
        <RiskScore score={result.risk_score} level={result.risk_level} summary={result.summary} />
        {pdfButton}
        <div className="border border-green-500/30 rounded-lg bg-green-500/5 p-8 text-center">
          <div className="w-14 h-14 mx-auto mb-3 rounded-full bg-green-500/20 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <p className="text-green-300 font-semibold mb-1">Güvenlik Sorunu Bulunamadı</p>
          <p className="text-slate-400 text-sm">Dosyanız temel güvenlik kontrollerini geçti.</p>
        </div>

        <PipelineSnippet snippets={result.pipeline_snippets} />
      </div>
    )
  }

  // Tarama tamamlandı ve bulgular var
  return (
    <div>
      <RiskScore score={result.risk_score} level={result.risk_level} summary={result.summary} />
      {pdfButton}

      <div className="space-y-3 max-h-[450px] overflow-y-auto pr-2">
        {result.findings.map((finding) => (
          <FindingCard
            key={finding.check_id + finding.line_start}
            finding={finding}
            originalCode={originalCode}
            fileType={fileType}
          />
        ))}
      </div>

      <PipelineSnippet snippets={result.pipeline_snippets} />
    </div>
  )
}

export default ResultPanel
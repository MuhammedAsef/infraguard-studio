// Backend API ile konuşan fonksiyonlar

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

/**
 * Verilen kodu güvenlik açısından tara
 */
export async function scanCode(code, fileType = 'dockerfile', lang = 'tr') {
  const response = await fetch(`${API_BASE_URL}/scan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code,
      file_type: fileType,
      lang,
    }),
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    const errorMessage =
      errorData.detail?.error ||
      errorData.detail ||
      `Sunucu hatası (${response.status})`
    throw new Error(errorMessage)
  }

  return await response.json()
}

/**
 * Hazır demo dosyalarını getir
 */
export async function getSamples() {
  const response = await fetch(`${API_BASE_URL}/samples`)
  if (!response.ok) {
    throw new Error('Demo dosyaları yüklenemedi')
  }
  return await response.json()
}

export async function downloadScanPdf(code, fileType, lang = 'tr') {
  const response = await fetch(`${API_BASE_URL}/scan/pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, file_type: fileType, lang }),
  })

  if (!response.ok) {
    throw new Error('PDF üretilemedi')
  }

  // Response'u Blob olarak al
  const blob = await response.blob()

  // Dosya adını response header'dan çek
  const contentDisposition = response.headers.get('Content-Disposition') || ''
  const match = contentDisposition.match(/filename="(.+)"/)
  const filename = match ? match[1] : 'infraguard-report.pdf'

  // Tarayıcıda indirme tetikle
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url)
}
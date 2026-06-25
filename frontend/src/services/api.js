// Backend API ile konuşan fonksiyonlar

const API_BASE_URL = 'http://localhost:8000/api'

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
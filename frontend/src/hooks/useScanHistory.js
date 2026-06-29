import { useState, useEffect, useCallback } from 'react'

const STORAGE_KEY = 'infraguard_scan_history'
const MAX_ENTRIES = 20

/**
 * Tarama geçmişini localStorage'da yöneten hook.
 *
 * Gizlilik kararı: Kullanıcı kodu ASLA saklanmaz - sadece tarama sonuç özeti
 * (risk skoru, bulgular, severity counts).
 */
export function useScanHistory() {
  const [history, setHistory] = useState([])

  // İlk yüklemede localStorage'dan oku
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const parsed = JSON.parse(stored)
        if (Array.isArray(parsed)) {
          setHistory(parsed)
        }
      }
    } catch (err) {
      console.warn('Scan history could not be loaded:', err)
    }
  }, [])

  const addEntry = useCallback((scanResult, fileType) => {
    if (!scanResult || !scanResult.scan_id) return

    const newEntry = {
      scan_id: scanResult.scan_id,
      timestamp: Date.now(),
      file_type: fileType,
      risk_score: scanResult.risk_score,
      risk_level: scanResult.risk_level,
      total_findings: scanResult.summary?.total_findings || 0,
      severity_counts: scanResult.summary?.severity_counts || {
        CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0
      },
      // Tam sonuç snapshot'ı (kod hariç) - "Tekrar Aç" için
      result_snapshot: scanResult,
    }

    setHistory(prev => {
      // Aynı scan_id varsa override et, yoksa başa ekle
      const filtered = prev.filter(e => e.scan_id !== newEntry.scan_id)
      const updated = [newEntry, ...filtered].slice(0, MAX_ENTRIES)

      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch (err) {
        // QuotaExceededError olabilir
        console.warn('Scan history could not be saved:', err)
      }

      return updated
    })
  }, [])

  const removeEntry = useCallback((scanId) => {
    setHistory(prev => {
      const updated = prev.filter(e => e.scan_id !== scanId)
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch (err) {
        console.warn('Could not update history:', err)
      }
      return updated
    })
  }, [])

  const clearAll = useCallback(() => {
    setHistory([])
    try {
      localStorage.removeItem(STORAGE_KEY)
    } catch (err) {
      console.warn('Could not clear history:', err)
    }
  }, [])

  const getEntry = useCallback((scanId) => {
    return history.find(e => e.scan_id === scanId)
  }, [history])

  return { history, addEntry, removeEntry, clearAll, getEntry }
}
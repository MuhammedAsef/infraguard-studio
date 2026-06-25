"""
LLM Enricher Modülü

Knowledge base'de olmayan kurallar için OpenAI ile dinamik açıklama üretir.

Güvenlik katmanları:
1. CACHE: Aynı kural ID için bir kez sorulur, sonuç kalıcı cache'lenir
2. DAILY BUDGET: Günlük max LLM çağrısı (sunucu seviyesi)
3. IP RATE LIMIT: IP başına saatte max N yeni kural sorabilir
4. INPUT LIMIT: Max token bağırma engellenir

NOT: LLM çağrıları async olarak yapılmaz - tarama sonucu sonradan
zenginleştirilir, yoksa kullanıcı çok bekler.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from threading import Lock

from dotenv import load_dotenv

load_dotenv()

# Konfigürasyon
LLM_ENABLED = os.getenv("LLM_ENABLED", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_DAILY_BUDGET = int(os.getenv("LLM_DAILY_BUDGET", "100"))
LLM_PER_IP_HOURLY_LIMIT = int(os.getenv("LLM_PER_IP_HOURLY_LIMIT", "5"))
LLM_MAX_INPUT_TOKENS = int(os.getenv("LLM_MAX_INPUT_TOKENS", "500"))

# Cache dosyası (kalıcı, restart'ta korunur)
CACHE_DIR = Path(__file__).parent / "_cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "llm_enrichments.json"

# Rate limit state (in-memory, restart'ta sıfırlanır)
_daily_call_count = 0
_daily_reset_time = datetime.now() + timedelta(days=1)
_ip_call_history: dict[str, list[float]] = {}  # ip -> [timestamp, timestamp, ...]
_lock = Lock()


def _load_cache() -> dict:
    """Kalıcı cache'i yükle."""
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache: dict):
    """Cache'i diske kaydet."""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # Cache kaydedilemese de uygulamayı çökertme


def _check_daily_budget() -> bool:
    """Günlük bütçe içinde miyiz?"""
    global _daily_call_count, _daily_reset_time

    with _lock:
        now = datetime.now()
        # Gün geçtiyse sayacı sıfırla
        if now >= _daily_reset_time:
            _daily_call_count = 0
            _daily_reset_time = now + timedelta(days=1)

        return _daily_call_count < LLM_DAILY_BUDGET


def _increment_daily_count():
    """Günlük çağrı sayısını artır."""
    global _daily_call_count
    with _lock:
        _daily_call_count += 1


def _check_ip_rate_limit(client_ip: str) -> bool:
    """IP başına saatlik limit içinde miyiz?"""
    with _lock:
        now = time.time()
        one_hour_ago = now - 3600

        # Eski kayıtları temizle
        if client_ip in _ip_call_history:
            _ip_call_history[client_ip] = [
                t for t in _ip_call_history[client_ip] if t > one_hour_ago
            ]

        # Limit kontrol
        current_count = len(_ip_call_history.get(client_ip, []))
        return current_count < LLM_PER_IP_HOURLY_LIMIT


def _record_ip_call(client_ip: str):
    """IP çağrısını kaydet."""
    with _lock:
        if client_ip not in _ip_call_history:
            _ip_call_history[client_ip] = []
        _ip_call_history[client_ip].append(time.time())


def _call_openai(check_id: str, check_name: str, file_type: str, code_snippet: str) -> dict | None:
    """
    OpenAI'a istek at, Türkçe açıklama + severity + kategori üret.
    Hata durumunda None döner.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        # Input token limitini koruma için kod parçasını kısalt
        if code_snippet and len(code_snippet) > 1000:
            code_snippet = code_snippet[:1000] + "..."

        system_prompt = """Sen DevSecOps uzmanı bir güvenlik mühendisisin. IaC (Infrastructure as Code) güvenlik kurallarını Türkçe açıklayan asistansın.

Sana bir Checkov kural ID'si ve İngilizce başlığı verilecek. Senden istenen:
1. Türkçe başlık (kısa, max 80 karakter)
2. Türkçe detaylı açıklama (neden riskli, nasıl sömürülür, real-world örnek varsa onu da ekle - max 3 cümle)
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Kategori (örn: "Network Security", "Encryption", "Access Control", "Container Hardening", "Resource Management", "Best Practice")

Çıktıyı sadece JSON olarak ver, başka bir şey yazma. JSON format:
{
  "title_tr": "...",
  "explanation_tr": "...",
  "severity": "MEDIUM",
  "category": "..."
}"""

        user_prompt = f"""Dosya tipi: {file_type}
Kural ID: {check_id}
İngilizce başlık: {check_name}
Hatalı kod parçası: {code_snippet or "(yok)"}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=400,
            response_format={"type": "json_object"},
        )

        result_text = response.choices[0].message.content
        result = json.loads(result_text)

        # Doğrula
        required_keys = ["title_tr", "explanation_tr", "severity", "category"]
        if not all(k in result for k in required_keys):
            return None

        # Severity normalize et
        sev = result["severity"].upper()
        if sev not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            sev = "MEDIUM"
        result["severity"] = sev

        return result

    except Exception as e:
        print(f"[LLM] Hata: {e}")
        return None


def enrich_finding_with_llm(
    check_id: str,
    check_name: str,
    file_type: str,
    code_snippet: str = "",
    client_ip: str = "anonymous",
) -> dict | None:
    """
    Bilinmeyen bir kural için LLM ile zenginleştirme dene.

    Returns:
        Zenginleştirilmiş açıklama dict'i veya None (LLM kullanılamadıysa)
    """
    if not LLM_ENABLED or not OPENAI_API_KEY:
        return None

    # 1. Cache kontrolü
    cache = _load_cache()
    if check_id in cache:
        return cache[check_id]

    # 2. Daily budget kontrolü
    if not _check_daily_budget():
        return None

    # 3. IP rate limit kontrolü
    if not _check_ip_rate_limit(client_ip):
        return None

    # 4. LLM çağrısı
    result = _call_openai(check_id, check_name, file_type, code_snippet)

    if result is None:
        return None

    # Kayıt ve cache
    _increment_daily_count()
    _record_ip_call(client_ip)

    cache[check_id] = result
    _save_cache(cache)

    return result


def get_llm_stats() -> dict:
    """LLM kullanım istatistikleri (debug için)."""
    with _lock:
        return {
            "enabled": LLM_ENABLED,
            "daily_call_count": _daily_call_count,
            "daily_budget": LLM_DAILY_BUDGET,
            "daily_reset_at": _daily_reset_time.isoformat(),
            "ip_count": len(_ip_call_history),
            "cache_size": len(_load_cache()),
        }
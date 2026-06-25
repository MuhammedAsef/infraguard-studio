import asyncio

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from app.config import MAX_CODE_SIZE_BYTES, MAX_CONCURRENT_SCANS, FILE_TYPE_CONFIG
from app.scanners.checkov_scanner import run_checkov_scan, ScanError, ScanTimeoutError
from app.normalizer.unified_format import normalize_checkov_results

router = APIRouter()

# Concurrency limiti — aynı anda max 2 tarama
# Bu, VPS'in CPU/RAM'ini koruyor
_scan_semaphore = asyncio.Semaphore(MAX_CONCURRENT_SCANS)


class ScanRequest(BaseModel):
    """Frontend'den gelecek istek formatı"""
    code: str
    file_type: str = "dockerfile"
    lang: str = "tr"  # "tr" veya "en"

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        # Boş kod kabul etme
        if not v or not v.strip():
            raise ValueError("Kod boş olamaz")

        # Boyut kontrolü - çok büyük dosya atılmasın
        code_bytes = len(v.encode("utf-8"))
        if code_bytes > MAX_CODE_SIZE_BYTES:
            raise ValueError(
                f"Dosya boyutu çok büyük: {code_bytes} bytes "
                f"(max {MAX_CODE_SIZE_BYTES} bytes)"
            )

        # Null byte kontrolü (path traversal önlemi)
        if "\x00" in v:
            raise ValueError("Geçersiz karakter")

        return v

    @field_validator("file_type")
    @classmethod
    def validate_file_type(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in FILE_TYPE_CONFIG:
            allowed = ", ".join(FILE_TYPE_CONFIG.keys())
            raise ValueError(
                f"Desteklenmeyen dosya tipi: {v}. Desteklenenler: {allowed}"
            )
        return v

    @field_validator("lang")
    @classmethod
    def validate_lang(cls, v: str) -> str:
        if v not in ("tr", "en"):
            return "tr"  # Varsayılan Türkçe
        return v


class ScanResponse(BaseModel):
    """Frontend'e dönecek cevap formatı"""
    scan_id: str
    file_type: str
    findings: list
    summary: dict
    risk_score: int
    risk_level: str
    pipeline_snippets: dict


@router.post("/scan", response_model=ScanResponse)
async def scan_code(request: ScanRequest):
    """
    IaC dosyasını güvenlik açısından tara.

    Kullanıcının gönderdiği kodu geçici bir dosyaya yazar,
    Checkov ile tarar, sonuçları normalize edip döner.
    Kod sunucuda kalıcı olarak saklanmaz.
    """

    # Tüm slotlar doluysa hata dön (beklemek yerine)
    if _scan_semaphore.locked():
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Sunucu şu an yoğun. Lütfen birkaç saniye sonra tekrar deneyin.",
                "error_code": "RATE_LIMITED",
            },
        )

    async with _scan_semaphore:
        try:
            # Scanner'ı thread'e at (subprocess blocking olmasın)
            raw_scan = await asyncio.to_thread(
                run_checkov_scan, request.code, request.file_type
            )

             # Normalize et ve zenginleştir (fix engine için orijinal kod da lazım)
            result = normalize_checkov_results(
                raw_scan,
                original_code=request.code,
                lang=request.lang,
            )

            return ScanResponse(**result)

        except ScanTimeoutError:
            raise HTTPException(
                status_code=408,
                detail={
                    "error": "Tarama zaman aşımına uğradı. Daha küçük bir dosya deneyin.",
                    "error_code": "SCAN_TIMEOUT",
                },
            )

        except ScanError as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Tarama sırasında hata oluştu: {str(e)[:200]}",
                    "error_code": "SCAN_ERROR",
                },
            )

        except Exception as e:
            import traceback
            traceback.print_exc()  # Sunucu logunda görsek de
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Beklenmeyen bir hata oluştu",
                    "error_code": "INTERNAL_ERROR",
                },
            )
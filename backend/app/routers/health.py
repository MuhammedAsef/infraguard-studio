import subprocess
from fastapi import APIRouter

router = APIRouter()


def _get_checkov_version() -> str:
    """Yüklü Checkov versiyonunu döner."""
    try:
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "checkov.main", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unavailable"


@router.get("/health")
async def health_check():
    """Sağlık kontrolü - API çalışıyor mu?"""
    return {"status": "ok"}


@router.get("/version")
async def version_info():
    """Scanner versiyon bilgileri."""
    return {
        "api_version": "0.1.0",
        "scanners": {
            "checkov": _get_checkov_version(),
        },
    }
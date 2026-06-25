import json
import subprocess
import uuid
import shutil
from pathlib import Path

from app.config import SCAN_TIMEOUT_SECONDS, FILE_TYPE_CONFIG


class ScanError(Exception):
    """Tarama sırasında oluşan hatalar"""
    pass


class ScanTimeoutError(ScanError):
    """Tarama zaman aşımı"""
    pass


def run_checkov_scan(code: str, file_type: str) -> dict:
    """
    Checkov CLI'ı güvenli bir şekilde çalıştır.

    Güvenlik kararları:
    - Dosya adı kullanıcıdan ALINMAZ, sabit isim verilir
    - shell=False ile çalıştırılır (command injection önlemi)
    - Timeout uygulanır (kaynak tüketimi önlemi)
    - Temp dizin UUID ile izole edilir
    - Tarama bitince dizin silinir (her durumda)
    """

    if file_type not in FILE_TYPE_CONFIG:
        raise ScanError(f"Desteklenmeyen dosya tipi: {file_type}")

    config = FILE_TYPE_CONFIG[file_type]
    scan_id = str(uuid.uuid4())

    # Windows ve Linux'ta çalışsın diye tempfile kullanıyoruz
    import tempfile
    scan_dir = Path(tempfile.gettempdir()) / f"scan-{scan_id}"

    try:
        # 1. İzole dizin oluştur
        scan_dir.mkdir(parents=True, exist_ok=False)

        # 2. Kodu sabit isimle yaz (kullanıcı dosya adı YOK)
        file_path = scan_dir / config["filename"]
        file_path.write_text(code, encoding="utf-8")

        # 3. Checkov komutunu oluştur (allowlisted argümanlar)
        import sys
        cmd = [
            sys.executable,
            "-m", "checkov.main",
            "-f", str(file_path),
            "--output", "json",
            "--compact",
            "--quiet",
            "--download-external-modules", "false",
        ]

        # 4. Güvenli subprocess çalıştır
        result = subprocess.run(
            cmd,
            cwd=str(scan_dir),
            timeout=SCAN_TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
            shell=False,  # ÖNEMLİ: command injection önlemi
        )


        # 5. Checkov çıkış kodları:
        #    0 = tüm kontroller geçti
        #    1 = başarısız kontroller var (bu normal!)
        #    2 = hata
        if result.returncode == 2:
            raise ScanError(f"Checkov hata verdi: {result.stderr[:500]}")

        # 6. JSON parse et
        stdout = result.stdout.strip()
        if not stdout:
            return {
                "scan_id": scan_id,
                "scanner": "checkov",
                "file_type": file_type,
                "raw_results": None,
                "error": None,
            }

        # Checkov bazen list, bazen dict döner
        parsed = json.loads(stdout)
        if isinstance(parsed, list):
            # Birden fazla framework sonucu - bizim istediğimizi al
            raw_results = None
            for item in parsed:
                if item.get("check_type") == config["checkov_framework"]:
                    raw_results = item
                    break
            if raw_results is None and len(parsed) > 0:
                raw_results = parsed[0]
        else:
            raw_results = parsed

        return {
            "scan_id": scan_id,
            "scanner": "checkov",
            "file_type": file_type,
            "raw_results": raw_results,
            "error": None,
        }

    except subprocess.TimeoutExpired:
        raise ScanTimeoutError(
            f"Tarama {SCAN_TIMEOUT_SECONDS} saniye içinde tamamlanamadı"
        )

    except json.JSONDecodeError as e:
        raise ScanError(f"Scanner çıktısı parse edilemedi: {str(e)[:200]}")

    finally:
        # 7. Temp dizini HER DURUMDA sil (hata olsa bile)
        if scan_dir.exists():
            shutil.rmtree(scan_dir, ignore_errors=True)
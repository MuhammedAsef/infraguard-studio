"""
Multi-file scanner: ZIP dosyasını alır, içindeki IaC dosyalarını tipe göre tarar.

Güvenlik:
- Max zip boyutu: 10MB
- Max dosya sayısı: 50
- Zip slip koruması (path traversal)
- Sandbox dizinde extract, işlem sonrası silme
"""

import os
import uuid
import shutil
import zipfile
import tempfile

from app.config import FILE_TYPE_CONFIG, SEVERITY_WEIGHTS
from app.scanners.checkov_scanner import run_checkov_scan, ScanError
from app.normalizer.unified_format import normalize_checkov_results


# Limitler
MAX_ZIP_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
MAX_FILES_PER_ZIP = 50
MAX_FILE_SIZE_BYTES = 50 * 1024  # Tekil dosya 50KB


def detect_file_type(filepath: str) -> str | None:
    """
    Dosya yoluna göre IaC tipini tespit eder.
    None dönerse desteklenmeyen dosya tipi demektir, atlanır.
    """
    filename = os.path.basename(filepath).lower()

    # Dockerfile (Dockerfile, Dockerfile.dev, vb.)
    if filename == "dockerfile" or filename.startswith("dockerfile."):
        return "dockerfile"

    # Terraform
    if filename.endswith(".tf"):
        return "terraform"

    # Kubernetes YAML (her .yaml/.yml'yi k8s sayıyoruz; Checkov gereksiz bulgu üretmez)
    if filename.endswith(".yaml") or filename.endswith(".yml"):
        return "kubernetes"

    return None


def safe_extract_zip(zip_path: str, extract_dir: str) -> list[str]:
    """
    Zip dosyasını güvenli şekilde extract eder.
    Zip slip (path traversal) saldırılarına karşı koruma içerir.
    """
    extracted_files = []

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        if len(names) > MAX_FILES_PER_ZIP:
            raise ValueError(
                f"Zip içinde çok fazla dosya var ({len(names)}). "
                f"Maksimum {MAX_FILES_PER_ZIP} dosya kabul edilir."
            )

        for member in zf.infolist():
            # Klasörleri atla
            if member.is_dir():
                continue

            # Tekil dosya boyutu kontrolü (uncompressed)
            if member.file_size > MAX_FILE_SIZE_BYTES:
                continue

            # ZIP SLIP KORUMASI
            target_path = os.path.realpath(os.path.join(extract_dir, member.filename))
            extract_dir_real = os.path.realpath(extract_dir)

            if not target_path.startswith(extract_dir_real + os.sep) and target_path != extract_dir_real:
                raise ValueError(f"Zip slip saldırı tespiti: {member.filename}")

            zf.extract(member, extract_dir)
            extracted_files.append(target_path)

    return extracted_files


def scan_zip_file(zip_bytes: bytes, lang: str = "tr", client_ip: str = "anonymous") -> dict:
    """
    Zip dosyasını alır, IaC dosyalarını tipe göre tarar, sonuçları birleştirir.
    """
    # Zip boyutu kontrolü
    if len(zip_bytes) > MAX_ZIP_SIZE_BYTES:
        raise ValueError(
            f"Zip çok büyük ({len(zip_bytes) // 1024}KB). "
            f"Maksimum {MAX_ZIP_SIZE_BYTES // 1024 // 1024}MB kabul edilir."
        )

    scan_id = str(uuid.uuid4())
    temp_root = tempfile.mkdtemp(prefix=f"infraguard_multi_{scan_id}_")

    try:
        # Zip'i diske yaz
        zip_path = os.path.join(temp_root, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(zip_bytes)

        # Extract directory
        extract_dir = os.path.join(temp_root, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        # Güvenli extract
        try:
            extracted_files = safe_extract_zip(zip_path, extract_dir)
        except zipfile.BadZipFile:
            raise ValueError("Geçersiz veya bozuk zip dosyası.")

        # Dosyaları IaC tipine göre grupla
        files_by_type = {}
        for filepath in extracted_files:
            file_type = detect_file_type(filepath)
            if file_type is None:
                continue
            files_by_type.setdefault(file_type, []).append(filepath)

        # Hiç desteklenen dosya yoksa
        if not files_by_type:
            return {
                "scan_id": scan_id,
                "total_files_scanned": 0,
                "total_findings": 0,
                "summary": {
                    "total_findings": 0,
                    "severity_counts": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
                },
                "risk_score": 100,
                "risk_level": "LOW",
                "files": [],
                "message": "Zip içinde desteklenen IaC dosyası bulunamadı (Dockerfile, *.tf, *.yaml).",
            }

        # Her dosyayı tara
        per_file_results = []
        total_severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        total_findings = 0

        for file_type, paths in files_by_type.items():
            for filepath in paths:
                rel_path = os.path.relpath(filepath, extract_dir)

                try:
                    # Dosyayı oku
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # İçerik çok büyükse atla
                    if len(content.encode("utf-8")) > MAX_FILE_SIZE_BYTES:
                        continue

                    # Boş dosyaları atla
                    if not content.strip():
                        continue

                    # Tara (mevcut single-file scanner)
                    raw_scan = run_checkov_scan(content, file_type)
                    normalized = normalize_checkov_results(
                        raw_scan,
                        original_code=content,
                        lang=lang,
                        client_ip=client_ip,
                    )

                    per_file_results.append({
                        "file_path": rel_path,
                        "file_type": file_type,
                        "findings": normalized.get("findings", []),
                        "summary": normalized.get("summary", {}),
                        "risk_score": normalized.get("risk_score", 100),
                        "risk_level": normalized.get("risk_level", "LOW"),
                    })

                    # Toplam sayaçlara ekle
                    file_summary = normalized.get("summary", {})
                    file_counts = file_summary.get("severity_counts", {})
                    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                        total_severity_counts[sev] += file_counts.get(sev, 0)
                    total_findings += file_summary.get("total_findings", 0)

                except (ScanError, Exception) as e:
                    # Bir dosya tarayamadıysak diğerlerine devam et
                    per_file_results.append({
                        "file_path": rel_path,
                        "file_type": file_type,
                        "error": f"Tarama hatası: {str(e)[:150]}",
                        "findings": [],
                        "summary": {
                            "total_findings": 0,
                            "severity_counts": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
                        },
                        "risk_score": 100,
                        "risk_level": "LOW",
                    })

        # Genel risk skoru hesabı
        # Single-file'dakine benzer mantık ama daha basit
        # (her dosyanın passed_checks'i ayrı, multi'de bunu kümülatif yapmıyoruz)
        if total_findings == 0:
            risk_score = 100
        else:
            weighted_penalty = sum(
                total_severity_counts[sev] * SEVERITY_WEIGHTS.get(sev, 1)
                for sev in total_severity_counts
            )
            # Her dosya için max 100 puan; toplam dosya sayısı * 100 üzerinden normalize
            max_possible = max(1, len(per_file_results)) * 100
            risk_score = max(0, 100 - int((weighted_penalty / max_possible) * 100))

        if total_severity_counts["CRITICAL"] > 0:
            risk_level = "CRITICAL"
        elif total_severity_counts["HIGH"] > 0:
            risk_level = "HIGH"
        elif total_severity_counts["MEDIUM"] > 0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # En riskli dosyalar üstte (bulgu sayısına göre)
        per_file_results.sort(
            key=lambda x: -x.get("summary", {}).get("total_findings", 0)
        )

        return {
            "scan_id": scan_id,
            "total_files_scanned": len(per_file_results),
            "total_findings": total_findings,
            "summary": {
                "total_findings": total_findings,
                "severity_counts": total_severity_counts,
            },
            "risk_score": risk_score,
            "risk_level": risk_level,
            "files": per_file_results,
        }

    finally:
        # Her durumda temizle
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root, ignore_errors=True)
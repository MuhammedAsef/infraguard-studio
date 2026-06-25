from app.knowledge_base import DOCKERFILE_RULES, FALLBACK_RULE
from app.config import SEVERITY_WEIGHTS


def normalize_checkov_results(raw_scan: dict, lang: str = "tr") -> dict:
    """
    Checkov'un ham JSON çıktısını, açıklamalı ve skorlanmış
    birleşik formata dönüştür.

    Bu katman projeyi "scanner wrapper"dan ayıran şey:
    - Her bulguya severity atanır (Checkov bazen severity vermez)
    - Her bulguya Türkçe/İngilizce açıklama eklenir
    - Risk skoru hesaplanır
    - Bulguların konumu (satır) eklenir
    """

    raw_results = raw_scan.get("raw_results")
    scan_id = raw_scan.get("scan_id", "")
    file_type = raw_scan.get("file_type", "unknown")

    # Sonuç yoksa veya hata varsa
    if not raw_results or not raw_results.get("results"):
        return {
            "scan_id": scan_id,
            "file_type": file_type,
            "findings": [],
            "summary": _empty_summary(),
            "risk_score": 100,  # Bulgu yok = tam puan
            "risk_level": "LOW",
        }

    results = raw_results["results"]
    failed_checks = results.get("failed_checks", [])
    passed_checks = results.get("passed_checks", [])

    # Her başarısız kontrolü normalize et
    findings = []
    for check in failed_checks:
        finding = _normalize_single_finding(check, file_type, lang)
        findings.append(finding)

    # Severity'ye göre sırala: CRITICAL > HIGH > MEDIUM > LOW
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings.sort(key=lambda f: severity_order.get(f["severity"], 4))

    # Risk skoru hesapla
    risk_score = _calculate_risk_score(findings, len(passed_checks))
    risk_level = _score_to_level(risk_score)

    # Özet
    summary = _build_summary(findings, len(passed_checks))

    return {
        "scan_id": scan_id,
        "file_type": file_type,
        "findings": findings,
        "summary": summary,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


def _normalize_single_finding(check: dict, file_type: str, lang: str) -> dict:
    """Tek bir Checkov bulgusunu zenginleştirilmiş formata dönüştür."""

    check_id = check.get("check_id", "UNKNOWN")

    # Knowledge base'den açıklama ve severity al
    if file_type == "dockerfile":
        rule_info = DOCKERFILE_RULES.get(check_id, FALLBACK_RULE)
    else:
        rule_info = FALLBACK_RULE

    # Severity: önce Checkov'un verdiğini al, yoksa bizimkini kullan
    severity = check.get("severity") or rule_info["severity"]
    severity = severity.upper() if severity else rule_info["severity"]

    # Başlık: knowledge base varsa onu, yoksa Checkov'unkini kullan
    title_key = f"title_{lang}"
    title = rule_info.get(title_key) or check.get("check_name", check_id)

    # Açıklama
    explanation_key = f"explanation_{lang}"
    explanation = rule_info.get(explanation_key, FALLBACK_RULE[explanation_key])

    # Satır bilgisi
    line_range = check.get("file_line_range", [0, 0])

    # Hatalı kod satırı (Checkov'un bulduğu)
    code_content = None
    check_result = check.get("check_result", {})
    results_config = check_result.get("results_configuration", [])
    if results_config and len(results_config) > 0:
        code_content = results_config[0].get("content", "").strip()

    return {
        "check_id": check_id,
        "severity": severity,
        "category": rule_info.get("category", "Security"),
        "title": title,
        "explanation": explanation,
        "line_start": line_range[0] if len(line_range) > 0 else 0,
        "line_end": line_range[1] if len(line_range) > 1 else 0,
        "code_snippet": code_content,
        "references": rule_info.get("references", []),
        "checkov_name": check.get("check_name", ""),
    }


def _calculate_risk_score(findings: list, passed_count: int) -> int:
    """
    0-100 arası risk skoru hesapla.
    100 = güvenli, 0 = çok riskli.

    Formül: 100 - (ağırlıklı bulgu puanı / toplam kontrol * 100)
    """
    if not findings and passed_count == 0:
        return 100

    total_checks = len(findings) + passed_count
    if total_checks == 0:
        return 100

    weighted_penalty = sum(
        SEVERITY_WEIGHTS.get(f["severity"], 1)
        for f in findings
    )

    # Maksimum penaltı: tüm kontroller CRITICAL olsa
    max_penalty = total_checks * SEVERITY_WEIGHTS["CRITICAL"]

    # Normalize et: 0-100 arası
    score = max(0, 100 - int((weighted_penalty / max_penalty) * 100))
    return score


def _score_to_level(score: int) -> str:
    """Risk skorunu seviyeye çevir."""
    if score >= 80:
        return "LOW"
    elif score >= 60:
        return "MEDIUM"
    elif score >= 40:
        return "HIGH"
    else:
        return "CRITICAL"


def _build_summary(findings: list, passed_count: int) -> dict:
    """Bulgu özeti."""
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        sev = f["severity"]
        if sev in severity_counts:
            severity_counts[sev] += 1

    return {
        "total_findings": len(findings),
        "passed_checks": passed_count,
        "severity_counts": severity_counts,
    }


def _empty_summary() -> dict:
    return {
        "total_findings": 0,
        "passed_checks": 0,
        "severity_counts": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
    }
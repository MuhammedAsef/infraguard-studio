"""
PDF Rapor Üretici

Tarama sonucundan kurumsal görünümlü bir PDF raporu üretir.
Kullanıcı bu raporu yöneticilerine sunmak için indirebilir.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


# Severity'ye göre renkler
SEVERITY_COLORS = {
    "CRITICAL": colors.HexColor("#dc2626"),
    "HIGH": colors.HexColor("#ea580c"),
    "MEDIUM": colors.HexColor("#ca8a04"),
    "LOW": colors.HexColor("#2563eb"),
}

SEVERITY_LABELS_TR = {
    "CRITICAL": "KRITIK",
    "HIGH": "YUKSEK",
    "MEDIUM": "ORTA",
    "LOW": "DUSUK",
}

FILE_TYPE_LABELS = {
    "dockerfile": "Dockerfile",
    "kubernetes": "Kubernetes YAML",
    "terraform": "Terraform",
}


def _safe_text(text: str, max_len: int = None) -> str:
    """ReportLab'a güvenli hale getir (HTML escape + Türkçe karakterleri ASCII'ye çevirme yok)."""
    if not text:
        return ""
    # HTML escape karakterleri
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if max_len and len(text) > max_len:
        text = text[:max_len] + "..."
    return text


def generate_pdf_report(scan_result: dict) -> bytes:
    """
    Tarama sonucundan PDF üret, bytes olarak dön.
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    # Özel stiller
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#0891b2"),
        spaceAfter=10,
        alignment=TA_CENTER,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#64748b"),
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    section_title_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=8,
        spaceBefore=12,
        borderPadding=4,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
        leading=14,
    )

    small_meta_style = ParagraphStyle(
        "SmallMeta",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#64748b"),
    )

    elements = []

    # === BAŞLIK ===
    elements.append(Paragraph("InfraGuard Studio", title_style))
    elements.append(Paragraph("IaC Guvenlik Tarama Raporu", subtitle_style))

    # Meta bilgi (tarih, dosya tipi, scan ID)
    file_type_label = FILE_TYPE_LABELS.get(
        scan_result.get("file_type", "unknown"), scan_result.get("file_type", "unknown")
    )
    meta_text = (
        f"<b>Tarih:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')} &nbsp;&nbsp;"
        f"<b>Dosya Tipi:</b> {file_type_label} &nbsp;&nbsp;"
        f"<b>Tarama ID:</b> {scan_result.get('scan_id', 'N/A')[:8]}"
    )
    elements.append(Paragraph(meta_text, small_meta_style))
    elements.append(Spacer(1, 20))

    # === ÖZET / RISK SKORU ===
    elements.append(Paragraph("Genel Ozet", section_title_style))

    risk_score = scan_result.get("risk_score", 100)
    risk_level = scan_result.get("risk_level", "LOW")
    risk_label_tr = SEVERITY_LABELS_TR.get(risk_level, risk_level)
    summary = scan_result.get("summary", {})
    severity_counts = summary.get("severity_counts", {})

    # Skor + risk seviyesi tablosu
    score_color = SEVERITY_COLORS.get(risk_level, colors.HexColor("#64748b"))
    score_data = [
        [
            Paragraph(f"<font size='28' color='{score_color.hexval()}'><b>{risk_score}/100</b></font>", body_style),
            Paragraph(f"<font size='14' color='{score_color.hexval()}'><b>{risk_label_tr} RISK</b></font><br/>"
                      f"<font size='9' color='#64748b'>{summary.get('total_findings', 0)} bulgu tespit edildi</font>", body_style),
        ]
    ]
    score_table = Table(score_data, colWidths=[5 * cm, 11 * cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 12))

    # Severity dağılımı tablosu
    severity_data = [
        [
            Paragraph(f"<b>{severity_counts.get('CRITICAL', 0)}</b>", body_style),
            Paragraph(f"<b>{severity_counts.get('HIGH', 0)}</b>", body_style),
            Paragraph(f"<b>{severity_counts.get('MEDIUM', 0)}</b>", body_style),
            Paragraph(f"<b>{severity_counts.get('LOW', 0)}</b>", body_style),
        ],
        [
            Paragraph("<font color='#dc2626'>Kritik</font>", small_meta_style),
            Paragraph("<font color='#ea580c'>Yuksek</font>", small_meta_style),
            Paragraph("<font color='#ca8a04'>Orta</font>", small_meta_style),
            Paragraph("<font color='#2563eb'>Dusuk</font>", small_meta_style),
        ],
    ]
    severity_table = Table(severity_data, colWidths=[4 * cm, 4 * cm, 4 * cm, 4 * cm])
    severity_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(severity_table)
    elements.append(Spacer(1, 20))

    # === BULGULAR ===
    findings = scan_result.get("findings", [])

    if not findings:
        elements.append(Paragraph("Guvenlik Bulgulari", section_title_style))
        elements.append(Paragraph(
            "<font color='#16a34a'><b>Bu dosyada guvenlik sorunu bulunamadi.</b></font> "
            "Temel guvenlik kontrollerini gecti.",
            body_style,
        ))
    else:
        elements.append(Paragraph(f"Bulgular ({len(findings)})", section_title_style))

        for i, finding in enumerate(findings, 1):
            sev = finding.get("severity", "MEDIUM")
            sev_color = SEVERITY_COLORS.get(sev, colors.HexColor("#64748b"))
            sev_label = SEVERITY_LABELS_TR.get(sev, sev)

            ai_badge = ""
            if finding.get("enriched_by_llm"):
                ai_badge = " <font color='#9333ea'><b>[AI]</b></font>"

            # Bulgu kartı
            finding_elements = []

            # Başlık satırı
            header = (
                f"<font color='{sev_color.hexval()}'><b>[{sev_label}]</b></font> "
                f"<font color='#64748b' size='8'>{_safe_text(finding.get('check_id', ''))}</font>"
                f"{ai_badge} "
                f"<font color='#64748b' size='8'>- Satir {finding.get('line_start', 0)}</font>"
            )
            finding_elements.append(Paragraph(header, body_style))

            # Başlık (Türkçe)
            title = _safe_text(finding.get("title", ""), 200)
            finding_elements.append(Paragraph(f"<b>{title}</b>", body_style))

            # Açıklama
            explanation = _safe_text(finding.get("explanation", ""), 500)
            finding_elements.append(Paragraph(explanation, body_style))

            # Kategori
            category = _safe_text(finding.get("category", ""))
            finding_elements.append(Paragraph(
                f"<font size='8' color='#64748b'><b>Kategori:</b> {category}</font>",
                small_meta_style,
            ))

            # Hatalı kod parçası varsa
            code_snippet = finding.get("code_snippet")
            if code_snippet:
                finding_elements.append(Paragraph(
                    f"<font size='8' color='#dc2626'><b>Kod:</b> <font face='Courier'>{_safe_text(code_snippet, 100)}</font></font>",
                    small_meta_style,
                ))

            finding_elements.append(Spacer(1, 12))

            # Hepsini bir arada tut (sayfa başlangıcında kırılmasın)
            elements.append(KeepTogether(finding_elements))

    # === FOOTER ===
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "<font size='8' color='#94a3b8'>"
        "Bu rapor InfraGuard Studio tarafindan otomatik olarak uretilmistir. "
        "Bulgular Checkov 3.x ve isteğe bağli olarak GPT-4o-mini ile uretilmistir."
        "</font>",
        small_meta_style,
    ))

    # PDF'i oluştur
    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()
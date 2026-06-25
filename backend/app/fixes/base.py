"""
Fix engine temel yapısı.

Her dosya tipi için ayrı fix modülü olacak (dockerfile_fixes.py,
kubernetes_fixes.py, terraform_fixes.py).

Her modül:
- FIX_FUNCTIONS sözlüğü export eder: { check_id: fix_function }
- Her fix_function şu imzaya sahip: (original_code: str, finding: dict) -> str | None
- None döndürürse "düzeltme üretilemedi" demektir
"""


def get_fix_for_finding(file_type: str, check_id: str, original_code: str, finding: dict) -> str | None:
    """
    Verilen bulgu için düzeltilmiş kodu üret.

    Args:
        file_type: 'dockerfile', 'kubernetes', 'terraform'
        check_id: Checkov check ID (örn: 'CKV_DOCKER_8')
        original_code: Kullanıcının orijinal kodu
        finding: Normalize edilmiş bulgu objesi

    Returns:
        Düzeltilmiş kod (string) veya None (düzeltme yok)
    """

    # Modülü dinamik import et
    try:
        if file_type == "dockerfile":
            from app.fixes import dockerfile_fixes as fix_module
        elif file_type == "kubernetes":
            from app.fixes import kubernetes_fixes as fix_module
        elif file_type == "terraform":
            from app.fixes import terraform_fixes as fix_module
        else:
            return None
    except ImportError:
        return None

    fix_func = fix_module.FIX_FUNCTIONS.get(check_id)
    if not fix_func:
        return None

    try:
        return fix_func(original_code, finding)
    except Exception:
        # Fix sırasında hata olursa sessizce None dön (kullanıcı orijinal kodu görür)
        return None
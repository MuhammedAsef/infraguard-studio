"""
Kubernetes YAML için fix fonksiyonları.

NOT: YAML değiştirmek Dockerfile'dan daha zor çünkü indentation kritik.
Bu yüzden sadece en güvenli ve net düzeltmeleri yapıyoruz.
Karmaşık structural değişikliklerden kaçınıyoruz.
"""

import re


def fix_privileged_container(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_16: Privileged container kullanılıyor.

    Çözüm: privileged: true → privileged: false
    """
    if "privileged:" not in original_code.lower():
        return None

    # privileged: true → privileged: false
    fixed = re.sub(
        r"(privileged\s*:\s*)true",
        r"\1false",
        original_code,
        flags=re.IGNORECASE,
    )

    if fixed == original_code:
        return None

    return fixed


def fix_privilege_escalation(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_17: Privilege escalation engellenmemiş.

    Çözüm: allowPrivilegeEscalation: true → false
    Yoksa: securityContext altına ekle.
    """
    # allowPrivilegeEscalation: true varsa false yap
    if re.search(r"allowPrivilegeEscalation\s*:\s*true", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(allowPrivilegeEscalation\s*:\s*)true",
            r"\1false",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


def fix_run_as_root(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_20: Container root olarak çalışıyor.

    Çözüm: runAsUser: 0 → runAsUser: 1000
    Veya: runAsNonRoot: false → true
    """
    fixed = original_code
    changed = False

    # runAsUser: 0 → runAsUser: 1000
    if re.search(r"runAsUser\s*:\s*0\b", fixed):
        fixed = re.sub(
            r"(runAsUser\s*:\s*)0\b",
            r"\g<1>1000",
            fixed,
        )
        changed = True

    # runAsNonRoot: false → true
    if re.search(r"runAsNonRoot\s*:\s*false", fixed, re.IGNORECASE):
        fixed = re.sub(
            r"(runAsNonRoot\s*:\s*)false",
            r"\1true",
            fixed,
            flags=re.IGNORECASE,
        )
        changed = True

    return fixed if changed else None


def fix_latest_image(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_14: Image tag 'latest' kullanılıyor veya tanımlanmamış.

    Çözüm: image: app:latest → image: app:1.0.0 (kullanıcı kendisi güncellesin)
    """
    fixed = original_code
    changed = False

    # image: name:latest → image: name:VERSION
    matches = re.findall(r"image\s*:\s*([^\s:]+):latest", fixed, re.IGNORECASE)
    if matches:
        # Yaygın image'lar için akıllı öneriler
        version_suggestions = {
            "node": "18-alpine",
            "python": "3.12-slim",
            "nginx": "1.27-alpine",
            "ubuntu": "22.04",
            "alpine": "3.20",
            "redis": "7-alpine",
            "postgres": "16-alpine",
        }

        for image_name in matches:
            base = image_name.split("/")[-1].lower()
            suggested = version_suggestions.get(base, "VERSION")
            pattern = rf"(image\s*:\s*{re.escape(image_name)}):latest"
            replacement = rf"\1:{suggested}"
            fixed = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)
            changed = True

    return fixed if changed else None


def fix_default_namespace(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_21: Default namespace kullanılıyor.

    Çözüm: namespace: default → namespace: production
    Veya: namespace satırı yoksa metadata altına ekle (DİKKAT: yapılması zor)
    """
    # Mevcut "namespace: default" satırını değiştir
    if re.search(r"namespace\s*:\s*default\b", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(namespace\s*:\s*)default\b",
            r"\1production",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


# Check ID → Fix function mapping
FIX_FUNCTIONS = {
    "CKV_K8S_14": fix_latest_image,
    "CKV_K8S_16": fix_privileged_container,
    "CKV_K8S_20": fix_privilege_escalation,  # allowPrivilegeEscalation - CKV_K8S_20
    "CKV_K8S_23": fix_run_as_root,            # runAsNonRoot/runAsUser - CKV_K8S_23
    "CKV_K8S_21": fix_default_namespace,
}
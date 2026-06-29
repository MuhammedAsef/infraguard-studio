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

def fix_host_namespaces(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_17/18/19: hostPID, hostIPC, hostNetwork true.

    Çözüm: true → false
    """
    fixed = original_code
    changed = False

    for field in ["hostPID", "hostIPC", "hostNetwork"]:
        pattern = rf"({field}\s*:\s*)true"
        if re.search(pattern, fixed, re.IGNORECASE):
            fixed = re.sub(pattern, r"\1false", fixed, flags=re.IGNORECASE)
            changed = True

    return fixed if changed else None


def fix_read_only_root_fs(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_22: Read-only root filesystem kullanılmıyor.

    Çözüm: readOnlyRootFilesystem: false → true
    Veya yoksa: dokunma (structural değişiklik gerekir).
    """
    if re.search(r"readOnlyRootFilesystem\s*:\s*false", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(readOnlyRootFilesystem\s*:\s*)false",
            r"\1true",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


def fix_image_pull_policy(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_15: imagePullPolicy 'Always' olmalı.

    Çözüm: imagePullPolicy: IfNotPresent/Never → Always
    """
    fixed = original_code
    changed = False

    for old_value in ["IfNotPresent", "Never"]:
        pattern = rf"(imagePullPolicy\s*:\s*){old_value}\b"
        if re.search(pattern, fixed):
            fixed = re.sub(pattern, r"\1Always", fixed)
            changed = True

    return fixed if changed else None


def fix_automount_service_account(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_38/42: automountServiceAccountToken default'da true.

    Çözüm: automountServiceAccountToken: true → false
    """
    if re.search(r"automountServiceAccountToken\s*:\s*true", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(automountServiceAccountToken\s*:\s*)true",
            r"\1false",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


def fix_host_port(original_code: str, finding: dict) -> str | None:
    """
    CKV_K8S_26: hostPort kullanılmamalı.

    Çözüm: hostPort satırını kaldır (containerPort kalır).
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    for line in lines:
        if re.match(r"^\s*hostPort\s*:\s*\d+\s*$", line):
            # Satırı atla
            changed = True
            continue
        fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None

# Check ID → Fix function mapping
FIX_FUNCTIONS = {
    "CKV_K8S_14": fix_latest_image,                  # latest image tag
    "CKV_K8S_15": fix_image_pull_policy,             # imagePullPolicy Always
    "CKV_K8S_16": fix_privileged_container,          # privileged: true
    "CKV_K8S_17": fix_host_namespaces,               # hostPID
    "CKV_K8S_18": fix_host_namespaces,               # hostIPC
    "CKV_K8S_19": fix_host_namespaces,               # hostNetwork
    "CKV_K8S_20": fix_privilege_escalation,          # allowPrivilegeEscalation
    "CKV_K8S_21": fix_default_namespace,             # default namespace
    "CKV_K8S_22": fix_read_only_root_fs,             # readOnlyRootFilesystem
    "CKV_K8S_23": fix_run_as_root,                   # runAsNonRoot/runAsUser
    "CKV_K8S_26": fix_host_port,                     # hostPort
    "CKV_K8S_38": fix_automount_service_account,     # automountServiceAccountToken
    "CKV_K8S_42": fix_automount_service_account,     # automountServiceAccountToken (alternative)
}
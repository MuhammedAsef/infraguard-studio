"""
Dockerfile için fix fonksiyonları.

Her fonksiyon (original_code, finding) alır, düzeltilmiş kod döner.
Üretemezse None döner.
"""

import re


def fix_user_root(original_code: str, finding: dict) -> str | None:
    """
    CKV_DOCKER_3: USER eksik (container root çalışıyor).
    CKV_DOCKER_8: Son USER root olarak ayarlanmış.

    Çözüm:
    - Eğer "USER root" varsa → non-root user ile değiştir
    - Eğer hiç USER yoksa → CMD/ENTRYPOINT'ten önce non-root user ekle
    """
    lines = original_code.split("\n")

    # 1. Önce "USER root" var mı kontrol et
    user_root_found = False
    fixed_lines = []
    for line in lines:
        stripped = line.strip().upper()
        if stripped == "USER ROOT" or stripped.startswith("USER ROOT "):
            user_root_found = True
            indent = line[: len(line) - len(line.lstrip())]
            fixed_lines.append(f"{indent}# Non-root kullanıcı oluştur ve ona geç")
            fixed_lines.append(f"{indent}RUN addgroup -S appgroup && adduser -S appuser -G appgroup")
            fixed_lines.append(f"{indent}USER appuser")
        else:
            fixed_lines.append(line)

    if user_root_found:
        return "\n".join(fixed_lines)

    # 2. Hiç USER yoksa, CMD/ENTRYPOINT'ten önce ekle (CKV_DOCKER_3 senaryosu)
    has_any_user = any(
        line.strip().upper().startswith("USER ")
        for line in lines
    )

    if has_any_user:
        return None  # USER var ama root değil, başka durum

    # USER hiç yok, ekleyelim
    fixed_lines = []
    user_added = False
    for line in lines:
        stripped_upper = line.strip().upper()
        if not user_added and (
            stripped_upper.startswith("CMD ") or
            stripped_upper.startswith("CMD[") or
            stripped_upper.startswith("ENTRYPOINT ") or
            stripped_upper.startswith("ENTRYPOINT[")
        ):
            indent = line[: len(line) - len(line.lstrip())]
            fixed_lines.append(f"{indent}# Non-root kullanıcı oluştur ve ona geç")
            fixed_lines.append(f"{indent}RUN addgroup -S appgroup && adduser -S appuser -G appgroup")
            fixed_lines.append(f"{indent}USER appuser")
            fixed_lines.append("")
            user_added = True
        fixed_lines.append(line)

    if not user_added:
        # CMD/ENTRYPOINT yok, sonuna ekle
        fixed_lines.append("")
        fixed_lines.append("RUN addgroup -S appgroup && adduser -S appuser -G appgroup")
        fixed_lines.append("USER appuser")

    return "\n".join(fixed_lines)


def fix_latest_tag(original_code: str, finding: dict) -> str | None:
    """
    CKV_DOCKER_7: Base image 'latest' etiketi kullanıyor.

    Çözüm: latest yerine spesifik versiyon kullan (yorum olarak öner).
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    for line in lines:
        # FROM ...latest pattern'i
        match = re.match(r"^(\s*FROM\s+)([^\s:]+):latest(.*)", line, re.IGNORECASE)
        if match:
            prefix, image, suffix = match.groups()
            # 'latest' yerine yorum + spesifik versiyon önerisi
            # Yaygın image'lar için akıllı öneriler
            version_suggestions = {
                "node": "18-alpine",
                "python": "3.12-slim",
                "nginx": "1.27-alpine",
                "ubuntu": "22.04",
                "alpine": "3.20",
                "debian": "12-slim",
                "redis": "7-alpine",
                "postgres": "16-alpine",
                "mysql": "8.0",
            }
            suggested = version_suggestions.get(image.lower(), "VERSION")
            fixed_lines.append(f"{prefix}{image}:{suggested}{suffix}")
            changed = True
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None


def fix_missing_healthcheck(original_code: str, finding: dict) -> str | None:
    """
    CKV_DOCKER_2: HEALTHCHECK talimatı eksik.

    Çözüm: Dosyaya HEALTHCHECK ekle (CMD satırından önce).
    """
    if "HEALTHCHECK" in original_code.upper():
        return None  # Zaten var

    lines = original_code.split("\n")
    fixed_lines = []
    healthcheck_added = False

    # CMD veya ENTRYPOINT satırı bul, önüne HEALTHCHECK ekle
    for i, line in enumerate(lines):
        stripped_upper = line.strip().upper()
        if not healthcheck_added and (
            stripped_upper.startswith("CMD ") or
            stripped_upper.startswith("CMD[") or
            stripped_upper.startswith("ENTRYPOINT ") or
            stripped_upper.startswith("ENTRYPOINT[")
        ):
            fixed_lines.append("")
            fixed_lines.append("# Container sağlık kontrolü")
            fixed_lines.append("HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\")
            fixed_lines.append("  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1")
            fixed_lines.append("")
            healthcheck_added = True
        fixed_lines.append(line)

    if not healthcheck_added:
        # CMD/ENTRYPOINT bulunamadıysa sonuna ekle
        fixed_lines.append("")
        fixed_lines.append("HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\")
        fixed_lines.append("  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1")

    return "\n".join(fixed_lines)


def fix_add_to_copy(original_code: str, finding: dict) -> str | None:
    """
    CKV_DOCKER_1: ADD yerine COPY kullanılmalı.

    Çözüm: Yerel dosya kopyalayan ADD'leri COPY'ye çevir.
    Uzak URL veya .tar ADD'lerini değiştirme (farklı davranış var).
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    for line in lines:
        # ADD ile başlayan satırı yakala
        match = re.match(r"^(\s*)ADD(\s+.*)", line)
        if match:
            indent, rest = match.groups()
            # URL veya tar dosyası ise dokunma
            if "http://" in rest or "https://" in rest or ".tar" in rest.lower():
                fixed_lines.append(line)
            else:
                fixed_lines.append(f"{indent}COPY{rest}")
                changed = True
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None


def fix_ssh_port_exposed(original_code: str, finding: dict) -> str | None:
    """
    EXPOSE 22 (SSH portu) gibi tehlikeli portları kaldır.
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    dangerous_ports = {"22", "3389", "23"}  # SSH, RDP, Telnet

    for line in lines:
        match = re.match(r"^(\s*EXPOSE\s+)(.+)$", line, re.IGNORECASE)
        if match:
            prefix, ports_str = match.groups()
            # Portları split et, tehlikelileri filtrele
            ports = ports_str.split()
            safe_ports = [p for p in ports if p not in dangerous_ports]
            if len(safe_ports) != len(ports):
                changed = True
                if safe_ports:
                    fixed_lines.append(f"{prefix}{' '.join(safe_ports)}")
                else:
                    # Hiç güvenli port kalmadıysa satırı tamamen kaldır
                    fixed_lines.append("# EXPOSE satırı kaldırıldı - sadece SSH/RDP gibi yönetim portları içeriyordu")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None

def fix_sudo_usage(original_code: str, finding: dict) -> str | None:
    """
    CKV2_DOCKER_1: sudo kullanımı.

    Çözüm: sudo komutlarını kaldır (USER ile zaten doğru kullanıcı set ediliyorsa).
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    for line in lines:
        # RUN sudo ... → RUN ...
        match = re.match(r"^(\s*RUN\s+)sudo\s+(.+)$", line)
        if match:
            prefix, rest = match.groups()
            fixed_lines.append(f"{prefix}{rest}")
            changed = True
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None


def fix_curl_insecure(original_code: str, finding: dict) -> str | None:
    """
    CKV2_DOCKER_2: curl -k veya --insecure flag'i ile sertifika doğrulaması atlanıyor.

    Çözüm: -k ve --insecure flag'lerini kaldır.
    """
    if " -k " not in original_code and " --insecure " not in original_code and \
       " -k\n" not in original_code and " --insecure\n" not in original_code:
        return None

    fixed = re.sub(r"(\bcurl\b[^\n]*?)\s+-k\b", r"\1", original_code)
    fixed = re.sub(r"(\bcurl\b[^\n]*?)\s+--insecure\b", r"\1", fixed)

    return fixed if fixed != original_code else None


def fix_wget_insecure(original_code: str, finding: dict) -> str | None:
    """
    CKV2_DOCKER_3: wget --no-check-certificate kullanılıyor.

    Çözüm: --no-check-certificate flag'ini kaldır.
    """
    if "--no-check-certificate" not in original_code:
        return None

    fixed = re.sub(r"(\bwget\b[^\n]*?)\s+--no-check-certificate\b", r"\1", original_code)

    return fixed if fixed != original_code else None


def fix_apt_to_apt_get(original_code: str, finding: dict) -> str | None:
    """
    CKV_DOCKER_9: apt yerine apt-get kullanılmalı.

    Çözüm: 'apt install' → 'apt-get install', 'apt update' → 'apt-get update' vb.
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    for line in lines:
        # 'apt' başına/sonuna boşluk olan komutu yakala (ama 'apt-get' veya 'apt-cache' etkilenmesin)
        new_line = re.sub(
            r"(\bRUN\b[^\n]*?\s+)apt(\s+)(install|update|upgrade|remove|purge|autoremove)",
            r"\1apt-get\2\3",
            line
        )
        if new_line != line:
            fixed_lines.append(new_line)
            changed = True
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None


def fix_pip_no_cache(original_code: str, finding: dict) -> str | None:
    """
    CKV_DOCKER_15: pip install --no-cache-dir kullanılmalı.

    Çözüm: 'pip install' komutlarına --no-cache-dir ekle (yoksa).
    """
    if "--no-cache-dir" in original_code:
        return None  # Zaten var

    # pip install veya pip3 install pattern
    pattern = re.compile(r"(\bpip3?\s+install\b)(?!\s+--no-cache-dir)")
    if not pattern.search(original_code):
        return None

    fixed = pattern.sub(r"\1 --no-cache-dir", original_code)

    return fixed if fixed != original_code else None

# Check ID → Fix function mapping
FIX_FUNCTIONS = {
    "CKV_DOCKER_1": fix_ssh_port_exposed,      # SSH portu (22) açık
    "CKV_DOCKER_2": fix_missing_healthcheck,   # HEALTHCHECK eksik
    "CKV_DOCKER_3": fix_user_root,              # USER yok / root çalışıyor
    "CKV_DOCKER_4": fix_add_to_copy,            # ADD yerine COPY
    "CKV_DOCKER_7": fix_latest_tag,             # latest tag
    "CKV_DOCKER_8": fix_user_root,              # son USER root
    "CKV_DOCKER_9": fix_apt_to_apt_get,         # apt yerine apt-get
    "CKV_DOCKER_15": fix_pip_no_cache,          # pip --no-cache-dir
    "CKV2_DOCKER_1": fix_sudo_usage,            # sudo kullanımı
    "CKV2_DOCKER_2": fix_curl_insecure,         # curl -k
    "CKV2_DOCKER_3": fix_wget_insecure,         # wget --no-check-certificate
}
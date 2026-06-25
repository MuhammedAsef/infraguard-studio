"""
Terraform (HCL) için fix fonksiyonları.

HCL syntax'ı YAML kadar indentation-sensitive değil ama
yapısal değişiklikler hala karmaşık. En net değer değişikliklerini yapıyoruz.
"""

import re


def fix_public_s3_bucket(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_20: S3 bucket public erişime açık.

    Çözüm: acl = "public-read" → acl = "private"
    """
    public_acls = ["public-read", "public-read-write", "authenticated-read"]
    fixed = original_code
    changed = False

    for acl in public_acls:
        pattern = rf'(acl\s*=\s*)"{re.escape(acl)}"'
        if re.search(pattern, fixed):
            fixed = re.sub(pattern, r'\1"private"', fixed)
            changed = True

    return fixed if changed else None


def fix_ssh_open_to_world(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_24: Security group 22 portunu dünyaya açıyor.

    Çözüm: cidr_blocks = ["0.0.0.0/0"] olan SSH (port 22) bloğunda
    cidr'i VPC içi olarak değiştir.

    NOT: Bu fix tüm 0.0.0.0/0'ları değiştirmez, sadece port 22 olan ingress'i.
    """
    # SSH ingress bloğunu bulup cidr'i değiştirmek karmaşık (regex ile zor).
    # Pratik çözüm: tehlikeli portlu (22, 3389) ingress'lerin yanına yorum ekle
    # ve cidr_blocks değişikliği yap.

    # Basit ama net yaklaşım: tüm "cidr_blocks = ["0.0.0.0/0"]" satırlarının
    # öncesindeki birkaç satırda port 22 var mı bak, varsa değiştir.

    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    # Önce port bilgisini takip et
    for i, line in enumerate(lines):
        # cidr_blocks = ["0.0.0.0/0"] pattern
        if '"0.0.0.0/0"' in line and "cidr_blocks" in line:
            # Önceki 10 satıra bak, port 22 veya 3389 var mı?
            context_start = max(0, i - 10)
            context = "\n".join(lines[context_start:i])

            if re.search(r"(from_port|to_port)\s*=\s*(22|3389|23)\b", context):
                # Yorum + güvenli cidr önerisi
                indent = line[: len(line) - len(line.lstrip())]
                fixed_lines.append(f'{indent}# UYARI: SSH/RDP portu için 0.0.0.0/0 tehlikeli. VPC CIDR\'inizi kullanın.')
                fixed_lines.append(line.replace('"0.0.0.0/0"', '"10.0.0.0/8"'))
                changed = True
                continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None


def fix_unencrypted_rds(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_16: RDS instance şifrelenmemiş.

    Çözüm: storage_encrypted = false → true
    Yoksa: resource bloğuna ekle (zor olduğu için sadece var olanı değiştiriyoruz)
    """
    if re.search(r"storage_encrypted\s*=\s*false", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(storage_encrypted\s*=\s*)false",
            r"\1true",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


def fix_public_rds(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_17: RDS instance public erişime açık.

    Çözüm: publicly_accessible = true → false
    """
    if re.search(r"publicly_accessible\s*=\s*true", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(publicly_accessible\s*=\s*)true",
            r"\1false",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


def fix_unencrypted_ebs(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_8: EBS volume şifrelenmemiş.

    Çözüm: encrypted = false → true
    """
    if re.search(r"\bencrypted\s*=\s*false", original_code, re.IGNORECASE):
        fixed = re.sub(
            r"(\bencrypted\s*=\s*)false",
            r"\1true",
            original_code,
            flags=re.IGNORECASE,
        )
        return fixed

    return None


# Check ID → Fix function mapping
FIX_FUNCTIONS = {
    "CKV_AWS_8": fix_unencrypted_ebs,
    "CKV_AWS_16": fix_unencrypted_rds,
    "CKV_AWS_17": fix_public_rds,
    "CKV_AWS_20": fix_public_s3_bucket,
    "CKV_AWS_24": fix_ssh_open_to_world,
}
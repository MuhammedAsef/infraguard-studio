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

def fix_rdp_open_to_world(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_25: Security group 3389 portunu (RDP) dünyaya açıyor.

    Çözüm: SSH fix'iyle aynı mantık - context'te port 3389 varsa cidr'i değiştir.
    """
    lines = original_code.split("\n")
    fixed_lines = []
    changed = False

    for i, line in enumerate(lines):
        if '"0.0.0.0/0"' in line and "cidr_blocks" in line:
            context_start = max(0, i - 10)
            context = "\n".join(lines[context_start:i])

            if re.search(r"(from_port|to_port)\s*=\s*3389\b", context):
                indent = line[: len(line) - len(line.lstrip())]
                fixed_lines.append(f'{indent}# UYARI: RDP portu icin 0.0.0.0/0 tehlikeli. VPC CIDR\'inizi kullanin.')
                fixed_lines.append(line.replace('"0.0.0.0/0"', '"10.0.0.0/8"'))
                changed = True
                continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines) if changed else None


def fix_imdsv2_required(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_79: EC2 instance IMDSv2 zorunlu değil.

    Çözüm: http_tokens = "optional" → "required"
    Veya: metadata_options bloğu yoksa dokunma.
    """
    if re.search(r'http_tokens\s*=\s*"optional"', original_code):
        fixed = re.sub(
            r'(http_tokens\s*=\s*)"optional"',
            r'\1"required"',
            original_code,
        )
        return fixed

    return None


def fix_tls_version(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_103: Load balancer eski TLS protokolü kullanıyor.

    Çözüm: ssl_policy = "ELBSecurityPolicy-2016-08" gibi eski policy'leri yeni TLS 1.2'ye çevir.
    """
    old_policies = [
        "ELBSecurityPolicy-2016-08",
        "ELBSecurityPolicy-TLS-1-0-2015-04",
        "ELBSecurityPolicy-TLS-1-1-2017-01",
    ]
    fixed = original_code
    changed = False

    for old in old_policies:
        pattern = rf'(ssl_policy\s*=\s*)"{re.escape(old)}"'
        if re.search(pattern, fixed):
            fixed = re.sub(pattern, r'\1"ELBSecurityPolicy-TLS-1-2-2017-01"', fixed)
            changed = True

    return fixed if changed else None


def fix_cloudfront_https(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_34: CloudFront viewer protocol HTTPS zorunlu değil.

    Çözüm: viewer_protocol_policy = "allow-all" → "redirect-to-https"
    """
    if re.search(r'viewer_protocol_policy\s*=\s*"allow-all"', original_code):
        fixed = re.sub(
            r'(viewer_protocol_policy\s*=\s*)"allow-all"',
            r'\1"redirect-to-https"',
            original_code,
        )
        return fixed

    return None


def fix_ecr_immutable(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_51: ECR image tag mutability IMMUTABLE olmalı.

    Çözüm: image_tag_mutability = "MUTABLE" → "IMMUTABLE"
    """
    if re.search(r'image_tag_mutability\s*=\s*"MUTABLE"', original_code):
        fixed = re.sub(
            r'(image_tag_mutability\s*=\s*)"MUTABLE"',
            r'\1"IMMUTABLE"',
            original_code,
        )
        return fixed

    return None


def fix_dynamodb_encryption(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_28: DynamoDB encryption at rest yok.

    Çözüm: server_side_encryption.enabled = false → true
    """
    if re.search(r"enabled\s*=\s*false", original_code):
        # DynamoDB context'inde olduğunu varsayıyoruz (finding'den geldi)
        fixed = re.sub(
            r"(server_side_encryption\s*\{[^}]*?enabled\s*=\s*)false",
            r"\1true",
            original_code,
            flags=re.DOTALL,
        )
        if fixed != original_code:
            return fixed

    return None


def fix_cloudtrail_multi_region(original_code: str, finding: dict) -> str | None:
    """
    CKV_AWS_33: CloudTrail multi-region etkin değil.

    Çözüm: is_multi_region_trail = false → true
    """
    if re.search(r"is_multi_region_trail\s*=\s*false", original_code):
        fixed = re.sub(
            r"(is_multi_region_trail\s*=\s*)false",
            r"\1true",
            original_code,
        )
        return fixed

    return None

# Check ID → Fix function mapping
FIX_FUNCTIONS = {
    "CKV_AWS_8": fix_unencrypted_ebs,           # EBS encryption
    "CKV_AWS_16": fix_unencrypted_rds,          # RDS encryption
    "CKV_AWS_17": fix_public_rds,                # RDS publicly_accessible
    "CKV_AWS_20": fix_public_s3_bucket,         # S3 public ACL
    "CKV_AWS_24": fix_ssh_open_to_world,        # SSH 0.0.0.0/0
    "CKV_AWS_25": fix_rdp_open_to_world,        # RDP 0.0.0.0/0
    "CKV_AWS_28": fix_dynamodb_encryption,      # DynamoDB encryption
    "CKV_AWS_33": fix_cloudtrail_multi_region,  # CloudTrail multi-region
    "CKV_AWS_34": fix_cloudfront_https,         # CloudFront HTTPS
    "CKV_AWS_51": fix_ecr_immutable,            # ECR immutable tag
    "CKV_AWS_79": fix_imdsv2_required,          # EC2 IMDSv2
    "CKV_AWS_103": fix_tls_version,             # LB TLS 1.2
}
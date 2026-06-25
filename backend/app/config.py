import os

# Tarama limitleri
MAX_CODE_SIZE_BYTES = 50 * 1024  # 50KB - bundan büyük dosya kabul etme
SCAN_TIMEOUT_SECONDS = 30        # 30 saniyede bitmezse taramayı durdur
MAX_CONCURRENT_SCANS = 2         # Aynı anda max 2 tarama çalışsın

# Desteklenen dosya tipleri ve sabit dosya adları
# Kullanıcının dosya adını ASLA kullanma — güvenlik kararı
# Neden? Birisi dosya adına "../../etc/passwd" yazarsa path traversal olur
FILE_TYPE_CONFIG = {
    "dockerfile": {
        "filename": "Dockerfile",
        "label": "Dockerfile",
        "checkov_frameworks": ["dockerfile", "secrets"],
        "monaco_language": "dockerfile",
    },
    "kubernetes": {
        "filename": "manifest.yaml",
        "label": "Kubernetes YAML",
        "checkov_frameworks": ["kubernetes", "secrets"],
        "monaco_language": "yaml",
    },
    "terraform": {
        "filename": "main.tf",
        "label": "Terraform",
        "checkov_frameworks": ["terraform", "secrets"],
        "monaco_language": "hcl",
    },
}

# Severity skorlama ağırlıkları
# Risk skoru hesaplarken her bulgu tipine farklı ceza veriyoruz
SEVERITY_WEIGHTS = {
    "CRITICAL": 10,
    "HIGH": 5,
    "MEDIUM": 2,
    "LOW": 1,
}
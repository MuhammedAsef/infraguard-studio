"""
CI/CD pipeline snippet'leri üretir.

Her dosya tipi için GitLab CI ve GitHub Actions job'ları döner.
Kullanıcı kopyalayıp doğrudan kendi pipeline dosyasına yapıştırabilir.
"""


def get_pipeline_snippets(file_type: str) -> dict:
    """
    Verilen dosya tipi için CI/CD job snippet'leri döner.

    Returns:
        {
            "gitlab": "...",
            "github": "...",
            "explanation": "..."
        }
    """

    snippets = {
        "dockerfile": _dockerfile_snippets(),
        "kubernetes": _kubernetes_snippets(),
        "terraform": _terraform_snippets(),
    }

    return snippets.get(file_type, _generic_snippets())


def _dockerfile_snippets() -> dict:
    return {
        "explanation": (
            "Bu snippet'i CI/CD pipeline'ınıza ekleyerek, her commit'te "
            "Dockerfile'larınız otomatik olarak Checkov ile taranır. "
            "Kritik güvenlik bulgusu varsa pipeline başarısız olur ve "
            "kod merge edilemez. Bu, güvensiz Dockerfile'ların production'a "
            "ulaşmasını engelleyen bir 'security gate'tir."
        ),
        "gitlab": """# .gitlab-ci.yml
stages:
  - security

dockerfile-security-scan:
  stage: security
  image: bridgecrew/checkov:latest
  script:
    - checkov -f Dockerfile --framework dockerfile --output json --output-file-path .
    - checkov -f Dockerfile --framework dockerfile --hard-fail-on CRITICAL,HIGH
  artifacts:
    when: always
    paths:
      - results_json.json
    expire_in: 1 week
  rules:
    - changes:
        - Dockerfile
        - "**/Dockerfile"
""",
        "github": """# .github/workflows/dockerfile-security.yml
name: Dockerfile Security Scan

on:
  pull_request:
    paths:
      - '**/Dockerfile'
  push:
    branches: [main, master]
    paths:
      - '**/Dockerfile'

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov on Dockerfile
        uses: bridgecrewio/checkov-action@master
        with:
          framework: dockerfile
          soft_fail: false
          output_format: sarif
          output_file_path: reports/results.sarif

      - name: Upload SARIF results
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: reports/results.sarif
""",
    }


def _kubernetes_snippets() -> dict:
    return {
        "explanation": (
            "Bu snippet'i CI/CD pipeline'ınıza eklediğinizde, her commit'te "
            "Kubernetes manifest'leriniz Checkov ile otomatik taranır. "
            "Production'a privileged container, eksik resource limits veya "
            "güvensiz securityContext içeren YAML'lar ulaşamaz. "
            "Bonus: Bunu pre-commit hook olarak da kullanabilirsiniz."
        ),
        "gitlab": """# .gitlab-ci.yml
stages:
  - security

kubernetes-security-scan:
  stage: security
  image: bridgecrew/checkov:latest
  script:
    - checkov -d k8s/ --framework kubernetes --output json --output-file-path .
    - checkov -d k8s/ --framework kubernetes --hard-fail-on CRITICAL,HIGH
  artifacts:
    when: always
    paths:
      - results_json.json
    expire_in: 1 week
  rules:
    - changes:
        - "k8s/**/*.yaml"
        - "k8s/**/*.yml"
        - "manifests/**/*.yaml"
""",
        "github": """# .github/workflows/kubernetes-security.yml
name: Kubernetes Security Scan

on:
  pull_request:
    paths:
      - 'k8s/**'
      - 'manifests/**'
      - '**/*.yaml'
  push:
    branches: [main, master]

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov on Kubernetes manifests
        uses: bridgecrewio/checkov-action@master
        with:
          directory: k8s/
          framework: kubernetes
          soft_fail: false
          output_format: sarif
          output_file_path: reports/results.sarif

      - name: Upload SARIF results
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: reports/results.sarif
""",
    }


def _terraform_snippets() -> dict:
    return {
        "explanation": (
            "Bu snippet'i Terraform repository'nizin CI/CD'sine eklediğinizde, "
            "her plan/apply öncesi Checkov altyapı kodunuzu güvenlik açısından tarar. "
            "Public S3 bucket, açık SSH portu, şifrelenmemiş RDS gibi yapılandırma "
            "hatalarını cloud'a deploy edilmeden yakalar. "
            "Bu, milyon dolarlık veri ihlallerinin en yaygın sebebi olan IaC "
            "misconfiguration'larını önler."
        ),
        "gitlab": """# .gitlab-ci.yml
stages:
  - validate
  - security
  - plan

terraform-security-scan:
  stage: security
  image: bridgecrew/checkov:latest
  script:
    - checkov -d . --framework terraform --output json --output-file-path .
    - checkov -d . --framework terraform --hard-fail-on CRITICAL,HIGH
  artifacts:
    when: always
    paths:
      - results_json.json
    expire_in: 1 week
  rules:
    - changes:
        - "**/*.tf"
        - "**/*.tfvars"
""",
        "github": """# .github/workflows/terraform-security.yml
name: Terraform Security Scan

on:
  pull_request:
    paths:
      - '**/*.tf'
      - '**/*.tfvars'
  push:
    branches: [main, master]

jobs:
  checkov:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov on Terraform
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform
          soft_fail: false
          output_format: sarif
          output_file_path: reports/results.sarif

      - name: Upload SARIF results
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: reports/results.sarif
""",
    }


def _generic_snippets() -> dict:
    return {
        "explanation": "Bu dosya tipi için pipeline snippet'i henüz hazır değil.",
        "gitlab": "",
        "github": "",
    }
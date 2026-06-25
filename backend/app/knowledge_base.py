# Checkov Dockerfile kuralları için açıklama ve severity bilgisi
# Checkov bazen severity vermez, biz kendimiz atıyoruz
# + her kurala Türkçe/İngilizce açıklama ekliyoruz

DOCKERFILE_RULES = {
    "CKV_DOCKER_1": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "ADD yerine COPY kullanılmalı",
        "title_en": "Use COPY instead of ADD",
        "explanation_tr": (
            "ADD komutu uzak URL'lerden dosya indirebilir ve tar arşivlerini "
            "otomatik açabilir. Bu, supply chain saldırılarına kapı açar. "
            "COPY daha güvenlidir çünkü sadece yerel dosyaları kopyalar."
        ),
        "explanation_en": (
            "ADD can download files from remote URLs and auto-extract tar archives, "
            "which opens the door to supply chain attacks. COPY is safer as it only "
            "copies local files."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy",
            "CIS Docker Benchmark 4.9",
        ],
    },
    "CKV_DOCKER_2": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "HEALTHCHECK talimatı eksik",
        "title_en": "Missing HEALTHCHECK instruction",
        "explanation_tr": (
            "HEALTHCHECK olmadan container orchestration araçları (Kubernetes, Docker Swarm) "
            "container'ın gerçekten sağlıklı çalışıp çalışmadığını bilemez. "
            "Uygulama çökse bile container 'running' görünür ve trafik almaya devam eder. "
            "Production'da downtime ve veri kaybı riski oluşturur."
        ),
        "explanation_en": (
            "Without HEALTHCHECK, container orchestration tools cannot determine if the "
            "container is actually healthy. The app may crash but the container stays 'running' "
            "and keeps receiving traffic, causing downtime and potential data loss."
        ),
        "references": [
            "https://docs.docker.com/reference/dockerfile/#healthcheck",
            "CIS Docker Benchmark 4.6",
        ],
    },
    "CKV_DOCKER_3": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Tek bir RUN komutunda birden fazla paket yöneticisi komutu var",
        "title_en": "Multiple package manager commands in single RUN",
        "explanation_tr": (
            "apt-get update ve apt-get install komutları ayrı RUN satırlarında olursa, "
            "Docker layer cache nedeniyle eski paket listesiyle kurulum yapılabilir. "
            "Bu, bilinen güvenlik açıkları olan eski paketlerin yüklenmesine neden olur."
        ),
        "explanation_en": (
            "If apt-get update and install are in separate RUN layers, Docker's layer cache "
            "may use stale package lists, installing outdated packages with known vulnerabilities."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run",
        ],
    },
    "CKV_DOCKER_4": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "Güvenilir GPG anahtarı ile paket doğrulaması yapılmalı",
        "title_en": "Ensure package signature verification with trusted GPG key",
        "explanation_tr": (
            "Paket yöneticisinden yüklenen paketlerin GPG imzası doğrulanmazsa, "
            "man-in-the-middle saldırısıyla değiştirilmiş paketler yüklenebilir."
        ),
        "explanation_en": (
            "Without GPG signature verification, packages could be tampered with "
            "via man-in-the-middle attacks during download."
        ),
        "references": [
            "CIS Docker Benchmark 4.8",
        ],
    },
    "CKV_DOCKER_5": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "DOCKERIGNORE dosyası kullanılmalı",
        "title_en": "Use .dockerignore file",
        "explanation_tr": (
            ".dockerignore olmadan hassas dosyalar (.env, .git, private key'ler) "
            "Docker build context'e dahil edilebilir ve image'a sızabilir."
        ),
        "explanation_en": (
            "Without .dockerignore, sensitive files (.env, .git, private keys) "
            "may leak into the Docker build context and final image."
        ),
        "references": [
            "https://docs.docker.com/build/building/context/#dockerignore-files",
        ],
    },
    "CKV_DOCKER_7": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "Base image 'latest' etiketi kullanıyor",
        "title_en": "Base image uses 'latest' tag",
        "explanation_tr": (
            "'latest' etiketi her pull'da farklı bir image getirebilir. "
            "Bu, build tekrarlanabilirliğini bozar ve test edilmemiş "
            "değişikliklerin production'a geçmesine neden olabilir. "
            "Spesifik bir versiyon etiketi kullanın (örn: ubuntu:22.04)."
        ),
        "explanation_en": (
            "The 'latest' tag can pull a different image on each build, breaking "
            "reproducibility and potentially introducing untested changes into production. "
            "Use a specific version tag (e.g., ubuntu:22.04)."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#from",
            "CIS Docker Benchmark 4.7",
        ],
    },
    "CKV_DOCKER_8": {
        "severity": "CRITICAL",
        "category": "Container Hardening",
        "title_tr": "Son USER root olarak ayarlanmış",
        "title_en": "Last USER is set to root",
        "explanation_tr": (
            "Container root kullanıcıyla çalışırsa, bir saldırgan container'dan "
            "kaçmayı başardığında host sisteme root erişimi elde edebilir. "
            "Bu, tüm altyapının ele geçirilmesi anlamına gelir. "
            "Her zaman non-root kullanıcı oluşturun ve USER ile ayarlayın."
        ),
        "explanation_en": (
            "If a container runs as root and an attacker escapes the container, "
            "they gain root access to the host system, potentially compromising "
            "the entire infrastructure. Always create and switch to a non-root user."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user",
            "CIS Docker Benchmark 4.1",
            "OWASP Docker Security - D04",
        ],
    },
    "CKV_DOCKER_9": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "Gereksiz port expose edilmemeli",
        "title_en": "Avoid unnecessary port exposure",
        "explanation_tr": (
            "İhtiyaç duyulmayan portları EXPOSE etmek saldırı yüzeyini genişletir. "
            "Sadece uygulamanın gerçekten ihtiyaç duyduğu portları açın."
        ),
        "explanation_en": (
            "Exposing unnecessary ports increases the attack surface. "
            "Only expose ports that the application actually needs."
        ),
        "references": [
            "CIS Docker Benchmark 4.12",
        ],
    },
    "CKV_DOCKER_10": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "EXPOSE ile yalnızca gerekli portlar açılmalı",
        "title_en": "Only expose necessary ports with EXPOSE",
        "explanation_tr": (
            "Yaygın servis portlarını (22/SSH, 3389/RDP vb.) expose etmek "
            "container'a doğrudan uzaktan erişim riski oluşturur."
        ),
        "explanation_en": (
            "Exposing common service ports (22/SSH, 3389/RDP, etc.) creates "
            "a risk of direct remote access to the container."
        ),
        "references": [
            "CIS Docker Benchmark 4.12",
        ],
    },
    "CKV_DOCKER_11": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "FROM komutunda alias kullanılmalı",
        "title_en": "Use alias in FROM instruction",
        "explanation_tr": (
            "Multi-stage build'lerde alias kullanmak (FROM node:18 AS builder) "
            "Dockerfile okunurluğunu artırır ve yanlış stage'den COPY yapmayı önler."
        ),
        "explanation_en": (
            "Using aliases in multi-stage builds (FROM node:18 AS builder) "
            "improves readability and prevents copying from wrong stages."
        ),
        "references": [
            "https://docs.docker.com/build/building/multi-stage/",
        ],
    },
}

# Bilmediğimiz kurallar için fallback
# Checkov yeni kural eklerse knowledge base'de olmayabilir
# O zaman bu varsayılan açıklamayı kullanırız
FALLBACK_RULE = {
    "severity": "MEDIUM",
    "category": "Security",
    "title_tr": None,  # None ise Checkov'un kendi check_name'ini kullanacağız
    "title_en": None,
    "explanation_tr": "Bu güvenlik kontrolü başarısız oldu. Detaylar için referans linklerini inceleyin.",
    "explanation_en": "This security check has failed. See reference links for details.",
    "references": [],
}
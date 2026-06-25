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

# Kubernetes kuralları
KUBERNETES_RULES = {
    "CKV_K8S_8": {
        "severity": "MEDIUM",
        "category": "Observability",
        "title_tr": "Liveness Probe tanımlanmamış",
        "title_en": "Liveness Probe is not defined",
        "explanation_tr": (
            "Liveness Probe olmadan Kubernetes pod'un canlı olup olmadığını anlayamaz. "
            "Uygulama deadlock'a girse veya yanıt vermez hale gelse bile pod 'Running' "
            "görünür ve trafik almaya devam eder. Production'da zincir reaksiyon hatalarına yol açar."
        ),
        "explanation_en": (
            "Without a Liveness Probe, Kubernetes cannot determine if the pod is alive. "
            "Even if the app deadlocks or becomes unresponsive, the pod stays 'Running' "
            "and continues receiving traffic, causing cascade failures in production."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes",
        ],
    },
    "CKV_K8S_9": {
        "severity": "MEDIUM",
        "category": "Observability",
        "title_tr": "Readiness Probe tanımlanmamış",
        "title_en": "Readiness Probe is not defined",
        "explanation_tr": (
            "Readiness Probe olmadan Kubernetes pod'un trafik almaya hazır olup olmadığını "
            "bilemez. Uygulama henüz başlatılmadığında bile pod'a istek gönderilir, "
            "bu da 5xx hatalarına ve kötü kullanıcı deneyimine neden olur."
        ),
        "explanation_en": (
            "Without a Readiness Probe, Kubernetes cannot determine if the pod is ready "
            "to receive traffic. Requests may be sent before the app is initialized, "
            "causing 5xx errors and poor user experience."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes",
        ],
    },
    "CKV_K8S_10": {
        "severity": "MEDIUM",
        "category": "Resource Management",
        "title_tr": "CPU request tanımlanmamış",
        "title_en": "CPU request is not defined",
        "explanation_tr": (
            "CPU request olmadan Kubernetes scheduler pod'un kaynak ihtiyacını bilemez. "
            "Bu, başka pod'ların kaynaklarını çalmaya, 'noisy neighbor' problemine "
            "ve cluster'da öngörülemeyen davranışlara yol açar."
        ),
        "explanation_en": (
            "Without CPU request, the Kubernetes scheduler cannot predict resource needs. "
            "This leads to resource contention, 'noisy neighbor' issues, "
            "and unpredictable cluster behavior."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/",
        ],
    },
    "CKV_K8S_11": {
        "severity": "HIGH",
        "category": "Resource Management",
        "title_tr": "CPU limit tanımlanmamış",
        "title_en": "CPU limit is not defined",
        "explanation_tr": (
            "CPU limit olmadan bir container tüm node CPU'sunu tüketebilir. "
            "Bu, aynı node'daki diğer pod'ları yavaşlatır veya çökertir. "
            "Production'da DoS benzeri durumlara neden olabilir."
        ),
        "explanation_en": (
            "Without CPU limit, a container can consume all node CPU, "
            "slowing down or crashing other pods on the same node. "
            "Can cause DoS-like situations in production."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/",
        ],
    },
    "CKV_K8S_12": {
        "severity": "MEDIUM",
        "category": "Resource Management",
        "title_tr": "Memory request tanımlanmamış",
        "title_en": "Memory request is not defined",
        "explanation_tr": (
            "Memory request olmadan scheduler doğru node atamasını yapamaz. "
            "Pod'lar yetersiz kaynaklı node'lara atanabilir ve OOM (Out of Memory) ile çökebilir."
        ),
        "explanation_en": (
            "Without memory request, the scheduler cannot make proper node assignments. "
            "Pods may be scheduled on under-resourced nodes and crash with OOM errors."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/",
        ],
    },
    "CKV_K8S_13": {
        "severity": "HIGH",
        "category": "Resource Management",
        "title_tr": "Memory limit tanımlanmamış",
        "title_en": "Memory limit is not defined",
        "explanation_tr": (
            "Memory limit olmadan bir container node'un tüm RAM'ini tüketebilir. "
            "Bu, aynı node'daki diğer pod'ların OOM ile çökmesine ve "
            "tüm node'un instabil hale gelmesine yol açar."
        ),
        "explanation_en": (
            "Without memory limit, a container can consume all node RAM, "
            "causing OOM crashes for other pods and destabilizing the entire node."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/",
        ],
    },
    "CKV_K8S_14": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "Image tag 'latest' kullanılıyor veya tanımlanmamış",
        "title_en": "Image tag is 'latest' or not specified",
        "explanation_tr": (
            "'latest' tag veya tag eksikliği, deploy sırasında farklı image versiyonlarının "
            "çekilmesine neden olabilir. Bu, build tekrarlanabilirliğini bozar ve rollback'i zorlaştırır. "
            "Spesifik bir versiyon veya immutable digest kullanın."
        ),
        "explanation_en": (
            "'latest' tag or missing tag may cause different image versions to be pulled. "
            "This breaks build reproducibility and complicates rollbacks. "
            "Use specific versions or immutable digests."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/containers/images/#image-names",
        ],
    },
    "CKV_K8S_15": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "Image pull policy 'Always' olarak ayarlanmamış",
        "title_en": "Image pull policy is not 'Always'",
        "explanation_tr": (
            "Image pull policy 'Always' değilse, node'da cache'lenmiş eski image kullanılabilir. "
            "Mutable tag'lerle (örn: latest, stable) çalışırken bu güvenlik güncellemelerinin "
            "geç uygulanmasına neden olur."
        ),
        "explanation_en": (
            "If image pull policy is not 'Always', cached old images on the node may be used. "
            "With mutable tags (e.g. latest, stable), this delays security updates."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy",
        ],
    },
    "CKV_K8S_16": {
        "severity": "CRITICAL",
        "category": "Container Hardening",
        "title_tr": "Privileged container kullanılıyor",
        "title_en": "Privileged container is used",
        "explanation_tr": (
            "Privileged container, host'un tüm kernel yeteneklerine erişim sağlar. "
            "Bu, container'dan host'a geçişi (container escape) çok kolaylaştırır. "
            "Bir saldırgan privileged container'a erişirse, tüm Kubernetes cluster'ı tehlikeye girer."
        ),
        "explanation_en": (
            "Privileged containers have access to all host kernel capabilities, "
            "making container escapes trivial. If an attacker compromises a privileged container, "
            "the entire Kubernetes cluster is at risk."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
            "CIS Kubernetes Benchmark 5.2.1",
        ],
    },
    "CKV_K8S_17": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Container privilege escalation engellenmemiş",
        "title_en": "Privilege escalation not prevented",
        "explanation_tr": (
            "allowPrivilegeEscalation: true (veya tanımsız), child process'lerin "
            "parent'tan daha fazla yetki almasına izin verir. setuid binary'leri ile "
            "saldırgan privilege escalation yapabilir."
        ),
        "explanation_en": (
            "allowPrivilegeEscalation: true (or undefined) allows child processes to gain "
            "more privileges than the parent. Attackers can use setuid binaries for privilege escalation."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
            "CIS Kubernetes Benchmark 5.2.5",
        ],
    },
    "CKV_K8S_20": {
        "severity": "CRITICAL",
        "category": "Container Hardening",
        "title_tr": "Container root olarak çalışıyor",
        "title_en": "Container runs as root",
        "explanation_tr": (
            "runAsNonRoot: true ayarlanmamışsa container root kullanıcıyla çalışabilir. "
            "Bir saldırgan container'a sızarsa root yetkileriyle hareket eder, "
            "bu da privilege escalation ve host kompromizasyonu riskini artırır."
        ),
        "explanation_en": (
            "If runAsNonRoot: true is not set, the container may run as root. "
            "An attacker compromising the container gains root privileges, "
            "increasing the risk of privilege escalation and host compromise."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
            "CIS Kubernetes Benchmark 5.2.6",
        ],
    },
    "CKV_K8S_21": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "Default namespace kullanılıyor",
        "title_en": "Default namespace is used",
        "explanation_tr": (
            "Default namespace kullanmak isolation'ı zayıflatır. "
            "Production workload'lar için ayrı namespace'ler kullanarak RBAC, "
            "network policy ve resource quota uygulamak daha güvenlidir."
        ),
        "explanation_en": (
            "Using the default namespace weakens isolation. "
            "Use dedicated namespaces for production workloads to apply RBAC, "
            "network policies, and resource quotas more effectively."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/",
        ],
    },
    "CKV_K8S_22": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "Read-only root filesystem kullanılmıyor",
        "title_en": "Read-only root filesystem is not used",
        "explanation_tr": (
            "readOnlyRootFilesystem: true ayarlanmamışsa saldırgan container'ın dosya sistemine yazabilir. "
            "Bu, malware indirme, persistent backdoor kurma ve runtime tampering riski oluşturur. "
            "Yazma gereken dizinler için ayrı emptyDir volume'ları kullanın."
        ),
        "explanation_en": (
            "Without readOnlyRootFilesystem: true, attackers can write to the container filesystem, "
            "enabling malware drops, persistent backdoors, and runtime tampering. "
            "Use separate emptyDir volumes for directories that need to be writable."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
        ],
    },
    "CKV_K8S_23": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "Root group olarak çalışıyor",
        "title_en": "Runs as root group",
        "explanation_tr": (
            "runAsGroup root (0) olarak ayarlanmışsa container root grup yetkileriyle çalışır. "
            "Root grubun erişebildiği dosyalara da erişim sağlanır, bu da güvenlik riskini artırır."
        ),
        "explanation_en": (
            "If runAsGroup is set to root (0), the container runs with root group privileges, "
            "gaining access to files accessible by the root group and increasing security risks."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
        ],
    },
    "CKV_K8S_28": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "NET_RAW capability düşürülmemiş",
        "title_en": "NET_RAW capability not dropped",
        "explanation_tr": (
            "NET_RAW capability container'ın raw socket oluşturmasına izin verir. "
            "Bu, ARP spoofing, packet sniffing ve diğer ağ saldırıları için kötüye kullanılabilir. "
            "Mutlaka gerekmediği sürece drop edilmelidir."
        ),
        "explanation_en": (
            "NET_RAW capability allows raw socket creation, "
            "which can be abused for ARP spoofing, packet sniffing, and other network attacks. "
            "Drop it unless absolutely necessary."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_29": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "Container için securityContext tanımlanmamış",
        "title_en": "securityContext not defined for container",
        "explanation_tr": (
            "securityContext olmadan container varsayılan (genelde güvensiz) ayarlarla çalışır. "
            "runAsNonRoot, readOnlyRootFilesystem, allowPrivilegeEscalation gibi kritik "
            "güvenlik ayarları açıkça tanımlanmalıdır."
        ),
        "explanation_en": (
            "Without securityContext, the container runs with default (usually insecure) settings. "
            "Critical security settings like runAsNonRoot, readOnlyRootFilesystem, "
            "and allowPrivilegeEscalation must be explicitly defined."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_30": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "Pod için securityContext tanımlanmamış",
        "title_en": "securityContext not defined for pod",
        "explanation_tr": (
            "Pod seviyesinde securityContext, pod'daki tüm container'lar için varsayılan "
            "güvenlik ayarlarını tanımlar. Tanımlanmazsa pod'lar varsayılan (genelde güvensiz) "
            "ayarlarla çalışır."
        ),
        "explanation_en": (
            "Pod-level securityContext defines default security settings for all containers in the pod. "
            "Without it, pods run with default (usually insecure) settings."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_31": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "seccomp profili tanımlanmamış",
        "title_en": "seccomp profile not defined",
        "explanation_tr": (
            "seccomp (secure computing mode) container'ın yapabileceği system call'ları kısıtlar. "
            "Tanımlanmadığında container tüm syscall'ları yapabilir, bu da kernel saldırı yüzeyini "
            "büyütür ve container escape risklerini artırır."
        ),
        "explanation_en": (
            "seccomp (secure computing mode) restricts the syscalls a container can make. "
            "Without it, containers can perform any syscall, expanding the kernel attack surface "
            "and increasing container escape risks."
        ),
        "references": [
            "https://kubernetes.io/docs/tutorials/security/seccomp/",
        ],
    },
    "CKV_K8S_37": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Tüm capability'ler düşürülmemiş",
        "title_en": "Not all capabilities are dropped",
        "explanation_tr": (
            "Linux capability'leri kernel yetkilerini parçalara böler. "
            "Tüm capability'leri drop etmeden çalıştırılan container'lar, ihtiyaç duymadıkları "
            "yetkilerle çalışır. Best practice: 'drop: [ALL]' yapın ve sadece gerekli olanları add edin."
        ),
        "explanation_en": (
            "Linux capabilities break down kernel privileges into smaller units. "
            "Containers running without dropping all capabilities have unnecessary privileges. "
            "Best practice: 'drop: [ALL]' and add back only what's needed."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-capabilities-for-a-container",
        ],
    },
    "CKV_K8S_38": {
        "severity": "MEDIUM",
        "category": "Service Account",
        "title_tr": "Service account token otomatik mount ediliyor",
        "title_en": "Service account token is automounted",
        "explanation_tr": (
            "automountServiceAccountToken: false ayarlanmamışsa, pod Kubernetes API'ye erişim "
            "için service account token'ını otomatik mount eder. Container kompromize olursa "
            "saldırgan bu token ile API'ye erişebilir."
        ),
        "explanation_en": (
            "Without automountServiceAccountToken: false, pods automatically mount the "
            "service account token for Kubernetes API access. If compromised, attackers "
            "can use this token to access the API."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/",
        ],
    },
}

# Terraform kuralları (AWS odaklı - en yaygın olanlar)
TERRAFORM_RULES = {
    # === S3 Bucket Kuralları ===
    "CKV_AWS_18": {
        "severity": "MEDIUM",
        "category": "Logging & Audit",
        "title_tr": "S3 bucket access logging etkin değil",
        "title_en": "S3 bucket access logging is not enabled",
        "explanation_tr": (
            "S3 bucket'a yapılan istekler loglanmadığında, veri sızıntısı veya yetkisiz erişim "
            "durumlarında forensik analiz yapılamaz. Compliance gereksinimleri için (SOC2, "
            "PCI-DSS, HIPAA) access logging zorunludur."
        ),
        "explanation_en": (
            "Without S3 access logging, forensic analysis is impossible during data leaks "
            "or unauthorized access. Compliance requirements (SOC2, PCI-DSS, HIPAA) mandate access logging."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html",
        ],
    },
    "CKV_AWS_19": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "S3 bucket sunucu tarafında şifreleme (SSE) yok",
        "title_en": "S3 bucket lacks server-side encryption (SSE)",
        "explanation_tr": (
            "S3'te depolanan veriler şifrelenmediğinde, AWS altyapısına fiziksel erişim "
            "sağlayan veya backup'lara erişen bir saldırgan veriyi okuyabilir. "
            "SSE-S3 veya SSE-KMS ile encryption-at-rest sağlanmalıdır."
        ),
        "explanation_en": (
            "Unencrypted S3 data can be read by attackers with physical AWS access or backup access. "
            "Use SSE-S3 or SSE-KMS for encryption-at-rest."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html",
        ],
    },
    "CKV_AWS_20": {
        "severity": "CRITICAL",
        "category": "Access Control",
        "title_tr": "S3 bucket public erişime açık",
        "title_en": "S3 bucket is publicly accessible",
        "explanation_tr": (
            "Public S3 bucket'lar veri sızıntılarının en yaygın nedenidir. "
            "Capital One, Verizon, Accenture gibi büyük şirketler bu yüzden milyonlarca kayıt kaybetti. "
            "Public access mutlaka 'block all public access' ile engellenmelidir."
        ),
        "explanation_en": (
            "Public S3 buckets are the most common cause of data breaches. "
            "Capital One, Verizon, Accenture lost millions of records this way. "
            "Public access must be blocked with 'block all public access'."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html",
        ],
    },
    "CKV_AWS_21": {
        "severity": "MEDIUM",
        "category": "Data Protection",
        "title_tr": "S3 bucket versioning etkin değil",
        "title_en": "S3 bucket versioning is not enabled",
        "explanation_tr": (
            "Versioning olmadan accidental delete veya ransomware şifrelemesi sonrası "
            "veri kurtarılamaz. Versioning, her objenin geçmiş versiyonlarını saklar ve "
            "veri kaybına karşı koruma sağlar."
        ),
        "explanation_en": (
            "Without versioning, accidental deletes or ransomware encryption cannot be recovered. "
            "Versioning keeps historical versions of each object and protects against data loss."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html",
        ],
    },

    # === Security Group Kuralları ===
    "CKV_AWS_23": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "Security group açıklaması eksik",
        "title_en": "Security group description is missing",
        "explanation_tr": (
            "Security group ve kurallarına açıklama eklemek, audit ve troubleshooting "
            "süreçlerini kolaylaştırır. Kuralın neden var olduğu anlaşılmazsa, "
            "gereksiz kurallar yıllarca kalabilir."
        ),
        "explanation_en": (
            "Adding descriptions to security groups and rules simplifies audit and troubleshooting. "
            "Without context, unnecessary rules may persist for years."
        ),
        "references": [],
    },
    "CKV_AWS_24": {
        "severity": "CRITICAL",
        "category": "Network Security",
        "title_tr": "Security group 22 portunu (SSH) dünyaya açıyor",
        "title_en": "Security group exposes port 22 (SSH) to the world",
        "explanation_tr": (
            "0.0.0.0/0 → port 22 (SSH) açık olması, brute-force saldırılarına davet çıkarmaktır. "
            "İnternette her zaman binlerce bot SSH portlarını tarıyor. "
            "SSH erişimi VPN, bastion host veya en azından IP whitelist ile sınırlandırılmalıdır."
        ),
        "explanation_en": (
            "0.0.0.0/0 → port 22 (SSH) open invites brute-force attacks. "
            "Thousands of bots scan SSH ports on the internet constantly. "
            "SSH access should be restricted via VPN, bastion host, or IP whitelist."
        ),
        "references": [
            "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html",
        ],
    },
    "CKV_AWS_25": {
        "severity": "CRITICAL",
        "category": "Network Security",
        "title_tr": "Security group 3389 portunu (RDP) dünyaya açıyor",
        "title_en": "Security group exposes port 3389 (RDP) to the world",
        "explanation_tr": (
            "0.0.0.0/0 → port 3389 (RDP) açık olması, Windows sunucuları için ciddi bir risktir. "
            "BlueKeep gibi RDP zafiyetleri ile uzaktan kod yürütme mümkündür. "
            "RDP erişimi VPN veya bastion host üzerinden yapılmalıdır."
        ),
        "explanation_en": (
            "0.0.0.0/0 → port 3389 (RDP) open is critical for Windows servers. "
            "RDP vulnerabilities like BlueKeep allow remote code execution. "
            "RDP access should be via VPN or bastion host."
        ),
        "references": [
            "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html",
        ],
    },

    # === EC2 / EBS Kuralları ===
    "CKV_AWS_8": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "EBS volume şifrelenmemiş",
        "title_en": "EBS volume is not encrypted",
        "explanation_tr": (
            "EBS volume'lar şifrelenmediğinde, snapshot'lara veya backup'lara erişim sağlayan "
            "bir saldırgan veriyi okuyabilir. AWS KMS ile encryption-at-rest sağlanmalıdır."
        ),
        "explanation_en": (
            "Unencrypted EBS volumes allow attackers with access to snapshots or backups "
            "to read the data. Use AWS KMS for encryption-at-rest."
        ),
        "references": [
            "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html",
        ],
    },

    # === RDS Database Kuralları ===
    "CKV_AWS_16": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "RDS instance şifrelenmemiş",
        "title_en": "RDS instance is not encrypted",
        "explanation_tr": (
            "RDS şifrelenmediğinde, database'deki tüm hassas veriler (kullanıcı bilgileri, "
            "kredi kartları, sağlık verileri) snapshot/backup erişimi ile sızabilir. "
            "Encryption-at-rest tüm production database'ler için zorunludur."
        ),
        "explanation_en": (
            "Without RDS encryption, all sensitive data (user info, credit cards, health data) "
            "may leak via snapshot/backup access. Encryption-at-rest is mandatory for production databases."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html",
        ],
    },
    "CKV_AWS_17": {
        "severity": "CRITICAL",
        "category": "Access Control",
        "title_tr": "RDS instance public erişime açık",
        "title_en": "RDS instance is publicly accessible",
        "explanation_tr": (
            "publicly_accessible = true ile RDS internet üzerinden erişilebilir hale gelir. "
            "Database'ler ASLA internete açık olmamalıdır. VPC içinde, private subnet'te "
            "olmalı ve sadece application servers erişebilmelidir."
        ),
        "explanation_en": (
            "publicly_accessible = true makes RDS reachable from the internet. "
            "Databases must NEVER be exposed to the internet. Keep them in VPC private subnets, "
            "accessible only by application servers."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html",
        ],
    },

    # === IAM Kuralları ===
    "CKV_AWS_40": {
        "severity": "HIGH",
        "category": "Identity & Access",
        "title_tr": "IAM policy kullanıcılara doğrudan atanmış",
        "title_en": "IAM policy is directly attached to users",
        "explanation_tr": (
            "Policy'leri doğrudan kullanıcılara atamak, izin yönetimini ve audit'i zorlaştırır. "
            "Best practice: kullanıcıları gruplara koy, policy'leri gruplara ata. "
            "Bu, organizasyon büyüdükçe yönetimi sağlar."
        ),
        "explanation_en": (
            "Directly attaching policies to users complicates permission management and audit. "
            "Best practice: put users into groups and attach policies to groups. "
            "This scales as the organization grows."
        ),
        "references": [
            "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html",
        ],
    },
    "CKV_AWS_41": {
        "severity": "CRITICAL",
        "category": "Secrets Management",
        "title_tr": "Hardcoded AWS access key tespit edildi",
        "title_en": "Hardcoded AWS access key detected",
        "explanation_tr": (
            "Terraform dosyasında AWS access key/secret bulunmak, GitHub'a commit edildiğinde "
            "saatler içinde kötü amaçlı botlar tarafından bulunup AWS hesabınızı sömürmek için "
            "kullanılır. Sonuç: binlerce dolarlık fatura ve veri ihlali. "
            "Asla hardcoded credentials kullanmayın — AWS provider varsayılan zincir kullansın."
        ),
        "explanation_en": (
            "Hardcoded AWS keys in Terraform, when committed to GitHub, are found by "
            "malicious bots within hours and used to exploit your AWS account. "
            "Result: thousands of dollars in charges and data breach. "
            "Never use hardcoded credentials — let the AWS provider use the default chain."
        ),
        "references": [
            "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#remove-credentials",
        ],
    },

    # === CloudTrail / Logging ===
    "CKV_AWS_35": {
        "severity": "MEDIUM",
        "category": "Logging & Audit",
        "title_tr": "CloudTrail log dosyaları şifrelenmemiş",
        "title_en": "CloudTrail logs are not encrypted",
        "explanation_tr": (
            "CloudTrail logları kim ne yaptı bilgisini içerir. Şifrelenmediğinde, "
            "log dosyalarına erişen bir saldırgan saldırı planlamak için kullanılabilir "
            "veya saldırı izlerini gizleyebilir. KMS ile şifrelenmelidir."
        ),
        "explanation_en": (
            "CloudTrail logs contain who-did-what info. Unencrypted, attackers accessing them "
            "can plan attacks or hide their tracks. Encrypt with KMS."
        ),
        "references": [
            "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/encrypting-cloudtrail-log-files-with-aws-kms.html",
        ],
    },

    # === VPC / Network ===
    "CKV_AWS_130": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "VPC subnet otomatik public IP atıyor",
        "title_en": "VPC subnet auto-assigns public IPs",
        "explanation_tr": (
            "map_public_ip_on_launch = true, subnet'te oluşturulan tüm EC2 instance'lara "
            "otomatik public IP verir. Bu yanlışlıkla internal servisleri internete açabilir. "
            "Public IP gereken instance'larda explicit olarak ayarlanmalıdır."
        ),
        "explanation_en": (
            "map_public_ip_on_launch = true auto-assigns public IPs to all EC2 instances in the subnet. "
            "This may accidentally expose internal services. Set public IPs explicitly per instance when needed."
        ),
        "references": [
            "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html",
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
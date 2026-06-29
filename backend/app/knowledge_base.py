# Checkov kuralları için Türkçe/İngilizce açıklamalar
# Resmi Checkov v3 kural listesinden doğrulanmıştır
# Kaynak: https://github.com/bridgecrewio/checkov/blob/main/docs/5.Policy%20Index/

DOCKERFILE_RULES = {
    "CKV_DOCKER_1": {
        "severity": "HIGH",
        "category": "Network Security",
        "title_tr": "SSH portu (22) açık",
        "title_en": "Port 22 (SSH) is exposed",
        "explanation_tr": (
            "EXPOSE 22 komutu SSH portunu container'da açar. Container'ların SSH erişimi olmamalı, "
            "kubectl exec veya docker exec gibi araçlarla erişim sağlanmalı. SSH portu açık container, "
            "brute-force saldırılarına ve lateral movement riskine açıktır."
        ),
        "explanation_en": (
            "EXPOSE 22 opens the SSH port in the container. Containers should not have SSH access; "
            "use kubectl exec or docker exec instead. Exposed SSH ports invite brute-force attacks "
            "and lateral movement risks."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-port-22-is-not-exposed",
            "CIS Docker Benchmark 4.12",
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
        "severity": "CRITICAL",
        "category": "Container Hardening",
        "title_tr": "USER talimatı eksik - container root olarak çalışıyor",
        "title_en": "USER instruction missing - container runs as root",
        "explanation_tr": (
            "USER talimatı tanımlanmamışsa container root kullanıcıyla çalışır. "
            "Bir saldırgan container'a sızarsa root yetkileriyle hareket eder ve "
            "container escape ile host sisteme erişebilir. Dockerfile'da non-root user "
            "oluşturulup USER ile ayarlanmalıdır."
        ),
        "explanation_en": (
            "Without a USER instruction, the container runs as root. "
            "An attacker compromising the container gains root privileges and may achieve "
            "container escape to access the host system. Create and switch to a non-root user."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user",
            "CIS Docker Benchmark 4.1",
            "OWASP Docker Security - D04",
        ],
    },
    "CKV_DOCKER_4": {
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
    "CKV_DOCKER_5": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "Update komutu RUN içinde tek başına kullanılıyor",
        "title_en": "Update instruction used alone in RUN",
        "explanation_tr": (
            "apt-get update gibi update komutları kendi RUN satırında olursa, Docker layer "
            "cache nedeniyle install komutu farklı bir RUN'da çalıştırıldığında eski paket "
            "listesi kullanılır. Bu, bilinen güvenlik açıklarına sahip eski paketlerin "
            "yüklenmesine neden olur. Update ve install aynı RUN içinde olmalıdır."
        ),
        "explanation_en": (
            "When update commands like apt-get update are in their own RUN line, Docker's "
            "layer cache may use stale package lists if install runs in a different RUN. "
            "This installs outdated packages with known vulnerabilities. "
            "Update and install must be in the same RUN."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run",
        ],
    },
    "CKV_DOCKER_6": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "MAINTAINER yerine LABEL maintainer kullanılmalı",
        "title_en": "Use LABEL maintainer instead of MAINTAINER",
        "explanation_tr": (
            "MAINTAINER talimatı Docker 1.13'den beri deprecated'dır. "
            "LABEL maintainer=\"...\" daha esnek ve standart bir yaklaşımdır."
        ),
        "explanation_en": (
            "MAINTAINER instruction is deprecated since Docker 1.13. "
            "LABEL maintainer=\"...\" is the more flexible and standard approach."
        ),
        "references": [
            "https://docs.docker.com/reference/dockerfile/#maintainer-deprecated",
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
        "severity": "LOW",
        "category": "Supply Chain",
        "title_tr": "APT paket yöneticisi kullanılıyor",
        "title_en": "APT package manager is being used",
        "explanation_tr": (
            "apt (apt-get'in kullanıcı dostu hali) interaktif kullanım için tasarlanmıştır ve "
            "stable bir CLI değildir. Script'lerde apt yerine apt-get kullanmak daha güvenlidir, "
            "ayrıca minimal base image'lar tercih edilmelidir."
        ),
        "explanation_en": (
            "apt (the user-friendly wrapper for apt-get) is designed for interactive use "
            "and its CLI is not stable. Use apt-get in scripts and prefer minimal base images."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-that-apt-isnt-used",
        ],
    },
    "CKV_DOCKER_10": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "WORKDIR absolute path olmalı",
        "title_en": "WORKDIR must use absolute path",
        "explanation_tr": (
            "WORKDIR relatif yol kullanırsa (./app gibi) sonraki komutların hangi dizinde "
            "çalışacağı belirsizleşir ve build davranışı öngörülemez hale gelir. "
            "Her zaman absolute path kullanın (/app gibi)."
        ),
        "explanation_en": (
            "If WORKDIR uses a relative path (like ./app), the working directory for "
            "subsequent commands becomes ambiguous and build behavior unpredictable. "
            "Always use absolute paths (like /app)."
        ),
        "references": [
            "https://docs.docker.com/reference/dockerfile/#workdir",
        ],
    },
    "CKV_DOCKER_11": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "Multi-stage build'de FROM alias unique olmalı",
        "title_en": "FROM aliases must be unique in multi-stage builds",
        "explanation_tr": (
            "Aynı alias birden fazla FROM ile kullanılırsa, COPY --from=builder gibi "
            "komutlar yanlış stage'den dosya kopyalayabilir. Her FROM alias unique olmalıdır."
        ),
        "explanation_en": (
            "If the same alias is used in multiple FROM instructions, commands like "
            "COPY --from=builder may copy from the wrong stage. Each FROM alias must be unique."
        ),
        "references": [
            "https://docs.docker.com/build/building/multi-stage/",
        ],
    },
    # Graph-based CKV2 kuralları
    "CKV2_DOCKER_1": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "sudo komutu kullanılmamalı",
        "title_en": "sudo should not be used",
        "explanation_tr": (
            "Container içinde sudo kullanmak, root'a privilege escalation imkanı verir. "
            "Bunun yerine USER ile doğru kullanıcıya geçiş yapılmalıdır. "
            "sudo bağımlılığı container'ın saldırı yüzeyini de artırır."
        ),
        "explanation_en": (
            "Using sudo inside a container enables privilege escalation to root. "
            "Switch users with the USER instruction instead. "
            "sudo dependency also increases the container's attack surface."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-that-sudo-isnt-used",
        ],
    },
    "CKV2_DOCKER_2": {
        "severity": "HIGH",
        "category": "Supply Chain",
        "title_tr": "curl ile sertifika doğrulaması devre dışı bırakılmış",
        "title_en": "curl certificate validation disabled",
        "explanation_tr": (
            "curl -k veya --insecure ile TLS sertifika doğrulaması devre dışı bırakılırsa, "
            "man-in-the-middle saldırıları ile değiştirilmiş içerik indirilebilir. "
            "Sertifika hataları varsa kök sebebi düzeltin, doğrulamayı asla atlamayın."
        ),
        "explanation_en": (
            "Disabling TLS certificate validation with curl -k or --insecure allows "
            "man-in-the-middle attacks to deliver tampered content. "
            "Fix the root cause of certificate errors instead of skipping validation."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-that-certificate-validation-is-not-disabled-with-curl",
        ],
    },
    "CKV2_DOCKER_3": {
        "severity": "HIGH",
        "category": "Supply Chain",
        "title_tr": "wget ile sertifika doğrulaması devre dışı bırakılmış",
        "title_en": "wget certificate validation disabled",
        "explanation_tr": (
            "wget --no-check-certificate ile TLS doğrulaması atlanırsa, indirilen dosyalar "
            "MITM saldırısıyla değiştirilebilir. Bu özellikle binary indirip çalıştıran "
            "Dockerfile'larda kritik bir tehdittir."
        ),
        "explanation_en": (
            "Skipping TLS validation with wget --no-check-certificate allows downloaded "
            "files to be tampered with via MITM attacks. This is critical especially for "
            "Dockerfiles that download and execute binaries."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-that-certificate-validation-is-not-disabled-with-wget",
        ],
    },
    "CKV2_DOCKER_7": {
        "severity": "HIGH",
        "category": "Supply Chain",
        "title_tr": "apk --allow-untrusted ile imzasız paket yükleniyor",
        "title_en": "Packages without trusted signature installed via apk --allow-untrusted",
        "explanation_tr": (
            "apk --allow-untrusted GPG imza doğrulamasını atlar. İmzasız paketler "
            "kötü amaçlı veya değiştirilmiş olabilir. Bu opsiyon production'da asla "
            "kullanılmamalıdır."
        ),
        "explanation_en": (
            "apk --allow-untrusted bypasses GPG signature verification. Unsigned packages "
            "may be malicious or tampered. This option should never be used in production."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-that-packages-with-untrusted-or-missing-signatures-are-not-used-by-apk",
        ],
    },
    "CKV2_DOCKER_8": {
        "severity": "HIGH",
        "category": "Supply Chain",
        "title_tr": "apt-get --allow-unauthenticated ile imzasız paket yükleniyor",
        "title_en": "Packages without authentication installed via apt-get --allow-unauthenticated",
        "explanation_tr": (
            "apt-get --allow-unauthenticated, GPG imza doğrulamasını atlayarak imzasız veya "
            "şüpheli kaynaklı paketlerin yüklenmesine izin verir. Supply chain saldırılarına "
            "açık kapı bırakır."
        ),
        "explanation_en": (
            "apt-get --allow-unauthenticated skips GPG signature verification, allowing "
            "installation of unsigned or untrusted packages. Leaves the door open to "
            "supply chain attacks."
        ),
        "references": [
            "https://docs.prismacloud.io/en/enterprise-edition/policy-reference/docker-policies/ensure-that-packages-with-untrusted-or-missing-signatures-are-not-used-by-apt-get",
        ],
    },
    # === Ek Dockerfile kuralları ===
    "CKV_DOCKER_12": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "ADD/COPY ile dosya sahipliği belirlenmemiş",
        "title_en": "Ensure that the chown flag is used with COPY/ADD",
        "explanation_tr": (
            "COPY ve ADD komutları varsayılan olarak dosyaları root sahipliğiyle kopyalar. "
            "Non-root kullanıcıyla çalışan container'larda bu, dosya erişim sorunlarına ve "
            "güvenlik risklerine yol açabilir. COPY --chown=appuser:appgroup ile sahipliği belirleyin."
        ),
        "explanation_en": (
            "COPY and ADD copy files with root ownership by default. In containers running as "
            "non-root, this can cause file access issues and security risks. "
            "Use COPY --chown=appuser:appgroup to set ownership explicitly."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/",
        ],
    },
    "CKV_DOCKER_13": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "Bilinen güvensiz registry kullanılıyor",
        "title_en": "Known insecure registry being used",
        "explanation_tr": (
            "HTTP (TLS olmayan) registry'lerden image çekmek, MITM saldırılarıyla image'ın "
            "değiştirilmesine olanak verir. Sadece HTTPS destekleyen trusted registry'leri kullanın."
        ),
        "explanation_en": (
            "Pulling images from HTTP (non-TLS) registries allows MITM attacks to alter images. "
            "Use only HTTPS-supported, trusted registries."
        ),
        "references": [
            "https://docs.docker.com/registry/deploying/",
        ],
    },
    "CKV_DOCKER_14": {
        "severity": "MEDIUM",
        "category": "Resource Management",
        "title_tr": "Container memory limit tanımlanmamış",
        "title_en": "Ensure that HEALTHCHECK instructions have been added to container images",
        "explanation_tr": (
            "Container'a memory limit konmadığında, runaway process'ler tüm host belleğini "
            "tüketebilir ve diğer container'ları etkileyebilir. docker run --memory ile limit konmalı."
        ),
        "explanation_en": (
            "Without a memory limit, runaway processes can consume all host memory, "
            "affecting other containers. Set a limit with docker run --memory."
        ),
        "references": [
            "https://docs.docker.com/config/containers/resource_constraints/",
        ],
    },
    "CKV_DOCKER_15": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "Image içinde paket cache temizlenmemiş",
        "title_en": "Ensure that PIP install has the --no-cache-dir option",
        "explanation_tr": (
            "pip install --no-cache-dir kullanılmadığında, paket cache image'da kalır ve "
            "image boyutu gereksiz yere büyür. Ayrıca image içinde gereksiz dosyalar saldırı "
            "yüzeyini artırır. --no-cache-dir flag'i her zaman kullanılmalıdır."
        ),
        "explanation_en": (
            "Without pip install --no-cache-dir, package cache remains in the image, "
            "unnecessarily increasing its size and attack surface. Always use --no-cache-dir."
        ),
        "references": [
            "https://pip.pypa.io/en/stable/topics/caching/",
        ],
    },
    "CKV2_DOCKER_4": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Container içinde gpg ile imza doğrulama atlanmış",
        "title_en": "Ensure that gpg signature verification is not skipped",
        "explanation_tr": (
            "rpm --nosignature veya benzeri flag'lerle paket imza doğrulamasının atlanması, "
            "kötü amaçlı veya tampered paketlerin yüklenmesine olanak verir. "
            "İmza doğrulaması her zaman aktif olmalıdır."
        ),
        "explanation_en": (
            "Skipping package signature verification with rpm --nosignature or similar flags "
            "allows installation of malicious or tampered packages. "
            "Signature verification must always be enabled."
        ),
        "references": [
            "https://www.redhat.com/sysadmin/rpm-signing-keys",
        ],
    },
    "CKV2_DOCKER_5": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "JSON formatında CMD/ENTRYPOINT kullanılmalı",
        "title_en": "Ensure CMD and ENTRYPOINT use JSON array format",
        "explanation_tr": (
            "Shell form (CMD command param1) yerine exec form (CMD [\"command\", \"param1\"]) "
            "kullanılmalıdır. Shell form, shell injection saldırılarına açıktır ve sinyallerin "
            "doğru şekilde iletilmesini engeller."
        ),
        "explanation_en": (
            "Use exec form (CMD [\"command\", \"param1\"]) instead of shell form (CMD command param1). "
            "Shell form is vulnerable to shell injection and prevents proper signal forwarding."
        ),
        "references": [
            "https://docs.docker.com/reference/dockerfile/#cmd",
        ],
    },
    "CKV2_DOCKER_6": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Container içinde port 22 (SSH) servisi çalıştırılıyor",
        "title_en": "Ensure that no container is running SSH service",
        "explanation_tr": (
            "Container içinde SSH daemon çalıştırmak best practice'e aykırıdır. "
            "Container'a erişim için docker exec veya kubectl exec kullanılmalıdır. "
            "SSH servisi attack surface'i büyütür ve credential management problemine yol açar."
        ),
        "explanation_en": (
            "Running an SSH daemon inside a container violates best practices. "
            "Use docker exec or kubectl exec to access containers. "
            "SSH service enlarges attack surface and creates credential management issues."
        ),
        "references": [
            "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/",
        ],
    },
}


# Kubernetes kuralları (resmi Checkov v3 listesinden doğrulanmış)
KUBERNETES_RULES = {
    "CKV_K8S_8": {
        "severity": "MEDIUM",
        "category": "Observability",
        "title_tr": "Liveness Probe yapılandırılmamış",
        "title_en": "Liveness Probe should be configured",
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
        "title_tr": "Readiness Probe yapılandırılmamış",
        "title_en": "Readiness Probe should be configured",
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
        "title_en": "CPU requests should be set",
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
        "title_en": "CPU limits should be set",
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
        "title_en": "Memory requests should be set",
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
        "title_en": "Memory limits should be set",
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
        "title_tr": "Image tag fixed değil ('latest' veya boş)",
        "title_en": "Image tag should be fixed - not latest or blank",
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
        "title_tr": "Image pull policy 'Always' olmalı",
        "title_en": "Image pull policy should be 'Always'",
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
        "title_en": "Container should not be privileged",
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
        "title_tr": "Host PID namespace paylaşılıyor",
        "title_en": "Containers share host PID namespace",
        "explanation_tr": (
            "hostPID: true ayarı, container'a host'un tüm process'lerini görme ve "
            "onlarla etkileşim kurma imkanı verir. Bu, /proc üzerinden hassas bilgilerin "
            "okunmasına ve diğer process'lere müdahaleye yol açabilir."
        ),
        "explanation_en": (
            "hostPID: true allows the container to see and interact with all host processes. "
            "This can lead to reading sensitive information via /proc and "
            "interfering with other processes."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
        ],
    },
    "CKV_K8S_18": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Host IPC namespace paylaşılıyor",
        "title_en": "Containers share host IPC namespace",
        "explanation_tr": (
            "hostIPC: true, container'ın host'un inter-process communication mekanizmalarına "
            "erişmesine izin verir. Shared memory ve message queue'lar üzerinden hassas verilere "
            "erişim mümkün olabilir."
        ),
        "explanation_en": (
            "hostIPC: true allows the container to access the host's inter-process "
            "communication mechanisms. Sensitive data may be exposed via shared memory "
            "and message queues."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
        ],
    },
    "CKV_K8S_19": {
        "severity": "HIGH",
        "category": "Network Security",
        "title_tr": "Host network namespace paylaşılıyor",
        "title_en": "Containers share host network namespace",
        "explanation_tr": (
            "hostNetwork: true, container'ı doğrudan host'un network interface'lerine bağlar. "
            "Bu, container'ın diğer process'lerin trafiğini sniff etmesine, host'taki tüm portları "
            "kullanmasına ve network isolasyonunu bypass etmesine olanak verir."
        ),
        "explanation_en": (
            "hostNetwork: true connects the container directly to the host's network interfaces. "
            "This lets the container sniff other processes' traffic, use any port on the host, "
            "and bypass network isolation."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
        ],
    },
    "CKV_K8S_20": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "allowPrivilegeEscalation engellenmemiş",
        "title_en": "allowPrivilegeEscalation not prevented",
        "explanation_tr": (
            "allowPrivilegeEscalation: true (veya tanımsız), child process'lerin "
            "parent'tan daha fazla yetki almasına izin verir. setuid binary'leri ile "
            "saldırgan privilege escalation yapabilir. allowPrivilegeEscalation: false olmalı."
        ),
        "explanation_en": (
            "allowPrivilegeEscalation: true (or undefined) allows child processes to gain "
            "more privileges than the parent. Attackers can use setuid binaries for privilege escalation. "
            "Set allowPrivilegeEscalation: false."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
            "CIS Kubernetes Benchmark 5.2.5",
        ],
    },
    "CKV_K8S_21": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "Default namespace kullanılıyor",
        "title_en": "The default namespace should not be used",
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
        "title_en": "Use read-only filesystem where possible",
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
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Root container kabul ediliyor (runAsNonRoot eksik)",
        "title_en": "Minimize admission of root containers",
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
    "CKV_K8S_25": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "Eklenen capability'leri olan container kabul ediliyor",
        "title_en": "Minimize admission of containers with added capability",
        "explanation_tr": (
            "Container'a ekstra Linux capability eklemek (SYS_ADMIN, NET_ADMIN vb.) "
            "saldırı yüzeyini büyütür. Sadece kesinlikle gerekli capability'ler eklenmeli, "
            "geri kalanlar drop edilmelidir."
        ),
        "explanation_en": (
            "Adding extra Linux capabilities (SYS_ADMIN, NET_ADMIN, etc.) to a container "
            "increases the attack surface. Only add absolutely necessary capabilities; "
            "drop the rest."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_26": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "hostPort kullanılıyor",
        "title_en": "Do not specify hostPort unless absolutely necessary",
        "explanation_tr": (
            "hostPort, container'ın host'un belirli bir portunu doğrudan kullanmasını sağlar. "
            "Bu, network policy bypass'ına ve aynı host'ta port çakışmasına yol açar. "
            "Service kullanılması tercih edilmelidir."
        ),
        "explanation_en": (
            "hostPort lets the container directly use a specific host port. This can bypass "
            "network policies and cause port conflicts on the same host. Prefer using a Service."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/services-networking/",
        ],
    },
    "CKV_K8S_27": {
        "severity": "CRITICAL",
        "category": "Container Hardening",
        "title_tr": "Docker daemon socket container'a expose ediliyor",
        "title_en": "Do not expose docker daemon socket to containers",
        "explanation_tr": (
            "/var/run/docker.sock'ın container içine mount edilmesi, container'a host'taki "
            "tüm container'ları yönetme yetkisi verir. Bir saldırgan bu socket'e erişirse, "
            "yeni privileged container başlatarak host'u tamamen ele geçirebilir."
        ),
        "explanation_en": (
            "Mounting /var/run/docker.sock into a container gives it authority to manage all "
            "containers on the host. An attacker accessing this socket can launch new "
            "privileged containers and fully compromise the host."
        ),
        "references": [
            "https://docs.docker.com/engine/security/",
        ],
    },
    "CKV_K8S_28": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "NET_RAW capability düşürülmemiş",
        "title_en": "Minimize admission of containers with NET_RAW capability",
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
        "title_tr": "Pod ve container için securityContext tanımlanmamış",
        "title_en": "Apply security context to pods and containers",
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
        "title_tr": "Container için securityContext tanımlanmamış",
        "title_en": "Apply security context to containers",
        "explanation_tr": (
            "Container seviyesinde securityContext eksikse, container kritik güvenlik "
            "ayarlarını miras almaz ve varsayılan (zayıf) konfigürasyonla çalışır. "
            "Pod seviyesi ayarları container seviyesinde özelleştirilmelidir."
        ),
        "explanation_en": (
            "Without container-level securityContext, the container inherits no critical "
            "security settings and runs with default (weak) configuration. "
            "Pod-level settings should be customized at the container level."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_31": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "seccomp profili tanımlanmamış",
        "title_en": "Ensure seccomp profile is set to runtime/default",
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
        "title_tr": "Container'a capability eklenmiş",
        "title_en": "Minimize admission of containers with capabilities assigned",
        "explanation_tr": (
            "Linux capability'leri kernel yetkilerini parçalara böler. "
            "Capabilities ekleyerek çalıştırılan container'lar, ihtiyaç duymadıkları "
            "yetkilerle çalışır. Best practice: 'drop: [ALL]' yapın ve sadece gerekli olanları add edin."
        ),
        "explanation_en": (
            "Linux capabilities break down kernel privileges into smaller units. "
            "Containers with added capabilities have unnecessary privileges. "
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
        "title_en": "Ensure that service account tokens are only mounted where necessary",
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
    "CKV_K8S_40": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Container'da runAsUser yüksek bir UID değil",
        "title_en": "Containers should run as a high UID to avoid host conflict",
        "explanation_tr": (
            "runAsUser düşük bir UID (10000'den küçük) ise host sistemindeki gerçek "
            "kullanıcılarla çakışabilir. 10000+ UID kullanmak host kullanıcılarıyla "
            "izolasyon sağlar."
        ),
        "explanation_en": (
            "If runAsUser is a low UID (below 10000), it may conflict with real users "
            "on the host system. Using UIDs 10000+ ensures isolation from host users."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_43": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "Image digest (hash) ile pin edilmemiş",
        "title_en": "Image should use digest",
        "explanation_tr": (
            "Image sadece tag ile referans verilirse (örn: nginx:1.21), tag aynı kalsa bile "
            "altındaki image değişebilir. Immutable digest (sha256:...) kullanmak tam "
            "reproducibility ve supply chain güvenliği sağlar."
        ),
        "explanation_en": (
            "If an image is referenced only by tag (e.g., nginx:1.21), the underlying image "
            "may change even with the same tag. Using an immutable digest (sha256:...) "
            "ensures full reproducibility and supply chain security."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/containers/images/#image-names",
        ],
    },
    # === Ek Kubernetes kuralları ===
    "CKV_K8S_24": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "PodSecurityPolicy / Pod Security Standards uygulanmamış",
        "title_en": "Do not allow containers without PodSecurityPolicy or PSS",
        "explanation_tr": (
            "PodSecurityPolicy (deprecated) veya yeni Pod Security Standards (PSS) olmadan, "
            "cluster'a güvensiz pod'lar deploy edilebilir. Namespace seviyesinde Pod Security "
            "Standards (restricted/baseline/privileged) uygulanmalıdır."
        ),
        "explanation_en": (
            "Without PodSecurityPolicy (deprecated) or Pod Security Standards (PSS), "
            "insecure pods can be deployed to the cluster. Apply Pod Security Standards "
            "at namespace level (restricted/baseline/privileged)."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/security/pod-security-standards/",
        ],
    },
    "CKV_K8S_32": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "AppArmor profili tanımlanmamış",
        "title_en": "Ensure default AppArmor profile is not set to unconfined",
        "explanation_tr": (
            "AppArmor profili tanımlanmadığında veya 'unconfined' bırakıldığında, "
            "container kernel seviyesinde kısıtlamalar olmadan çalışır. "
            "Bu, container escape risklerini ciddi şekilde artırır. "
            "container.apparmor.security.beta.kubernetes.io/<container-name> annotation'ı kullanın."
        ),
        "explanation_en": (
            "Without an AppArmor profile or with 'unconfined', the container runs without "
            "kernel-level restrictions, severely increasing container escape risks. "
            "Use container.apparmor.security.beta.kubernetes.io/<container-name> annotation."
        ),
        "references": [
            "https://kubernetes.io/docs/tutorials/security/apparmor/",
        ],
    },
    "CKV_K8S_33": {
        "severity": "HIGH",
        "category": "Network Security",
        "title_tr": "Kubernetes Dashboard deploy edilmiş",
        "title_en": "Ensure the Kubernetes dashboard is not deployed",
        "explanation_tr": (
            "Kubernetes Dashboard, geçmişte birçok kez güvenlik açığı nedeniyle compromise "
            "edilmiş bir bileşendir. Production cluster'larda dashboard deploy edilmemeli, "
            "yönetim kubectl veya benzeri CLI araçlarıyla yapılmalıdır."
        ),
        "explanation_en": (
            "Kubernetes Dashboard has been compromised multiple times due to security issues. "
            "Avoid deploying it in production clusters; manage via kubectl or similar CLI tools."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/",
        ],
    },
    "CKV_K8S_34": {
        "severity": "MEDIUM",
        "category": "Container Hardening",
        "title_tr": "Tiller (Helm v2) servisi tespit edildi",
        "title_en": "Ensure Tiller (Helm V2) is not deployed",
        "explanation_tr": (
            "Helm v2'nin Tiller bileşeni, cluster üzerinde geniş yetkilerle çalışan bir process'tir "
            "ve önemli güvenlik açıklarına neden olmuştur. Helm v3'e geçilmelidir; Tiller hiçbir "
            "production cluster'da bulunmamalıdır."
        ),
        "explanation_en": (
            "Helm v2's Tiller component runs with broad cluster privileges and has caused major "
            "security issues. Migrate to Helm v3; Tiller must not exist in any production cluster."
        ),
        "references": [
            "https://helm.sh/docs/faq/changes_since_helm2/",
        ],
    },
    "CKV_K8S_35": {
        "severity": "MEDIUM",
        "category": "Secrets Management",
        "title_tr": "Secret olarak environment variable kullanılmış",
        "title_en": "Prefer using secrets as files over secrets as environment variables",
        "explanation_tr": (
            "Secret'ları environment variable olarak mount etmek; process listesinde, crash dump'larda "
            "ve child process'lerde sızıntıya yol açar. Secret'ları volume olarak mount etmek "
            "(filesystem) çok daha güvenlidir."
        ),
        "explanation_en": (
            "Mounting secrets as environment variables leaks them via process listings, crash dumps, "
            "and child processes. Mounting secrets as volume files is significantly safer."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/configuration/secret/",
        ],
    },
    "CKV_K8S_36": {
        "severity": "HIGH",
        "category": "Container Hardening",
        "title_tr": "Container'da NET_RAW dahil tehlikeli capability'ler düşürülmemiş",
        "title_en": "Minimize the admission of containers with capabilities",
        "explanation_tr": (
            "NET_RAW, SYS_ADMIN, NET_ADMIN gibi capability'ler raw packet creation, "
            "host network değişikliği ve daha fazlasına izin verir. Best practice: 'drop: [ALL]' "
            "yapın ve sadece gerekli olanları add edin."
        ),
        "explanation_en": (
            "Capabilities like NET_RAW, SYS_ADMIN, NET_ADMIN allow raw packet creation, "
            "host network changes, and more. Best practice: 'drop: [ALL]' and add only what's required."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/",
        ],
    },
    "CKV_K8S_39": {
        "severity": "CRITICAL",
        "category": "Container Hardening",
        "title_tr": "Container 'docker.sock' veya benzer host path'i mount ediyor",
        "title_en": "Do not use the CAP_SYS_ADMIN linux capability",
        "explanation_tr": (
            "CAP_SYS_ADMIN, neredeyse root ile eşdeğer geniş yetkiler sağlar. "
            "Filesystem mount, kernel modülü yükleme, namespace yönetimi gibi tehlikeli "
            "işlemlere izin verir. Bu capability hiçbir durumda eklenmemelidir."
        ),
        "explanation_en": (
            "CAP_SYS_ADMIN provides nearly root-equivalent privileges, allowing filesystem mounts, "
            "kernel module loading, namespace management, and more. Never add this capability."
        ),
        "references": [
            "https://man7.org/linux/man-pages/man7/capabilities.7.html",
        ],
    },
    "CKV_K8S_41": {
        "severity": "MEDIUM",
        "category": "Service Account",
        "title_tr": "Default service account aktif olarak kullanılıyor",
        "title_en": "Ensure that default service accounts are not actively used",
        "explanation_tr": (
            "Default service account'ın doğrudan kullanılması least-privilege prensibine aykırıdır. "
            "Her workload için spesifik bir service account oluşturulmalı, gerekli minimum RBAC "
            "yetkileri o account'a bağlanmalıdır."
        ),
        "explanation_en": (
            "Using the default service account directly violates least-privilege. "
            "Create a dedicated service account per workload with minimum required RBAC permissions."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/",
        ],
    },
    "CKV_K8S_42": {
        "severity": "MEDIUM",
        "category": "Service Account",
        "title_tr": "Service account otomatik mount edilmiş",
        "title_en": "Ensure that default service accounts are not actively used",
        "explanation_tr": (
            "automountServiceAccountToken: false ayarlanmadan, default service account token "
            "her pod'a otomatik mount edilir. Pod kompromize olursa saldırgan bu token ile "
            "Kubernetes API'sine erişebilir. Açıkça gerekmedikçe false yapılmalıdır."
        ),
        "explanation_en": (
            "Without automountServiceAccountToken: false, the default service account token is "
            "auto-mounted into every pod. If compromised, attackers can access the Kubernetes API. "
            "Set to false unless explicitly required."
        ),
        "references": [
            "https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/",
        ],
    },
    "CKV_K8S_44": {
        "severity": "MEDIUM",
        "category": "Best Practice",
        "title_tr": "Service için 'app' label tanımlanmamış",
        "title_en": "Ensure Services do not forward traffic to pods without an 'app' label selector",
        "explanation_tr": (
            "Service selector'larında 'app' label'ı tanımlanmazsa, yanlış pod'lara trafik "
            "yönlendirilebilir. Bu, hem güvenlik (yanlış servise istek) hem de operasyonel "
            "sorunlara yol açar."
        ),
        "explanation_en": (
            "Without an 'app' label in Service selectors, traffic may be forwarded to wrong pods. "
            "This causes security issues (requests to wrong service) and operational problems."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/",
        ],
    },
    "CKV_K8S_45": {
        "severity": "LOW",
        "category": "Best Practice",
        "title_tr": "Resource için recommended label'lar eksik",
        "title_en": "Ensure that Kubernetes resources have recommended labels",
        "explanation_tr": (
            "app.kubernetes.io/name, app.kubernetes.io/version, app.kubernetes.io/managed-by "
            "gibi standart label'lar eksik olduğunda, resource'ların izlenmesi ve yönetimi zorlaşır. "
            "Audit, monitoring ve troubleshooting süreçleri için gereklidir."
        ),
        "explanation_en": (
            "Without standard labels like app.kubernetes.io/name, version, managed-by, "
            "tracking and managing resources becomes difficult. Required for audit, monitoring, "
            "and troubleshooting."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/",
        ],
    },
    "CKV_K8S_49": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "NetworkPolicy tanımlanmamış",
        "title_en": "Ensure NetworkPolicies are defined",
        "explanation_tr": (
            "NetworkPolicy tanımlanmamış namespace'lerde tüm pod'lar birbirine ve dış dünyaya "
            "kısıtsız iletişim kurabilir. Bir pod kompromize olursa, lateral movement çok kolaylaşır. "
            "Zero-trust prensibiyle, varsayılan deny politikası kurulup gerekli trafiğe explicit "
            "izin verilmelidir."
        ),
        "explanation_en": (
            "Without NetworkPolicy, all pods can communicate freely with each other and outside. "
            "If a pod is compromised, lateral movement is trivial. Apply zero-trust: default-deny "
            "policy with explicit allow rules for required traffic."
        ),
        "references": [
            "https://kubernetes.io/docs/concepts/services-networking/network-policies/",
        ],
    },
    "CKV_K8S_68": {
        "severity": "HIGH",
        "category": "Network Security",
        "title_tr": "Kubelet anonymous-auth aktif",
        "title_en": "Ensure that the --anonymous-auth argument is set to false",
        "explanation_tr": (
            "Kubelet anonymous-auth: true ile yapılandırılırsa, kimliği doğrulanmamış istekler "
            "kabul edilir. Saldırgan herhangi bir credential olmadan kubelet API'ye erişebilir. "
            "Her zaman --anonymous-auth=false olmalıdır."
        ),
        "explanation_en": (
            "If Kubelet is configured with anonymous-auth: true, unauthenticated requests are "
            "accepted. An attacker can access the kubelet API without any credentials. "
            "Always set --anonymous-auth=false."
        ),
        "references": [
            "https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/",
        ],
    },
}


# Terraform kuralları (AWS - en yaygın)
TERRAFORM_RULES = {
    # === S3 Bucket Kuralları ===
    "CKV_AWS_18": {
        "severity": "MEDIUM",
        "category": "Logging & Audit",
        "title_tr": "S3 bucket access logging etkin değil",
        "title_en": "Ensure S3 bucket has access logging enabled",
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
        "title_tr": "S3 bucket sunucu tarafında şifreleme yok",
        "title_en": "Ensure S3 bucket has server-side encryption",
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
        "title_en": "Ensure S3 bucket is not public",
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
        "title_en": "Ensure S3 bucket versioning is enabled",
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
        "title_en": "Ensure security group rules have descriptions",
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
        "title_en": "Ensure SSH is not open to 0.0.0.0/0",
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
        "title_en": "Ensure RDP is not open to 0.0.0.0/0",
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
    # === EBS Encryption ===
    "CKV_AWS_8": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "EBS volume şifrelenmemiş",
        "title_en": "Ensure EBS volume is encrypted",
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
    # === RDS Database ===
    "CKV_AWS_16": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "RDS instance şifrelenmemiş",
        "title_en": "Ensure RDS instance is encrypted",
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
        "title_en": "Ensure RDS instance is not publicly accessible",
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
    # === IAM ===
    "CKV_AWS_40": {
        "severity": "HIGH",
        "category": "Identity & Access",
        "title_tr": "IAM policy kullanıcılara doğrudan atanmış",
        "title_en": "Ensure IAM policies are attached to groups or roles, not users",
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
        "title_en": "Ensure no hardcoded AWS access keys",
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
        "title_en": "Ensure CloudTrail logs are encrypted at rest using KMS CMKs",
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
        "title_en": "Ensure VPC subnets do not assign public IP by default",
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
    # === Ek AWS kuralları ===
    "CKV_AWS_5": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "Elasticsearch domain encryption at rest yok",
        "title_en": "Ensure all data stored in the Elasticsearch is securely encrypted at rest",
        "explanation_tr": (
            "Elasticsearch domain'inde encryption_at_rest = false ise, indekslenen tüm veri "
            "(loglar, dokümanlar, hassas bilgiler) şifrelenmemiş olarak EBS volume'larda saklanır. "
            "AWS infrastructure'a fiziksel erişim sağlayan saldırganlar veriyi okuyabilir."
        ),
        "explanation_en": (
            "With encryption_at_rest = false on Elasticsearch domains, all indexed data "
            "(logs, documents, sensitive info) is stored unencrypted on EBS volumes. "
            "Attackers with physical AWS access can read the data."
        ),
        "references": [
            "https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/encryption-at-rest.html",
        ],
    },
    "CKV_AWS_7": {
        "severity": "MEDIUM",
        "category": "Identity & Access",
        "title_tr": "IAM key rotation 90 günden uzun",
        "title_en": "Ensure IAM password policy requires keys to be rotated every 90 days or less",
        "explanation_tr": (
            "IAM access key'ler 90 günden uzun rotate edilmediğinde, sızdırılmış bir key'in "
            "saldırgan tarafından uzun süre kötüye kullanılma riski büyür. "
            "Düzenli rotation, compromise window'unu kısaltır."
        ),
        "explanation_en": (
            "IAM access keys not rotated within 90 days increase the window for misuse if leaked. "
            "Regular rotation shortens the compromise window."
        ),
        "references": [
            "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html",
        ],
    },
    "CKV_AWS_28": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "DynamoDB tablo encryption at rest yok",
        "title_en": "Ensure DynamoDB tables have point in time recovery enabled",
        "explanation_tr": (
            "DynamoDB tablolarında server_side_encryption.enabled = true olmadığında, "
            "tabloya yazılan tüm hassas veriler şifrelenmemiş şekilde saklanır. "
            "KMS ile encryption-at-rest standart hale gelmelidir."
        ),
        "explanation_en": (
            "Without server_side_encryption.enabled = true on DynamoDB tables, all sensitive data "
            "is stored unencrypted. KMS-based encryption-at-rest should be standard."
        ),
        "references": [
            "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html",
        ],
    },
    "CKV_AWS_33": {
        "severity": "MEDIUM",
        "category": "Logging & Audit",
        "title_tr": "CloudTrail multi-region etkin değil",
        "title_en": "Ensure CloudTrail is enabled in all regions",
        "explanation_tr": (
            "CloudTrail tek region'da çalışırsa, başka region'larda yapılan saldırı aktiviteleri "
            "loglanmaz. is_multi_region_trail = true olmalıdır ki tüm AWS API çağrıları "
            "merkezi olarak kayıt altına alınsın."
        ),
        "explanation_en": (
            "If CloudTrail runs in a single region, attack activities in other regions are not "
            "logged. Set is_multi_region_trail = true to centrally record all AWS API calls."
        ),
        "references": [
            "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/receive-cloudtrail-log-files-from-multiple-regions.html",
        ],
    },
    "CKV_AWS_34": {
        "severity": "HIGH",
        "category": "Network Security",
        "title_tr": "CloudFront viewer protocol HTTPS zorunlu değil",
        "title_en": "Ensure CloudFront distribution ViewerProtocolPolicy is set to HTTPS",
        "explanation_tr": (
            "CloudFront distribution'da viewer_protocol_policy = 'allow-all' ise, HTTP üzerinden "
            "trafik kabul edilir. Bu, MITM saldırılarına ve plaintext credential iletimine yol açar. "
            "'redirect-to-https' veya 'https-only' kullanılmalıdır."
        ),
        "explanation_en": (
            "With viewer_protocol_policy = 'allow-all' on CloudFront, HTTP traffic is accepted, "
            "enabling MITM attacks and plaintext credential exposure. "
            "Use 'redirect-to-https' or 'https-only'."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https.html",
        ],
    },
    "CKV_AWS_45": {
        "severity": "HIGH",
        "category": "Secrets Management",
        "title_tr": "Lambda environment variable'larda hardcoded secret",
        "title_en": "Ensure no hardcoded secrets exist in lambda environment",
        "explanation_tr": (
            "Lambda environment variable'larında API key, password gibi secret'ları tutmak; "
            "Terraform state dosyasında ve AWS console'da plain text olarak görünür hale getirir. "
            "AWS Secrets Manager veya Parameter Store kullanılmalıdır."
        ),
        "explanation_en": (
            "Storing secrets like API keys or passwords in Lambda environment variables exposes "
            "them in Terraform state and AWS console in plain text. "
            "Use AWS Secrets Manager or Parameter Store instead."
        ),
        "references": [
            "https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html",
        ],
    },
    "CKV_AWS_50": {
        "severity": "MEDIUM",
        "category": "Logging & Audit",
        "title_tr": "Lambda X-Ray tracing aktif değil",
        "title_en": "X-Ray tracing is enabled for Lambda",
        "explanation_tr": (
            "Lambda function'larında tracing_config.mode = 'Active' olmadığında, hata ayıklama "
            "ve performans analizi için gerekli trace data eksik kalır. Bu, güvenlik incidentlerinde "
            "forensic analizi zorlaştırır."
        ),
        "explanation_en": (
            "Without tracing_config.mode = 'Active' on Lambda functions, trace data needed for "
            "debugging and performance analysis is missing. This hinders forensic analysis during "
            "security incidents."
        ),
        "references": [
            "https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html",
        ],
    },
    "CKV_AWS_51": {
        "severity": "MEDIUM",
        "category": "Supply Chain",
        "title_tr": "ECR image scanning aktif değil",
        "title_en": "Ensure ECR Image Tags are immutable",
        "explanation_tr": (
            "ECR repository'lerinde image_tag_mutability = 'IMMUTABLE' olmadığında, aynı tag "
            "farklı image'lara işaret edebilir. Bu, supply chain saldırılarına ve "
            "tekrarlanabilirlik sorunlarına yol açar. IMMUTABLE her zaman tercih edilmelidir."
        ),
        "explanation_en": (
            "Without image_tag_mutability = 'IMMUTABLE' on ECR repositories, the same tag may "
            "point to different images, causing supply chain attacks and reproducibility issues. "
            "Always prefer IMMUTABLE."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html",
        ],
    },
    "CKV_AWS_57": {
        "severity": "CRITICAL",
        "category": "Access Control",
        "title_tr": "S3 bucket write erişimi public",
        "title_en": "Ensure S3 bucket does not allow WRITE permissions to authenticated users",
        "explanation_tr": (
            "S3 bucket'a public write izni verilmesi, herhangi birinin (kötü amaçlı veya kazara) "
            "objeleri silmesine, değiştirmesine veya bucket'ı zararlı içerik için kullanmasına izin verir. "
            "Write erişimi sadece spesifik IAM principal'larla sınırlandırılmalıdır."
        ),
        "explanation_en": (
            "Public write access on S3 buckets allows anyone (malicious or accidental) to delete, "
            "modify objects, or use the bucket for harmful content. "
            "Restrict write access to specific IAM principals only."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-best-practices.html",
        ],
    },
    "CKV_AWS_61": {
        "severity": "MEDIUM",
        "category": "Identity & Access",
        "title_tr": "IAM role için trust policy aşırı geniş",
        "title_en": "Ensure IAM role allows only specific services or principals to assume it",
        "explanation_tr": (
            "IAM role'ün assume_role_policy'sinde Principal: '*' veya çok geniş Service tanımı "
            "olduğunda, beklenmeyen AWS servislerinin veya hesapların role'ü üstlenmesine izin verir. "
            "Trust policy en dar şekilde tanımlanmalıdır."
        ),
        "explanation_en": (
            "An IAM role's assume_role_policy with Principal: '*' or overly broad Service "
            "definitions allows unexpected AWS services or accounts to assume the role. "
            "Define trust policies as narrowly as possible."
        ),
        "references": [
            "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html",
        ],
    },
    "CKV_AWS_79": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "EC2 instance IMDSv2 zorunlu değil",
        "title_en": "Ensure Instance Metadata Service Version 2 (IMDSv2) is required",
        "explanation_tr": (
            "metadata_options.http_tokens = 'required' olmadığında IMDSv1 hala kullanılabilir. "
            "IMDSv1, SSRF (Server-Side Request Forgery) saldırılarıyla EC2 credential'larının "
            "çalınmasına izin verir (Capital One ihlali bu yöntemle yaşandı). IMDSv2 token-based "
            "olduğu için bu saldırıları engeller."
        ),
        "explanation_en": (
            "Without metadata_options.http_tokens = 'required', IMDSv1 remains usable. "
            "IMDSv1 enables EC2 credential theft via SSRF attacks (the Capital One breach used this). "
            "IMDSv2 is token-based and prevents such attacks."
        ),
        "references": [
            "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html",
        ],
    },
    "CKV_AWS_103": {
        "severity": "HIGH",
        "category": "Network Security",
        "title_tr": "Load Balancer TLS 1.2'den eski protokol kullanıyor",
        "title_en": "Ensure load balancer is using TLS 1.2",
        "explanation_tr": (
            "Load balancer listener'da TLS 1.0 veya 1.1 kullanmak, BEAST, POODLE gibi bilinen "
            "saldırılara açıktır. Modern SSL policy'leri (ELBSecurityPolicy-TLS-1-2-2017-01 veya "
            "daha yenisi) kullanılmalıdır."
        ),
        "explanation_en": (
            "TLS 1.0 or 1.1 on load balancer listeners is vulnerable to known attacks like BEAST, "
            "POODLE. Use modern SSL policies (ELBSecurityPolicy-TLS-1-2-2017-01 or newer)."
        ),
        "references": [
            "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html",
        ],
    },
    "CKV_AWS_115": {
        "severity": "MEDIUM",
        "category": "Resource Management",
        "title_tr": "Lambda concurrent execution limit tanımlanmamış",
        "title_en": "Ensure that AWS Lambda function is configured for function-level concurrent execution limit",
        "explanation_tr": (
            "reserved_concurrent_executions tanımlanmadığında, tek bir Lambda function tüm hesap "
            "concurrency limit'ini tüketebilir. Bu, diğer function'ların throttle olmasına ve "
            "potansiyel DoS durumuna yol açar."
        ),
        "explanation_en": (
            "Without reserved_concurrent_executions, a single Lambda can consume the entire account "
            "concurrency limit, causing other functions to throttle and potential DoS conditions."
        ),
        "references": [
            "https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html",
        ],
    },
    "CKV_AWS_116": {
        "severity": "MEDIUM",
        "category": "Resource Management",
        "title_tr": "Lambda dead letter queue tanımlanmamış",
        "title_en": "Ensure that AWS Lambda function is configured for a Dead Letter Queue (DLQ)",
        "explanation_tr": (
            "Lambda'da DLQ tanımlanmadığında, başarısız async event'ler kaybolur. "
            "Bu, kritik işlemlerin sessizce başarısız olmasına ve forensic analizin "
            "imkansızlaşmasına yol açar."
        ),
        "explanation_en": (
            "Without a DLQ configured for Lambda, failed async events are lost. "
            "This causes critical operations to silently fail and makes forensic analysis impossible."
        ),
        "references": [
            "https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html",
        ],
    },
    "CKV_AWS_117": {
        "severity": "MEDIUM",
        "category": "Network Security",
        "title_tr": "Lambda VPC içinde çalışmıyor",
        "title_en": "Ensure that AWS Lambda function is configured inside a VPC",
        "explanation_tr": (
            "Hassas backend kaynaklarına (RDS, ElastiCache vb.) erişen Lambda function'lar "
            "VPC dışında çalışırsa, network isolation sağlanamaz. vpc_config bloğu ile "
            "Lambda VPC içine alınmalıdır."
        ),
        "explanation_en": (
            "Lambda functions accessing sensitive backend resources (RDS, ElastiCache, etc.) "
            "outside a VPC lack network isolation. Use vpc_config block to place Lambda in a VPC."
        ),
        "references": [
            "https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html",
        ],
    },
    "CKV_AWS_158": {
        "severity": "HIGH",
        "category": "Encryption",
        "title_tr": "CloudWatch log group encryption yok",
        "title_en": "Ensure that CloudWatch Log Group is encrypted by KMS",
        "explanation_tr": (
            "CloudWatch log group'larda kms_key_id tanımlanmadığında, loglar default şifreleme ile "
            "saklanır. Hassas application logları için customer-managed KMS key ile encryption "
            "ek bir güvenlik katmanı sağlar."
        ),
        "explanation_en": (
            "Without kms_key_id on CloudWatch log groups, logs use default encryption. "
            "For sensitive application logs, customer-managed KMS key encryption provides "
            "an additional security layer."
        ),
        "references": [
            "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html",
        ],
    },
}


# Bilmediğimiz kurallar için fallback
FALLBACK_RULE = {
    "severity": "MEDIUM",
    "category": "Security",
    "title_tr": None,
    "title_en": None,
    "explanation_tr": "Bu güvenlik kontrolü başarısız oldu. Detaylar için referans linklerini inceleyin.",
    "explanation_en": "This security check has failed. See reference links for details.",
    "references": [],
}
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
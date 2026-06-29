# InfraGuard Studio

Web tabanlı interaktif **IaC (Infrastructure as Code) güvenlik denetim platformu**. Dockerfile, Kubernetes manifest ve Terraform dosyalarınızı saniyeler içinde tarar; Türkçe açıklamalı bulgular, otomatik düzeltme önerileri ve CI/CD pipeline snippet'leri sunar.

**Canlı Demo:** [https://infraguard.muhammedasef.com](https://infraguard.muhammedasef.com)

---

## Öne Çıkan Özellikler

### Çok Katmanlı Tarama
- **3 dosya tipi desteği**: Dockerfile, Kubernetes YAML, Terraform (HCL)
- **Çift mod**: Tek dosya yapıştırma + **çoklu dosya tarama (zip upload)**
- **Checkov 3.x entegrasyonu** ile 1000+ güvenlik kuralı
- **Hardcoded secret tespiti** (`detect-secrets` framework)
- Sandbox edilmiş izole tarama (geçici UUID dizinleri, shell injection koruması, zip slip koruması)

### Hibrit Akıllı Açıklama Sistemi
- **Statik knowledge base**: 87+ kural için manuel Türkçe açıklama ve gerçek dünya örnekleri (Capital One, BlueKeep vb.)
- **LLM Fallback**: Bilinmeyen kurallar için **OpenAI GPT-4o-mini** ile dinamik Türkçe açıklama üretimi
- **4 katmanlı koruma**: Kalıcı JSON cache, günlük bütçe limiti, IP başına saatlik rate limit, OpenAI hard limit

### Otomatik Düzeltme Engine
- **36 kural için otomatik düzeltme** (USER root, latest tag, privileged container, public S3 bucket, IMDSv2, hostNamespaces vb.)
- **Monaco Diff Editor** ile yan yana Before/After karşılaştırma
- Tek tıkla kopyalama

### Multi-File Repo Tarama
- **Zip upload** — kullanıcı bir IaC repo zip'i yükler, tüm dosyalar otomatik tipi tespit edilip taranır
- **Per-file breakdown** — her dosyanın risk skoru, severity dağılımı ve bulgu listesi ayrı görüntülenir
- **En riskli dosya üstte** sıralama
- Güvenlik: max 10MB zip, max 50 dosya, zip slip path traversal koruması

### Tarama Geçmişi (Browser Storage)
- Son 20 tarama tarayıcıda lokal olarak saklanır
- Tek tıkla yeniden açma
- **Gizlilik öncelikli tasarım**: kullanıcı kodu hiçbir yerde saklanmaz, sadece sonuç özeti

### CI/CD Pipeline Snippet Üretici
- Her tarama sonucunda **GitLab CI** ve **GitHub Actions** için hazır job snippet'i
- "Bul ve bildir"den "üretime entegre et"e DevSecOps tam döngüsü

### Kurumsal PDF Rapor
- **ReportLab** ile profesyonel PDF raporu üretimi
- **DejaVu Sans font** ile tam Türkçe karakter desteği
- Risk skoru, severity dağılımı, her bulgu için detaylı kart
- AI ile zenginleştirilen bulgular `[AI]` rozetli

### Mobile Responsive
- Hero, stats row, finding cards, diff viewer, sample selector — hepsi mobile-first tasarım
- Monaco diff editor mobilde otomatik dikey (alt alta) moda geçer

---

## Mimari

İstek akışı:

**Frontend (React + Vite + Monaco)** → HTTPS → **Nginx (Reverse Proxy + Security Headers + SSL)** → **FastAPI Backend (systemd)** → **Scanner (Checkov) + Normalizer (LLM Layer) + Fix Engine + PDF Generator**

### Backend
- **Python 3.12** + **FastAPI** + **Uvicorn**
- **Checkov 3.3** (multi-framework: dockerfile, kubernetes, terraform, secrets)
- **OpenAI 2.x** (GPT-4o-mini)
- **ReportLab** (PDF üretimi)
- **Pydantic v2** (request validation)
- **python-multipart** (file upload)

### Frontend
- **React 19** + **Vite**
- **Tailwind CSS v4**
- **Monaco Editor** (VS Code editor, syntax highlighting + diff viewer)
- **Browser localStorage** (tarama geçmişi)
- **Oxlint**

### Altyapı
- **Ubuntu 24 VPS** + **Nginx 1.24** + **Let's Encrypt SSL**
- **Cloudflare DNS**
- **systemd service** (auto-restart, isolation)

---

## CI/CD Pipeline

Her commit, **6 aşamalı bir DevSecOps gate**'inden geçer:

### 1. Security Scan (Paralel, ~45s)

| Tool | Görev |
|------|-------|
| **Gitleaks** | Sızdırılmış API key, password, token taraması (tüm commit geçmişi) |
| **Trivy** | Dependency CVE + IaC misconfiguration taraması (SARIF → GitHub Security) |
| **Hadolint** | Dockerfile linting (mevcutsa) |
| **InfraGuard Self-Scan** | **Dogfood pattern** — proje kendi kendisini Checkov ile tarar |

### 2. Deploy to Production
- Security gate yeşil olursa otomatik tetiklenir
- SSH ile VPS'e bağlanır, `deploy.sh` script çalıştırır
- Git pull → backend reinstall → frontend rebuild → systemd restart
- ~20 saniye

### 3. DAST Scan (OWASP ZAP)
- Deploy tamamlandıktan sonra **canlı siteye** baseline scan
- HTTP security headers, XSS potansiyel, CORS misconfiguration
- HTML rapor + JSON + SARIF artifact olarak 30 gün saklanır

---

## Güvenlik Tasarımı

### Backend Hardening
- **Sandbox**: Her tarama izole UUID dizininde, geçici dosyalarla
- **Subprocess güvenliği**: `shell=False`, 30s timeout, `sys.executable` ile path injection engelleme
- **Concurrency limit**: `Semaphore(2)` — DoS koruması
- **Input validation**: 50KB dosya boyutu limiti, null byte kontrolü, file type whitelist
- **Zip slip koruması**: Zip extraction'da path traversal engellenmiş

### LLM Cost Exhaustion Koruması (4 katman)
1. **Persistent cache** — Aynı kural için tek çağrı
2. **Daily budget** — Sunucu seviyesi günlük çağrı limiti
3. **IP rate limit** — Saatte 5 yeni kural/IP
4. **OpenAI hard limit** — Hesap seviyesi $5 cap

### Network Security
- **HTTPS only** (Let's Encrypt, otomatik yenileme)
- **Sıkılaştırılmış CSP**: `script-src` direktifinden `unsafe-inline` kaldırıldı (sadece Monaco için zorunlu `unsafe-eval` kabul edildi)
- **HSTS, X-Frame-Options, COEP/COOP/CORP** header'ları
- **CORS whitelist** (sadece izinli origin'ler)
- **Cloudflare DNS** (DDoS koruması mevcut)

### Veri Saklama Politikası
- **Kullanıcı kodu hiçbir yerde kalıcı saklanmaz** — tarama sonrası geçici dizin tamamen silinir
- **LLM çağrılarında kod gönderilmez** — sadece check_id ve context
- **Tarama geçmişi** kullanıcının kendi tarayıcısında localStorage'da (sunucuya hiçbir şey yazılmaz)

### Pipeline Security
- **SSH key GitHub Secrets'ta**, asla kodda değil
- **Workflow permissions** minimum yetkili (least privilege)
- **SARIF upload** otomatik GitHub Security tab'ine

---

## Proje İstatistikleri

| Metrik | Değer |
|---|---|
| Desteklenen IaC formatı | 3 (Dockerfile, Kubernetes, Terraform) |
| Güvenlik kuralı sayısı | 1000+ (Checkov 3.x) |
| Türkçe knowledge base | 87+ kural |
| Otomatik düzeltme fonksiyonu | 36 |
| Tarama modu | 2 (tek dosya + zip upload) |
| Hazır demo dosyası | 10 |
| Production deploy süresi | ~5 dakika (commit → live) |

## Yazar

**Muhammed Asef** — Aspiring DevSecOps Engineer

[muhammedasef.com](https://muhammedasef.com) · [LinkedIn](https://linkedin.com/in/muhammedasef) · [GitHub](https://github.com/MuhammedAsef)

---

## Lisans

MIT License — bkz. [LICENSE](LICENSE)
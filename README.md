# 🛡️ InfraGuard Studio

Web tabanlı interaktif **IaC (Infrastructure as Code) güvenlik denetim platformu**. Dockerfile, Kubernetes manifest ve Terraform dosyalarınızı saniyeler içinde tarar; Türkçe açıklamalı bulgular, otomatik düzeltme önerileri ve CI/CD pipeline snippet'leri sunar.

🌐 **Canlı Demo:** [https://infraguard.muhammedasef.com](https://infraguard.muhammedasef.com)

---

## ✨ Öne Çıkan Özellikler

### 🔍 Çok Katmanlı Tarama
- **3 dosya tipi desteği**: Dockerfile, Kubernetes YAML, Terraform (HCL)
- **Checkov 3.x entegrasyonu** ile 1000+ güvenlik kuralı
- **Hardcoded secret tespiti** (`detect-secrets` framework)
- Sandbox edilmiş izole tarama (geçici UUID dizinleri, shell injection koruması)

### 🤖 Hibrit Akıllı Açıklama Sistemi
- **Statik knowledge base**: 45+ kural için manuel Türkçe açıklama ve gerçek dünya örnekleri (Capital One, BlueKeep vb.)
- **LLM Fallback**: Bilinmeyen kurallar için **OpenAI GPT-4o-mini** ile dinamik Türkçe açıklama üretimi
- **4 katmanlı koruma**: Kalıcı JSON cache, günlük bütçe limiti, IP başına saatlik rate limit, input token limiti

### 🔧 Otomatik Düzeltme Engine
- **15 yüksek-etkili kural** için otomatik düzeltme (USER root, latest tag, privileged container, public S3 bucket vb.)
- **Monaco Diff Editor** ile yan yana Before/After karşılaştırma
- Tek tıkla kopyalama

### ⚙️ CI/CD Pipeline Snippet Üretici
- Her tarama sonucunda **GitLab CI** ve **GitHub Actions** için hazır job snippet'i
- "Bul ve bildir"den "üretime entegre et"e DevSecOps tam döngüsü

### 📄 Kurumsal PDF Rapor
- **ReportLab** ile profesyonel PDF raporu üretimi
- Risk skoru, severity dağılımı, her bulgu için detaylı kart
- AI ile zenginleştirilen bulgular `[AI]` rozetli

---

## 🏗️ Mimari

İstek akışı:

**Frontend (React + Vite + Monaco)** → HTTPS → **Nginx (Reverse Proxy + Security Headers + SSL)** → **FastAPI Backend (systemd)** → **Scanner (Checkov) + Normalizer (LLM Layer) + Fix Engine + PDF Generator**

### Backend
- **Python 3.12** + **FastAPI** + **Uvicorn**
- **Checkov 3.3** (multi-framework: dockerfile, kubernetes, terraform, secrets)
- **OpenAI 2.x** (GPT-4o-mini)
- **ReportLab** (PDF üretimi)
- **Pydantic v2** (request validation)

### Frontend
- **React 19** + **Vite** + **TypeScript-ready**
- **Tailwind CSS v4**
- **Monaco Editor** (VS Code editor, syntax highlighting + diff viewer)
- **Oxlint**

### Altyapı
- **Ubuntu 24 VPS** + **Nginx 1.24** + **Let's Encrypt SSL**
- **Cloudflare DNS**
- **systemd service** (auto-restart, isolation)

---

## 🚀 CI/CD Pipeline

Her commit, **6 aşamalı bir DevSecOps gate**'inden geçer:

### 1. Security Scan (Paralel, ~45s)

| Tool | Görev |
|------|-------|
| **Gitleaks** | Sızdırılmış API key, password, token taraması (tüm commit geçmişi) |
| **Trivy** | Dependency CVE + IaC misconfiguration taraması (SARIF → GitHub Security) |
| **Hadolint** | Dockerfile linting (mevcutsa) |
| **InfraGuard Self-Scan** ⭐ | **Dogfood pattern** — proje kendi kendisini Checkov ile tarar |

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

## 🔒 Güvenlik Tasarımı

### Backend Hardening
- **Sandbox**: Her tarama izole UUID dizininde, geçici dosyalarla
- **Subprocess güvenliği**: `shell=False`, 30s timeout, `sys.executable` ile path injection engelleme
- **Concurrency limit**: `Semaphore(2)` — DoS koruması
- **Input validation**: 50KB dosya boyutu limiti, null byte kontrolü, file type whitelist

### LLM Cost Exhaustion Koruması (4 katman)
1. **Persistent cache** — Aynı kural için tek çağrı
2. **Daily budget** — Sunucu seviyesi günlük çağrı limiti
3. **IP rate limit** — Saatte 5 yeni kural/IP
4. **OpenAI hard limit** — Hesap seviyesi $5 cap

### Network Security
- **HTTPS only** (Let's Encrypt, otomatik yenileme)
- **HSTS, CSP, X-Frame-Options, COEP/COOP/CORP** header'ları
- **CORS whitelist** (sadece izinli origin'ler)
- **Cloudflare DNS** (DDoS koruması mevcut)

### Pipeline Security
- **SSH key GitHub Secrets'ta**, asla kodda değil
- **Workflow permissions** minimum yetkili (least privilege)
- **SARIF upload** otomatik GitHub Security tab'ine

---

## 📊 Mülakat Anlatım Noktaları

> "Bu proje **DevSecOps döngüsünün tamamını** kapsıyor. Sadece bir scanner yazmadım — scanner'ı production'a koydum, kendi pipeline'ımda kendisini kullanıyorum (dogfood pattern), CSP gibi tradeoff'ları bilinçli olarak yönettim, LLM cost exhaustion saldırılarına karşı 4 katmanlı bir savunma kurdum. Her commit otomatik 4 farklı güvenlik aracından geçiyor, raporlar SARIF formatında GitHub Security tab'inde toplanıyor."

---

## 🧑‍💻 Yazar

**Muhammed Asef** — Aspiring DevSecOps Engineer

🌐 [muhammedasef.com](https://muhammedasef.com) · 💼 [LinkedIn](https://linkedin.com/in/muhammedasef) · 🐙 [GitHub](https://github.com/MuhammedAsef)

---

## 📜 Lisans

MIT License — bkz. [LICENSE](LICENSE)
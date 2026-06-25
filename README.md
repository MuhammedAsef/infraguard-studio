# 🛡️ InfraGuard Studio

> Web tabanlı interaktif IaC (Infrastructure as Code) güvenlik denetim platformu.

Dockerfile, Kubernetes manifest, Docker Compose ve Terraform dosyalarındaki güvenlik açıklarını anında tespit eden, geliştiricinin anlayacağı dilde açıklayan ve düzeltme önerileri sunan açık kaynak DevSecOps aracı.

## 🎯 Projenin Amacı

DevSecOps'un en önemli prensiplerinden biri **Shift-Left Security** — yani güvenliği yazılım geliştirme yaşam döngüsünün en erken aşamasına çekmek. Kod henüz production'a deploy edilmeden, hatta merge edilmeden önce güvenlik açıklarını yakalamak.

Checkov gibi güçlü açık kaynak araçlar var ama CLI çıktıları junior/orta seviye geliştiriciler için anlaşılması zor. InfraGuard Studio bu boşluğu kapatmayı hedefliyor:

- **Görsel ve interaktif deneyim** — Monaco Editor ile VS Code benzeri kod düzenleme
- **Türkçe/İngilizce açıklamalar** — "CKV_DOCKER_8" yerine "Container root kullanıcıyla çalışırsa, bir saldırgan container'dan kaçmayı başardığında host sisteme root erişimi elde edebilir."
- **Risk skorlama** — 0-100 arası genel güvenlik skoru
- **Severity dağılımı** — Critical / High / Medium / Low görsel olarak
- **Referans linkler** — Her bulgu için CIS Benchmark, OWASP ve resmi Docker dokümantasyon linkleri

## 🚀 Özellikler

- ✅ **Dockerfile tarama** — Container hardening, supply chain ve best practice kontrolleri
- ✅ **Monaco Editor** — VS Code'un editörü, syntax highlighting ile
- ✅ **Hazır demo dosyaları** — Tek tıkla insecure/secure örnekleri deneyin
- ✅ **Sandbox güvenliği** — Kullanıcı kodu izole geçici dizinde işlenir, kalıcı saklanmaz
- ✅ **Concurrency koruması** — Aynı anda max 2 tarama (VPS kaynak koruması)
- ✅ **Timeout & rate limiting** — DoS koruması
- 🔜 **Kubernetes, Docker Compose, Terraform** desteği (Faz 2)
- 🔜 **Before/After diff** — Düzeltilmiş kodu yan yana göster (Faz 2)
- 🔜 **CI/CD gate snippet** — Pipeline'a nasıl entegre edileceği önerisi (Faz 2)
- 🔜 **PDF rapor export** (Faz 3)

## 🛠️ Teknoloji Yığını

### Frontend
- **React 19** — UI framework
- **Vite** — Build tool ve dev server
- **Tailwind CSS v4** — Utility-first CSS
- **Monaco Editor** — VS Code'un kod editörü

### Backend
- **Python 3.14** — Backend dili
- **FastAPI** — Async Python web framework
- **Checkov** — IaC güvenlik tarayıcısı (1000+ kural)
- **Pydantic** — Veri doğrulama

### DevSecOps
- **Sandbox isolation** — UUID temp dizinler, sabit dosya adları
- **subprocess güvenliği** — shell=False, allowlisted arguments, minimal env
- **Async concurrency** — asyncio.Semaphore ile yük yönetimi

## 📦 Kurulum

### Gereksinimler

- Python 3.11+
- Node.js 20+
- npm

### Backend Kurulumu

    cd backend
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload --port 8000

Backend çalışıyor: http://localhost:8000

API docs (Swagger): http://localhost:8000/docs

### Frontend Kurulumu

    cd frontend
    npm install
    npm run dev

Frontend çalışıyor: http://localhost:5173

## 🏗️ Mimari

    ┌────────────────┐         ┌──────────────────┐         ┌─────────────┐
    │  React + Vite  │ ──────▶ │  FastAPI Backend │ ──────▶ │   Checkov   │
    │  Monaco Editor │  HTTP   │     (Async)      │ subproc │    (CLI)    │
    └────────────────┘         └──────────────────┘         └─────────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │    Normalizer    │
                               │ + Knowledge Base │
                               │   (TR/EN i18n)   │
                               └──────────────────┘

### Güvenlik Tasarım Kararları

1. **Dosya adı kullanıcıdan alınmaz** — Path traversal önlemi olarak backend sabit isim verir (Dockerfile)
2. **shell=False** — subprocess command injection önlemi
3. **UUID temp dizinler** — Her tarama izole, bitince shutil.rmtree ile silinir
4. **Timeout** — Max 30 saniye, kaynak tüketimi önlemi
5. **Boyut limiti** — Max 50KB dosya
6. **Concurrency** — asyncio.Semaphore(2) ile aynı anda max 2 tarama
7. **--download-external-modules false** — SSRF önlemi
8. **Minimal subprocess env** — Ortam değişkeni sızıntısı önlemi

## 📊 API Endpoint'leri

| Method | Endpoint        | Açıklama                       |
|--------|-----------------|--------------------------------|
| POST   | /api/scan       | IaC dosyasını tara             |
| GET    | /api/samples    | Hazır demo dosyalarını getir   |
| GET    | /api/health     | Sağlık kontrolü                |
| GET    | /api/version    | Scanner versiyonları           |

Detaylı API dokümantasyonu için backend çalışırken http://localhost:8000/docs adresini ziyaret edin.

## 🗺️ Yol Haritası

- [x] **Faz 1** — Dockerfile tarama + risk skoru + Monaco Editor (MVP)
- [ ] **Faz 2** — Kubernetes, Docker Compose, Terraform desteği
- [ ] **Faz 2** — Before/After diff ve düzeltme önerileri
- [ ] **Faz 2** — CI/CD gate snippet önerileri (GitLab/GitHub Actions)
- [ ] **Faz 3** — PDF rapor export
- [ ] **Faz 3** — Hadolint ve Trivy entegrasyonu
- [ ] **Faz 4** — Policy-as-Code modu (OPA/Rego, Kyverno)

## 🎓 Neden Bu Proje?

DevSecOps kariyerime yönelik üçüncü portfolyo projem. Diğerleri:

1. **AI Destekli Zafiyet Yönetim Paneli** (Python CLI) — Nuclei + Nmap + LLM destekli remediation
2. **DevSecOps Portfolyo Sitesi** (Next.js) — SonarCloud + Trivy + ZAP entegre CI/CD
3. **InfraGuard Studio** (Bu proje) — Deploy öncesi IaC güvenlik gate'i

Bu üçü birlikte DevSecOps yaşam döngüsünün tüm aşamalarını kapsıyor: **tespit → güvenli geliştirme → deployment öncesi denetim**.

## 📝 Lisans

MIT

## 👤 Yazar

**Muhammed Asef**

Aspiring DevSecOps Engineer

[LinkedIn](https://www.linkedin.com/in/muhammedasef/) • [GitHub](https://github.com/MuhammedAsef)
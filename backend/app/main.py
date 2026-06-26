import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import scan, samples, health

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="InfraGuard Studio API",
    description="IaC Security Auditor Backend",
    version="0.1.0",
)

# CORS middleware - frontend farklı origin'de çalışacağı için gerekli
# Production'da sadece whitelist'teki origin'ler API'ye erişebilir
# Dev için localhost, prod için canlı subdomain
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,https://infraguard.muhammedasef.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    max_age=600,
)

# Router'ları ekle - hepsi /api prefix'i altında
app.include_router(scan.router, prefix="/api")
app.include_router(samples.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/")
async def root():
    """Ana sayfa - API hakkında bilgi."""
    return {
        "name": "InfraGuard Studio API",
        "version": "0.1.0",
        "docs": "/docs",
    }
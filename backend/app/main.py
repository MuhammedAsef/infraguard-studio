from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import scan, samples, health

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="InfraGuard Studio API",
    description="IaC Security Auditor Backend",
    version="0.1.0",
)

# CORS middleware - frontend farklı portta çalışacağı için gerekli
# React varsayılan olarak 5173 portunda, backend 8000'de çalışıyor
# CORS olmadan tarayıcı isteği bloklar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için. Production'da domain ile sınırlandırılacak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
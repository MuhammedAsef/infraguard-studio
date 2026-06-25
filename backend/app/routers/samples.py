from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# Hazır demo Dockerfile'lar - "Örnek Dene" butonları için
SAMPLES = [
    {
        "id": "dockerfile-insecure-web",
        "file_type": "dockerfile",
        "title": "Güvenliksiz Web Uygulaması",
        "title_en": "Insecure Web Application",
        "description": "Root kullanıcı, latest tag, HEALTHCHECK yok",
        "code": """FROM node:latest

RUN apt-get update
RUN apt-get install -y curl wget

ADD . /app
WORKDIR /app

RUN npm install

USER root

EXPOSE 3000 22

CMD ["node", "server.js"]
""",
    },
    {
        "id": "dockerfile-insecure-python",
        "file_type": "dockerfile",
        "title": "Güvenliksiz Python API",
        "title_en": "Insecure Python API",
        "description": "Root kullanıcı, pip cache temizlenmemiş, secret environment variable",
        "code": """FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DATABASE_PASSWORD=super_secret_123
ENV API_KEY=sk-1234567890abcdef

USER root

EXPOSE 8000 5432

CMD ["python", "main.py"]
""",
    },
    {
        "id": "dockerfile-secure-example",
        "file_type": "dockerfile",
        "title": "Güvenli Dockerfile Örneği",
        "title_en": "Secure Dockerfile Example",
        "description": "Best practice uygulanmış, karşılaştırma için",
        "code": """FROM node:18.20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .

FROM node:18.20-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app .

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
""",
    },
]


class SampleFile(BaseModel):
    """Demo dosya formatı"""
    id: str
    file_type: str
    title: str
    title_en: str
    description: str
    code: str


@router.get("/samples", response_model=list[SampleFile])
async def get_samples():
    """Hazır demo dosyalarını dön."""
    return SAMPLES
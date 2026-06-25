from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


SAMPLES = [
    # === DOCKERFILE ÖRNEKLERİ ===
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
        "description": "Root, hardcoded secrets, latest tag",
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
        "description": "Best practice uygulanmış",
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

    # === KUBERNETES ÖRNEKLERİ ===
    {
        "id": "kubernetes-insecure-deployment",
        "file_type": "kubernetes",
        "title": "Güvenliksiz K8s Deployment",
        "title_en": "Insecure K8s Deployment",
        "description": "Privileged, root user, resource limit yok",
        "code": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: vulnerable-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vulnerable-app
  template:
    metadata:
      labels:
        app: vulnerable-app
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        securityContext:
          privileged: true
          allowPrivilegeEscalation: true
          runAsUser: 0
""",
    },
    {
        "id": "kubernetes-insecure-pod",
        "file_type": "kubernetes",
        "title": "Güvenliksiz K8s Pod",
        "title_en": "Insecure K8s Pod",
        "description": "Probe yok, securityContext yok, default namespace",
        "code": """apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: web
    image: nginx:latest
    ports:
    - containerPort: 80
""",
    },
    {
        "id": "kubernetes-secure-example",
        "file_type": "kubernetes",
        "title": "Güvenli K8s Deployment",
        "title_en": "Secure K8s Deployment",
        "description": "Hardened pod, probes, resource limits",
        "code": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: myapp:1.2.3
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
""",
    },

    # === TERRAFORM ÖRNEKLERİ ===
    {
        "id": "terraform-insecure-s3",
        "file_type": "terraform",
        "title": "Güvenliksiz S3 Bucket",
        "title_en": "Insecure S3 Bucket",
        "description": "Public, şifrelenmemiş, versioning yok",
        "code": """resource "aws_s3_bucket" "data" {
  bucket = "my-company-data"
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
""",
    },
    {
        "id": "terraform-insecure-sg",
        "file_type": "terraform",
        "title": "Güvenliksiz Security Group",
        "title_en": "Insecure Security Group",
        "description": "SSH ve RDP dünyaya açık",
        "code": """resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
""",
    },
    {
        "id": "terraform-insecure-rds",
        "file_type": "terraform",
        "title": "Güvenliksiz RDS Database",
        "title_en": "Insecure RDS Database",
        "description": "Public, şifrelenmemiş, hardcoded password",
        "code": """resource "aws_db_instance" "main" {
  identifier             = "production-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20

  db_name  = "appdb"
  username = "admin"
  password = "super_secret_password_123"

  publicly_accessible    = true
  storage_encrypted      = false
  backup_retention_period = 0
  skip_final_snapshot    = true
}
""",
    },
    {
        "id": "terraform-secure-example",
        "file_type": "terraform",
        "title": "Güvenli Terraform Örneği",
        "title_en": "Secure Terraform Example",
        "description": "Encrypted, private, hardened",
        "code": """resource "aws_s3_bucket" "data" {
  bucket = "my-company-data-secure"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "data" {
  bucket = aws_s3_bucket.data.id

  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "log/"
}

resource "aws_s3_bucket" "logs" {
  bucket = "my-company-data-secure-logs"
}
""",
    },
]


class SampleFile(BaseModel):
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
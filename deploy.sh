#!/bin/bash
# InfraGuard Studio - Production Deploy Script
# GitHub Actions tarafindan otomatik calistirilir

set -e

echo "=== InfraGuard deploy basliyor ==="
cd /opt/infraguard-studio

echo "[1/5] GitHub'dan son kodlari cekiyorum..."
git pull

echo "[2/5] Backend bagimliliklarini guncelliyorum..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
deactivate

echo "[3/5] Frontend bagimliliklarini guncelliyorum..."
cd ../frontend
npm install --silent

echo "[4/5] Frontend production build aliyorum..."
npm run build

echo "[5/5] Backend service'ini yeniden basliyorum..."
systemctl restart infraguard-backend

echo ""
echo "=== Deploy tamamlandi ==="
echo "URL: https://infraguard.muhammedasef.com"
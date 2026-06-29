\# Nginx Configuration



Production Nginx config dosyası. CSP, SSL, security header'lar ve API proxy yapılandırması içerir.



\## Kurulum (Yeni VPS)



```bash

\# Config'i sembolik link olarak yerleştir

sudo cp infraguard.conf /etc/nginx/sites-available/infraguard

sudo ln -s /etc/nginx/sites-available/infraguard /etc/nginx/sites-enabled/



\# SSL sertifikası (Let's Encrypt)

sudo certbot --nginx -d infraguard.muhammedasef.com



\# Test ve reload

sudo nginx -t

sudo systemctl reload nginx

```



\## Güvenlik Header'ları



\- \*\*Content-Security-Policy\*\*: Script ve style kaynakları kısıtlandı (unsafe-inline script kaldırıldı, unsafe-eval Monaco için kabul edilmiş tradeoff)

\- \*\*HSTS\*\*: HTTPS zorla, 1 yıl

\- \*\*X-Frame-Options\*\*: DENY (clickjacking koruması)

\- \*\*X-Content-Type-Options\*\*: nosniff (MIME-sniff koruması)

\- \*\*Referrer-Policy\*\*: strict-origin-when-cross-origin

\- \*\*Permissions-Policy\*\*: kamera/mikrofon/lokasyon/ödeme/USB devre dışı

\- \*\*COOP/COEP/CORP\*\*: Cross-origin isolation



\## Güncelleme



Production'da CSP veya başka bir header değişikliği yapıldığında, bu dosyayı da güncelleyip commit et.


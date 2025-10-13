# 🚀 Deployment Rehberi

## Railway.app ile Deployment (ÖNERİLEN)

### 1. Hazırlık

```bash
# Git repository oluştur (yoksa)
git init
git add .
git commit -m "Initial commit"
```

### 2. Railway.app'e Deploy

1. **Railway.app'e Git:** https://railway.app/
2. **GitHub ile Giriş Yap**
3. **New Project** → **Deploy from GitHub repo**
4. **Repository'yi Seç**
5. **Deploy**

### 3. Environment Variables Ekle

Railway dashboard'da **Variables** sekmesinde:

```
SUPABASE_URL=https://rkjndkslanwyoyefsicd.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=8501
```

### 4. Domain Ayarla

**Settings** → **Networking** → **Generate Domain**

---

## Render.com ile Deployment (ALTERNATIF)

### 1. Render.com'a Git
https://render.com/

### 2. New Web Service

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `bash start_railway.sh`

### 3. Environment Variables

```
SUPABASE_URL=https://rkjndkslanwyoyefsicd.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=8501
```

---

## VPS Deployment (Manuel)

### 1. VPS Satın Al
- Digital Ocean: https://www.digitalocean.com/
- Linode: https://www.linode.com/
- AWS EC2: https://aws.amazon.com/ec2/

### 2. Sunucuya Bağlan

```bash
ssh root@your-server-ip
```

### 3. Sistemi Kur

```bash
# Python ve pip kur
apt update
apt install python3 python3-pip git -y

# Projeyi klonla
git clone <your-repo-url>
cd tarama

# Bağımlılıkları kur
pip3 install -r requirements.txt

# Sistemi başlat
chmod +x start_production.sh
./start_production.sh
```

### 4. Systemd Service (Otomatik Başlatma)

```bash
nano /etc/systemd/system/crypto-scanner.service
```

İçeriği:
```ini
[Unit]
Description=Crypto Signal Scanner
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/tarama
ExecStart=/bin/bash /root/tarama/start_production.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktif et:
```bash
systemctl enable crypto-scanner
systemctl start crypto-scanner
systemctl status crypto-scanner
```

---

## Nginx ile Reverse Proxy (VPS için)

```bash
# Nginx kur
apt install nginx -y

# Config dosyası oluştur
nano /etc/nginx/sites-available/crypto-scanner
```

İçeriği:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Aktif et:
```bash
ln -s /etc/nginx/sites-available/crypto-scanner /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

---

## SSL Sertifikası (Let's Encrypt)

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## Monitoring

### Log Kontrolü

**Railway/Render:**
- Dashboard'da **Logs** sekmesi

**VPS:**
```bash
# Gerçek zamanlı loglar
tail -f scanner.log

# Systemd logları
journalctl -u crypto-scanner -f
```

### Health Check

```bash
# Dashboard çalışıyor mu?
curl http://localhost:8501

# Scanner çalışıyor mu?
ps aux | grep scanner_core_dual.py
```

---

## Güncelleme

**Railway/Render:**
```bash
git add .
git commit -m "Update"
git push
# Otomatik deploy olur
```

**VPS:**
```bash
cd /root/tarama
git pull
systemctl restart crypto-scanner
```

---

## Tavsiyeler

1. **Monitoring:** UptimeRobot (ücretsiz) ile uptime izle
2. **Backup:** Supabase otomatik backup yapıyor
3. **Logs:** Railway/Render/VPS loglarını düzenli kontrol et
4. **Maliyet:** 
   - Railway: İlk 500 saat ücretsiz, sonra ~$5/ay
   - Render: Ücretsiz plan yavaş, Pro ~$7/ay
   - VPS: Digital Ocean ~$6/ay

---

## Sorun Giderme

### "Connection to remote host was lost"
- Normal, TradingView rate limit
- Scanner devam eder

### "ModuleNotFoundError"
- `pip install -r requirements.txt` çalıştır

### Dashboard açılmıyor
- PORT environment variable'ını kontrol et
- Logs'a bak

### Scanner durmuş
- Sistemd servisi restart et (VPS)
- Railway/Render otomatik restart yapar

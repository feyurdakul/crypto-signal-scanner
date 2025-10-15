# 🔐 GitHub Secrets Kurulum Rehberi

## 📋 Gerekli Secrets

Aşağıdaki 3 secret'ı GitHub repository'ne eklemeniz gerekiyor:

### 1️⃣ VERCEL_TOKEN

**Nasıl Alınır:**

```bash
# Terminal'de:
vercel login
vercel token create github-actions
```

**Veya Web UI ile:**
1. https://vercel.com/account/tokens
2. "Create" butonuna tıkla
3. Token name: `github-actions-deploy`
4. Scope: **Full Account**
5. Expiration: **No Expiration**
6. Token'ı kopyala ⚠️ (bir daha gösterilmeyecek!)

---

### 2️⃣ VERCEL_PROJECT_ID

```
prj_AYrjVcXkYM7vMr7bkddkD6hiDWkJ
```

*(Bu değer `.vercel/project.json` dosyasından alındı)*

---

### 3️⃣ VERCEL_ORG_ID

```
team_iJMVCPwVXbbzVbJxkU6WQcnR
```

*(Bu değer `.vercel/project.json` dosyasından alındı)*

---

## 🔧 GitHub'a Secrets Ekleme

### Adım 1: GitHub Repository'ye Git
https://github.com/feyurdakul/crypto-signal-scanner

### Adım 2: Settings
Repository üst menüsünden **Settings** sekmesine tıkla

### Adım 3: Secrets and Variables
Sol menüden **Secrets and variables** → **Actions** seçeneğine tıkla

### Adım 4: Secrets Ekle

Her biri için:
1. **New repository secret** butonuna tıkla
2. **Name** alanına secret adını yaz (yukarıdaki isimlerle aynı)
3. **Secret** alanına değeri yapıştır
4. **Add secret** butonuna tıkla

#### Eklenecek Secrets:

| Name | Value |
|------|-------|
| `VERCEL_TOKEN` | *(Vercel'den aldığın token)* |
| `VERCEL_PROJECT_ID` | `prj_AYrjVcXkYM7vMr7bkddkD6hiDWkJ` |
| `VERCEL_ORG_ID` | `team_iJMVCPwVXbbzVbJxkU6WQcnR` |

---

## ✅ Kontrol

Secrets ekledikten sonra:

1. Repository'de bir değişiklik yap (örnek: README'yi düzenle)
2. Commit ve push et
3. **Actions** sekmesine git: https://github.com/feyurdakul/crypto-signal-scanner/actions
4. "Deploy Frontend to Vercel" workflow'unun çalıştığını gör
5. ~1-2 dakika içinde deploy tamamlanır

---

## 🚀 Otomatik Deploy Aktif!

Artık her `git push` sonrası:
- ✅ Railway (Backend) otomatik deploy olur
- ✅ Vercel (Frontend) GitHub Actions ile otomatik deploy olur

**Tek yapman gereken:**
```bash
git add .
git commit -m "Update: açıklama"
git push
```

**Her şey otomatik! 🎉**

---

## 🔍 Troubleshooting

### Hata: "VERCEL_TOKEN is not set"
- GitHub Secrets'da `VERCEL_TOKEN` ekli mi kontrol et
- Token'ın doğru kopyalandığından emin ol

### Hata: "Project not found"
- `VERCEL_PROJECT_ID` doğru mu kontrol et
- `VERCEL_ORG_ID` doğru mu kontrol et

### GitHub Actions çalışmıyor
- `.github/workflows/deploy.yml` dosyası main branch'te mi?
- `frontend/` klasöründe değişiklik yaptın mı?
- Actions sekmesinde hata loglarını kontrol et

---

## 📞 Yardım

Sorun yaşarsan:
1. GitHub Actions logs: https://github.com/feyurdakul/crypto-signal-scanner/actions
2. Vercel dashboard: https://vercel.com/dashboard
3. Railway logs: https://railway.app/dashboard


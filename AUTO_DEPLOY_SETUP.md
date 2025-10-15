# 🚀 Otomatik Deployment Kurulumu

## ✅ Durum:

### Railway (Backend):
- **Status:** ✅ Otomatik deploy AÇIK
- **Trigger:** Her `git push` sonrası otomatik deploy
- **Süre:** ~2-3 dakika
- **Yapılacak:** ❌ Hiçbir şey (zaten çalışıyor)

### Vercel (Frontend):
- **Status:** ⚙️ Manuel kurulum gerekli
- **Trigger:** GitHub Actions ile otomatik olacak
- **Süre:** ~1-2 dakika
- **Yapılacak:** ✅ Aşağıdaki adımlar

---

## 📋 Vercel Otomatik Deploy Kurulumu

### 1️⃣ Vercel Token Al

```bash
# Terminal'de çalıştır:
cd /Users/furkanyurdakul/tarama/frontend
vercel login
vercel token create
```

**Veya:**

1. https://vercel.com/account/tokens sayfasına git
2. "Create" butonuna tıkla
3. Token adı: `github-actions-deploy`
4. Scope: "Full Account"
5. Expiration: "No Expiration"
6. Token'ı kopyala (bir daha gösterilmeyecek!)

---

### 2️⃣ GitHub Secrets'a Ekle

1. GitHub reposuna git: https://github.com/feyurdakul/crypto-signal-scanner
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret** butonuna tıkla
4. **Name:** `VERCEL_TOKEN`
5. **Secret:** (Kopyaladığın token'ı yapıştır)
6. **Add secret** butonuna tıkla

---

### 3️⃣ Vercel Project ID ve Org ID Al

```bash
cd /Users/furkanyurdakul/tarama/frontend
cat .vercel/project.json
```

**Çıktı:**
```json
{
  "projectId": "prj_xxxxxxxxxxxxx",
  "orgId": "team_xxxxxxxxxxxxx"
}
```

Bu değerleri de GitHub secrets'a ekle:
- **VERCEL_PROJECT_ID:** `prj_xxxxxxxxxxxxx`
- **VERCEL_ORG_ID:** `team_xxxxxxxxxxxxx`

---

### 4️⃣ Test Et

```bash
# Herhangi bir değişiklik yap ve push et:
cd /Users/furkanyurdakul/tarama
git add .
git commit -m "Test: Auto-deploy"
git push
```

**Sonuç:**
- GitHub Actions otomatik başlayacak
- ~1-2 dakika içinde Vercel'e deploy edilecek
- https://github.com/feyurdakul/crypto-signal-scanner/actions adresinden takip edebilirsin

---

## 🎯 Alternatif: Vercel GitHub Integration (ÖNERİLEN)

Daha kolay yol: Vercel'in kendi GitHub entegrasyonunu kullan

### Adımlar:

1. **Vercel Dashboard'a git:** https://vercel.com/dashboard
2. **Add New** → **Project**
3. **Import Git Repository** → GitHub'u seç
4. **Select Repository:** `crypto-signal-scanner`
5. **Configure Project:**
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
   - **Install Command:** `npm install`
6. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL` = `https://cryptoscanner.up.railway.app`
7. **Deploy** butonuna tıkla

**✅ Artık her push'ta otomatik deploy olacak!**

---

## 📊 Deploy Durumu Kontrol

### Railway (Backend):
```bash
curl https://cryptoscanner.up.railway.app/health
```

### Vercel (Frontend):
```bash
curl https://tradingscreener.vercel.app
```

### GitHub Actions:
https://github.com/feyurdakul/crypto-signal-scanner/actions

---

## 🔄 Deploy Sırası:

Her `git push` sonrası:
1. **Railway Backend:** Otomatik deploy başlar (~2-3 dk)
2. **Vercel Frontend:** Otomatik deploy başlar (~1-2 dk)
3. **Toplam:** ~3-5 dakika içinde her iki ortam da güncellenir

---

## ⚠️ Önemli Notlar:

1. **Railway:** `.env` değişkenleri Railway dashboard'dan ayarlanmalı
2. **Vercel:** `NEXT_PUBLIC_API_URL` env variable Vercel dashboard'dan ayarlanmalı
3. **GitHub Actions:** Vercel token'ı asla repo'ya push etme!

---

## ✅ Kurulum Sonrası:

Artık her değişiklikten sonra sadece:

```bash
git add .
git commit -m "Update: description"
git push
```

**Her şey otomatik!** 🚀


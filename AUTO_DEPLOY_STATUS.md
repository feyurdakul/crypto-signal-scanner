# 🚀 Otomatik Deployment Durumu

**Son Güncelleme:** 15 Ekim 2025, 21:35 UTC

---

## ✅ RAILWAY (Backend) - AKTİF

### Durum: 🟢 Otomatik Deploy AÇIK

**Nasıl Çalışıyor:**
- Her `git push` sonrası Railway otomatik algılar
- `main.py` dosyasını bulur ve başlatır
- Scanner arka planda çalışır
- FastAPI backend serve edilir

**Deploy Süresi:** ~2-3 dakika

**Kontrol:**
```bash
curl https://cryptoscanner.up.railway.app/health
```

**Dashboard:** https://railway.app/dashboard

✅ **Yapılacak:** Hiçbir şey (zaten aktif!)

---

## ⚙️ VERCEL (Frontend) - KURULUM GEREKLİ

### Durum: 🟡 GitHub Actions Hazır - Secrets Eklenmeli

**Hazırlananlar:**
- ✅ GitHub Actions workflow oluşturuldu (`.github/workflows/deploy.yml`)
- ✅ Vercel project bağlandı
- ✅ Project ID ve Org ID alındı
- ⏳ GitHub Secrets eklenmesi bekleniyor

**Gerekli Adımlar:**

### 1️⃣ Vercel Token Al

```bash
vercel login
vercel token create github-actions
```

Token'ı kopyala! ⚠️

### 2️⃣ GitHub Secrets Ekle

https://github.com/feyurdakul/crypto-signal-scanner/settings/secrets/actions

Şu 3 secret'ı ekle:

| Secret Name | Value |
|-------------|-------|
| `VERCEL_TOKEN` | *(Vercel'den aldığın token)* |
| `VERCEL_PROJECT_ID` | `prj_AYrjVcXkYM7vMr7bkddkD6hiDWkJ` |
| `VERCEL_ORG_ID` | `team_iJMVCPwVXbbzVbJxkU6WQcnR` |

### 3️⃣ Test Et

```bash
# Küçük bir değişiklik yap:
cd /Users/furkanyurdakul/tarama
echo "# Test" >> README.md
git add README.md
git commit -m "Test: Auto-deploy"
git push
```

**Sonuç:**
- GitHub Actions otomatik başlar
- ~1-2 dakika içinde Vercel'e deploy edilir
- https://github.com/feyurdakul/crypto-signal-scanner/actions adresinden takip edebilirsin

**Deploy Süresi:** ~1-2 dakika

---

## 📋 Detaylı Kurulum

📄 **Tam rehber:** `GITHUB_SECRETS_SETUP.md` dosyasını oku

---

## 🔄 Her Push Sonrası (Secrets Eklendikten Sonra)

### Otomatik Olan:

```bash
git add .
git commit -m "Update: açıklama"
git push
```

**Railway:**
1. ⚙️ Build başlar (~1 dk)
2. 🚀 Deploy edilir (~1 dk)
3. ✅ Backend hazır (~2-3 dk toplam)

**Vercel (GitHub Actions):**
1. ⚙️ Workflow tetiklenir (anında)
2. 🏗️ Build yapılır (~1 dk)
3. 🚀 Deploy edilir (~30 sn)
4. ✅ Frontend hazır (~1-2 dk toplam)

**Toplam:** ~3-5 dakika içinde her iki ortam da güncellenir!

---

## 📊 Deploy Takibi

### Railway (Backend):
- **Dashboard:** https://railway.app/dashboard
- **Logs:** Railway dashboard → Project → Deployments
- **Health:** https://cryptoscanner.up.railway.app/health

### Vercel (Frontend):
- **GitHub Actions:** https://github.com/feyurdakul/crypto-signal-scanner/actions
- **Dashboard:** https://vercel.com/dashboard
- **URL:** https://tradingscreener.vercel.app

---

## ⚡ Hızlı Kontrol

```bash
# Backend sağlık kontrolü
curl https://cryptoscanner.up.railway.app/health

# Frontend çalışıyor mu
curl -I https://tradingscreener.vercel.app

# GitHub Actions durumu
gh run list --limit 5  # (GitHub CLI gerekli)
```

---

## 🎯 Sonraki Adımlar

### Şimdi Yap:
1. ✅ Railway zaten otomatik (hiçbir şey yapma)
2. ⚠️ **Vercel token al** → `vercel token create`
3. ⚠️ **GitHub Secrets ekle** → 3 tane (VERCEL_TOKEN, PROJECT_ID, ORG_ID)
4. ✅ Test et → `git push` yap ve Actions'ı izle

### Artık Her Push'ta:
- 🔄 Otomatik build
- 🚀 Otomatik deploy
- ✅ Her şey hazır!

---

## 🔧 Troubleshooting

### GitHub Actions başlamıyor:
- `frontend/` klasöründe değişiklik yap (workflow sadece frontend değişikliklerinde çalışır)
- `.github/workflows/deploy.yml` dosyası main branch'te mi kontrol et

### Vercel deploy başarısız:
- GitHub Secrets doğru eklendi mi?
- Token expired olmadı mı?
- Project ID ve Org ID doğru mu?

### Railway deploy başarısız:
- `main.py` dosyası var mı?
- `requirements.txt` güncel mi?
- Railway logs'u kontrol et

---

## 📞 Destek

**Belgeler:**
- 📄 `AUTO_DEPLOY_SETUP.md` - Detaylı kurulum
- 📄 `GITHUB_SECRETS_SETUP.md` - GitHub secrets rehberi
- 📄 `SCANNER_STATUS_REPORT.md` - Scanner durum raporu

**Dashboard Links:**
- Railway: https://railway.app/dashboard
- Vercel: https://vercel.com/dashboard
- GitHub Actions: https://github.com/feyurdakul/crypto-signal-scanner/actions

---

**✅ Railway otomatik!**  
**⏳ Vercel secrets eklendikten sonra otomatik!**  
**🚀 Her push sonrası her şey otomatik deploy olacak!**


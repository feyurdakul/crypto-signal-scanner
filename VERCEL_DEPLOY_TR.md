# 🚀 Vercel Deployment Rehberi (TÜRKÇE)

## ⚡ Hızlı Başlangıç

### Adım 1: Vercel Hesabı ve CLI

```bash
# Vercel CLI'yi global olarak yükle
npm install -g vercel

# Vercel'e login ol
vercel login
```

### Adım 2: Backend API Deploy (Railway)

Backend'iniz Railway'de çalışmalı. Eğer henüz deploy etmediyseniz:

1. **Railway'e git**: https://railway.app/
2. **GitHub ile giriş yap**
3. **New Project** → **Deploy from GitHub repo**
4. Bu projeyi seç
5. **Environment Variables** ekle:
   ```
   SUPABASE_URL=https://rkjndkslanwyoyefsicd.supabase.co
   SUPABASE_KEY=<your-key>
   PORT=8000
   ```
6. Deploy tamamlandığında **URL'yi kopyala** (örn: https://xxx.up.railway.app)

### Adım 3: Vercel Deploy (Frontend)

```bash
# Proje dizininde
cd /Users/furkanyurdakul/tarama

# Vercel'e deploy et
vercel
```

İlk deploy sırasında sorulacak sorular:
- **Set up and deploy**: `Y`
- **Which scope**: Hesabını seç
- **Link to existing project**: `N`
- **Project name**: `tarama-signals` (veya istediğin isim)
- **In which directory is your code located**: `./`
- **Override settings**: `N`

### Adım 4: Environment Variables

Vercel dashboard'da (`https://vercel.com/<username>/tarama-signals`):

1. **Settings** → **Environment Variables**
2. Ekle:
   ```
   NEXT_PUBLIC_API_URL = https://your-railway-backend.up.railway.app
   ```
3. **Save**
4. **Redeploy** → En son deployment'ı redeploy et

### Adım 5: Production Deploy

```bash
# Production'a deploy
vercel --prod
```

## 🔧 Sorun Giderme

### Hata: "No framework detected"

```bash
cd frontend
vercel
```

Frontend klasöründen deploy et.

### Hata: "API connection failed"

1. `NEXT_PUBLIC_API_URL` environment variable'ının doğru olduğundan emin ol
2. Railway backend'inin çalıştığını kontrol et
3. CORS ayarlarını kontrol et (`backend_api.py`)

### Hata: "Build failed"

```bash
# Local'de test et
cd frontend
npm install
npm run build
```

Eğer local'de çalışıyorsa:
1. Vercel dashboard → Settings → Git
2. **Redeploy** butonu

### Hata: "Module not found"

`frontend/package.json` dosyasındaki tüm dependencies'in yüklü olduğundan emin ol:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 📱 Test

Deploy sonrası:

1. **Vercel URL'yi ziyaret et**: https://tarama-signals.vercel.app
2. **API bağlantısını test et**: Dashboard'da sinyallerin görünüp görünmediğini kontrol et
3. **Mobile test**: Telefonda aç ve responsive olduğunu kontrol et

## 🎯 GitHub Actions (Otomatik Deploy)

Her push'da otomatik deploy için `.github/workflows/deploy.yml` ekle:

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install Vercel CLI
        run: npm install -g vercel
      - name: Deploy to Vercel
        run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

**Secrets ekle** (GitHub → Settings → Secrets):
- `VERCEL_TOKEN`: Vercel dashboard → Settings → Tokens
- `VERCEL_ORG_ID`: `.vercel/project.json` dosyasında
- `VERCEL_PROJECT_ID`: `.vercel/project.json` dosyasında

## 🚀 Final URL'ler

**Frontend (Vercel)**: https://tarama-signals.vercel.app
**Backend (Railway)**: https://your-backend.up.railway.app
**Database**: Supabase (zaten çalışıyor)

## ✅ Checklist

- [ ] Railway'de backend deploy edildi
- [ ] Railway environment variables eklendi
- [ ] Vercel'e frontend deploy edildi
- [ ] Vercel'de `NEXT_PUBLIC_API_URL` eklendi
- [ ] Production URL test edildi
- [ ] Mobile responsive çalışıyor
- [ ] Sinyaller görünüyor

## 💡 İpuçları

1. **Her değişiklikte**: `git push` yeterli, Vercel otomatik deploy eder
2. **Hızlı test**: `vercel dev` ile local'de Vercel ortamını simüle et
3. **Logs**: Vercel dashboard → Deployments → Build logs
4. **Preview**: Her branch için otomatik preview URL
5. **Custom Domain**: Vercel → Settings → Domains

## 🆘 Yardım

Hala sorun varsa:
1. Vercel logs'a bak
2. Railway logs'a bak
3. Browser console'da hata var mı kontrol et
4. Network tab'da API call'ları izle

**Başarılar!** 🎉


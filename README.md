# 📊 Kripto Sinyal Takip Sistemi

Binance'deki **TÜM USDT çiftlerini** 7/24 tarayan, VWAP+RSI+ADX stratejisi ile giriş/çıkış sinyalleri üreten ve işlem performansını takip eden profesyonel bir sistem.

## 🚀 Özellikler

✅ **Binance'deki TÜM USDT çiftleri** (300+ parite)  
✅ **7/24 otomatik tarama** (arka planda çalışır)  
✅ **Canlı sinyal bildirimleri** (LONG/SHORT giriş-çıkış)  
✅ **Otomatik işlem takibi** (Giriş+Çıkış = Kar/Zarar hesabı)  
✅ **Streamlit dashboard** (Güzel görsel arayüz)  
✅ **Gerçek zamanlı performans analizi**  
✅ **Açık/Kapalı işlem yönetimi**  

## 📈 Strateji

**Giriş Sinyalleri:**
- **LONG:** Fiyat > VWAP + ADX < 30 + RSI > 55 (yukarı kırılım)
- **SHORT:** Fiyat < VWAP + ADX < 30 + RSI < 35 (aşağı kırılım)

**Çıkış Sinyalleri:**
- **LONG ÇIKIŞ:** Fiyat VWAP'ın altına düşerse
- **SHORT ÇIKIŞ:** Fiyat VWAP'ın üstüne çıkarsa

## 🛠️ Kurulum

### 1. Kütüphaneleri Kur

```bash
pip install -r requirements.txt
```

**Önemli:** TVDatafeed için ayrıca:
```bash
pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git
```

### 2. Sistemi Başlat

#### macOS / Linux:
```bash
chmod +x start.sh
./start.sh
```

#### Windows:
```bash
start.bat
```

#### Manuel Başlatma:

**Terminal 1 - Tarayıcı:**
```bash
python scanner_core.py
```

**Terminal 2 - Dashboard:**
```bash
streamlit run dashboard.py
```

## 📱 Dashboard Kullanımı

Dashboard otomatik olarak tarayıcınızda açılacak: **http://localhost:8501**

### 📊 Sekmeler:

1. **🔔 Canlı Sinyaller**
   - Anlık giriş/çıkış sinyalleri
   - Fiyat, RSI, ADX, VWAP bilgileri
   - Zaman damgaları

2. **📊 Açık İşlemler**
   - Şu anda açık olan pozisyonlar
   - Giriş fiyatı ve zamanı
   - İşlem süresi

3. **📋 Kapalı İşlemler**
   - Tamamlanmış işlem geçmişi
   - Kar/Zarar oranları
   - Filtreleme (LONG/SHORT, Kazanan/Kaybeden)
   - CSV indirme

4. **📈 Analitik**
   - Kümülatif kar/zarar grafiği
   - İşlem dağılımı (pie chart)
   - PnL histogramı
   - Tip bazında performans

## 📁 Dosya Yapısı

```
tarama/
├── scanner_core.py          # Ana tarama motoru
├── dashboard.py             # Streamlit arayüzü
├── crypto_scanner.py        # Eski versiyon (yedek)
├── requirements.txt         # Bağımlılıklar
├── start.sh                 # macOS/Linux başlatıcı
├── start.bat                # Windows başlatıcı
├── README.md                # Bu dosya
├── trading_signals.json     # Sinyal verileri (otomatik)
└── trade_history.json       # İşlem geçmişi (otomatik)
```

## 🎯 İşlem Akışı

1. **Tarayıcı** → Binance'den sembol listesini çeker
2. **Tarayıcı** → Her 60 saniyede tüm paritileri tarar
3. **Strateji** → VWAP+RSI+ADX sinyallerini üretir
4. **İşlem Takibi** → Giriş sinyali gelirse işlem açar
5. **İşlem Takibi** → Çıkış sinyali gelirse işlem kapatır ve kar/zarar hesaplar
6. **Dashboard** → Her 10 saniyede verileri günceller
7. **Dashboard** → Açık/Kapalı işlemleri ve analitiği gösterir

## ⚙️ Ayarlar

`scanner_core.py` dosyasında değiştirebilirsiniz:

```python
# Strateji parametreleri
ADX_LENGTH = 20          # ADX periyodu
ADX_LEVEL = 30           # ADX eşik değeri
RSI_LENGTH = 14          # RSI periyodu
RSI_BUY_LEVEL = 55       # LONG için RSI eşiği
RSI_SELL_LEVEL = 35      # SHORT için RSI eşiği

# Tarama ayarları
scan_interval = 60       # Tarama aralığı (saniye)
```

`dashboard.py` dosyasında:

```python
refresh_interval = 10    # Dashboard yenileme (saniye)
```

## 📊 Veri Formatı

### trading_signals.json
```json
{
  "BTCUSDT": {
    "symbol": "BTCUSDT",
    "signal": "LONG_ENTRY",
    "message": "ALIM (VWAP+, ADX<30, RSI>55)",
    "price": 43250.50,
    "timestamp": "2025-10-13T15:30:00",
    "rsi": 58.5,
    "adx": 25.3,
    "vwap": 43100.25
  }
}
```

### trade_history.json
```json
{
  "open": {
    "ETHUSDT": {
      "symbol": "ETHUSDT",
      "type": "LONG",
      "entry_price": 2250.50,
      "entry_time": "2025-10-13T15:00:00",
      "status": "OPEN"
    }
  },
  "closed": [
    {
      "symbol": "BTCUSDT",
      "type": "LONG",
      "entry_price": 43000.00,
      "exit_price": 43500.00,
      "entry_time": "2025-10-13T14:00:00",
      "exit_time": "2025-10-13T15:00:00",
      "pnl_percent": 1.16,
      "status": "CLOSED"
    }
  ]
}
```

## 🔧 Sorun Giderme

### Tarayıcı hata veriyor
- TVDatafeed login gerektirmez ama rate limiting yapabilir
- Bazı semboller TradingView'de farklı isimle olabilir
- `VERI ÇEKILEMEDI` mesajları normaldir, tarama devam eder

### Dashboard boş görünüyor
- Tarayıcının çalıştığından emin olun
- JSON dosyalarının oluşup oluşmadığını kontrol edin
- En az 1 tarama döngüsü tamamlanmasını bekleyin

### Bağlantı hatası
- İnternet bağlantınızı kontrol edin
- Binance API'sine erişim olduğundan emin olun
- Firewall/VPN ayarlarını kontrol edin

## 📝 Notlar

- **Gerçek para ile işlem yapmaz** - Sadece sinyal üretir
- Manuel veya bot ile kullanabilirsiniz
- Geçmiş performans gelecek garantisi değildir
- Risk yönetimi sizin sorumluluğunuzdadır
- **Demo amaçlıdır, yatırım tavsiyesi değildir**

## 🤝 Katkıda Bulunma

Hata bulursanız veya iyileştirme öneriniz varsa issue açabilirsiniz.

## 📜 Lisans

Bu proje MIT lisansı altında açık kaynaklıdır.

---

**Made with ❤️ for crypto traders**


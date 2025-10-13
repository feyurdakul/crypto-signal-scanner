#!/bin/bash

echo "🚀 KRİPTO SİNYAL TARAYICI - PRODUCTION MODE"
echo "=============================================="

# Gerekli bağımlılıkları kontrol et
echo "1. Bağımlılıklar kontrol ediliyor..."
if ! python -c "import supabase" 2>/dev/null; then
    echo "❌ Supabase kurulu değil, kuruluyor..."
    pip install supabase python-dotenv
fi

# Eski süreçleri temizle
echo "2. Eski süreçler temizleniyor..."
pkill -f "python scanner_core.py" 2>/dev/null
pkill -f "streamlit run dashboard_v2.py" 2>/dev/null
sleep 2

# Tarayıcıyı arka planda başlat
echo "3. Tarayıcı başlatılıyor..."
cd /Users/furkanyurdakul/tarama
nohup python scanner_core.py > scanner.log 2>&1 &
SCANNER_PID=$!
echo "   ✓ Tarayıcı PID: $SCANNER_PID"

# 5 saniye bekle
echo "4. Dashboard hazırlanıyor (5 saniye)..."
sleep 5

# Dashboard'u başlat
echo "5. Dashboard başlatılıyor..."
echo "   🌐 http://localhost:8501 adresinde açılacak"
echo ""
echo "📊 SİSTEM ÇALIŞIYOR:"
echo "   - Tarayıcı: Arka planda çalışıyor"
echo "   - Dashboard: http://localhost:8501"
echo "   - Supabase: Otomatik kayıt aktif"
echo "   - Log: scanner.log dosyasında"
echo ""
echo "🛑 Durdurmak için: Ctrl+C"
echo ""

# Dashboard'u başlat (foreground)
streamlit run dashboard_v2.py --server.port 8501

# Temizlik (Ctrl+C ile kapatıldığında)
echo ""
echo "🛑 Sistem kapatılıyor..."
kill $SCANNER_PID 2>/dev/null
pkill -f "streamlit run dashboard_v2.py" 2>/dev/null
echo "✅ Sistem durduruldu."

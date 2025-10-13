#!/bin/bash

echo "========================================="
echo "Kripto Sinyal Takip Sistemi Başlatılıyor"
echo "========================================="
echo ""

# Tarayıcıyı arka planda başlat
echo "1. Sinyal tarayıcı başlatılıyor..."
python scanner_core.py &
SCANNER_PID=$!
echo "   ✓ Tarayıcı başlatıldı (PID: $SCANNER_PID)"
echo ""

# 5 saniye bekle
echo "2. Dashboard hazırlanıyor (5 saniye)..."
sleep 5
echo ""

# Streamlit dashboard'u başlat
echo "3. Dashboard açılıyor (Gelişmiş Versiyon)..."
echo "   🌐 Tarayıcınızda http://localhost:8501 açılacak"
echo ""
streamlit run dashboard_v2.py

# Temizlik (Ctrl+C ile kapatıldığında)
echo ""
echo "Sistem kapatılıyor..."
kill $SCANNER_PID 2>/dev/null
echo "✓ Kapatıldı"


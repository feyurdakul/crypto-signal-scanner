#!/bin/bash

echo "🚀 RAILWAY DEPLOYMENT - STARTING..."
echo "======================================"

# Scanner'ı arka planda başlat
echo "1. Starting scanner..."
python scanner_core_dual.py &
SCANNER_PID=$!
echo "   ✓ Scanner PID: $SCANNER_PID"

# 5 saniye bekle
sleep 5

# Dashboard'ı başlat
echo "2. Starting dashboard..."
streamlit run dashboard_dual_system.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true

# Eğer dashboard kapanırsa scanner'ı da kapat
echo "🛑 Dashboard stopped, cleaning up..."
kill $SCANNER_PID 2>/dev/null
echo "✅ Cleanup complete"

#!/bin/bash

echo "🚀 RAILWAY DEPLOYMENT - FASTAPI BACKEND"
echo "======================================"

# Tüm scanner'ları arka planda başlat (Kripto + BIST + US)
echo "1. Starting all scanners (Crypto + BIST + US)..."
python run_all_scanners.py &
SCANNER_PID=$!
echo "   ✓ Scanner PID: $SCANNER_PID"

# 5 saniye bekle
sleep 5

# FastAPI server'ı başlat
echo "2. Starting FastAPI server..."
uvicorn backend_api:app --host 0.0.0.0 --port=${PORT:-8000}

# Eğer API kapanırsa scanner'ı da kapat
echo "🛑 API stopped, cleaning up..."
kill $SCANNER_PID 2>/dev/null
echo "✅ Cleanup complete"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto Scanner - Sadece Hybrid Strategy
Railway üzerinde sürekli çalışır
"""

import threading
import time
from scanner_core import CryptoScanner

def run_crypto_scanner():
    """Crypto scanner'ı çalıştır"""
    print("🚀 Crypto Scanner (Hybrid Strategy) başlatılıyor...")
    scanner = CryptoScanner()
    if scanner.initialize():
        scanner.start()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("### CRYPTO SIGNAL SCANNER - HYBRID STRATEGY ONLY ###")
    print("="*70 + "\n")
    
    # Crypto scanner'ı başlat
    crypto_thread = threading.Thread(target=run_crypto_scanner, daemon=True)
    crypto_thread.start()
    
    print("✅ Scanner başlatıldı. Railway'de 7/24 çalışıyor...")
    print("🔄 FastAPI backend ile birlikte çalışır.")
    print("="*70 + "\n")
    
    # Ana thread'i canlı tut
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n\n🛑 Scanner durduruluyor...")

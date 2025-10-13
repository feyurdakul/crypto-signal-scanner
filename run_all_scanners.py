#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tüm Tarayıcıları Başlat
Kripto, BIST ve US tarayıcılarını paralel çalıştırır
"""

import threading
from scanner_core import CryptoScanner

def run_crypto_scanner():
    """Kripto tarayıcısını çalıştır"""
    scanner = CryptoScanner(market_type='CRYPTO')
    if scanner.initialize():
        scanner.start()

def run_bist_scanner():
    """BIST tarayıcısını çalıştır"""
    scanner = CryptoScanner(market_type='BIST')
    if scanner.initialize():
        scanner.start()

def run_us_scanner():
    """US tarayıcısını çalıştır"""
    scanner = CryptoScanner(market_type='US')
    if scanner.initialize():
        scanner.start()

if __name__ == "__main__":
    print("🚀 TÜM TARAYICILAR BAŞLATILIYOR...")
    print("="*70)
    
    # Kripto tarayıcısı thread
    crypto_thread = threading.Thread(target=run_crypto_scanner, daemon=True)
    crypto_thread.start()
    
    # BIST tarayıcısı thread
    bist_thread = threading.Thread(target=run_bist_scanner, daemon=True)
    bist_thread.start()
    
    # US tarayıcısı thread
    us_thread = threading.Thread(target=run_us_scanner, daemon=True)
    us_thread.start()
    
    # Ana thread'i beklet
    try:
        crypto_thread.join()
        bist_thread.join()
        us_thread.join()
    except KeyboardInterrupt:
        print("\n\n⛔ Tüm tarayıcılar durduruldu.")


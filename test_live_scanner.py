#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Canlı Scanner Testi - Gerçek sinyalleri kontrol et
"""

from scanner_core import CryptoScanner
import time

def test_live_scan():
    """Canlı tarama yap ve sonuçları göster"""
    print("=" * 70)
    print("🚀 CANLI SCANNER TESTİ - KRİPTO")
    print("=" * 70)
    
    scanner = CryptoScanner('CRYPTO')
    
    if scanner.initialize():
        print(f"\n✓ Scanner başlatıldı - {len(scanner.symbols)} sembol taranacak")
        print("\n" + "=" * 70)
        print("📊 TARAMAHere başlatılıyor...")
        print("=" * 70)
        
        # 3 tarama yap
        for i in range(3):
            print(f"\n[TARAMA #{i+1}]")
            scanner.scan_once()
            
            if i < 2:
                print("\n⏳ 30 saniye bekleniyor...")
                time.sleep(30)
        
        # Supabase'den son sinyalleri kontrol et
        print("\n" + "=" * 70)
        print("📋 SUPABASE'DEN SON SİNYALLER:")
        print("=" * 70)
        
        signals = scanner.data_manager.supabase.get_current_signals()
        
        if signals:
            print(f"\n✅ {len(signals)} sinyal bulundu:")
            for key, signal in list(signals.items())[:10]:
                print(f"\n  📢 {signal['symbol']}: {signal['signal']}")
                print(f"     Sistem: {signal.get('system', 'N/A')}")
                print(f"     Fiyat: ${signal['price']:.6f}")
                print(f"     Zaman: {signal['timestamp']}")
        else:
            print("\n❌ Henüz sinyal yok")
            print("\n💡 Neden sinyal yok olabilir:")
            print("   1. Piyasa koşulları uygun değil")
            print("   2. RSI crossover/crossunder nadir gerçekleşiyor")
            print("   3. ADX veya VWAP koşulları sağlanmıyor")
            print("\n📊 Tarama devam ediyor, bekleyin...")

if __name__ == "__main__":
    test_live_scan()


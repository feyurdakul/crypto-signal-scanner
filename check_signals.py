#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Supabase'deki sinyalleri kontrol et
"""

from supabase_client import SupabaseManager
from datetime import datetime

def check_signals():
    """Tüm sinyalleri kontrol et"""
    supabase = SupabaseManager()
    
    print("🔍 Supabase Sinyalleri Kontrol Ediliyor...")
    print("="*70)
    
    try:
        # Tüm sinyalleri al
        all_signals = supabase.get_current_signals()
        
        print(f"\n📊 Toplam Sinyal: {len(all_signals)}")
        
        # Market ve sistem bazlı gruplama
        crypto_hybrid = []
        crypto_elliott = []
        bist_hybrid = []
        bist_elliott = []
        us_hybrid = []
        us_elliott = []
        other = []
        
        for signal_key, signal_data in all_signals.items():
            system = signal_data.get('system', 'UNKNOWN')
            
            if system == 'HYBRID_CRYPTO':
                crypto_hybrid.append(signal_data)
            elif system == 'ELLIOTT_CRYPTO':
                crypto_elliott.append(signal_data)
            elif system == 'HYBRID_BIST':
                bist_hybrid.append(signal_data)
            elif system == 'ELLIOTT_BIST':
                bist_elliott.append(signal_data)
            elif system == 'HYBRID_US':
                us_hybrid.append(signal_data)
            elif system == 'ELLIOTT_US':
                us_elliott.append(signal_data)
            else:
                other.append((system, signal_data))
        
        print(f"\n💰 CRYPTO:")
        print(f"   - HYBRID_CRYPTO: {len(crypto_hybrid)} sinyal")
        print(f"   - ELLIOTT_CRYPTO: {len(crypto_elliott)} sinyal")
        
        print(f"\n🏛️  BIST:")
        print(f"   - HYBRID_BIST: {len(bist_hybrid)} sinyal")
        print(f"   - ELLIOTT_BIST: {len(bist_elliott)} sinyal")
        
        print(f"\n🇺🇸 US:")
        print(f"   - HYBRID_US: {len(us_hybrid)} sinyal")
        print(f"   - ELLIOTT_US: {len(us_elliott)} sinyal")
        
        if other:
            print(f"\n⚠️  Diğer/Eski Format: {len(other)} sinyal")
            for system, signal_data in other[:5]:  # İlk 5'ini göster
                print(f"   - {system}: {signal_data.get('symbol')} @ {signal_data.get('timestamp', 'N/A')[:16]}")
        
        # Son 5 CRYPTO HYBRID sinyali göster
        if crypto_hybrid:
            print(f"\n📋 Son 5 CRYPTO HYBRID Sinyal:")
            for signal in sorted(crypto_hybrid, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]:
                print(f"   - {signal.get('symbol')}: {signal.get('signal_type')} @ {signal.get('timestamp', 'N/A')[:16]}")
        
        print("\n✅ Kontrol tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    check_signals()


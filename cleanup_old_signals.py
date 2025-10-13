#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Eski Format Sinyalleri Temizle
HYBRID ve ELLIOTT formatındaki sinyalleri sil
Sadece HYBRID_CRYPTO, ELLIOTT_CRYPTO, HYBRID_BIST, ELLIOTT_BIST kalsın
"""

from supabase_client import SupabaseManager
from datetime import datetime

def cleanup_old_signals():
    """Eski format sinyalleri temizle"""
    supabase = SupabaseManager()
    
    print("🧹 Eski format sinyaller temizleniyor...")
    print("="*70)
    
    try:
        # Eski format sinyalleri sil (HYBRID ve ELLIOTT)
        response = supabase.client.table('crypto_signals').delete().in_('system', ['HYBRID', 'ELLIOTT']).execute()
        
        deleted_count = len(response.data) if response.data else 0
        print(f"✅ {deleted_count} eski format sinyal silindi")
        
        # Kalan sinyalleri göster
        all_signals = supabase.get_current_signals()
        
        crypto_hybrid = len([s for s in all_signals.values() if s.get('system') == 'HYBRID_CRYPTO'])
        crypto_elliott = len([s for s in all_signals.values() if s.get('system') == 'ELLIOTT_CRYPTO'])
        bist_hybrid = len([s for s in all_signals.values() if s.get('system') == 'HYBRID_BIST'])
        bist_elliott = len([s for s in all_signals.values() if s.get('system') == 'ELLIOTT_BIST'])
        
        print(f"\n📊 Kalan Sinyaller:")
        print(f"   💰 CRYPTO:")
        print(f"      - HYBRID_CRYPTO: {crypto_hybrid}")
        print(f"      - ELLIOTT_CRYPTO: {crypto_elliott}")
        print(f"   🏛️  BIST:")
        print(f"      - HYBRID_BIST: {bist_hybrid}")
        print(f"      - ELLIOTT_BIST: {bist_elliott}")
        print(f"\n   Toplam: {len(all_signals)} sinyal")
        
        print("\n✅ Temizlik tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    cleanup_old_signals()


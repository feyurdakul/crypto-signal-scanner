#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Açık İşlemleri Temizle
Tüm açık işlemleri kapatır
"""

from supabase_client import SupabaseManager
from datetime import datetime

def cleanup_open_trades():
    """Tüm açık işlemleri temizle"""
    supabase = SupabaseManager()
    
    print("🧹 Açık işlemler temizleniyor...")
    print("="*70)
    
    try:
        # Tüm açık işlemleri sil
        response = supabase.supabase.table('open_trades').delete().neq('id', 0).execute()
        
        deleted_count = len(response.data) if response.data else 0
        print(f"✅ {deleted_count} açık işlem silindi")
        
        # Kalan işlemleri göster
        open_trades = supabase.get_open_trades()
        
        print(f"\n📊 Kalan Açık İşlemler: {len(open_trades)}")
        
        print("\n✅ Temizlik tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    cleanup_open_trades()


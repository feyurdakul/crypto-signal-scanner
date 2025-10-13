#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strateji Değiştirme Scripti
scanner_core.py'deki STRATEGY_MODE değerini değiştirir
"""

import re
import sys

def change_strategy(new_strategy):
    """Strateji modunu değiştir"""
    if new_strategy not in ["HYBRID", "ELLIOTT"]:
        print("❌ Geçersiz strateji! Sadece 'HYBRID' veya 'ELLIOTT' kullanın.")
        return False
    
    try:
        # scanner_core.py dosyasını oku
        with open('scanner_core.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # STRATEGY_MODE satırını bul ve değiştir
        pattern = r'STRATEGY_MODE = "[^"]*"'
        replacement = f'STRATEGY_MODE = "{new_strategy}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        # Dosyayı yaz
        with open('scanner_core.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Strateji '{new_strategy}' olarak değiştirildi!")
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python change_strategy.py [HYBRID|ELLIOTT]")
        print("Örnek: python change_strategy.py ELLIOTT")
        sys.exit(1)
    
    new_strategy = sys.argv[1].upper()
    change_strategy(new_strategy)

if __name__ == "__main__":
    main()

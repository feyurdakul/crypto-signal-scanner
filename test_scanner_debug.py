#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scanner Debug Test - Stratejinin neden sinyal üretmediğini anlayalım
"""

from scanner_core import CryptoScanner
from data_fetcher import DataFetcher
from hybrid_intraday_strategy import HybridIntradayStrategy
import pandas as pd

def test_single_symbol():
    """Tek sembol için detaylı test"""
    print("=" * 70)
    print("DEBUG: HYBRID STRATEJI TEST - BTCUSDT")
    print("=" * 70)
    
    data_fetcher = DataFetcher()
    strategy = HybridIntradayStrategy(data_fetcher, 'BTCUSDT', '15m', 'CRYPTO')
    
    # Veri çek
    if strategy.fetch_data(n_bars=100):
        strategy.calculate_indicators()
        
        # Son 5 mum verisi
        df = strategy.df.tail(5)
        print("\nSON 5 MUM VERİSİ:")
        print(df[['Close', 'VWAP', 'RSI', 'ADX', 'ATR']])
        
        # Koşulları kontrol et
        latest = strategy.df.iloc[-1]
        prev = strategy.df.iloc[-2]
        
        print("\n" + "="*70)
        print("SİNYAL KOŞULLARI KONTROLÜ:")
        print("="*70)
        
        print(f"\n📊 Mevcut Değerler:")
        print(f"   Close: ${latest['Close']:.2f}")
        print(f"   VWAP:  ${latest['VWAP']:.2f}")
        print(f"   RSI:   {latest['RSI']:.2f}")
        print(f"   ADX:   {latest['ADX']:.2f}")
        print(f"   ATR:   ${latest['ATR']:.6f}")
        
        print(f"\n🟢 BUY KOŞULLARI:")
        buy_vwap = latest['Close'] > latest['VWAP']
        buy_adx = latest['ADX'] < 30
        buy_rsi_cross = prev['RSI'] <= 55 and latest['RSI'] > 55
        
        print(f"   1. Close > VWAP: {buy_vwap} (${latest['Close']:.2f} > ${latest['VWAP']:.2f})")
        print(f"   2. ADX < 30: {buy_adx} ({latest['ADX']:.2f} < 30)")
        print(f"   3. RSI crossover 55: {buy_rsi_cross} (prev: {prev['RSI']:.2f}, now: {latest['RSI']:.2f})")
        print(f"   ➜ BUY SİNYALİ: {'✅ EVET' if (buy_vwap and buy_adx and buy_rsi_cross) else '❌ HAYIR'}")
        
        print(f"\n🔴 SELL KOŞULLARI:")
        sell_vwap = latest['Close'] < latest['VWAP']
        sell_adx = latest['ADX'] < 30
        sell_rsi_cross = prev['RSI'] >= 35 and latest['RSI'] < 35
        
        print(f"   1. Close < VWAP: {sell_vwap} (${latest['Close']:.2f} < ${latest['VWAP']:.2f})")
        print(f"   2. ADX < 30: {sell_adx} ({latest['ADX']:.2f} < 30)")
        print(f"   3. RSI crossunder 35: {sell_rsi_cross} (prev: {prev['RSI']:.2f}, now: {latest['RSI']:.2f})")
        print(f"   ➜ SELL SİNYALİ: {'✅ EVET' if (sell_vwap and sell_adx and sell_rsi_cross) else '❌ HAYIR'}")
        
        # Sinyal üret
        signal, message, indicators = strategy.generate_signal('NONE')
        
        print(f"\n📢 SONUÇ:")
        if signal:
            print(f"   ✅ SİNYAL: {signal}")
            print(f"   📝 MESAJ: {message}")
        else:
            print(f"   ❌ SİNYAL YOK")
            print(f"\n💡 NEDEN SİNYAL YOK?")
            if not buy_adx and not sell_adx:
                print(f"   - ADX çok yüksek ({latest['ADX']:.2f} >= 30) - Güçlü trend var, stratejimiz düşük volatilite bekliyor")
            if not buy_rsi_cross and not sell_rsi_cross:
                print(f"   - RSI crossover/crossunder yok - RSI seviyesi değişmedi")
                print(f"     (Buy için: RSI'ın 55'i yukarı kesmesi gerek, Sell için 35'i aşağı kesmesi gerek)")
    else:
        print("❌ Veri çekilemedi!")

def test_scanner_symbols():
    """Kaç sembol taranıyor"""
    print("\n" + "=" * 70)
    print("DEBUG: SCANNER SEMBOL LİSTESİ")
    print("=" * 70)
    
    scanner = CryptoScanner('CRYPTO')
    scanner.initialize()
    
    print(f"\n✓ Toplam {len(scanner.symbols)} sembol taranıyor")
    print(f"\n📋 İlk 10 sembol:")
    for i, symbol in enumerate(scanner.symbols[:10], 1):
        print(f"   {i}. {symbol}")
    
    print(f"\n🔄 Tek tarama yapılıyor...")
    scanner.scan_once()

if __name__ == "__main__":
    # Tek sembol detaylı test
    test_single_symbol()
    
    # Scanner genel test
    print("\n" + "=" * 70)
    input("DEVAM için Enter'a basın (Scanner test için)...")
    test_scanner_debug()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Strategy - Sinyal üretiyor mu kontrol et
"""

from data_fetcher import DataFetcher
from hybrid_intraday_strategy import HybridIntradayStrategy
import pandas as pd

# Test sembolleri
test_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']

print("="*70)
print("STRATEJİ TEST - SİNYAL KONTROLÜ")
print("="*70)

data_fetcher = DataFetcher()

for symbol in test_symbols:
    print(f"\n📊 {symbol} test ediliyor...")
    
    strategy = HybridIntradayStrategy(data_fetcher, symbol, '15m', 'CRYPTO')
    
    if strategy.fetch_data(n_bars=100):
        strategy.calculate_indicators()
        
        # Son değerleri göster
        if strategy.df is not None and not strategy.df.empty:
            latest = strategy.df.iloc[-1]
            
            print(f"   Close: ${latest['Close']:.2f}")
            print(f"   VWAP: ${latest['VWAP']:.2f} | Close > VWAP: {latest['Close'] > latest['VWAP']}")
            print(f"   ADX: {latest['ADX']:.2f} | ADX < 30: {latest['ADX'] < 30}")
            print(f"   RSI: {latest['RSI']:.2f}")
            
            # RSI crossover/crossunder kontrolü
            if len(strategy.df) >= 3:
                print(f"   RSI[-3]: {strategy.df.iloc[-3]['RSI']:.2f}")
                print(f"   RSI[-2]: {strategy.df.iloc[-2]['RSI']:.2f}")
                print(f"   RSI[-1]: {strategy.df.iloc[-1]['RSI']:.2f}")
                
                # Son 3 mumda RSI 55 cross up var mı?
                for i in range(1, 4):
                    if i < len(strategy.df):
                        prev_rsi = strategy.df.iloc[-(i+1)]['RSI']
                        curr_rsi = strategy.df.iloc[-i]['RSI']
                        if prev_rsi <= 55 and curr_rsi > 55:
                            print(f"   ✅ RSI CROSS UP 55 bulundu! (i={i}, {prev_rsi:.2f} -> {curr_rsi:.2f})")
                
                # Son 3 mumda RSI 35 cross down var mı?
                for i in range(1, 4):
                    if i < len(strategy.df):
                        prev_rsi = strategy.df.iloc[-(i+1)]['RSI']
                        curr_rsi = strategy.df.iloc[-i]['RSI']
                        if prev_rsi >= 35 and curr_rsi < 35:
                            print(f"   ✅ RSI CROSS DOWN 35 bulundu! (i={i}, {prev_rsi:.2f} -> {curr_rsi:.2f})")
            
            # Sinyal üret
            signal, message, indicators = strategy.generate_signal('NONE')
            
            if signal:
                print(f"   🎯 SİNYAL: {signal}")
                print(f"   💬 MESAJ: {message}")
            else:
                print(f"   ⚪ Sinyal yok")
    else:
        print(f"   ❌ Veri çekilemedi")

print("\n" + "="*70)
print("TEST TAMAMLANDI")
print("="*70)


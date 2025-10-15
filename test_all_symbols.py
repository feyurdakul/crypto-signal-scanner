#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tüm Paritelerde Test - Hangi sembollerden sinyal geliyor?
"""

from scanner_core import CryptoScanner
from data_fetcher import DataFetcher
from hybrid_intraday_strategy import HybridIntradayStrategy
import pandas as pd

def test_all_symbols():
    """Tüm sembolleri tara ve potansiyel sinyalleri göster"""
    print("=" * 80)
    print("🔍 TÜM PARİTELERDE HYBRİD STRATEJİ TESTİ")
    print("=" * 80)
    
    data_fetcher = DataFetcher()
    symbols = data_fetcher.get_all_usdt_pairs()
    
    print(f"\n✓ {len(symbols)} sembol taranacak\n")
    
    # Potansiyel sinyaller
    buy_signals = []
    sell_signals = []
    close_to_buy = []
    close_to_sell = []
    
    for idx, symbol in enumerate(symbols, 1):
        try:
            strategy = HybridIntradayStrategy(data_fetcher, symbol, '15m', 'CRYPTO')
            
            if strategy.fetch_data(n_bars=100):
                strategy.calculate_indicators()
                
                latest = strategy.df.iloc[-1]
                prev = strategy.df.iloc[-2]
                
                # Koşulları kontrol et
                buy_vwap = latest['Close'] > latest['VWAP']
                buy_adx = latest['ADX'] < 30
                sell_vwap = latest['Close'] < latest['VWAP']
                sell_adx = latest['ADX'] < 30
                
                # Son 3 mumda RSI crossover/crossunder var mı?
                buy_rsi_cross = False
                sell_rsi_cross = False
                
                if len(strategy.df) >= 3:
                    for i in range(1, 4):
                        if i < len(strategy.df):
                            prev_rsi = strategy.df.iloc[-(i+1)]['RSI']
                            curr_rsi = strategy.df.iloc[-i]['RSI']
                            
                            if prev_rsi <= 55 and curr_rsi > 55:
                                buy_rsi_cross = True
                            if prev_rsi >= 35 and curr_rsi < 35:
                                sell_rsi_cross = True
                
                # BUY SİNYALİ
                if buy_vwap and buy_adx and buy_rsi_cross:
                    buy_signals.append({
                        'symbol': symbol,
                        'price': latest['Close'],
                        'rsi': latest['RSI'],
                        'adx': latest['ADX'],
                        'vwap': latest['VWAP']
                    })
                    print(f"✅ BUY: {symbol} - RSI:{latest['RSI']:.1f} ADX:{latest['ADX']:.1f} Price:${latest['Close']:.2f}")
                
                # SELL SİNYALİ
                elif sell_vwap and sell_adx and sell_rsi_cross:
                    sell_signals.append({
                        'symbol': symbol,
                        'price': latest['Close'],
                        'rsi': latest['RSI'],
                        'adx': latest['ADX'],
                        'vwap': latest['VWAP']
                    })
                    print(f"✅ SELL: {symbol} - RSI:{latest['RSI']:.1f} ADX:{latest['ADX']:.1f} Price:${latest['Close']:.2f}")
                
                # YAKINDA BUY OLABİLİR (VWAP ve ADX uygun, RSI 55'e yakın)
                elif buy_vwap and buy_adx and latest['RSI'] > 50 and latest['RSI'] < 55:
                    close_to_buy.append({
                        'symbol': symbol,
                        'rsi': latest['RSI'],
                        'adx': latest['ADX'],
                        'distance': 55 - latest['RSI']
                    })
                
                # YAKINDA SELL OLABİLİR (VWAP ve ADX uygun, RSI 35'e yakın)
                elif sell_vwap and sell_adx and latest['RSI'] > 35 and latest['RSI'] < 40:
                    close_to_sell.append({
                        'symbol': symbol,
                        'rsi': latest['RSI'],
                        'adx': latest['ADX'],
                        'distance': latest['RSI'] - 35
                    })
                
                # Her 10 sembolde bir progress göster
                if idx % 10 == 0:
                    print(f"   [{idx}/{len(symbols)}] tarandı...")
                    
        except Exception as e:
            if "no data" not in str(e).lower():
                print(f"   ⚠️ {symbol}: {str(e)[:50]}")
    
    # SONUÇLAR
    print("\n" + "=" * 80)
    print("📊 TARAMA SONUÇLARI")
    print("=" * 80)
    
    print(f"\n🟢 ANLIK BUY SİNYALLERİ: {len(buy_signals)}")
    for s in buy_signals[:10]:
        print(f"   ✅ {s['symbol']}: ${s['price']:.6f} (RSI:{s['rsi']:.1f}, ADX:{s['adx']:.1f})")
    
    print(f"\n🔴 ANLIK SELL SİNYALLERİ: {len(sell_signals)}")
    for s in sell_signals[:10]:
        print(f"   ✅ {s['symbol']}: ${s['price']:.6f} (RSI:{s['rsi']:.1f}, ADX:{s['adx']:.1f})")
    
    print(f"\n🟡 YAKINDA BUY OLABİLİR: {len(close_to_buy)}")
    close_to_buy_sorted = sorted(close_to_buy, key=lambda x: x['distance'])[:10]
    for s in close_to_buy_sorted:
        print(f"   ⚡ {s['symbol']}: RSI {s['rsi']:.1f} (55'e {s['distance']:.1f} kaldı)")
    
    print(f"\n🟡 YAKINDA SELL OLABİLİR: {len(close_to_sell)}")
    close_to_sell_sorted = sorted(close_to_sell, key=lambda x: x['distance'])[:10]
    for s in close_to_sell_sorted:
        print(f"   ⚡ {s['symbol']}: RSI {s['rsi']:.1f} (35'ten {s['distance']:.1f} uzakta)")
    
    print("\n" + "=" * 80)
    print("📈 STRATEJİ ANALİZİ")
    print("=" * 80)
    
    total_potential = len(buy_signals) + len(sell_signals) + len(close_to_buy) + len(close_to_sell)
    
    if len(buy_signals) > 0 or len(sell_signals) > 0:
        print(f"\n✅ Şu anda {len(buy_signals) + len(sell_signals)} AKTİF SİNYAL VAR!")
        print("   Scanner çalışıyor olsaydı bu sinyaller Supabase'e kaydedilecekti.")
    else:
        print(f"\n⚠️ Şu anda aktif sinyal YOK")
        print(f"   Ama {len(close_to_buy) + len(close_to_sell)} sembol yakında sinyal verebilir")
        print(f"   Scanner sürekli çalıştığı için bunları yakalayacak")
    
    print(f"\n📊 Toplam Potansiyel: {total_potential}/{len(symbols)} sembol")
    print(f"   %{(total_potential/len(symbols)*100):.1f} piyasa aktif veya yakında aktif olabilir")
    
    if total_potential == 0:
        print("\n💡 NEDEN SİNYAL YOK?")
        print("   1. RSI crossover/crossunder şu anda gerçekleşmiyor")
        print("   2. Piyasa trend halinde (ADX > 30)")
        print("   3. Fiyatlar VWAP civarında (belirsiz durum)")
        print("\n⏰ ÖNERİ: Scanner'ı sürekli çalıştır, 15 dakikada durum değişir!")

if __name__ == "__main__":
    test_all_symbols()


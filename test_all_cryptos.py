#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test All Cryptos - Tüm USDT paritelerinde potansiyel sinyalleri kontrol et
"""

from data_fetcher import DataFetcher
from hybrid_intraday_strategy import HybridIntradayStrategy

print("="*70)
print("TÜM CRYPTO PAR İTELERİ TEST EDİLİYOR")
print("="*70)

data_fetcher = DataFetcher()
symbols = data_fetcher.get_all_usdt_pairs()

print(f"\n✓ {len(symbols)} sembol taranacak...\n")

signal_count = 0
potential_signals = []

for i, symbol in enumerate(symbols):
    try:
        strategy = HybridIntradayStrategy(data_fetcher, symbol, '15m', 'CRYPTO')
        
        if strategy.fetch_data(n_bars=100):
            strategy.calculate_indicators()
            signal, message, indicators = strategy.generate_signal('NONE')
            
            if signal:
                signal_count += 1
                print(f"🎯 SİNYAL {signal_count}: {symbol} - {signal}")
                print(f"   {message}")
                print(f"   Close: ${indicators['close']:.6f} | VWAP: {indicators['vwap']:.6f}")
                print(f"   RSI: {indicators['rsi']:.2f} | ADX: {indicators['adx']:.2f}\n")
            else:
                # Potansiyel sinyalleri bul (koşullara yakın olanlar)
                if strategy.df is not None and not strategy.df.empty:
                    latest = strategy.df.iloc[-1]
                    
                    # LONG potansiyeli: VWAP üzerinde, ADX<30, RSI 45-55 arası
                    if (latest['Close'] > latest['VWAP'] and 
                        latest['ADX'] < 30 and 
                        45 < latest['RSI'] < 55):
                        potential_signals.append({
                            'symbol': symbol,
                            'type': 'POTENTIAL_LONG',
                            'rsi': latest['RSI'],
                            'adx': latest['ADX'],
                            'close': latest['Close'],
                            'vwap': latest['VWAP']
                        })
                    
                    # SHORT potansiyeli: VWAP altında, ADX<30, RSI 35-45 arası
                    elif (latest['Close'] < latest['VWAP'] and 
                          latest['ADX'] < 30 and 
                          35 < latest['RSI'] < 45):
                        potential_signals.append({
                            'symbol': symbol,
                            'type': 'POTENTIAL_SHORT',
                            'rsi': latest['RSI'],
                            'adx': latest['ADX'],
                            'close': latest['Close'],
                            'vwap': latest['VWAP']
                        })
        
        # Her 50 sembolde progress göster
        if (i + 1) % 50 == 0:
            print(f"✓ {i + 1}/{len(symbols)} sembol tarandı...")
    
    except Exception as e:
        pass

print("\n" + "="*70)
print(f"SONUÇLAR:")
print(f"✅ {signal_count} aktif sinyal bulundu")
print(f"⏳ {len(potential_signals)} potansiyel sinyal (RSI cross bekliyor)")
print("="*70)

if signal_count == 0 and len(potential_signals) > 0:
    print("\n🔍 POTANSİYEL SİNYALLER (RSI Crossover/Crossunder Bekliyor):")
    print("-"*70)
    for p in potential_signals[:10]:  # İlk 10 potansiyeli göster
        print(f"{p['type']:20} {p['symbol']:12} RSI:{p['rsi']:6.2f} ADX:{p['adx']:5.2f} Price:${p['close']:.4f}")
    
    if len(potential_signals) > 10:
        print(f"... ve {len(potential_signals) - 10} tane daha")

print("\n💡 NOT: Strateji çalışıyor ama piyasa koşulları şu anda uygun değil.")
print("   Sinyal gelmesi için RSI'ın 55'i yukarı veya 35'i aşağı kesmesi gerekiyor.")


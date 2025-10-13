# -*- coding: utf-8 -*-
"""
Kripto Sinyal Tarayıcı - Çoklu Sistem Motoru
Her iki sistemi aynı anda çalıştırır ve sistem bazlı takip yapar
"""

import pandas as pd
import numpy as np
import pandas_ta as ta
from tvDatafeed import TvDatafeed, Interval
import ccxt
import time
from datetime import datetime
import pytz
import threading
import json
from pathlib import Path
from supabase_client import SupabaseManager
from hybrid_intraday_strategy import HybridIntradayStrategy
from ewp_fibonacci_strategy import ElliottWaveFibonacciStrategy

# ----------------------------------------------------------------------
# 1. AYARLAR
# ----------------------------------------------------------------------

TV_USERNAME = None
TV_PASSWORD = None
TV_EXCHANGE = 'BINANCE'
TIMEFRAME = Interval.in_15_minute

# Çoklu Sistem Modu - Her iki sistem aynı anda çalışır
DUAL_SYSTEM_MODE = True

# Hibrit Gün İçi Momentum ve Sistemik Risk Yönetimi Stratejisi Parametreleri
ADX_LENGTH = 20
ADX_LEVEL = 30
RSI_LENGTH = 14
RSI_BUY_LEVEL = 55
RSI_SELL_LEVEL = 35
ATR_LENGTH = 14
ATR_SL_MULTIPLIER = 2.5  # Stop Loss: 2.5 x ATR
ATR_TP_MULTIPLIER = 7.5  # Take Profit: 7.5 x ATR (3:1 Risk/Reward)

# İşlem Saatleri (UTC)
TRADING_START_HOUR = 6  # 09:15 TR (UTC+3) = 06:15 UTC
TRADING_END_HOUR = 11   # 14:30 TR (UTC+3) = 11:30 UTC
SQUARE_OFF_HOUR = 12    # 15:00 TR (UTC+3) = 12:00 UTC

# Elliott Dalga ve Fibonacci Stratejisi Parametreleri
EWP_ATR_SL_MULTIPLIER = 3.0  # Swing trading için daha geniş SL
EWP_ATR_TP_MULTIPLIER = 7.5  # 1:2.5 risk/ödül oranı

# Veri Depolama
DATA_FILE = 'trading_signals.json'
TRADES_FILE = 'trade_history.json'

# ----------------------------------------------------------------------
# 2. VERİ YÖNETİCİSİ
# ----------------------------------------------------------------------

class DataManager:
    """Veri yönetimi - Supabase entegrasyonu"""
    
    def __init__(self):
        self.supabase = SupabaseManager()
        self.open_trades = {}
        self.closed_trades = []
        self.load_data()
    
    def load_data(self):
        """Mevcut verileri yükle"""
        try:
            # Supabase'den açık işlemleri çek
            self.open_trades = self.supabase.get_open_trades()
            print(f"✅ {len(self.open_trades)} açık işlem yüklendi")
            
            # Supabase'den kapalı işlemleri çek
            self.closed_trades = self.supabase.get_closed_trades()
            print(f"✅ {len(self.closed_trades)} kapalı işlem yüklendi")
            
        except Exception as e:
            print(f"❌ Veri yükleme hatası: {e}")
            self.open_trades = {}
            self.closed_trades = []
    
    def add_signal(self, symbol, signal_type, message, price, indicators, system=None):
        """Yeni sinyali kaydet"""
        try:
            success = self.supabase.add_signal(symbol, signal_type, message, price, indicators)
            if success:
                print(f"✓ Sinyal kaydedildi: {symbol} [{system}] {signal_type}")
            else:
                print(f"❌ Sinyal kaydedilemedi: {symbol}")
                
        except Exception as e:
            print(f"❌ Sinyal ekleme hatası: {e}")
    
    def open_trade(self, symbol, entry_type, entry_price, timestamp, atr_value, sl_multiplier=None, tp_multiplier=None, system=None):
        """Yeni işlem aç - Sistem bazlı"""
        try:
            trade_type = 'LONG' if 'LONG' in entry_type else 'SHORT'
            
            # ATR çarpanları
            if sl_multiplier is None:
                sl_multiplier = ATR_SL_MULTIPLIER
            if tp_multiplier is None:
                tp_multiplier = ATR_TP_MULTIPLIER
            
            # ATR tabanlı Stop Loss ve Take Profit hesapla
            if trade_type == 'LONG':
                stop_loss = entry_price - (atr_value * sl_multiplier)
                take_profit = entry_price + (atr_value * tp_multiplier)
            else:  # SHORT
                stop_loss = entry_price + (atr_value * sl_multiplier)
                take_profit = entry_price - (atr_value * tp_multiplier)
            
            # Sistem bazlı işlem açma
            trade_key = f"{symbol}_{system}" if system else symbol
            
            # Supabase'e kaydet
            success = self.supabase.open_trade(trade_key, trade_type, entry_price, atr_value, stop_loss, take_profit, system)
            
            if success:
                self.open_trades[trade_key] = {
                    'symbol': symbol,
                    'system': system,
                    'type': trade_type,
                    'entry_price': entry_price,
                    'entry_time': timestamp,
                    'status': 'OPEN',
                    'atr_value': atr_value,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
                print(f"✓ İşlem açıldı: {symbol} [{system}] {trade_type} @ ${entry_price:.6f}")
                print(f"   SL: ${stop_loss:.6f} | TP: ${take_profit:.6f} | ATR: {atr_value:.6f}")
            else:
                print(f"❌ İşlem açılamadı: {symbol} [{system}]")
                
        except Exception as e:
            print(f"❌ İşlem açma hatası: {e}")
    
    def close_trade(self, symbol, exit_type, exit_price, system=None):
        """İşlem kapat"""
        try:
            trade_key = f"{symbol}_{system}" if system else symbol
            
            if trade_key in self.open_trades:
                trade = self.open_trades[trade_key]
                
                # Kar/zarar hesapla
                if trade['type'] == 'LONG':
                    pnl = exit_price - trade['entry_price']
                    pnl_pct = (pnl / trade['entry_price']) * 100
                else:  # SHORT
                    pnl = trade['entry_price'] - exit_price
                    pnl_pct = (pnl / trade['entry_price']) * 100
                
                # Kapalı işlem olarak kaydet
                closed_trade = {
                    'symbol': symbol,
                    'system': system,
                    'type': trade['type'],
                    'entry_price': trade['entry_price'],
                    'exit_price': exit_price,
                    'entry_time': trade['entry_time'],
                    'exit_time': datetime.now(pytz.utc).isoformat(),
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'status': 'CLOSED'
                }
                
                # Supabase'e kaydet
                success = self.supabase.close_trade(trade_key, exit_price, pnl, pnl_pct)
                
                if success:
                    self.closed_trades.append(closed_trade)
                    del self.open_trades[trade_key]
                    print(f"✓ İşlem kapatıldı: {symbol} [{system}] PnL: ${pnl:.6f} ({pnl_pct:.2f}%)")
                else:
                    print(f"❌ İşlem kapatılamadı: {symbol} [{system}]")
            else:
                print(f"❌ Açık işlem bulunamadı: {symbol} [{system}]")
                
        except Exception as e:
            print(f"❌ İşlem kapatma hatası: {e}")
    
    def get_position_status(self, symbol, system=None):
        """Pozisyon durumunu kontrol et"""
        trade_key = f"{symbol}_{system}" if system else symbol
        return self.open_trades.get(trade_key, {}).get('type', 'NONE')
    
    def get_summary(self):
        """Özet istatistikler"""
        total_trades = len(self.closed_trades)
        if total_trades == 0:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'avg_pnl': 0,
                'total_pnl': 0,
                'hybrid_stats': {'trades': 0, 'win_rate': 0, 'avg_pnl': 0},
                'elliott_stats': {'trades': 0, 'win_rate': 0, 'avg_pnl': 0}
            }
        
        # Genel istatistikler
        winning_trades = [t for t in self.closed_trades if t['pnl'] > 0]
        win_rate = len(winning_trades) / total_trades * 100
        total_pnl = sum(t['pnl'] for t in self.closed_trades)
        avg_pnl = total_pnl / total_trades
        
        # Sistem bazlı istatistikler
        hybrid_trades = [t for t in self.closed_trades if t.get('system') == 'HYBRID']
        elliott_trades = [t for t in self.closed_trades if t.get('system') == 'ELLIOTT']
        
        hybrid_stats = self._calculate_system_stats(hybrid_trades)
        elliott_stats = self._calculate_system_stats(elliott_trades)
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'avg_pnl': avg_pnl,
            'total_pnl': total_pnl,
            'hybrid_stats': hybrid_stats,
            'elliott_stats': elliott_stats
        }
    
    def _calculate_system_stats(self, trades):
        """Sistem bazlı istatistik hesapla"""
        if not trades:
            return {'trades': 0, 'win_rate': 0, 'avg_pnl': 0}
        
        winning_trades = [t for t in trades if t['pnl'] > 0]
        win_rate = len(winning_trades) / len(trades) * 100
        avg_pnl = sum(t['pnl'] for t in trades) / len(trades)
        
        return {
            'trades': len(trades),
            'win_rate': win_rate,
            'avg_pnl': avg_pnl
        }

# ----------------------------------------------------------------------
# 3. BİNANCE SEMBOLLERİ
# ----------------------------------------------------------------------

def get_all_binance_usdt_pairs():
    """Binance'den tüm USDT çiftlerini al"""
    try:
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        
        usdt_pairs = []
        for symbol, market in markets.items():
            if market['quote'] == 'USDT' and market['active']:
                usdt_pairs.append(symbol)
        
        usdt_pairs.sort()
        print(f"✓ {len(usdt_pairs)} USDT çifti bulundu")
        return usdt_pairs[:50]  # İlk 50 çift (test için)
        
    except Exception as e:
        print(f"❌ Binance sembol çekme hatası: {e}")
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']  # Fallback

# ----------------------------------------------------------------------
# 4. ANA TARAYICI
# ----------------------------------------------------------------------

class CryptoScanner:
    """Çoklu sistem tarayıcı"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.tv_client = None
        self.symbols = []
        self.hybrid_strategies = {}
        self.elliott_strategies = {}
        self.running = False
        self.scan_interval = 60
        self.dual_system_mode = DUAL_SYSTEM_MODE
        print(f"🚀 Kripto Sinyal Tarayıcı başlatıldı! Mod: {'Çoklu Sistem' if self.dual_system_mode else 'Tek Sistem'}")
    
    def initialize(self):
        """Başlat"""
        print("\n" + "="*70)
        print("### KRİPTO SİNYAL TARAYICI - ÇOKLU SİSTEM BAŞLATILIYOR ###")
        print("="*70)
        
        # TVDatafeed başlat
        try:
            self.tv_client = TvDatafeed(username=TV_USERNAME, password=TV_PASSWORD)
            print("✓ TVDatafeed bağlantısı kuruldu")
        except Exception as e:
            print(f"❌ TVDatafeed bağlantı hatası: {e}")
            return False
        
        # Sembolleri çek
        self.symbols = get_all_binance_usdt_pairs()
        print(f"✓ {len(self.symbols)} sembol yüklendi")
        
        # Her iki sistemi de oluştur
        for symbol in self.symbols:
            # Hibrit Strateji
            self.hybrid_strategies[symbol] = HybridIntradayStrategy(
                self.tv_client, symbol, TV_EXCHANGE, TIMEFRAME
            )
            
            # Elliott Strateji
            self.elliott_strategies[symbol] = ElliottWaveFibonacciStrategy(
                symbol, '1h'  # Swing trading için 1 saatlik
            )
        
        print("✓ Çoklu stratejiler hazırlandı")
        print("="*70 + "\n")
        return True
    
    def scan_once(self):
        """Çoklu sistem tarama döngüsü - Her iki sistemi de tarar"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}] Çoklu sistem taraması başladı...")
        
        total_signals = 0
        total_errors = 0
        
        # Her sembol için her iki sistemi de tara
        for symbol in self.symbols:
            try:
                # Mevcut pozisyon durumunu kontrol et (sistem bazlı)
                hybrid_position = self.data_manager.get_position_status(symbol, 'HYBRID')
                elliott_position = self.data_manager.get_position_status(symbol, 'ELLIOTT')
                
                # HİBRİT SİSTEM TARAMASI
                hybrid_strategy = self.hybrid_strategies[symbol]
                hybrid_strategy.fetch_data(n_bars=100)
                
                if hybrid_strategy.df is not None and not hybrid_strategy.df.empty:
                    hybrid_strategy.calculate_indicators()
                    signal, message, indicators = hybrid_strategy.generate_signal(hybrid_position)
                    
                    if signal and message:
                        price = indicators.get('close', 0)
                        atr_value = indicators.get('atr', 0)
                        
                        # Sistem adını ekle
                        system_message = f"[HİBRİT] {message}"
                        
                        # Sinyali kaydet
                        self.data_manager.add_signal(symbol, signal, system_message, price, indicators, 'HYBRID')
                        
                        # Giriş sinyali ise işlem aç
                        if signal in ['LONG_ENTRY', 'SHORT_ENTRY']:
                            self.data_manager.open_trade(symbol, signal, price, 
                                                       datetime.now(pytz.utc).isoformat(), 
                                                       atr_value, ATR_SL_MULTIPLIER, ATR_TP_MULTIPLIER, 'HYBRID')
                        
                        total_signals += 1
                        print(f"🔔 [HİBRİT] {symbol}: {signal} -> {message} @ ${price:.6f}")
                
                # ELLİOTT SİSTEM TARAMASI
                elliott_strategy = self.elliott_strategies[symbol]
                elliott_strategy.fetch_data(self.tv_client, limit=500)
                
                if elliott_strategy.df is not None and not elliott_strategy.df.empty:
                    elliott_strategy.calculate_indicators()
                    signal, message, indicators = elliott_strategy.generate_signal(elliott_position)
                    
                    if signal and message:
                        price = indicators.get('close', 0)
                        atr_value = indicators.get('atr', 0)
                        
                        # Sistem adını ekle
                        system_message = f"[ELLİOTT] {message}"
                        
                        # Sinyali kaydet
                        self.data_manager.add_signal(symbol, signal, system_message, price, indicators, 'ELLIOTT')
                        
                        # Giriş sinyali ise işlem aç
                        if signal in ['LONG_ENTRY', 'SHORT_ENTRY']:
                            self.data_manager.open_trade(symbol, signal, price, 
                                                       datetime.now(pytz.utc).isoformat(), 
                                                       atr_value, EWP_ATR_SL_MULTIPLIER, EWP_ATR_TP_MULTIPLIER, 'ELLIOTT')
                        
                        total_signals += 1
                        print(f"🌊 [ELLİOTT] {symbol}: {signal} -> {message} @ ${price:.6f}")
                        
            except Exception as e:
                total_errors += 1
                if total_errors <= 5:  # İlk 5 hatayı göster
                    print(f"⚠️ {symbol} hatası: {str(e)[:50]}...")
        
        if total_signals > 0:
            print(f"✅ {total_signals} yeni sinyal Supabase'e kaydedildi!")
        else:
            print(f"📊 Çoklu tarama tamamlandı. Yeni sinyal yok.")
        
        if total_errors > 0:
            print(f"⚠️ {total_errors} hata oluştu.")
    
    def run_continuous(self, interval_seconds=60):
        """Sürekli tarama"""
        print(f"🔄 Sürekli tarama başlatıldı ({interval_seconds}s aralık)")
        self.running = True
        
        while self.running:
            try:
                self.scan_once()
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\n🛑 Tarama durduruldu")
                break
            except Exception as e:
                print(f"❌ Tarama hatası: {e}")
                time.sleep(interval_seconds)

# ----------------------------------------------------------------------
# 5. ANA PROGRAM
# ----------------------------------------------------------------------

def main():
    """Ana program"""
    scanner = CryptoScanner()
    
    if not scanner.initialize():
        print("❌ Başlatma başarısız!")
        return
    
    try:
        # Tek tarama
        scanner.scan_once()
        
        # Sürekli tarama (opsiyonel)
        # scanner.run_continuous(interval_seconds=60)
        
    except KeyboardInterrupt:
        print("\n🛑 Program durduruldu")
    except Exception as e:
        print(f"❌ Program hatası: {e}")

if __name__ == "__main__":
    main()

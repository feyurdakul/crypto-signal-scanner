# -*- coding: utf-8 -*-
"""
Kripto Sinyal Tarayıcı - Ana Motor
CCXT ile Binance'deki tüm USDT çiftlerini tarar
İşlem takibi yapar (giriş/çıkış/kar-zarar)
"""

import pandas as pd
import numpy as np
import time
from datetime import datetime
import pytz
import threading
from supabase_client import SupabaseManager
from hybrid_intraday_strategy import HybridIntradayStrategy
from ewp_fibonacci_strategy import ElliottWaveFibonacciStrategy
from data_fetcher import DataFetcher

# ----------------------------------------------------------------------
# 1. AYARLAR
# ----------------------------------------------------------------------

# Çoklu Sistem Modu - Her iki sistem aynı anda çalışır
DUAL_SYSTEM_MODE = True

# Hibrit Strateji Parametreleri
ATR_SL_MULTIPLIER = 2.5  # Stop Loss: 2.5 x ATR
ATR_TP_MULTIPLIER = 7.5  # Take Profit: 7.5 x ATR

# Elliott Strateji Parametreleri
EWP_ATR_SL_MULTIPLIER = 3.0  # Swing trading için daha geniş SL
EWP_ATR_TP_MULTIPLIER = 7.5  # 1:2.5 risk/ödül oranı

# ----------------------------------------------------------------------
# 2. VERİ YÖNETİMİ
# ----------------------------------------------------------------------

class DataManager:
    """Supabase ile sinyal ve işlem verilerini yönetir"""
    
    def __init__(self):
        self.supabase = SupabaseManager()
        self.current_signals = {}
        self.open_trades = {}
        self.closed_trades = []
        self.load_data()
    
    def load_data(self):
        """Mevcut verileri Supabase'den yükle"""
        try:
            self.current_signals = self.supabase.get_current_signals()
            self.open_trades = self.supabase.get_open_trades()
            self.closed_trades = self.supabase.get_closed_trades()
            print(f"✓ Supabase'den {len(self.current_signals)} sinyal, {len(self.open_trades)} açık işlem yüklendi")
        except Exception as e:
            print(f"⚠️ Supabase veri yükleme hatası: {e}")
            self.current_signals = {}
            self.open_trades = {}
            self.closed_trades = []
    
    def add_signal(self, symbol, signal_type, message, price, indicators, system='HYBRID'):
        """Yeni sinyal ekle"""
        try:
            # Supabase'e ekle
            success = self.supabase.add_signal(symbol, signal_type, message, price, indicators, system)
            
            if success:
                # Local cache'i güncelle
                timestamp = datetime.now(pytz.utc).isoformat()
                key = f"{symbol}_{system}"
                self.current_signals[key] = {
                    'symbol': symbol,
                    'signal': signal_type,
                    'message': message,
                    'price': price,
                    'timestamp': timestamp,
                    'system': system,
                    **indicators
                }
                print(f"✅ [{system}] {symbol}: {signal_type} @ ${price:.6f}")
            else:
                print(f"❌ Sinyal eklenemedi: {symbol}")
                
        except Exception as e:
            print(f"❌ Sinyal ekleme hatası: {e}")
    
    def open_trade(self, symbol, entry_type, entry_price, timestamp, atr_value, sl_multiplier=None, tp_multiplier=None, system='HYBRID'):
        """Yeni işlem aç - ATR tabanlı SL/TP ile"""
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
            
            # Supabase'e kaydet
            success = self.supabase.open_trade(symbol, trade_type, entry_price, atr_value, stop_loss, take_profit, system)
            
            if success:
                key = f"{symbol}_{system}"
                self.open_trades[key] = {
                    'symbol': symbol,
                    'type': trade_type,
                    'entry_price': entry_price,
                    'entry_time': timestamp,
                    'status': 'OPEN',
                    'atr_value': atr_value,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'system': system
                }
                print(f"✓ [{system}] İşlem açıldı: {symbol} {trade_type} @ ${entry_price:.6f}")
                print(f"   SL: ${stop_loss:.6f} | TP: ${take_profit:.6f}")
            else:
                print(f"❌ İşlem açılamadı: {symbol}")
                
        except Exception as e:
            print(f"❌ İşlem açma hatası: {e}")
    
    def close_trade(self, symbol, exit_type, exit_price, timestamp, system='HYBRID'):
        """İşlem kapat ve kar/zarar hesapla"""
        try:
            closed_trade = self.supabase.close_trade(symbol, exit_price, system)
            
            if closed_trade:
                self.closed_trades.append(closed_trade)
                key = f"{symbol}_{system}"
                if key in self.open_trades:
                    del self.open_trades[key]
                print(f"✓ [{system}] İşlem kapandı: {symbol} PnL: {closed_trade['pnl_percent']:.2f}%")
            else:
                print(f"❌ İşlem kapatılamadı: {symbol}")
                
        except Exception as e:
            print(f"❌ İşlem kapatma hatası: {e}")
    
    def get_position_status(self, symbol, system='HYBRID'):
        """Sembol için pozisyon durumu"""
        return self.supabase.get_position_status(symbol, system)
    
    def get_summary(self):
        """Özet istatistikler"""
        return self.supabase.get_summary()

# ----------------------------------------------------------------------
# 3. TARAYICI
# ----------------------------------------------------------------------

class CryptoScanner:
    """Ana tarayıcı sınıfı"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.data_fetcher = DataFetcher()
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
        print("### KRİPTO SİNYAL TARAYICI - BAŞLATILIYOR ###")
        print("="*70)
        
        # Sembolleri çek
        self.symbols = self.data_fetcher.get_all_usdt_pairs()
        print(f"✓ {len(self.symbols)} sembol yüklendi")
        
        # Her iki sistemi de oluştur
        for symbol in self.symbols:
            # Hibrit Strateji (15 dakika)
            self.hybrid_strategies[symbol] = HybridIntradayStrategy(
                self.data_fetcher, symbol, '15m'
            )
            
            # Elliott Strateji (1 saat)
            self.elliott_strategies[symbol] = ElliottWaveFibonacciStrategy(
                self.data_fetcher, symbol, '1h'
            )
        
        print("✓ Stratejiler hazırlandı")
        print("="*70 + "\n")
        return True
    
    def scan_once(self):
        """Tek tarama döngüsü"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}] Tarama başladı...")
        
        signal_count = 0
        error_count = 0
        
        # Hibrit Sistem Taraması
        for symbol, strategy in self.hybrid_strategies.items():
            try:
                # Mevcut pozisyon durumunu kontrol et
                current_position = self.data_manager.get_position_status(symbol, 'HYBRID')
                
                # Veri çek ve analiz et
                if strategy.fetch_data(n_bars=100):
                    strategy.calculate_indicators()
                    signal, message, indicators = strategy.generate_signal(current_position)
                    
                    if signal and message:
                        price = indicators.get('close', 0)
                        atr_value = indicators.get('atr', 0)
                        
                        # Sinyali kaydet
                        self.data_manager.add_signal(symbol, signal, message, price, indicators, 'HYBRID')
                        
                        # Giriş sinyali ise işlem aç
                        if signal in ['LONG_ENTRY', 'SHORT_ENTRY']:
                            self.data_manager.open_trade(
                                symbol, signal, price, 
                                datetime.now(pytz.utc).isoformat(), 
                                atr_value, ATR_SL_MULTIPLIER, ATR_TP_MULTIPLIER, 'HYBRID'
                            )
                        # Çıkış sinyali ise işlem kapat
                        elif signal in ['LONG_EXIT', 'SHORT_EXIT']:
                            self.data_manager.close_trade(
                                symbol, signal, price,
                                datetime.now(pytz.utc).isoformat(), 'HYBRID'
                            )
                        
                        signal_count += 1
                        
            except Exception as e:
                error_count += 1
                if error_count <= 3:
                    print(f"⚠️ [HYBRID] {symbol} hatası: {str(e)[:50]}...")
        
        # Elliott Sistem Taraması
        for symbol, strategy in self.elliott_strategies.items():
            try:
                # Mevcut pozisyon durumunu kontrol et
                current_position = self.data_manager.get_position_status(symbol, 'ELLIOTT')
                
                # Veri çek ve analiz et
                if strategy.fetch_data(limit=500):
                    strategy.calculate_indicators()
                    signal, message, indicators = strategy.generate_signal(current_position)
                    
                    if signal and message:
                        price = indicators.get('close', 0)
                        atr_value = indicators.get('atr', 0)
                        
                        # Sinyali kaydet
                        self.data_manager.add_signal(symbol, signal, message, price, indicators, 'ELLIOTT')
                        
                        # Giriş sinyali ise işlem aç
                        if signal in ['LONG_ENTRY', 'SHORT_ENTRY']:
                            self.data_manager.open_trade(
                                symbol, signal, price, 
                                datetime.now(pytz.utc).isoformat(), 
                                atr_value, EWP_ATR_SL_MULTIPLIER, EWP_ATR_TP_MULTIPLIER, 'ELLIOTT'
                            )
                        # Çıkış sinyali ise işlem kapat
                        elif signal in ['LONG_EXIT', 'SHORT_EXIT']:
                            self.data_manager.close_trade(
                                symbol, signal, price,
                                datetime.now(pytz.utc).isoformat(), 'ELLIOTT'
                            )
                        
                        signal_count += 1
                        
            except Exception as e:
                error_count += 1
                if error_count <= 3:
                    print(f"⚠️ [ELLIOTT] {symbol} hatası: {str(e)[:50]}...")
        
        if signal_count > 0:
            print(f"✅ {signal_count} yeni sinyal Supabase'e kaydedildi!")
        else:
            print(f"📊 Tarama tamamlandı. Yeni sinyal yok.")
        
        if error_count > 0:
            print(f"⚠️ {error_count} sembol hatası (normal)")
    
    def start(self):
        """Sürekli taramayı başlat"""
        self.running = True
        
        while self.running:
            try:
                self.scan_once()
                time.sleep(self.scan_interval)
            except KeyboardInterrupt:
                print("\n\nTarama durduruldu.")
                self.running = False
                break
            except Exception as e:
                print(f"Hata: {e}")
                time.sleep(10)
    
    def stop(self):
        """Taramayı durdur"""
        self.running = False

# ----------------------------------------------------------------------
# 4. ANA FONKSİYON
# ----------------------------------------------------------------------

def run_scanner_background():
    """Arka planda tarayıcıyı başlat"""
    scanner = CryptoScanner()
    if scanner.initialize():
        scanner.start()

if __name__ == "__main__":
    run_scanner_background()

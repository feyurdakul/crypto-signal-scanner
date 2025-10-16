# -*- coding: utf-8 -*-
"""
Kripto Sinyal Tarayıcı - Sadece Hybrid Intraday Strategy
CCXT ile Binance'deki tüm USDT çiftlerini tarar
"""

import pandas as pd
import numpy as np
import time
from datetime import datetime
import pytz
import threading
from supabase_client import SupabaseManager
from hybrid_intraday_strategy import HybridIntradayStrategy
from data_fetcher import TVDataFetcher
import json
from pathlib import Path

# ----------------------------------------------------------------------
# 1. AYARLAR
# ----------------------------------------------------------------------

# Hibrit Strateji Parametreleri
ATR_SL_MULTIPLIER = 2.5  # Stop Loss: 2.5 x ATR
ATR_TP_MULTIPLIER = 7.5  # Take Profit: 7.5 x ATR

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
    
    def add_signal(self, symbol, signal_type, message, price, indicators, system='HYBRID_CRYPTO'):
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
    
    def open_trade(self, symbol, entry_type, entry_price, timestamp, atr_value, system='HYBRID_CRYPTO'):
        """Yeni işlem aç - ATR tabanlı SL/TP ile"""
        try:
            trade_type = 'LONG' if 'LONG' in entry_type else 'SHORT'
            
            # ATR tabanlı Stop Loss ve Take Profit hesapla
            if trade_type == 'LONG':
                stop_loss = entry_price - (atr_value * ATR_SL_MULTIPLIER)
                take_profit = entry_price + (atr_value * ATR_TP_MULTIPLIER)
            else:  # SHORT
                stop_loss = entry_price + (atr_value * ATR_SL_MULTIPLIER)
                take_profit = entry_price - (atr_value * ATR_TP_MULTIPLIER)
            
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
    
    def close_trade(self, symbol, exit_type, exit_price, timestamp, system='HYBRID_CRYPTO'):
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
    
    def get_position_status(self, symbol, system='HYBRID_CRYPTO'):
        """Sembol için pozisyon durumu"""
        return self.supabase.get_position_status(symbol, system)
    
    def get_summary(self):
        """Özet istatistikler"""
        return self.supabase.get_summary()

# ----------------------------------------------------------------------
# 3. TARAYICI
# ----------------------------------------------------------------------

class CryptoScanner:
    """Ana tarayıcı sınıfı - Sadece Crypto + Hybrid Strategy"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.data_fetcher = TVDataFetcher()
        self.symbols = []
        self.strategies = {}
        self.running = False
        self.scan_interval = 300  # 5 dakika = 300 saniye (15 dakikalık mum için optimal)
        print(f"🚀 Crypto Sinyal Tarayıcı başlatıldı! (TVDatafeed + Hybrid Strategy)")
        print(f"⏰ Tarama aralığı: {self.scan_interval} saniye ({self.scan_interval/60:.1f} dakika)")
    
    def initialize(self):
        """Başlat"""
        print("\n" + "="*70)
        print("### CRYPTO SİNYAL TARAYICI - HYBRID STRATEGY ###")
        print("="*70)
        
        # Sembolleri çek
        self.symbols = self.data_fetcher.get_all_usdt_pairs()
        print(f"✓ {len(self.symbols)} kripto sembolü yüklendi")
        
        # Hibrit Strateji oluştur (15 dakika)
        for symbol in self.symbols:
            self.strategies[symbol] = HybridIntradayStrategy(
                self.data_fetcher, symbol, '15m', 'CRYPTO'
            )
        
        print("✓ Stratejiler hazırlandı")
        print("="*70 + "\n")
        return True
    
    def scan_once(self):
        """Tek tarama döngüsü"""
        scan_time = datetime.now(pytz.utc)
        print(f"\n[{scan_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] Tarama başladı...")
        
        # Heartbeat dosyası yaz - Railway için
        self._write_heartbeat(scan_time)
        
        signal_count = 0
        error_count = 0
        
        # Hibrit Sistem Taraması
        for symbol, strategy in self.strategies.items():
            try:
                # Mevcut pozisyon durumunu kontrol et
                current_position = self.data_manager.get_position_status(symbol, 'HYBRID_CRYPTO')
                
                # Veri çek ve analiz et
                if strategy.fetch_data(n_bars=100):
                    strategy.calculate_indicators()
                    signal, message, indicators = strategy.generate_signal(current_position)
                    
                    if signal and message:
                        # Enhanced duplicate prevention
                        if current_position == 'LONG' and signal == 'LONG_ENTRY':
                            print(f"Skipping duplicate LONG_ENTRY for {symbol} (already in LONG position)")
                            continue
                        if current_position == 'SHORT' and signal == 'SHORT_ENTRY':
                            print(f"Skipping duplicate SHORT_ENTRY for {symbol} (already in SHORT position)")
                            continue
                        
                        price = indicators.get('close', 0)
                        atr_value = indicators.get('atr', 0)
                        
                        # Add signal (will be rejected if duplicate)
                        success = self.data_manager.add_signal(symbol, signal, message, price, indicators, 'HYBRID_CRYPTO')
                        
                        if success:
                            signal_count += 1
                            print(f"Processing signal: {symbol} {signal} @ ${price:.6f}")
                            
                            # Open/close trades with enhanced checks
                            if signal in ['LONG_ENTRY', 'SHORT_ENTRY']:
                                trade_success = self.data_manager.open_trade(
                                    symbol, signal, price, 
                                    atr_value, 0, 0, 'HYBRID_CRYPTO'
                                )
                                if trade_success:
                                    print(f"Trade opened: {symbol} {signal}")
                                else:
                                    print(f"Failed to open trade: {symbol} {signal}")
                            elif signal in ['LONG_EXIT', 'SHORT_EXIT']:
                                closed_trade = self.data_manager.close_trade(
                                    symbol, price, 'HYBRID_CRYPTO'
                                )
                                if closed_trade:
                                    print(f"Trade closed: {symbol} P&L: ${closed_trade.get('pnl_usd', 0):.2f}")
                                else:
                                    print(f"Failed to close trade: {symbol}")
                        
            except Exception as e:
                error_count += 1
                if error_count <= 3:
                    print(f"⚠️ {symbol} hatası: {str(e)[:50]}...")
        
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
    
    def _write_heartbeat(self, scan_time):
        """Heartbeat dosyası yaz - uygulamanın çalıştığını gösterir"""
        try:
            heartbeat_file = Path('heartbeat.json')
            heartbeat_data = {
                'last_scan': scan_time.isoformat(),
                'status': 'running',
                'timestamp': datetime.now(pytz.utc).isoformat()
            }
            heartbeat_file.write_text(json.dumps(heartbeat_data, indent=2))
        except Exception as e:
            print(f"⚠️ Heartbeat yazma hatası: {e}")

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

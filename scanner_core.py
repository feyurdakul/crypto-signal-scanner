# -*- coding: utf-8 -*-
"""
Kripto Sinyal Tarayıcı - Ana Motor
CCXT ile Binance'deki tüm USDT çiftlerini tarar
İşlem takibi yapar (giriş/çıkış/kar-zarar)
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

# Elliott Dalga ve Fibonacci Stratejisi Parametreleri
EWP_ATR_SL_MULTIPLIER = 3.0  # Swing trading için daha geniş SL
EWP_ATR_TP_MULTIPLIER = 7.5  # 1:2.5 risk/ödül oranı

# İşlem Saatleri (UTC)
TRADING_START_HOUR = 6  # 09:15 TR (UTC+3) = 06:15 UTC
TRADING_END_HOUR = 11   # 14:30 TR (UTC+3) = 11:30 UTC
SQUARE_OFF_HOUR = 12    # 15:00 TR (UTC+3) = 12:00 UTC

# Veri Depolama
DATA_FILE = 'trading_signals.json'
TRADES_FILE = 'trade_history.json'

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
    
    def add_signal(self, symbol, signal_type, message, price, indicators):
        """Yeni sinyal ekle"""
        try:
            # Supabase'e ekle
            success = self.supabase.add_signal(symbol, signal_type, message, price, indicators)
            
            if success:
                # Local cache'i güncelle
                timestamp = datetime.now(pytz.utc).isoformat()
                self.current_signals[symbol] = {
                    'symbol': symbol,
                    'signal': signal_type,
                    'message': message,
                    'price': price,
                    'timestamp': timestamp,
                    'rsi': indicators.get('rsi'),
                    'adx': indicators.get('adx'),
                    'vwap': indicators.get('vwap')
                }
                
                # İşlem takibi
                if signal_type in ['LONG_ENTRY', 'SHORT_ENTRY']:
                    self.open_trade(symbol, signal_type, price, timestamp)
                elif signal_type in ['LONG_EXIT', 'SHORT_EXIT']:
                    self.close_trade(symbol, signal_type, price, timestamp)
            else:
                print(f"❌ Sinyal eklenemedi: {symbol}")
                
        except Exception as e:
            print(f"❌ Sinyal ekleme hatası: {e}")
    
    def open_trade(self, symbol, entry_type, entry_price, timestamp, atr_value, sl_multiplier=None, tp_multiplier=None):
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
            success = self.supabase.open_trade(symbol, trade_type, entry_price, atr_value, stop_loss, take_profit)
            
            if success:
                self.open_trades[symbol] = {
                    'symbol': symbol,
                    'type': trade_type,
                    'entry_price': entry_price,
                    'entry_time': timestamp,
                    'status': 'OPEN',
                    'atr_value': atr_value,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
                print(f"✓ İşlem açıldı: {symbol} {trade_type} @ ${entry_price:.6f}")
                print(f"   SL: ${stop_loss:.6f} | TP: ${take_profit:.6f} | ATR: {atr_value:.6f}")
            else:
                print(f"❌ İşlem açılamadı: {symbol}")
                
        except Exception as e:
            print(f"❌ İşlem açma hatası: {e}")
    
    def close_trade(self, symbol, exit_type, exit_price, timestamp):
        """İşlem kapat ve kar/zarar hesapla"""
        try:
            closed_trade = self.supabase.close_trade(symbol, exit_price)
            
            if closed_trade:
                self.closed_trades.append(closed_trade)
                if symbol in self.open_trades:
                    del self.open_trades[symbol]
                print(f"✓ İşlem kapandı: {symbol} PnL: {closed_trade['pnl_percent']:.2f}%")
            else:
                print(f"❌ İşlem kapatılamadı: {symbol}")
                
        except Exception as e:
            print(f"❌ İşlem kapatma hatası: {e}")
    
    def get_position_status(self, symbol):
        """Sembol için pozisyon durumu"""
        return self.supabase.get_position_status(symbol)
    
    def get_summary(self):
        """Özet istatistikler"""
        return self.supabase.get_summary()

# ----------------------------------------------------------------------
# 3. SEMBOL ÇEKME (CCXT + TVDatafeed)
# ----------------------------------------------------------------------

def get_all_binance_usdt_pairs():
    """CCXT ile Binance'deki TÜM USDT çiftlerini çek"""
    try:
        exchange = ccxt.binance({'enableRateLimit': True})
        markets = exchange.load_markets()
        
        usdt_pairs = [
            symbol.replace('/', '') 
            for symbol, market in markets.items() 
            if market['quote'] == 'USDT' and market['active']
        ]
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Binance'den {len(usdt_pairs)} adet USDT çifti bulundu!")
        return sorted(usdt_pairs)
    
    except Exception as e:
        print(f"CCXT Hatası: {e}")
        # Fallback: Manuel liste
        return [
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
            'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT', 'LINKUSDT'
        ]

# ----------------------------------------------------------------------
# 4. STRATEJİ SINIFI
# ----------------------------------------------------------------------

class HybridIntradayStrategy:
    """Hibrit Gün İçi Momentum ve Sistemik Risk Yönetimi Stratejisi"""
    
    def __init__(self, tv_client, symbol, tv_exchange, timeframe):
        self.tv_client = tv_client
        self.symbol = symbol
        self.tv_exchange = tv_exchange
        self.timeframe = timeframe
        self.df = None
    
    def fetch_data(self, n_bars=100):
        """Veri çek"""
        try:
            df = self.tv_client.get_hist(
                symbol=self.symbol,
                exchange=self.tv_exchange,
                interval=self.timeframe,
                n_bars=n_bars
            )
            if df is not None and not df.empty and 'open' in df.columns:
                df.columns = [col.lower() for col in df.columns]
                self.df = df
            else:
                self.df = None
        except:
            self.df = None
    
    def calculate_indicators(self):
        """Göstergeleri hesapla - VWAP, RSI, ADX, ATR"""
        if self.df is None or len(self.df) < max(ADX_LENGTH, RSI_LENGTH, ATR_LENGTH) + 2:
            return
        
        # VWAP (Hacim Ağırlıklı Ortalama Fiyat)
        self.df['typical_price'] = (self.df['high'] + self.df['low'] + self.df['close']) / 3
        self.df['tp_volume'] = self.df['typical_price'] * self.df['volume']
        self.df['cumulative_tp_volume'] = self.df['tp_volume'].cumsum()
        self.df['cumulative_volume'] = self.df['volume'].cumsum()
        self.df['VWAP'] = self.df['cumulative_tp_volume'] / self.df['cumulative_volume']
        
        # RSI (Göreceli Güç Endeksi)
        self.df.ta.rsi(length=RSI_LENGTH, append=True)
        self.df['RSI'] = self.df[f'RSI_{RSI_LENGTH}']
        self.df['RSI_Prev'] = self.df['RSI'].shift(1)
        
        # ADX (Ortalama Yön Endeksi)
        self.df.ta.adx(length=ADX_LENGTH, append=True)
        self.df['ADX'] = self.df[f'ADX_{ADX_LENGTH}']
        
        # ATR (Ortalama Gerçek Aralık) - Volatilite ve Risk Yönetimi
        self.df.ta.atr(length=ATR_LENGTH, append=True)
        self.df['ATR'] = self.df[f'ATR_{ATR_LENGTH}']
        
        # Temel fiyat verileri
        self.df['Close'] = self.df['close']
        self.df['High'] = self.df['high']
        self.df['Low'] = self.df['low']
        
        self.df.dropna(inplace=True)
    
    def is_trading_time(self):
        """İşlem saatlerinde mi kontrol et (09:15-14:30 TR)"""
        now = datetime.now(pytz.utc)
        current_hour = now.hour
        return TRADING_START_HOUR <= current_hour <= TRADING_END_HOUR
    
    def is_square_off_time(self):
        """Square off zamanı mı (15:00 TR)"""
        now = datetime.now(pytz.utc)
        return now.hour >= SQUARE_OFF_HOUR
    
    def generate_signal(self, current_position='NONE'):
        """Hibrit strateji sinyali üret"""
        if self.df is None or self.df.empty or len(self.df) < 2:
            return None, None, {}
        
        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2]
        
        indicators = {
            'rsi': round(latest['RSI'], 2),
            'adx': round(latest['ADX'], 2),
            'vwap': round(latest['VWAP'], 2),
            'atr': round(latest['ATR'], 6),
            'close': round(latest['Close'], 6)
        }
        
        # ZAMAN TABANLI ÇIKIŞ - Zorunlu Square Off
        if self.is_square_off_time():
            if current_position == 'LONG':
                return 'LONG_EXIT', "🚪 SEANS SONU - UZUN POZİSYON KAPAT", indicators
            elif current_position == 'SHORT':
                return 'SHORT_EXIT', "🚪 SEANS SONU - KISA POZİSYON KAPAT", indicators
        
        # AÇIK POZİSYON VARSA - ÇIKIŞ SİNYALLERİ KONTROL ET
        if current_position == 'LONG':
            # LONG pozisyon açık - ATR tabanlı SL/TP veya VWAP çıkış kontrol et
            # ATR Stop Loss kontrolü (2.5 x ATR)
            if latest['Low'] <= latest['stop_loss'] if 'stop_loss' in latest else False:
                return 'LONG_EXIT', "🛑 STOP LOSS - UZUN POZİSYON KAPAT", indicators
            
            # ATR Take Profit kontrolü (7.5 x ATR)
            if latest['High'] >= latest['take_profit'] if 'take_profit' in latest else False:
                return 'LONG_EXIT', "💰 TAKE PROFIT - UZUN POZİSYON KAPAT", indicators
            
            # VWAP tabanlı çıkış
            if latest['Close'] < latest['VWAP']:
                return 'LONG_EXIT', "📉 VWAP KIRILIMI - UZUN POZİSYON KAPAT", indicators
            
            return None, None, indicators
        
        elif current_position == 'SHORT':
            # SHORT pozisyon açık - ATR tabanlı SL/TP veya VWAP çıkış kontrol et
            # ATR Stop Loss kontrolü (2.5 x ATR)
            if latest['High'] >= latest['stop_loss'] if 'stop_loss' in latest else False:
                return 'SHORT_EXIT', "🛑 STOP LOSS - KISA POZİSYON KAPAT", indicators
            
            # ATR Take Profit kontrolü (7.5 x ATR)
            if latest['Low'] <= latest['take_profit'] if 'take_profit' in latest else False:
                return 'SHORT_EXIT', "💰 TAKE PROFIT - KISA POZİSYON KAPAT", indicators
            
            # VWAP tabanlı çıkış
            if latest['Close'] > latest['VWAP']:
                return 'SHORT_EXIT', "📈 VWAP KIRILIMI - KISA POZİSYON KAPAT", indicators
            
            return None, None, indicators
        
        # POZİSYON KAPALI - GİRİŞ SİNYALLERİ ARAYIN
        # Sadece işlem saatlerinde giriş sinyali ver
        if not self.is_trading_time():
            return None, None, indicators
        
        # LONG GİRİŞ KOŞULLARI
        buy_vwap = latest['Close'] > latest['VWAP']  # VWAP Onayı
        buy_adx = latest['ADX'] < ADX_LEVEL  # Trend Zayıflığı (Konsolidasyon)
        buy_rsi_cross = prev['RSI'] <= RSI_BUY_LEVEL and latest['RSI'] > RSI_BUY_LEVEL  # RSI 55'i yukarı kesme
        
        if buy_vwap and buy_adx and buy_rsi_cross:
            return 'LONG_ENTRY', "📈 ALIM SİNYALİ", indicators
        
        # SHORT GİRİŞ KOŞULLARI
        sell_vwap = latest['Close'] < latest['VWAP']  # VWAP Onayı
        sell_adx = latest['ADX'] < ADX_LEVEL  # Trend Zayıflığı (Konsolidasyon)
        sell_rsi_cross = prev['RSI'] >= RSI_SELL_LEVEL and latest['RSI'] < RSI_SELL_LEVEL  # RSI 35'i aşağı kesme
        
        if sell_vwap and sell_adx and sell_rsi_cross:
            return 'SHORT_ENTRY', "📉 SATIM SİNYALİ", indicators
        
        return None, None, indicators

# ----------------------------------------------------------------------
# 5. TARAYICI
# ----------------------------------------------------------------------

class CryptoScanner:
    """Ana tarayıcı sınıfı"""
    
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
        print("### KRİPTO SİNYAL TARAYICI - BAŞLATILIYOR ###")
        print("="*70)
        
        # TradingView bağlantısı
        try:
            self.tv_client = TvDatafeed(TV_USERNAME, TV_PASSWORD)
            print("✓ TradingView bağlantısı kuruldu")
        except Exception as e:
            print(f"✗ TradingView hatası: {e}")
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
        
        print("✓ Stratejiler hazırlandı")
        print("="*70 + "\n")
        return True
    
    def scan_once(self):
        """Tek tarama döngüsü"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}] Tarama başladı...")
        
        signal_count = 0
        error_count = 0
        
        for symbol, strategy in self.strategies.items():
            try:
                # Mevcut pozisyon durumunu kontrol et
                current_position = 'NONE'
                if symbol in self.data_manager.open_trades:
                    current_position = self.data_manager.open_trades[symbol]['type']
                
                # Strateji tipine göre veri çek
                if self.strategy_mode == "HYBRID":
                    strategy.fetch_data(n_bars=100)
                elif self.strategy_mode == "ELLIOTT":
                    strategy.fetch_data(self.tv_client, limit=500)
                
                if strategy.df is not None and not strategy.df.empty:
                    strategy.calculate_indicators()
                    # Pozisyon durumunu gönder
                    signal, message, indicators = strategy.generate_signal(current_position)
                    
                    if signal and message:
                        price = indicators.get('close', 0)
                        atr_value = indicators.get('atr', 0)
                        
                        # Sinyali kaydet
                        self.data_manager.add_signal(symbol, signal, message, price, indicators)
                        
                        # Giriş sinyali ise işlem aç
                        if signal in ['LONG_ENTRY', 'SHORT_ENTRY']:
                            # Strateji tipine göre ATR çarpanları
                            if self.strategy_mode == "ELLIOTT":
                                sl_multiplier = EWP_ATR_SL_MULTIPLIER
                                tp_multiplier = EWP_ATR_TP_MULTIPLIER
                            else:
                                sl_multiplier = ATR_SL_MULTIPLIER
                                tp_multiplier = ATR_TP_MULTIPLIER
                            
                            self.data_manager.open_trade(symbol, signal, price, 
                                                       datetime.now(pytz.utc).isoformat(), 
                                                       atr_value, sl_multiplier, tp_multiplier)
                        
                        signal_count += 1
                        print(f"🔔 {symbol}: {signal} -> {message} @ ${price:.6f}")
                        
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # İlk 5 hatayı göster
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

# ----------------------------------------------------------------------
# 6. ANA FONKSİYON
# ----------------------------------------------------------------------

def run_scanner_background():
    """Arka planda tarayıcıyı başlat"""
    scanner = CryptoScanner()
    if scanner.initialize():
        scanner.start()

if __name__ == "__main__":
    run_scanner_background()


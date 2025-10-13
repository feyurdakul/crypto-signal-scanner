"""
Hibrit Gün İçi Momentum ve Sistemik Risk Yönetimi Stratejisi
============================================================

Bu strateji, VWAP, ADX ve RSI göstergelerini kullanarak gün içi momentum takibi yapar.
ATR tabanlı risk yönetimi ile sistemik risk kontrolü sağlar.

Özellikler:
- VWAP tabanlı fiyat yönü belirleme
- ADX ile trend gücü kontrolü (konsolidasyon arama)
- RSI ile momentum kırılması teyidi
- ATR tabanlı dinamik Stop Loss/Take Profit
- Zaman tabanlı square off
"""

import pandas as pd
import numpy as np
import pandas_ta as ta
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pytz

class HybridIntradayStrategy:
    """Hibrit Gün İçi Momentum ve Sistemik Risk Yönetimi Stratejisi"""
    
    def __init__(self, tv_client, symbol: str, exchange: str, timeframe):
        self.tv_client = tv_client
        self.symbol = symbol
        self.exchange = exchange
        self.timeframe = timeframe
        self.df = None
        
        # Strateji parametreleri
        self.ADX_LENGTH = 20
        self.RSI_LENGTH = 14
        self.ATR_LENGTH = 14
        self.ADX_LEVEL = 30
        self.RSI_BUY_LEVEL = 55
        self.RSI_SELL_LEVEL = 35
        
        # İşlem saatleri (UTC)
        self.TRADING_START_HOUR = 6   # 09:15 TR (UTC+3) = 06:15 UTC
        self.TRADING_END_HOUR = 11    # 14:30 TR (UTC+3) = 11:30 UTC
        self.SQUARE_OFF_HOUR = 12     # 15:00 TR (UTC+3) = 12:00 UTC
        
        print(f"🎯 Hibrit Strateji başlatıldı: {symbol}")
    
    def fetch_data(self, n_bars: int = 100) -> bool:
        """Veri çek"""
        try:
            data = self.tv_client.get_hist(
                symbol=self.symbol,
                exchange=self.exchange,
                interval=self.timeframe,
                n_bars=n_bars
            )
            
            if data is not None and not data.empty:
                self.df = data.copy()
                self.df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ {self.symbol} veri çekme hatası: {e}")
            return False
    
    def calculate_indicators(self):
        """Teknik göstergeleri hesapla"""
        if self.df is None or self.df.empty:
            return
        
        try:
            # VWAP hesaplama (manuel)
            self.df['typical_price'] = (self.df['high'] + self.df['low'] + self.df['close']) / 3
            self.df['tp_volume'] = self.df['typical_price'] * self.df['volume']
            self.df['cumulative_tp_volume'] = self.df['tp_volume'].cumsum()
            self.df['cumulative_volume'] = self.df['volume'].cumsum()
            self.df['VWAP'] = self.df['cumulative_tp_volume'] / self.df['cumulative_volume']
            
            # ADX hesaplama
            self.df['ADX'] = ta.adx(self.df['high'], self.df['low'], self.df['close'], length=self.ADX_LENGTH)['ADX_20']
            
            # RSI hesaplama
            self.df['RSI'] = ta.rsi(self.df['close'], length=self.RSI_LENGTH)
            
            # ATR hesaplama
            self.df['ATR'] = ta.atr(self.df['high'], self.df['low'], self.df['close'], length=self.ATR_LENGTH)
            
        except Exception as e:
            print(f"❌ {self.symbol} gösterge hesaplama hatası: {e}")
    
    def is_trading_time(self) -> bool:
        """İşlem saatlerinde mi kontrol et (09:15-14:30 TR)"""
        now = datetime.now(pytz.utc)
        current_hour = now.hour
        return self.TRADING_START_HOUR <= current_hour <= self.TRADING_END_HOUR
    
    def is_square_off_time(self) -> bool:
        """Square off zamanı mı (15:00 TR)"""
        now = datetime.now(pytz.utc)
        return now.hour >= self.SQUARE_OFF_HOUR
    
    def generate_signal(self, current_position: str = 'NONE') -> Tuple[Optional[str], Optional[str], Dict]:
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
            # LONG pozisyon açık - VWAP çıkış kontrol et
            if latest['Close'] < latest['VWAP']:
                return 'LONG_EXIT', "📉 VWAP KIRILIMI - UZUN POZİSYON KAPAT", indicators
            
            return None, None, indicators
        
        elif current_position == 'SHORT':
            # SHORT pozisyon açık - VWAP çıkış kontrol et
            if latest['Close'] > latest['VWAP']:
                return 'SHORT_EXIT', "📈 VWAP KIRILIMI - KISA POZİSYON KAPAT", indicators
            
            return None, None, indicators
        
        # POZİSYON KAPALI - GİRİŞ SİNYALLERİ ARAYIN
        # Sadece işlem saatlerinde giriş sinyali ver
        if not self.is_trading_time():
            return None, None, indicators
        
        # LONG GİRİŞ KOŞULLARI
        buy_vwap = latest['Close'] > latest['VWAP']  # VWAP Onayı
        buy_adx = latest['ADX'] < self.ADX_LEVEL  # Trend Zayıflığı (Konsolidasyon)
        buy_rsi_cross = prev['RSI'] <= self.RSI_BUY_LEVEL and latest['RSI'] > self.RSI_BUY_LEVEL  # RSI 55'i yukarı kesme
        
        if buy_vwap and buy_adx and buy_rsi_cross:
            return 'LONG_ENTRY', "📈 ALIM SİNYALİ", indicators
        
        # SHORT GİRİŞ KOŞULLARI
        sell_vwap = latest['Close'] < latest['VWAP']  # VWAP Onayı
        sell_adx = latest['ADX'] < self.ADX_LEVEL  # Trend Zayıflığı (Konsolidasyon)
        sell_rsi_cross = prev['RSI'] >= self.RSI_SELL_LEVEL and latest['RSI'] < self.RSI_SELL_LEVEL  # RSI 35'i aşağı kesme
        
        if sell_vwap and sell_adx and sell_rsi_cross:
            return 'SHORT_ENTRY', "📉 SATIM SİNYALİ", indicators
        
        return None, None, indicators

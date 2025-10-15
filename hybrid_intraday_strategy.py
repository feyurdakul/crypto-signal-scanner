"""
Intraday Trading Strategy (VWAP + ADX + RSI)
============================================

Bu strateji, VWAP, ADX ve RSI göstergelerini kullanarak gün içi momentum takibi yapar.

BUY RULES:
1. Fiyat VWAP üzerinde kapanmalı
2. ADX 30'un altında olmalı
3. RSI 55'i yukarı kesip üzerinde kapanmalı

SELL RULES:
1. Fiyat VWAP altında kapanmalı
2. ADX 30'un altında olmalı
3. RSI 35'i aşağı kesip altında kapanmalı

EXIT RULES:
- BUY EXIT: Fiyat VWAP altına düşerse veya square off zamanında otomatik kapat
- SELL EXIT: Fiyat VWAP üzerine çıkarsa veya square off zamanında otomatik kapat

İşlem Saatleri:
- CRYPTO: 7/24 (Her zaman açık)
- BIST: 10:00-17:00 TR (Hafta içi)
- US: 09:30-16:00 ET (Hafta içi)

Square Off:
- CRYPTO: Yok (7/24 çalışır)
- BIST: 18:00 TR (Tüm pozisyonlar otomatik kapanır)
- US: 16:00 ET (Market kapanışında otomatik kapanır)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pytz
from technical_indicators import calculate_rsi, calculate_adx, calculate_atr, calculate_vwap

class HybridIntradayStrategy:
    """Hibrit Gün İçi Momentum ve Sistemik Risk Yönetimi Stratejisi"""
    
    def __init__(self, data_fetcher, symbol: str, timeframe='15m', market_type='CRYPTO'):
        self.data_fetcher = data_fetcher
        self.symbol = symbol
        self.timeframe = timeframe
        self.market_type = market_type  # 'CRYPTO' veya 'BIST'
        self.df = None
        
        # Strateji parametreleri (TradingView koduna göre)
        self.ADX_LENGTH = 20
        self.DI_LENGTH = 10
        self.RSI_LENGTH = 14
        self.ATR_LENGTH = 14
        self.ADX_LEVEL = 30
        self.RSI_BUY_LEVEL = 55
        self.RSI_SELL_LEVEL = 35
        
        # İşlem saatleri (Market type'a göre)
        if market_type == 'CRYPTO':
            # Kripto: 7/24 çalışır
            self.TRADING_START_TIME = None
            self.TRADING_END_TIME = None
            self.SQUARE_OFF_TIME = None
            self.TIMEZONE = None
        elif market_type == 'BIST':
            # BIST: 10:00-17:00 TR, Square Off: 18:00 TR
            self.TRADING_START_TIME = "10:00"
            self.TRADING_END_TIME = "17:00"
            self.SQUARE_OFF_TIME = "18:00"
            self.TIMEZONE = 'Europe/Istanbul'
        else:  # US
            # US: 09:30-16:00 ET, Square Off: 16:00 ET (market kapanışı)
            self.TRADING_START_TIME = "09:30"
            self.TRADING_END_TIME = "16:00"
            self.SQUARE_OFF_TIME = "16:00"
            self.TIMEZONE = 'America/New_York'
        
        print(f"🎯 Hibrit Strateji başlatıldı: {symbol} ({market_type})")
    
    def fetch_data(self, n_bars: int = 100) -> bool:
        """Veri çek"""
        try:
            self.df = self.data_fetcher.get_ohlcv(self.symbol, self.timeframe, n_bars)
            return self.df is not None and not self.df.empty
                
        except Exception as e:
            print(f"❌ {self.symbol} veri çekme hatası: {e}")
            return False
    
    def calculate_indicators(self):
        """Teknik göstergeleri hesapla"""
        if self.df is None or self.df.empty:
            return
        
        try:
            # VWAP hesaplama
            self.df['VWAP'] = calculate_vwap(
                self.df['High'], 
                self.df['Low'], 
                self.df['Close'], 
                self.df['Volume']
            )
            
            # ADX hesaplama
            self.df['ADX'] = calculate_adx(
                self.df['High'], 
                self.df['Low'], 
                self.df['Close'], 
                length=self.ADX_LENGTH
            )
            
            # RSI hesaplama
            self.df['RSI'] = calculate_rsi(self.df['Close'], length=self.RSI_LENGTH)
            
            # ATR hesaplama
            self.df['ATR'] = calculate_atr(
                self.df['High'], 
                self.df['Low'], 
                self.df['Close'], 
                length=self.ATR_LENGTH
            )
            
        except Exception as e:
            print(f"❌ {self.symbol} gösterge hesaplama hatası: {e}")
    
    def is_trading_time(self) -> bool:
        """İşlem saatlerinde mi kontrol et"""
        # Kripto için her zaman True
        if self.market_type == 'CRYPTO':
            return True
        
        # BIST ve US için işlem saatleri kontrolü
        tz = pytz.timezone(self.TIMEZONE)
        now_local = datetime.now(tz)
        current_time = now_local.time()
        
        start_time = datetime.strptime(self.TRADING_START_TIME, '%H:%M').time()
        end_time = datetime.strptime(self.TRADING_END_TIME, '%H:%M').time()
        
        return start_time <= current_time <= end_time
    
    def is_square_off_time(self) -> bool:
        """Square off zamanı mı"""
        # Kripto için square off yok
        if self.market_type == 'CRYPTO':
            return False
        
        # BIST ve US için square off kontrolü
        tz = pytz.timezone(self.TIMEZONE)
        now_local = datetime.now(tz)
        current_time = now_local.time()
        
        square_off_time = datetime.strptime(self.SQUARE_OFF_TIME, '%H:%M').time()
        
        return current_time >= square_off_time
    
    def generate_signal(self, current_position: str = 'NONE') -> Tuple[Optional[str], Optional[str], Dict]:
        """Intraday Trading Strategy - TradingView koduna göre"""
        if self.df is None or self.df.empty or len(self.df) < 2:
            return None, None, {}
        
        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2]
        
        indicators = {
            'rsi': round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else 0,
            'adx': round(latest['ADX'], 2) if not pd.isna(latest['ADX']) else 0,
            'vwap': round(latest['VWAP'], 2) if not pd.isna(latest['VWAP']) else 0,
            'atr': round(latest['ATR'], 6) if not pd.isna(latest['ATR']) else 0,
            'close': round(latest['Close'], 6)
        }
        
        # ZAMAN TABANLI ÇIKIŞ - Square Off (Sadece BIST için 18:00 TR)
        if self.is_square_off_time():
            if current_position == 'LONG':
                return 'LONG_EXIT', "🚪 18:00 SQUARE OFF - UZUN POZİSYON KAPAT", indicators
            elif current_position == 'SHORT':
                return 'SHORT_EXIT', "🚪 18:00 SQUARE OFF - KISA POZİSYON KAPAT", indicators
        
        # AÇIK POZİSYON VARSA - ÇIKIŞ SİNYALLERİ
        if current_position == 'LONG':
            # BUY EXIT: Fiyat VWAP altına düşerse
            if latest['Close'] < latest['VWAP']:
                return 'LONG_EXIT', "📉 VWAP ALTINA DÜŞTÜ - UZUN POZİSYON KAPAT", indicators
            return None, None, indicators
        
        elif current_position == 'SHORT':
            # SELL EXIT: Fiyat VWAP üzerine çıkarsa
            if latest['Close'] > latest['VWAP']:
                return 'SHORT_EXIT', "📈 VWAP ÜSTÜNE ÇIKTI - KISA POZİSYON KAPAT", indicators
            return None, None, indicators
        
        # POZİSYON KAPALI - GİRİŞ SİNYALLERİ
        # Sadece işlem saatlerinde giriş (09:15-14:30 TR)
        if not self.is_trading_time():
            return None, None, indicators
        
        # BUY RULES (Esnek versiyon - daha fazla sinyal için)
        # 1. Fiyat VWAP üzerinde kapanmalı
        buy_vwap = latest['Close'] > latest['VWAP']
        
        # 2. ADX 30'un altında olmalı (düşük volatilite)
        buy_adx = latest['ADX'] < self.ADX_LEVEL
        
        # 3. RSI 55'in üzerinde (momentum var)
        buy_rsi = latest['RSI'] > self.RSI_BUY_LEVEL
        
        if buy_vwap and buy_adx and buy_rsi:
            return 'LONG_ENTRY', "📈 ALIM SİNYALİ", indicators
        
        # SELL RULES (Esnek versiyon - daha fazla sinyal için)
        # 1. Fiyat VWAP altında kapanmalı
        sell_vwap = latest['Close'] < latest['VWAP']
        
        # 2. ADX 30'un altında olmalı (düşük volatilite)
        sell_adx = latest['ADX'] < self.ADX_LEVEL
        
        # 3. RSI 35'in altında (zayıf momentum)
        sell_rsi = latest['RSI'] < self.RSI_SELL_LEVEL
        
        if sell_vwap and sell_adx and sell_rsi:
            return 'SHORT_ENTRY', "📉 SATIM SİNYALİ", indicators
        
        return None, None, indicators

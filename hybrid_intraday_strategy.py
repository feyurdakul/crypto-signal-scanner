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
- BUY EXIT: Fiyat VWAP altına düşerse veya saat 15:00'da otomatik kapat
- SELL EXIT: Fiyat VWAP üzerine çıkarsa veya saat 15:00'da otomatik kapat

İşlem Saatleri: 09:15 - 14:30 (Sadece bu saatler arası giriş)
Square Off: 15:00 (Tüm pozisyonlar otomatik kapanır)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pytz
from technical_indicators import calculate_rsi, calculate_adx, calculate_atr, calculate_vwap

class HybridIntradayStrategy:
    """Hibrit Gün İçi Momentum ve Sistemik Risk Yönetimi Stratejisi"""
    
    def __init__(self, data_fetcher, symbol: str, timeframe='15m'):
        self.data_fetcher = data_fetcher
        self.symbol = symbol
        self.timeframe = timeframe
        self.df = None
        
        # Strateji parametreleri (TradingView koduna göre)
        self.ADX_LENGTH = 20
        self.DI_LENGTH = 10
        self.RSI_LENGTH = 14
        self.ATR_LENGTH = 14
        self.ADX_LEVEL = 30
        self.RSI_BUY_LEVEL = 55
        self.RSI_SELL_LEVEL = 35
        
        # İşlem saatleri (TR saati - UTC+3)
        self.TRADING_START_TIME = "09:15"  # 09:15 TR
        self.TRADING_END_TIME = "14:30"    # 14:30 TR
        self.SQUARE_OFF_TIME = "15:00"     # 15:00 TR (Otomatik kapat)
        
        print(f"🎯 Hibrit Strateji başlatıldı: {symbol}")
    
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
        """İşlem saatlerinde mi kontrol et (09:15-14:30 TR)"""
        tr_tz = pytz.timezone('Europe/Istanbul')
        now_tr = datetime.now(tr_tz)
        current_time = now_tr.time()
        
        start_time = datetime.strptime(self.TRADING_START_TIME, '%H:%M').time()
        end_time = datetime.strptime(self.TRADING_END_TIME, '%H:%M').time()
        
        return start_time <= current_time <= end_time
    
    def is_square_off_time(self) -> bool:
        """Square off zamanı mı (15:00 TR)"""
        tr_tz = pytz.timezone('Europe/Istanbul')
        now_tr = datetime.now(tr_tz)
        current_time = now_tr.time()
        
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
        
        # ZAMAN TABANLI ÇIKIŞ - Square Off (15:00 TR)
        if self.is_square_off_time():
            if current_position == 'LONG':
                return 'LONG_EXIT', "🚪 15:00 SQUARE OFF - UZUN POZİSYON KAPAT", indicators
            elif current_position == 'SHORT':
                return 'SHORT_EXIT', "🚪 15:00 SQUARE OFF - KISA POZİSYON KAPAT", indicators
        
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
        
        # BUY RULES (TradingView koduna göre)
        # 1. Fiyat VWAP üzerinde kapanmalı
        buy_vwap = latest['Close'] > latest['VWAP']
        
        # 2. ADX 30'un altında olmalı
        buy_adx = latest['ADX'] < self.ADX_LEVEL
        
        # 3. RSI 55'i yukarı kesip üzerinde kapanmalı (crossover)
        buy_rsi_cross = prev['RSI'] <= self.RSI_BUY_LEVEL and latest['RSI'] > self.RSI_BUY_LEVEL
        
        if buy_vwap and buy_adx and buy_rsi_cross:
            return 'LONG_ENTRY', "📈 ALIM SİNYALİ", indicators
        
        # SELL RULES (TradingView koduna göre)
        # 1. Fiyat VWAP altında kapanmalı
        sell_vwap = latest['Close'] < latest['VWAP']
        
        # 2. ADX 30'un altında olmalı
        sell_adx = latest['ADX'] < self.ADX_LEVEL
        
        # 3. RSI 35'i aşağı kesip altında kapanmalı (crossunder)
        sell_rsi_cross = prev['RSI'] >= self.RSI_SELL_LEVEL and latest['RSI'] < self.RSI_SELL_LEVEL
        
        if sell_vwap and sell_adx and sell_rsi_cross:
            return 'SHORT_ENTRY', "📉 SATIM SİNYALİ", indicators
        
        return None, None, indicators

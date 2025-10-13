"""
Elliott Dalga Prensibi ve Fibonacci Temelli Pozisyon Ticareti (Swing Trading) Stratejisi
======================================================================================

Bu strateji, ana trend içindeki güçlü itki dalgalarını (Dalga 3 ve Dalga 5) yakalamak
ve düzeltme dalgalarının (Dalga 2 ve Dalga 4) bittiği noktada pozisyona girmeyi hedefler.

Özellikler:
- Elliott Dalga sayımı
- Fibonacci retracement seviyeleri (%50, %61.8, %78.6)
- SMA 50/200 trend filtresi
- RSI momentum dönüş sinyali
- ATR tabanlı risk yönetimi (3.0x ATR SL, 7.5x ATR TP)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pytz
from technical_indicators import calculate_rsi, calculate_atr, calculate_sma

class ElliottWaveFibonacciStrategy:
    """Elliott Dalga ve Fibonacci Temelli Swing Trading Stratejisi"""
    
    def __init__(self, data_fetcher, symbol: str, timeframe: str = '1h'):
        self.data_fetcher = data_fetcher
        self.symbol = symbol
        self.timeframe = timeframe
        self.df = None
        
        # Strateji parametreleri
        self.SMA_FAST = 50
        self.SMA_SLOW = 200
        self.RSI_PERIOD = 14
        self.ATR_PERIOD = 14
        
        # Risk yönetimi
        self.ATR_SL_MULTIPLIER = 3.0  # Swing trading için daha geniş SL
        self.ATR_TP_MULTIPLIER = 7.5  # 1:2.5 risk/ödül oranı
        
        # Fibonacci seviyeleri
        self.FIB_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]
        
        # RSI seviyeleri
        self.RSI_OVERSOLD = 40
        self.RSI_OVERBOUGHT = 70
        self.RSI_MOMENTUM = 50
        
        print(f"🌊 Elliott Dalga Stratejisi başlatıldı: {symbol}")
    
    def fetch_data(self, limit: int = 500) -> bool:
        """Veri çek - Swing trading için daha uzun periyot"""
        try:
            self.df = self.data_fetcher.get_ohlcv(self.symbol, self.timeframe, limit)
            
            if self.df is not None and not self.df.empty:
                print(f"✅ {self.symbol} verisi çekildi: {len(self.df)} mum")
                return True
            else:
                print(f"❌ {self.symbol} veri çekilemedi")
                return False
                
        except Exception as e:
            print(f"❌ {self.symbol} veri çekme hatası: {e}")
            return False
    
    def calculate_indicators(self):
        """Teknik göstergeleri hesapla"""
        if self.df is None or self.df.empty:
            return
        
        try:
            # SMA'lar (Trend filtresi)
            self.df['SMA_50'] = calculate_sma(self.df['Close'], length=self.SMA_FAST)
            self.df['SMA_200'] = calculate_sma(self.df['Close'], length=self.SMA_SLOW)
            
            # RSI (Momentum)
            self.df['RSI'] = calculate_rsi(self.df['Close'], length=self.RSI_PERIOD)
            
            # ATR (Volatilite)
            self.df['ATR'] = calculate_atr(self.df['High'], self.df['Low'], self.df['Close'], length=self.ATR_PERIOD)
            
            # Fibonacci hesaplamaları için swing noktaları
            self._calculate_swing_points()
            self._calculate_fibonacci_levels()
            
            print(f"✅ {self.symbol} göstergeler hesaplandı")
            
        except Exception as e:
            print(f"❌ {self.symbol} gösterge hesaplama hatası: {e}")
    
    def _calculate_swing_points(self):
        """Swing yüksek ve düşük noktalarını hesapla"""
        try:
            # Basit swing point hesaplama (5 mumluk pencere)
            window = 5
            
            # Swing High'lar
            self.df['swing_high'] = self.df['High'].rolling(window=window, center=True).max()
            self.df['is_swing_high'] = (self.df['High'] == self.df['swing_high']) & (self.df['High'] > self.df['High'].shift(1)) & (self.df['High'] > self.df['High'].shift(-1))
            
            # Swing Low'lar
            self.df['swing_low'] = self.df['Low'].rolling(window=window, center=True).min()
            self.df['is_swing_low'] = (self.df['Low'] == self.df['swing_low']) & (self.df['Low'] < self.df['Low'].shift(1)) & (self.df['Low'] < self.df['Low'].shift(-1))
            
        except Exception as e:
            print(f"Swing point hesaplama hatası: {e}")
    
    def _calculate_fibonacci_levels(self):
        """Fibonacci retracement seviyelerini hesapla"""
        try:
            # Son swing high ve low'u bul
            swing_highs = self.df[self.df['is_swing_high'] == True]['High']
            swing_lows = self.df[self.df['is_swing_low'] == True]['Low']
            
            if len(swing_highs) >= 2 and len(swing_lows) >= 2:
                # Son iki swing point
                last_swing_high = swing_highs.iloc[-1]
                last_swing_low = swing_lows.iloc[-1]
                
                # Fibonacci seviyelerini hesapla
                range_size = last_swing_high - last_swing_low
                
                for level in self.FIB_LEVELS:
                    fib_price = last_swing_high - (range_size * level)
                    self.df[f'fib_{int(level*1000)}'] = fib_price
                    
        except Exception as e:
            print(f"Fibonacci hesaplama hatası: {e}")
    
    def is_uptrend(self) -> bool:
        """Ana trend yükseliş mi kontrol et"""
        if self.df is None or len(self.df) < 2:
            return False
        
        latest = self.df.iloc[-1]
        return (latest['Close'] > latest['SMA_200'] and 
                latest['SMA_50'] > latest['SMA_200'])
    
    def is_fibonacci_retracement_zone(self) -> bool:
        """Fiyat Fibonacci düzeltme bölgesinde mi"""
        if self.df is None or len(self.df) < 2:
            return False
        
        latest = self.df.iloc[-1]
        current_price = latest['Close']
        
        # Fibonacci seviyelerini kontrol et
        for level in [0.5, 0.618]:  # Ana seviyeler
            fib_col = f'fib_{int(level*1000)}'
            if fib_col in self.df.columns:
                fib_price = latest[fib_col]
                # %2 tolerans ile Fibonacci seviyesinde mi
                if abs(current_price - fib_price) / fib_price < 0.02:
                    return True
        
        return False
    
    def is_rsi_momentum_reversal(self) -> bool:
        """RSI momentum dönüş sinyali var mı"""
        if self.df is None or len(self.df) < 3:
            return False
        
        # Son 3 mum
        rsi_values = self.df['RSI'].tail(3).values
        
        # RSI 40'ın altından 50'nin üzerine çıkış
        return (rsi_values[0] < self.RSI_OVERSOLD and 
                rsi_values[1] < self.RSI_MOMENTUM and 
                rsi_values[2] > self.RSI_MOMENTUM)
    
    def is_elliott_wave_2_or_4(self) -> bool:
        """Elliott Dalga 2 veya 4 düzeltmesi mi (basitleştirilmiş)"""
        if self.df is None or len(self.df) < 20:
            return False
        
        # Basit Elliott dalga tespiti
        # Son 20 mumda düzeltme hareketi var mı?
        recent_high = self.df['High'].tail(20).max()
        recent_low = self.df['Low'].tail(20).min()
        current_price = self.df['Close'].iloc[-1]
        
        # Düzeltme: Yüksek seviyeden %5-15 düşüş
        retracement_pct = (recent_high - current_price) / recent_high
        
        return 0.05 <= retracement_pct <= 0.15
    
    def calculate_stop_loss_take_profit(self, entry_price: float, trade_type: str) -> Tuple[float, float]:
        """ATR tabanlı SL/TP hesapla"""
        if self.df is None or len(self.df) < 2:
            return 0, 0
        
        atr = self.df['ATR'].iloc[-1]
        
        if trade_type == 'LONG':
            stop_loss = entry_price - (atr * self.ATR_SL_MULTIPLIER)
            take_profit = entry_price + (atr * self.ATR_TP_MULTIPLIER)
        else:  # SHORT
            stop_loss = entry_price + (atr * self.ATR_SL_MULTIPLIER)
            take_profit = entry_price - (atr * self.ATR_TP_MULTIPLIER)
        
        return stop_loss, take_profit
    
    def generate_signal(self, current_position: str = 'NONE') -> Tuple[Optional[str], Optional[str], Dict]:
        """Elliott Dalga ve Fibonacci sinyali üret"""
        if self.df is None or self.df.empty or len(self.df) < 50:
            return None, None, {}
        
        latest = self.df.iloc[-1]
        
        indicators = {
            'rsi': round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else 0,
            'sma_50': round(latest['SMA_50'], 2) if not pd.isna(latest['SMA_50']) else 0,
            'sma_200': round(latest['SMA_200'], 2) if not pd.isna(latest['SMA_200']) else 0,
            'atr': round(latest['ATR'], 6) if not pd.isna(latest['ATR']) else 0,
            'close': round(latest['Close'], 6)
        }
        
        # AÇIK POZİSYON VARSA - ÇIKIŞ SİNYALLERİ
        if current_position == 'LONG':
            # RSI aşırı alım kontrolü
            if latest['RSI'] > self.RSI_OVERBOUGHT:
                return 'LONG_EXIT', "🌊 ELLIOTT DALGA 5 TAMAMLANDI - UZUN POZİSYON KAPAT", indicators
            
            # SMA 50 kırılımı
            if latest['Close'] < latest['SMA_50']:
                return 'LONG_EXIT', "📉 TREND KIRILIMI - UZUN POZİSYON KAPAT", indicators
            
            return None, None, indicators
        
        elif current_position == 'SHORT':
            # RSI aşırı satım kontrolü
            if latest['RSI'] < (100 - self.RSI_OVERBOUGHT):
                return 'SHORT_EXIT', "🌊 ELLIOTT DALGA 5 TAMAMLANDI - KISA POZİSYON KAPAT", indicators
            
            # SMA 50 kırılımı
            if latest['Close'] > latest['SMA_50']:
                return 'SHORT_EXIT', "📈 TREND KIRILIMI - KISA POZİSYON KAPAT", indicators
            
            return None, None, indicators
        
        # POZİSYON KAPALI - GİRİŞ SİNYALLERİ
        # Sadece yükseliş trendinde LONG giriş
        if not self.is_uptrend():
            return None, None, indicators
        
        # Elliott Dalga 2/4 düzeltmesi kontrolü
        if not self.is_elliott_wave_2_or_4():
            return None, None, indicators
        
        # Fibonacci düzeltme bölgesi kontrolü
        if not self.is_fibonacci_retracement_zone():
            return None, None, indicators
        
        # RSI momentum dönüş sinyali
        if self.is_rsi_momentum_reversal():
            return 'LONG_ENTRY', "🌊 ELLIOTT DALGA GİRİŞİ - FİBONACCİ DESTEK", indicators
        
        return None, None, indicators

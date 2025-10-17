"""
Intraday Trading Strategy (VWAP + ADX + RSI)
============================================

TradingView Original Strategy - Tam Uyumlu Versiyon

BUY RULES:
1. Prices should close above the VWAP
2. ADX should be below the 30 level
3. RSI should cross and close above the 55 level

SELL RULES:
1. Prices should close below the VWAP
2. ADX should be below the 30 level
3. RSI should cross and close below the 35 level

BUY EXIT RULES:
1. Prices should close below the VWAP or after 15:00 the buy position will automatically get squared off

SELL EXIT RULES:
1. Prices should close above the VWAP or after 15:00 the sell position will automatically get squared off

İşlem Saatleri (TradingView Original: 09:15-14:30):
- CRYPTO: 7/24 (Her zaman açık)
- BIST: 09:15-14:30 TR (Hafta içi)
- US: 09:15-14:30 ET (Hafta içi)

Square Off (TradingView Original: 14:45-15:00):
- CRYPTO: Yok (7/24 çalışır)
- BIST: 15:00 TR (Tüm pozisyonlar otomatik kapanır)
- US: 15:00 ET (Tüm pozisyonlar otomatik kapanır)

Timeframe: 15 dakika
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
        
        # Sinyal kalitesi parametreleri
        self.MIN_ADX_FOR_ENTRY = 25  # Sadece güçlü trendlerde pozisyon aç
        self.MIN_RSI_DISTANCE = 5    # RSI seviyelerinden minimum 5 puan uzaklık
        self.MIN_QUALITY_SCORE = 80  # Minimum 80/100 puan gerekli
        
        # İşlem saatleri (Market type'a göre)
        if market_type == 'CRYPTO':
            # Kripto: 7/24 çalışır
            self.TRADING_START_TIME = None
            self.TRADING_END_TIME = None
            self.SQUARE_OFF_TIME = None
            self.TIMEZONE = None
        elif market_type == 'BIST':
            # BIST: 09:15-14:30 TR (TradingView original), Square Off: 14:45-15:00 TR
            self.TRADING_START_TIME = "09:15"
            self.TRADING_END_TIME = "14:30"
            self.SQUARE_OFF_TIME = "15:00"
            self.TIMEZONE = 'Europe/Istanbul'
        else:  # US
            # US: 09:15-14:30 ET (same as BIST logic), Square Off: 15:00 ET
            self.TRADING_START_TIME = "09:15"
            self.TRADING_END_TIME = "14:30"
            self.SQUARE_OFF_TIME = "15:00"
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
    
    def calculate_signal_quality(self, signal_type: str, indicators: Dict) -> int:
        """Calculate signal quality score (0-100) based on multiple factors"""
        score = 0
        
        rsi = indicators.get('rsi', 0)
        adx = indicators.get('adx', 0)
        vwap = indicators.get('vwap', 0)
        close = indicators.get('close', 0)
        
        # 1. ADX Trend Strength (40 points max)
        if adx >= self.MIN_ADX_FOR_ENTRY:
            if adx >= 40:
                score += 40  # Very strong trend
            elif adx >= 30:
                score += 30  # Strong trend
            elif adx >= 25:
                score += 20  # Moderate trend
        else:
            return 0  # No trend, reject signal
        
        # 2. RSI Distance from Levels (30 points max)
        if signal_type == 'LONG_ENTRY':
            rsi_distance = rsi - self.RSI_BUY_LEVEL
            if rsi_distance >= self.MIN_RSI_DISTANCE:
                if rsi_distance >= 10:
                    score += 30  # Very clear breakout
                elif rsi_distance >= 5:
                    score += 20  # Clear breakout
        elif signal_type == 'SHORT_ENTRY':
            rsi_distance = self.RSI_SELL_LEVEL - rsi
            if rsi_distance >= self.MIN_RSI_DISTANCE:
                if rsi_distance >= 10:
                    score += 30  # Very clear breakdown
                elif rsi_distance >= 5:
                    score += 20  # Clear breakdown
        else:
            return 0  # Invalid signal type
        
        # 3. Price vs VWAP Position (20 points max)
        if signal_type == 'LONG_ENTRY' and close > vwap:
            vwap_distance = ((close - vwap) / vwap) * 100
            if vwap_distance >= 1.0:
                score += 20  # Strong above VWAP
            elif vwap_distance >= 0.5:
                score += 15  # Above VWAP
            else:
                score += 10  # Just above VWAP
        elif signal_type == 'SHORT_ENTRY' and close < vwap:
            vwap_distance = ((vwap - close) / vwap) * 100
            if vwap_distance >= 1.0:
                score += 20  # Strong below VWAP
            elif vwap_distance >= 0.5:
                score += 15  # Below VWAP
            else:
                score += 10  # Just below VWAP
        
        # 4. RSI Momentum (10 points max)
        if signal_type == 'LONG_ENTRY':
            if rsi >= 60:
                score += 10  # Strong bullish momentum
            elif rsi >= 55:
                score += 5   # Moderate bullish momentum
        elif signal_type == 'SHORT_ENTRY':
            if rsi <= 40:
                score += 10  # Strong bearish momentum
            elif rsi <= 35:
                score += 5   # Moderate bearish momentum
        
        return min(score, 100)  # Cap at 100
    
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
        
        # ZAMAN TABANLI ÇIKIŞ - Square Off (15:00 için)
        if self.is_square_off_time():
            if current_position == 'LONG':
                return 'LONG_EXIT', "🚪 15:00 SQUARE OFF - UZUN POZİSYON KAPAT", indicators
            elif current_position == 'SHORT':
                return 'SHORT_EXIT', "🚪 15:00 SQUARE OFF - KISA POZİSYON KAPAT", indicators
        
        # AÇIK POZİSYON VARSA - ÇIKIŞ SİNYALLERİ
        if current_position == 'LONG':
            # BUY EXIT: Fiyat VWAP altına düşerse (0.5% tolerans ile)
            if latest['Close'] < latest['VWAP'] * 0.995:
                return 'LONG_EXIT', "📉 VWAP ALTINA DÜŞTÜ - UZUN POZİSYON KAPAT", indicators
            return None, None, indicators
        
        elif current_position == 'SHORT':
            # SELL EXIT: Fiyat VWAP üzerine çıkarsa (0.5% tolerans ile)
            if latest['Close'] > latest['VWAP'] * 1.005:
                return 'SHORT_EXIT', "📈 VWAP ÜSTÜNE ÇIKTI - KISA POZİSYON KAPAT", indicators
            return None, None, indicators
        
        # POZİSYON KAPALI - GİRİŞ SİNYALLERİ
        # Sadece işlem saatlerinde giriş (09:15-14:30 TR)
        if not self.is_trading_time():
            return None, None, indicators
        
        # BUY RULES (TradingView original koduna göre - Esnek crossover)
        # 1. Fiyat VWAP üzerinde kapanmalı
        buy_vwap = latest['Close'] > latest['VWAP']
        
        # 2. ADX 30'un altında olmalı
        buy_adx = latest['ADX'] < self.ADX_LEVEL
        
        # 3. RSI 55'i yukarı kesip üzerinde kapanmalı (crossover)
        # Esnek: Son 3 mumdan birinde kesme varsa kabul et
        buy_rsi_cross = False
        if len(self.df) >= 3:
            for i in range(1, 4):  # Son 3 mumu kontrol et
                if i < len(self.df):
                    prev_rsi = self.df.iloc[-(i+1)]['RSI']
                    curr_rsi = self.df.iloc[-i]['RSI']
                    if prev_rsi <= self.RSI_BUY_LEVEL and curr_rsi > self.RSI_BUY_LEVEL:
                        buy_rsi_cross = True
                        break
        
        if buy_vwap and buy_adx and buy_rsi_cross:
            # Calculate signal quality score
            quality_score = self.calculate_signal_quality('LONG_ENTRY', indicators)
            if quality_score >= self.MIN_QUALITY_SCORE:
                return 'LONG_ENTRY', f"📈 ALIM SİNYALİ - RSI CROSS UP 55 (Kalite: {quality_score}/100)", indicators
            else:
                print(f"❌ {self.symbol} LONG_ENTRY sinyali kalite yetersiz: {quality_score}/100 < {self.MIN_QUALITY_SCORE}")
                return None, None, indicators
        
        # SELL RULES (TradingView original koduna göre - Esnek crossunder)
        # 1. Fiyat VWAP altında kapanmalı
        sell_vwap = latest['Close'] < latest['VWAP']
        
        # 2. ADX 30'un altında olmalı
        sell_adx = latest['ADX'] < self.ADX_LEVEL
        
        # 3. RSI 35'i aşağı kesip altında kapanmalı (crossunder)
        # Esnek: Son 3 mumdan birinde kesme varsa kabul et
        sell_rsi_cross = False
        if len(self.df) >= 3:
            for i in range(1, 4):  # Son 3 mumu kontrol et
                if i < len(self.df):
                    prev_rsi = self.df.iloc[-(i+1)]['RSI']
                    curr_rsi = self.df.iloc[-i]['RSI']
                    if prev_rsi >= self.RSI_SELL_LEVEL and curr_rsi < self.RSI_SELL_LEVEL:
                        sell_rsi_cross = True
                        break
        
        if sell_vwap and sell_adx and sell_rsi_cross:
            # Calculate signal quality score
            quality_score = self.calculate_signal_quality('SHORT_ENTRY', indicators)
            if quality_score >= self.MIN_QUALITY_SCORE:
                return 'SHORT_ENTRY', f"📉 SATIM SİNYALİ - RSI CROSS DOWN 35 (Kalite: {quality_score}/100)", indicators
            else:
                print(f"❌ {self.symbol} SHORT_ENTRY sinyali kalite yetersiz: {quality_score}/100 < {self.MIN_QUALITY_SCORE}")
                return None, None, indicators
        
        return None, None, indicators

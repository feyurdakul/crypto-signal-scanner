"""
Teknik Gösterge Hesaplamaları
pandas-ta yerine manuel hesaplamalar
"""

import pandas as pd
import numpy as np

def calculate_rsi(close: pd.Series, length: int = 14) -> pd.Series:
    """RSI (Relative Strength Index) hesapla"""
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_adx(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    """ADX (Average Directional Index) hesapla"""
    # True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=length).mean()
    
    # Directional Movement
    up = high - high.shift()
    down = low.shift() - low
    
    plus_dm = np.where((up > down) & (up > 0), up, 0)
    minus_dm = np.where((down > up) & (down > 0), down, 0)
    
    plus_dm = pd.Series(plus_dm, index=high.index).rolling(window=length).mean()
    minus_dm = pd.Series(minus_dm, index=high.index).rolling(window=length).mean()
    
    # Directional Indicators
    plus_di = 100 * (plus_dm / atr)
    minus_di = 100 * (minus_dm / atr)
    
    # ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=length).mean()
    
    return adx

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    """ATR (Average True Range) hesapla"""
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=length).mean()
    return atr

def calculate_sma(close: pd.Series, length: int) -> pd.Series:
    """SMA (Simple Moving Average) hesapla"""
    return close.rolling(window=length).mean()

def calculate_ema(close: pd.Series, length: int) -> pd.Series:
    """EMA (Exponential Moving Average) hesapla"""
    return close.ewm(span=length, adjust=False).mean()

def calculate_vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
    """VWAP (Volume Weighted Average Price) hesapla"""
    typical_price = (high + low + close) / 3
    tp_volume = typical_price * volume
    cumulative_tp_volume = tp_volume.cumsum()
    cumulative_volume = volume.cumsum()
    vwap = cumulative_tp_volume / cumulative_volume
    return vwap


"""
US Hisse Senedi Veri Çekici (Nasdaq & S&P500)
yfinance kullanarak US hisse verilerini çeker
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz

class USDataFetcher:
    """US hisse senedi verileri için data fetcher"""
    
    def __init__(self):
        # Nasdaq 100 ve S&P 500'den seçilmiş likit hisseler
        self.us_symbols = [
            # Tech Giants (Nasdaq)
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX',
            'AMD', 'INTC', 'CSCO', 'ADBE', 'CRM', 'ORCL', 'AVGO', 'QCOM',
            'TXN', 'INTU', 'AMAT', 'MU', 'ADI', 'LRCX', 'KLAC', 'SNPS',
            'CDNS', 'MRVL', 'FTNT', 'PANW', 'CRWD', 'ZS', 'DDOG', 'NET',
            
            # Consumer & Retail
            'COST', 'SBUX', 'PEP', 'KO', 'MCD', 'NKE', 'HD', 'LOW',
            'TGT', 'WMT', 'DIS', 'CMCSA', 'CHTR', 'T', 'VZ',
            
            # Finance (S&P 500)
            'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'SCHW',
            'AXP', 'USB', 'PNC', 'TFC', 'COF',
            
            # Healthcare & Pharma
            'JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'DHR', 'BMY',
            'AMGN', 'GILD', 'CVS', 'CI', 'HUM', 'ISRG', 'VRTX',
            
            # Industrial & Energy
            'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'BA', 'CAT', 'DE',
            'GE', 'HON', 'UPS', 'RTX', 'LMT', 'NOC', 'GD',
            
            # Other Major S&P 500
            'V', 'MA', 'PYPL', 'BKNG', 'UBER', 'ABNB', 'SQ', 'COIN'
        ]
        
        print(f"✓ {len(self.us_symbols)} US hisse senedi yüklendi")
    
    def get_all_us_symbols(self):
        """Tüm US sembollerini döndür"""
        return self.us_symbols
    
    def get_ohlcv(self, symbol, timeframe='15m', limit=100):
        """
        Belirtilen sembol için OHLCV verilerini çek
        
        Args:
            symbol: Hisse senedi sembolü (örn: 'AAPL')
            timeframe: Zaman dilimi ('1m', '5m', '15m', '1h', '1d')
            limit: Kaç bar veri çekilecek
        
        Returns:
            DataFrame veya None
        """
        try:
            # Timeframe çevirisi
            interval_map = {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '1d': '1d'
            }
            
            interval = interval_map.get(timeframe, '15m')
            
            # Period hesaplama
            if interval in ['1m', '5m']:
                period = '7d'  # Son 7 gün
            elif interval in ['15m', '30m']:
                period = '60d'  # Son 60 gün
            elif interval == '1h':
                period = '730d'  # Son 2 yıl
            else:
                period = 'max'
            
            # Veri çek
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                return None
            
            # Son 'limit' kadar bar al
            df = df.tail(limit)
            
            # Sütun isimlerini standartlaştır
            df = df.rename(columns={
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Close': 'Close',
                'Volume': 'Volume'
            })
            
            # Gerekli sütunları seç
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Index'i sıfırla
            df = df.reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"⚠️ {symbol} veri çekme hatası: {e}")
            return None
    
    def clean_symbol_for_display(self, symbol):
        """Sembol adını temizle (gösterim için)"""
        # US hisseleri için sembol aynen kalır
        return symbol


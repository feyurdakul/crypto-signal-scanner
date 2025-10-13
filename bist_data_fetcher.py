"""
BIST (Borsa Istanbul) Hisse Verisi Çekme
Yahoo Finance API kullanarak
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class BISTDataFetcher:
    """Yahoo Finance ile BIST hisse verisi çek"""
    
    def __init__(self):
        self.bist_symbols = self._get_bist_symbols()
    
    def _get_bist_symbols(self):
        """Popüler BIST hisseleri"""
        # BIST 30 endeksindeki önemli hisseler
        return [
            'AKBNK.IS',  # Akbank
            'THYAO.IS',  # Türk Hava Yolları
            'GARAN.IS',  # Garanti BBVA
            'ISCTR.IS',  # İş Bankası C
            'YKBNK.IS',  # Yapı Kredi
            'SISE.IS',   # Şişe Cam
            'SAHOL.IS',  # Sabancı Holding
            'KCHOL.IS',  # Koç Holding
            'TUPRS.IS',  # Tüpraş
            'EREGL.IS',  # Ereğli Demir Çelik
            'PETKM.IS',  # Petkim
            'BIMAS.IS',  # BIM
            'ASELS.IS',  # Aselsan
            'KOZAL.IS',  # Koza Altın
            'TAVHL.IS',  # TAV Havalimanları
            'TCELL.IS',  # Turkcell
            'TTKOM.IS',  # Türk Telekom
            'ENKAI.IS',  # Enka İnşaat
            'PGSUS.IS',  # Pegasus
            'SODA.IS',   # Soda Sanayi
            'TOASO.IS',  # Tofaş
            'VESTL.IS',  # Vestel
            'ARCLK.IS',  # Arçelik
            'FROTO.IS',  # Ford Otosan
            'HALKB.IS',  # Halkbank
            'VAKBN.IS',  # Vakıfbank
            'EKGYO.IS',  # Emlak Konut GYO
            'KOZAA.IS',  # Koza Anadolu Metal
            'MGROS.IS',  # Migros
            'DOHOL.IS',  # Doğan Holding
        ]
    
    def get_ohlcv(self, symbol, timeframe='15m', limit=100):
        """
        OHLCV verisi çek
        
        Args:
            symbol: Sembol (örn: AKBNK.IS)
            timeframe: Zaman dilimi (1m, 5m, 15m, 1h, 1d)
            limit: Kaç mum çekilecek
            
        Returns:
            pandas DataFrame veya None
        """
        try:
            # Yahoo Finance sembol formatı kontrol
            if not symbol.endswith('.IS'):
                symbol = f"{symbol}.IS"
            
            # Timeframe mapping
            interval_map = {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '1d': '1d'
            }
            
            yf_interval = interval_map.get(timeframe, '15m')
            
            # Period hesapla (limit'e göre)
            if yf_interval in ['1m', '5m']:
                period = '7d'  # Son 7 gün
            elif yf_interval in ['15m', '30m']:
                period = '60d'  # Son 60 gün
            elif yf_interval == '1h':
                period = '730d'  # Son 2 yıl
            else:
                period = 'max'
            
            # Veri çek
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=yf_interval)
            
            if df.empty:
                return None
            
            # Son N mumu al
            df = df.tail(limit)
            
            # Sütun isimlerini düzenle
            df = df.rename(columns={
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Close': 'Close',
                'Volume': 'Volume'
            })
            
            # Sadece gerekli sütunları al
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            return df
            
        except Exception as e:
            print(f"❌ {symbol} veri çekme hatası: {e}")
            return None
    
    def get_all_bist_symbols(self):
        """Tüm BIST sembollerini döndür"""
        return self.bist_symbols
    
    def clean_symbol_for_display(self, symbol):
        """Görüntüleme için sembol temizle (AKBNK.IS -> AKBNK)"""
        return symbol.replace('.IS', '')


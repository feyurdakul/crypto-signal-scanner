"""
CCXT ile Binance'den Veri Çekme
"""

import ccxt
import pandas as pd
from datetime import datetime

class DataFetcher:
    """CCXT ile kripto verisi çek"""
    
    def __init__(self):
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
    
    def get_ohlcv(self, symbol, timeframe='15m', limit=100):
        """
        OHLCV verisi çek
        
        Args:
            symbol: Sembol (örn: BTC/USDT)
            timeframe: Zaman dilimi (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Kaç mum çekilecek
            
        Returns:
            pandas DataFrame veya None
        """
        try:
            # Sembolü CCXT formatına çevir (BTCUSDT -> BTC/USDT)
            if '/' not in symbol:
                symbol = symbol.replace('USDT', '/USDT')
            
            # OHLCV verisi çek
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            if not ohlcv:
                return None
            
            # DataFrame'e çevir
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ {symbol} veri çekme hatası: {e}")
            return None
    
    def get_all_usdt_pairs(self):
        """Tüm USDT çiftlerini çek - Hardcoded liste (Binance API kısıtlaması nedeniyle)"""
        # Binance API erişimi engellendiği için hardcoded liste kullanıyoruz
        return [
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
            'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'LTCUSDT',
            'TRXUSDT', 'AVAXUSDT', 'LINKUSDT', 'ATOMUSDT', 'UNIUSDT',
            'ETCUSDT', 'XLMUSDT', 'FILUSDT', 'APTUSDT', 'NEARUSDT',
            'ARBUSDT', 'OPUSDT', 'ICPUSDT', 'STXUSDT', 'INJUSDT',
            'SUIUSDT', 'WIFUSDT', 'FETUSDT', 'IMXUSDT', 'TAOUSDT',
            'HBARUSDT', 'TIAUSDT', 'RENDERUSDT', 'SEIUSDT', 'ARUSDT',
            'BONKUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'SHIBUSDT', '1000PEPEUSDT'
        ]
    
    def clean_symbol_for_display(self, symbol):
        """Görüntüleme için sembol temizle (kripto için değişiklik yok)"""
        return symbol


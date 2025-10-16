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
        """Tüm USDT çiftlerini çek - Sadece Binance'te mevcut olanlar"""
        # Doğrulanmış ve Binance'te mevcut olan USDT pariteleri
        return [
            # Major Coins - Binance ana pariteleri
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
            'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'LTCUSDT',

            # DeFi Tokens - Popüler DeFi tokenları
            'UNIUSDT', 'LINKUSDT', 'AAVEUSDT', 'MKRUSDT', 'SNXUSDT',
            'COMPUSDT', 'SUSHIUSDT', 'CRVUSDT', 'YFIUSDT', 'CAKEUSDT',

            # Layer 1 & Infrastructure
            'ATOMUSDT', 'AVAXUSDT', 'NEARUSDT', 'ALGOUSDT', 'FTMUSDT',
            'FTTUSDT', 'EGLDUSDT', 'VETUSDT', 'ONEUSDT', 'ONTUSDT',

            # Gaming & Metaverse
            'AXSUSDT', 'SANDUSDT', 'MANAUSDT', 'GALAUSDT', 'ENJUSDT',
            'APEUSDT', 'IMXUSDT', 'FLOWUSDT', 'CHZUSDT', 'ALICEUSDT',

            # AI & Big Data
            'FETUSDT', 'AGIXUSDT', 'OCEANUSDT', 'NMRUSDT', 'COTIUSDT',
            'TAOUSDT', 'ARKMUSDT',

            # Privacy Coins
            'XMRUSDT', 'ZECUSDT', 'DASHUSDT', 'ZENUSDT', 'KSMUSDT',
            'SCUSDT', 'DCRUSDT', 'XVGUSDT', 'ZILUSDT', 'WAVESUSDT',

            # Storage & Computing
            'FILUSDT', 'ARUSDT', 'STORJUSDT', 'BTTUSDT', 'HOTUSDT',
            'GLMUSDT',

            # Oracle & Data
            'TRBUSDT', 'BANDUSDT', 'API3USDT', 'DIAUSDT', 'ACHUSDT',

            # Cross-chain & Bridges
            'INJUSDT', 'RUNEUSDT', 'ANKRUSDT', 'CELRUSDT',

            # Derivatives & Synthetics
            'PERPUSDT', 'DYDXUSDT', 'GMXUSDT', 'GNSUSDT',

            # Meme Coins & Community
            'SHIBUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'BONKUSDT',

            # Liquid Staking & LSD
            'LDOUSDT', 'FXSUSDT',

            # Additional Major Pairs
            'TRXUSDT', 'ETCUSDT', 'XLMUSDT', 'HBARUSDT', 'TIAUSDT',
            'SEIUSDT', 'SUIUSDT', 'WIFUSDT', 'RENDERUSDT', 'OPUSDT',
            'STXUSDT', 'ICPUSDT', 'ARBUSDT', 'APTUSDT',

            # More DeFi
            'CVXUSDT', 'BADGERUSDT', 'SPELLUSDT',

            # Additional Infrastructure
            'GRTUSDT', 'LRCUSDT', 'BATUSDT', 'ZRXUSDT', 'RENUSDT',
            'SKLUSDT', 'CHRUSDT', 'NKNUSDT',

            # More Gaming
            'DARUSDT', 'GHSTUSDT', 'TLMUSDT', 'BURGERUSDT', 'BAKEUSDT'
        ]
    
    def clean_symbol_for_display(self, symbol):
        """Görüntüleme için sembol temizle (kripto için değişiklik yok)"""
        return symbol


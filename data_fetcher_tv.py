# -*- coding: utf-8 -*-
"""
TVDatafeed ile Tüm Kripto Verisi Çekme
Binance yerine TradingView datafeed kullan
"""

import pandas as pd
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
import time

class TVDataFetcher:
    """TVDatafeed ile kripto verisi çeker"""

    def __init__(self):
        try:
            self.tv = TvDatafeed()
            print("✅ TVDatafeed bağlantısı başarılı")
        except Exception as e:
            print(f"❌ TVDatafeed bağlantı hatası: {e}")
            self.tv = None

    def get_ohlcv(self, symbol, timeframe='15m', limit=100):
        """
        OHLCV verisi çek - TradingView formatında

        Args:
            symbol: Sembol (örn: BINANCE:BTCUSDT)
            timeframe: Zaman dilimi (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Kaç mum çekilecek

        Returns:
            pandas DataFrame veya None
        """
        if self.tv is None:
            print("❌ TVDatafeed bağlantısı yok")
            return None

        try:
            # Zaman dilimini TradingView formatına çevir
            interval_map = {
                '1m': Interval.in_1_minute,
                '5m': Interval.in_5_minute,
                '15m': Interval.in_15_minute,
                '1h': Interval.in_1_hour,
                '4h': Interval.in_4_hour,
                '1d': Interval.in_1_day
            }

            interval = interval_map.get(timeframe, Interval.in_15_minute)

            # TradingView sembol formatı kullan
            tv_symbol = f"BINANCE:{symbol}"

            print(f"📊 {symbol} verisi çekiliyor (TVDatafeed)...")

            # TVDatafeed ile veri çek
            data = self.tv.get_hist(
                symbol=tv_symbol,
                exchange="BINANCE",
                interval=interval,
                n_bars=limit
            )

            if data is None or data.empty:
                print(f"❌ {symbol} verisi alınamadı")
                return None

            # Sütun isimlerini standartlaştır
            data.columns = ['symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
            data['timestamp'] = data.index
            data['symbol'] = symbol.replace('USDT', '')

            print(f"✅ {symbol} verisi çekildi: {len(data)} bar")
            return data

        except Exception as e:
            print(f"❌ {symbol} veri çekme hatası: {e}")
            return None

    def get_all_usdt_pairs(self):
        """Tüm USDT çiftlerini döndür - Genişletilmiş liste"""
        return [
            # Major Coins
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
            'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'LTCUSDT',

            # DeFi Tokens
            'UNIUSDT', 'LINKUSDT', 'AAVEUSDT', 'MKRUSDT', 'SNXUSDT',
            'COMPUSDT', 'SUSHIUSDT', 'CRVUSDT', 'YFIUSDT', 'CAKEUSDT',

            # Layer 1 & Infrastructure
            'ATOMUSDT', 'AVAXUSDT', 'NEARUSDT', 'ALGOUSDT', 'FTTUSDT',
            'LUNAUSDT', 'FTMUSDT', 'EGLDUSDT', 'XECUSDT', 'VETUSDT',

            # Gaming & Metaverse
            'AXSUSDT', 'SANDUSDT', 'MANAUSDT', 'GALAUSDT', 'ENJUSDT',
            'APEUSDT', 'IMXUSDT', 'FLOWUSDT', 'WAXPUSDT', 'CHZUSDT',

            # AI & Big Data
            'FETUSDT', 'AGIXUSDT', 'OCEANUSDT', 'NMRUSDT', 'COTIUSDT',
            'PAALUSDT', 'FETUSDT', 'TAOUSDT', 'ARKMUSDT', 'RSS3USDT',

            # Privacy Coins
            'XMRUSDT', 'ZECUSDT', 'DASHUSDT', 'ZENUSDT', 'KSMUSDT',
            'SCUSDT', 'DCRUSDT', 'XVGUSDT', 'ZILUSDT', 'WAVESUSDT',

            # Storage & Computing
            'FILUSDT', 'ARUSDT', 'STORJUSDT', 'BTTUSDT', 'HOTUSDT',
            'MTLUSDT', 'DENTUSDT', 'KEYUSDT', 'SCUSDT', 'GLMUSDT',

            # Oracle & Data
            'TRBUSDT', 'BANDUSDT', 'ORBUSDT', 'CQTUSDT', 'API3USDT',
            'DIAUSDT', 'ACHUSDT', 'PONDUSDT', 'RAMPUSDT', 'WOZXUSDT',

            # Cross-chain & Bridges
            'INJUSDT', 'RUNEUSDT', 'THORUSDT', 'CELUSDT', 'ONEUSDT',
            'ONTUSDT', 'ICXUSDT', 'IOSTUSDT', 'ANKRUSDT', 'CELRUSDT',

            # Derivatives & Synthetics
            'PERPUSDT', 'DYDXUSDT', 'GMXUSDT', 'GNSUSDT', 'VELAUSDT',
            'MUXUSDT', 'LVLUSDT', 'MORPHOUSDT', 'SYNUSDT', 'UMEEUSDT',

            # Meme Coins & Community
            'SHIBUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'BONKUSDT', 'WOJAKUSDT',
            'MIGGLESUSDT', 'SPONGEUSDT', 'LADYSUSDT', 'BABYDOGEUSDT', 'QUACKUSDT',

            # Liquid Staking & LSD
            'LDOUSDT', 'FXSUSDT', 'RPLUSDT', 'SFRXETHUSDT', 'ANKRUSDT',
            'SDUSDT', 'MSTETHUSDT', 'CBETHUSDT', 'RETHUSDT', 'SWETHUSDT',

            # RWA & Real World Assets
            'ONDOUSDT', 'OMUSDT', 'CFGUSDT', 'CENTUSDT', 'DPIUSDT',
            'GOLDUSDT', 'SILVERUSDT', 'OILUSDT', 'GASUSDT', 'COPPERUSDT',

            # Additional Major Pairs
            'TRXUSDT', 'ETCUSDT', 'XLMUSDT', 'HBARUSDT', 'TIAUSDT',
            'SEIUSDT', 'SUIUSDT', 'WIFUSDT', 'RENDERUSDT', 'OPUSDT',
            'STXUSDT', 'ICPUSDT', 'ARBUSDT', 'APTUSDT', 'INJUSDT',

            # More DeFi
            'CVXUSDT', 'FXSUSDT', 'BADGERUSDT', 'CONVEXUSDT', 'RIBBONUSDT',
            'DPXUSDT', 'JPEGUSDT', 'LOOKSUSDT', 'SPELLUSDT', 'ALCXUSDT',

            # Additional Infrastructure
            'GRTUSDT', 'LRCUSDT', 'BATUSDT', 'ZRXUSDT', 'RENUSDT',
            'SKLUSDT', 'CHRUSDT', 'PERLUSDT', 'DOCKUSDT', 'NKNUSDT',

            # More Gaming
            'ALICEUSDT', 'DARUSDT', 'GHSTUSDT', 'REVVUSDT', 'TLMUSDT',
            'BURGERUSDT', 'BAKEUSDT', 'NABOXUSDT', 'DODOUSDT', 'SWINGBYUSDT',

            # Additional AI tokens
            'CTSIUSDT', 'AGLDUSDT', 'HIGHUSDT', 'GFALUSDT', 'CUDOSUSDT',
            'OLASUSDT', 'AIUSDT', 'NMTUSDT', 'LAIKAUSDT', 'ARCUSDT'
        ]

    def clean_symbol_for_display(self, symbol):
        """Görüntüleme için sembol temizle"""
        return symbol.replace('USDT', '')

# Test fonksiyonu
def test_tvdatafeed():
    """TVDatafeed bağlantısını test et"""
    try:
        fetcher = TVDataFetcher()

        if fetcher.tv is None:
            print("❌ TVDatafeed test başarısız")
            return False

        # Test verisi çek
        test_data = fetcher.get_ohlcv('BTCUSDT', limit=10)

        if test_data is not None:
            print(f"✅ TVDatafeed test başarılı: {len(test_data)} kayıt")
            print(f"   Son BTC fiyatı: ${test_data['Close'].iloc[-1]:.2f}")
            return True
        else:
            print("❌ TVDatafeed test başarısız - veri alınamadı")
            return False

    except Exception as e:
        print(f"❌ TVDatafeed test hatası: {e}")
        return False

if __name__ == "__main__":
    test_tvdatafeed()
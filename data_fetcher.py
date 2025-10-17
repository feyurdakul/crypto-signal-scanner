#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CCXT ile Kripto Verisi Çekme
Binance API ile hızlı veri çekme
"""

import pandas as pd
from datetime import datetime
import ccxt
import time

class TVDataFetcher:
    """CCXT ile kripto verisi çeker"""

    def __init__(self):
        try:
            self.exchange = ccxt.binance({
                'apiKey': '',
                'secret': '',
                'sandbox': False,
                'enableRateLimit': True,
            })
            print("✅ CCXT Binance bağlantısı başarılı")
        except Exception as e:
            print(f"❌ CCXT bağlantı hatası: {e}")
            self.exchange = None

    def get_ohlcv(self, symbol, timeframe='15m', limit=100):
        """
        OHLCV verisi çek - CCXT formatında
        
        Args:
            symbol: Binance sembolü (örn: BTC/USDT)
            timeframe: Zaman dilimi (15m, 1h, 4h, 1d)
            limit: Veri sayısı
            
        Returns:
            DataFrame: OHLCV verisi
        """
        try:
            if not self.exchange:
                return None
            
            # Binance sembol formatı
            if not '/' in symbol:
                symbol = symbol.replace('USDT', '/USDT')
            
            # Zaman dilimi mapping
            timeframe_map = {
                '15m': '15m',
                '1h': '1h', 
                '4h': '4h',
                '1d': '1d'
            }
            
            tf = timeframe_map.get(timeframe, '15m')
            
            # Veri çek
            ohlcv = self.exchange.fetch_ohlcv(symbol, tf, limit=limit)
            
            if ohlcv:
                # DataFrame formatına çevir
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
                df = df.set_index('datetime')
                df = df.drop('timestamp', axis=1)
                
                return df
            else:
                print(f"❌ Veri bulunamadı: {symbol}")
                return None
                
        except Exception as e:
            print(f"❌ {symbol} veri çekme hatası: {e}")
            return None

    def get_all_usdt_pairs(self):
        """Tüm USDT çiftlerini döndür - pairs.md dosyasından"""
        try:
            with open('pairs.md', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            usdt_pairs = []
            for line in lines:
                line = line.strip()
                if line and '/USDT' in line:
                    pair = line.replace('/', '')
                    if pair.endswith('USDT'):
                        usdt_pairs.append(pair)
            
            # Remove duplicates while preserving order
            usdt_pairs = list(dict.fromkeys(usdt_pairs))
            
            print(f"📋 pairs.md'den {len(usdt_pairs)} USDT çifti yüklendi")
            return usdt_pairs
            
        except Exception as e:
            print(f"❌ pairs.md okuma hatası: {e}")
            # Fallback: Temel pariteler
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

    def test_connection(self):
        """Bağlantı testi"""
        try:
            if self.exchange:
                markets = self.exchange.load_markets()
                print(f"✅ Bağlantı başarılı: {len(markets)} market yüklendi")
                return True
            else:
                print("❌ Exchange bağlantısı yok")
                return False
        except Exception as e:
            print(f"❌ Bağlantı testi hatası: {e}")
            return False

if __name__ == "__main__":
    # Test
    fetcher = TVDataFetcher()
    fetcher.test_connection()
    
    # Test veri çekme
    data = fetcher.get_ohlcv('BTCUSDT', '15m', 10)
    if data is not None:
        print(f"✅ Test başarılı: {len(data)} veri çekildi")
        print(data.head())
    else:
        print("❌ Test başarısız")
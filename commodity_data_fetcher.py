# -*- coding: utf-8 -*-
"""
Emtia Verisi Çekme - TVDatafeed ile
Binance'te bulunmayan emtia verileri için
"""

import pandas as pd
from datetime import datetime, timedelta
from tvDatafeed import TvDatafeed, Interval

class CommodityDataFetcher:
    """Emtia verilerini TVDatafeed ile çeker"""

    def __init__(self):
        self.tv = TvDatafeed()
        self.commodities = {
            'GOLD': 'TVC:GOLD',      # Altın
            'SILVER': 'TVC:SILVER',  # Gümüş
            'OIL': 'TVC:USOIL',      # Petrol
            'COPPER': 'TVC:HG1!',    # Bakır
        }

    def get_commodity_data(self, commodity, exchange='TVC', interval=Interval.in_15_minute, n_bars=100):
        """
        Emtia verisi çek

        Args:
            commodity: Emtia sembolü (GOLD, SILVER, OIL, COPPER)
            exchange: Exchange (default: TVC)
            interval: Zaman aralığı
            n_bars: Kaç bar çekilecek

        Returns:
            pandas DataFrame veya None
        """
        try:
            symbol = self.commodities.get(commodity.upper())
            if not symbol:
                print(f"❌ Bilinmeyen emtia: {commodity}")
                return None

            print(f"📊 {commodity} verisi çekiliyor...")

            # TVDatafeed ile veri çek
            data = self.tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                n_bars=n_bars
            )

            if data is None or data.empty:
                print(f"❌ {commodity} verisi alınamadı")
                return None

            # Sütun isimlerini standartlaştır
            data.columns = ['symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
            data['timestamp'] = data.index
            data['symbol'] = commodity

            print(f"✅ {commodity} verisi çekildi: {len(data)} bar")
            return data

        except Exception as e:
            print(f"❌ {commodity} veri çekme hatası: {e}")
            return None

    def get_all_commodities_data(self, interval=Interval.in_15_minute, n_bars=100):
        """
        Tüm emtia verilerini çek

        Returns:
            Dictionary of DataFrames
        """
        all_data = {}

        for commodity in self.commodities.keys():
            data = self.get_commodity_data(commodity, interval=interval, n_bars=n_bars)
            if data is not None:
                all_data[commodity] = data

        return all_data

# Test fonksiyonu
def test_commodity_fetcher():
    """Commodity fetcher'ı test et"""
    fetcher = CommodityDataFetcher()

    print("🧪 Emtia veri çekme testi başlıyor...")

    # Tek emtia testi
    gold_data = fetcher.get_commodity_data('GOLD')
    if gold_data is not None:
        print(f"✅ Altın verisi başarıyla çekildi: {len(gold_data)} kayıt")
        print(f"   Son fiyat: ${gold_data['Close'].iloc[-1]:.2f}")
    else:
        print("❌ Altın verisi çekilemedi")

    # Tüm emtia testi
    all_data = fetcher.get_all_commodities_data()
    print(f"\n📊 Toplam {len(all_data)} emtia verisi çekildi")

    return len(all_data) > 0

if __name__ == "__main__":
    test_commodity_fetcher()
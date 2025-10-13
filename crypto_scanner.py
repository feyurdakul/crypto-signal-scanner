# pip install pandas numpy pandas-ta ccxt  --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git

import pandas as pd
import numpy as np
import pandas_ta as ta
from tvDatafeed import TvDatafeed, Interval
import time
from datetime import datetime, time as dt_time
import pytz 

# ----------------------------------------------------------------------
# 1. PARAMETRELER VE ZAMAN AYARLARI
# ----------------------------------------------------------------------

# TradingView Giriş Bilgileri (Giriş yapmadan da çalışır, ancak kısıtlamalar olabilir)
TV_USERNAME = None  # İsteğe bağlı
TV_PASSWORD = None  # İsteğe bağlı

# TV VERİ KAYNAĞI
TV_EXCHANGE = 'BINANCE' # TradingView'deki ilgili borsa adı (Örn: BINANCE, COINBASE, vb.)

# Mum çubuğu aralığı (TVDatafeed formatında)
TIMEFRAME = Interval.in_15_minute # Düzeltilmiş isim kullanıldı

# İşlem Saatleri - KRİPTO 7/24 AÇIK (Zaman kısıtı yok)
# Not: Kripto piyasaları 24 saat açık olduğu için zaman kontrolü devre dışı
TRADING_24_7 = True  # 7/24 işlem aktif 

# Strateji Parametreleri
ADX_LENGTH = 20
ADX_LEVEL = 30
RSI_LENGTH = 14
RSI_BUY_LEVEL = 55
RSI_SELL_LEVEL = 35

# ----------------------------------------------------------------------
# 2. SEMBOL ÇEKME FONKSİYONU (SADECE TVDatafeed Kullanır)
# ----------------------------------------------------------------------

def get_crypto_symbols_from_tv(tv_client, exchange_name):
    """
    tvDatafeed kullanarak TÜM USDT çiftlerini arar ve bir liste oluşturur.
    Geniş manuel liste + TVDatafeed aramalarını birleştirir.
    """
    
    # GENİŞ MANUEL LİSTE - Binance'deki popüler tüm USDT çiftleri
    MANUAL_SYMBOLS = [
        # Top 20 Market Cap
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
        'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT', 'LINKUSDT',
        'MATICUSDT', 'LTCUSDT', 'TRXUSDT', 'ATOMUSDT', 'UNIUSDT',
        'ETCUSDT', 'XLMUSDT', 'BCHUSDT', 'NEARUSDT', 'APTUSDT',
        
        # DeFi & Layer 1
        'ARBUSDT', 'OPUSDT', 'SUIUSDT', 'INJUSDT', 'FILUSDT',
        'VETUSDT', 'ALGOUSDT', 'ICPUSDT', 'HBARUSDT', 'QNTUSDT',
        'AAVEUSDT', 'MKRUSDT', 'COMPUSDT', 'CRVUSDT', 'SUSHIUSDT',
        
        # AI & Gaming
        'RENDERUSDT', 'IQUSDT', 'AGIXUSDT', 'FETUSDT', 'OCEUSDT',
        'SANDUSDT', 'MANAUSDT', 'AXSUSDT', 'GALAUSDT', 'ENJUSDT',
        'IMXUSDT', 'RONINUSDT', 'BLURUSDT', 'ILUVUSDT',
        
        # Meme Coins
        'SHIBUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'BONKUSDT', 'WIFUSDT',
        
        # Layer 2 & Scaling
        'STXUSDT', 'LDOUSDT', 'RUNEUSDT', 'CFXUSDT',
        
        # Infrastructure
        'THETAUSDT', 'FTMUSDT', 'EGLDUSDT', 'FLOWUSDT', 'ZILUSDT',
        'CHZUSDT', 'APEUSDT', 'LDOUSDT', 'GMXUSDT', 'RNDRUSDT',
        
        # Exchange Tokens
        'CAKEUSDT', '1INCHUSDT', 'DYDXUSDT',
        
        # Stablecoins pairs (bazıları)
        'WBTCUSDT', 'STETHUSDT',
        
        # Diğer popüler altcoinler
        'GRTUSDT', 'MINAUSDT', 'KAVAUSDT', 'KSMUSDT', 'WAVESUSDT',
        'COTIUSDT', 'DASHUSDT', 'IOTAUSDT', 'NEOUSDT', 'ONEUSDT',
        'ZECUSDT', 'XTZUSDT', 'OMGUSDT', 'IOSTUSDT', 'CELOUSDT',
        'ZENUSDT', 'JASMYUSDT', 'RVNUSDT', 'SKLUSDT', 'MASKUSDT'
    ]
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] TÜM USDT çiftleri aranıyor...")
    
    scanned_symbols = set(MANUAL_SYMBOLS)
    
    # Birden fazla arama terimi ile TVDatafeed'den sembol çek
    search_terms = ['USDT', 'BTC', 'ETH', 'BNB', 'USD']
    
    for search_term in search_terms:
        try:
            tv_results = tv_client.search_symbol(search_term, exchange=exchange_name)
            
            if tv_results is not None:
                for item in tv_results:
                    # Sadece USDT ile bitenleri al
                    if (item.get('exchange') == exchange_name and 
                        item.get('symbol', '').endswith('USDT')):
                        scanned_symbols.add(item['symbol'])
        except Exception as e:
            # Hata olursa devam et
            pass
    
    # Sınırsız liste - Tüm bulunan sembolleri döndür
    final_list = sorted(list(scanned_symbols))
    
    if len(final_list) > 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {exchange_name} için {len(final_list)} adet USDT çifti bulundu!")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] UYARI: Sembol bulunamadı!")

    return final_list


# ----------------------------------------------------------------------
# 3. STRATEJİ SINIFI (Önceki kodla aynı sinyal mantığı)
# ----------------------------------------------------------------------
# TVDatafeed'den gelen veriyi işler.
class IntradayVWAPRSIStrategy:
    """VWAP, ADX ve RSI kullanan 7/24 kripto alım-satım stratejisi. SADECE sinyal üretir."""

    def __init__(self, tv_client, symbol, tv_exchange, timeframe):
        self.tv_client = tv_client
        self.symbol = symbol # Artık BTCUSDT formatında geliyor
        self.tv_exchange = tv_exchange
        self.timeframe = timeframe
        self.df = None
        self.current_position = 'NONE'

    def fetch_data(self, n_bars=100):
        """TVDatafeed'den verileri çeker."""
        try:
            df = self.tv_client.get_hist(
                symbol=self.symbol,
                exchange=self.tv_exchange,
                interval=self.timeframe,
                n_bars=n_bars
            )
            if df is not None and not df.empty and 'open' in df.columns:
                df.columns = [col.lower() for col in df.columns] 
                self.df = df
            else:
                 self.df = None
        except Exception as e:
            # Sıklıkla oluşan TVDatafeed hatalarını sessize alabiliriz:
            # print(f"Hata! {self.symbol} verileri çekilemedi: {e}")
            self.df = None

    def calculate_indicators(self):
        """Teknik göstergeleri hesaplar."""
        if self.df is None or len(self.df) < max(ADX_LENGTH, RSI_LENGTH) + 2:
            return

        # VWAP Manuel Hesaplama (Typical Price × Volume)
        self.df['typical_price'] = (self.df['high'] + self.df['low'] + self.df['close']) / 3
        self.df['tp_volume'] = self.df['typical_price'] * self.df['volume']
        self.df['cumulative_tp_volume'] = self.df['tp_volume'].cumsum()
        self.df['cumulative_volume'] = self.df['volume'].cumsum()
        self.df['VWAP'] = self.df['cumulative_tp_volume'] / self.df['cumulative_volume']
        
        # RSI ve ADX hesaplama
        self.df.ta.rsi(length=RSI_LENGTH, append=True) 
        self.df.ta.adx(length=ADX_LENGTH, append=True) 

        self.df['RSI'] = self.df[f'RSI_{RSI_LENGTH}']
        self.df['ADX'] = self.df[f'ADX_{ADX_LENGTH}']
        self.df['Close'] = self.df['close']
        
        self.df['RSI_Prev'] = self.df['RSI'].shift(1)
        
        self.df.dropna(inplace=True) 

    # Zaman kontrol fonksiyonları - Kripto 7/24 açık
    def check_trading_time(self, timestamp):
        # Kripto piyasası 24 saat açık, her zaman işlem yapılabilir
        return True

    def check_square_off_time(self, timestamp):
        # Kripto'da otomatik kapanış saati yok (7/24 işlem)
        return False

    # generate_signal metodu... (değişiklik yok)
    def generate_signal(self):
        if self.df is None or self.df.empty or len(self.df) < 2:
            return None, "VERI YETERSIZ"
        
        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2]
        
        current_timestamp = latest.name.to_pydatetime().replace(tzinfo=pytz.utc)
        is_trading_session = self.check_trading_time(current_timestamp)
        is_square_off_time = self.check_square_off_time(current_timestamp)
        
        # 1. ÇIKIŞ MANTIĞI
        buy_exit_vwap = latest['Close'] < latest['VWAP']
        sell_exit_vwap = latest['Close'] > latest['VWAP']

        if self.current_position == 'LONG' and (buy_exit_vwap or is_square_off_time):
            self.current_position = 'NONE'
            return 'LONG_EXIT', f"UZUN POZİSYON KAPAT - {'VWAP Kırılımı' if buy_exit_vwap else 'Zaman (Square Off)'}"

        if self.current_position == 'SHORT' and (sell_exit_vwap or is_square_off_time):
            self.current_position = 'NONE'
            return 'SHORT_EXIT', f"KISA POZİSYON KAPAT - {'VWAP Kırılımı' if sell_exit_vwap else 'Zaman (Square Off)'}"

        # 2. GİRİŞ MANTIĞI
        if self.current_position != 'NONE':
            return None, "POZISYON ACIK"
        
        if not is_trading_session:
             return None, "ISLEM SAATI DISI"

        # ALIM
        buy_vwap = latest['Close'] > latest['VWAP']
        buy_adx = latest['ADX'] < ADX_LEVEL
        buy_rsi_cross = prev['RSI'] <= RSI_BUY_LEVEL and latest['RSI'] > RSI_BUY_LEVEL

        if buy_vwap and buy_adx and buy_rsi_cross:
            self.current_position = 'LONG'
            return 'LONG_ENTRY', "ALIM SINYALI (VWAP+, ADX<30, RSI>55)"

        # SATIM
        sell_vwap = latest['Close'] < latest['VWAP']
        sell_adx = latest['ADX'] < ADX_LEVEL
        sell_rsi_cross = prev['RSI'] >= RSI_SELL_LEVEL and latest['RSI'] < RSI_SELL_LEVEL
        
        if sell_vwap and sell_adx and sell_rsi_cross:
            self.current_position = 'SHORT'
            return 'SHORT_ENTRY', "SATIM SINYALI (VWAP-, ADX<30, RSI<35)"

        return None, "SINYAL YOK"


# ----------------------------------------------------------------------
# 4. ANA TARAMA DÖNGÜSÜ
# ----------------------------------------------------------------------

def run_scanner(interval_seconds=60):
    """TVDatafeed'i kullanarak sembolleri otomatik çeken ve tarayan ana döngü."""
    
    # 1. TVDatafeed istemcisini başlat
    try:
        tv = TvDatafeed(TV_USERNAME, TV_PASSWORD)
    except Exception as e:
        print(f"Hata: TVDatafeed bağlantı hatası: {e}. Lütfen login bilgilerinizi kontrol edin.")
        return
        
    # 2. Taranacak Sembolleri Otomatik Çek (TVDatafeed ile)
    symbols_to_scan = get_crypto_symbols_from_tv(tv, TV_EXCHANGE)
    if not symbols_to_scan:
        print("Hata: Taranacak sembol bulunamadı. Lütfen manuel listeyi kontrol edin.")
        return
        
    # 3. Her çift için strateji objesi oluştur
    strategies = {symbol: IntradayVWAPRSIStrategy(tv, symbol, TV_EXCHANGE, TIMEFRAME) 
                  for symbol in symbols_to_scan}
    
    print("=" * 70)
    print(f"### OTOMATİK KRİPTO SİNYAL TARAYICISI (7/24 Aktif) ###")
    print(f"Borsa: {TV_EXCHANGE} | Çift Sayısı: {len(symbols_to_scan)} | Aralık: {TIMEFRAME.name.replace('in_', '')}")
    print("=" * 70)
    
    while True:
        current_time = datetime.now(pytz.utc)
        print(f"\n[{current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] Tarama Başladı...")
        
        for symbol, strategy in strategies.items():
            
            strategy.fetch_data(n_bars=100)
            if strategy.df is not None and not strategy.df.empty:
                strategy.calculate_indicators()
                signal, message = strategy.generate_signal()
                
                # Konsola çıktı
                position_status = strategy.current_position
                if signal:
                    print(f"!!! {symbol}: {signal} -> {message} (Yeni Pozisyon: {position_status}) !!!")
                else:
                    print(f"   {symbol}: {message} (Aktif Pozisyon: {position_status})")
            else:
                 print(f"   {symbol}: VERI ÇEKILEMEDI veya YETERSİZ.")

        # Bir sonraki kontrole kadar bekle
        time.sleep(interval_seconds)

# Tarayıcıyı Başlat
run_scanner(interval_seconds=60)


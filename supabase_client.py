# -*- coding: utf-8 -*-
"""
Supabase Database Client
Kripto sinyalleri ve işlemler için kalıcı veri depolama
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz
from supabase import create_client, Client
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class SupabaseManager:
    """Supabase veri yönetimi"""
    
    def __init__(self):
        # Supabase bağlantı bilgileri
        self.url = "https://rkjndkslanwyoyefsicd.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJram5ka3NsYW53eW95ZWZzaWNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzOTY2MDcsImV4cCI6MjA3NDk3MjYwN30.XZd3mmNDhKHj2zIBovsFasj1S7LEhkHNvO79_OGJHxo"
        
        # Supabase client oluştur
        self.supabase: Client = create_client(self.url, self.key)
        
    def add_signal(self, symbol: str, signal_type: str, message: str, 
                   price: float, indicators: Dict, system: str = None) -> bool:
        """Yeni sinyal ekle - Sistem bazlı"""
        try:
            data = {
                'symbol': symbol,
                'signal_type': signal_type,
                'message': message,
                'price': price,
                'rsi': indicators.get('rsi'),
                'adx': indicators.get('adx'),
                'vwap': indicators.get('vwap'),
                'atr': indicators.get('atr'),
                'system': system,
                'timestamp': datetime.now(pytz.utc).isoformat()
            }
            
            result = self.supabase.table('crypto_signals').insert(data).execute()
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Supabase sinyal ekleme hatası: {e}")
            return False
    
    def open_trade(self, symbol: str, trade_type: str, entry_price: float, 
                   atr_value: float = 0, stop_loss: float = 0, take_profit: float = 0, system: str = None) -> bool:
        """Yeni işlem aç - ATR tabanlı SL/TP ile - Sistem bazlı"""
        try:
            data = {
                'symbol': symbol,
                'trade_type': trade_type,
                'entry_price': entry_price,
                'entry_time': datetime.now(pytz.utc).isoformat(),
                'status': 'OPEN',
                'atr_value': atr_value,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'system': system
            }
            
            result = self.supabase.table('open_trades').upsert(data).execute()
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Supabase işlem açma hatası: {e}")
            return False
    
    def close_trade(self, symbol: str, exit_price: float) -> Optional[Dict]:
        """İşlem kapat ve kar/zarar hesapla"""
        try:
            # Açık işlemi getir
            open_trade_result = self.supabase.table('open_trades').select('*').eq('symbol', symbol).execute()
            
            if not open_trade_result.data:
                print(f"Açık işlem bulunamadı: {symbol}")
                return None
            
            open_trade = open_trade_result.data[0]
            entry_price = float(open_trade['entry_price'])
            trade_type = open_trade['trade_type']
            
            # Kar/Zarar hesaplama
            if trade_type == 'LONG':
                pnl_percent = ((exit_price - entry_price) / entry_price) * 100
            else:  # SHORT
                pnl_percent = ((entry_price - exit_price) / entry_price) * 100
            
            # Kapalı işlemler tablosuna ekle
            closed_trade_data = {
                'symbol': symbol,
                'trade_type': trade_type,
                'entry_price': entry_price,
                'entry_time': open_trade['entry_time'],
                'exit_price': exit_price,
                'exit_time': datetime.now(pytz.utc).isoformat(),
                'pnl_percent': round(pnl_percent, 2),
                'status': 'CLOSED'
            }
            
            closed_result = self.supabase.table('closed_trades').insert(closed_trade_data).execute()
            
            # Açık işlemlerden sil
            delete_result = self.supabase.table('open_trades').delete().eq('symbol', symbol).execute()
            
            if len(closed_result.data) > 0:
                return closed_trade_data
            
            return None
            
        except Exception as e:
            print(f"Supabase işlem kapatma hatası: {e}")
            return None
    
    def get_current_signals(self) -> Dict:
        """Mevcut sinyalleri getir (son 200 adet) - Sistem bazlı"""
        try:
            result = self.supabase.table('crypto_signals').select('*').order('timestamp', desc=True).limit(200).execute()
            
            signals = {}
            for row in result.data:
                symbol = row['symbol']
                system = row.get('system', 'UNKNOWN')
                # Sistem bazlı unique key oluştur
                signal_key = f"{symbol}_{system}_{row['timestamp']}"
                
                signals[signal_key] = {
                    'symbol': symbol,
                    'system': system,
                    'signal_type': row['signal_type'],
                    'message': row['message'],
                    'price': row['price'],
                    'timestamp': row['timestamp'],
                    'rsi': row.get('rsi'),
                    'adx': row.get('adx'),
                    'vwap': row.get('vwap'),
                    'atr': row.get('atr')
                }
            
            return signals
            
        except Exception as e:
            print(f"Supabase sinyal getirme hatası: {e}")
            return {}
    
    def get_open_trades(self) -> Dict:
        """Açık işlemleri getir"""
        try:
            result = self.supabase.table('open_trades').select('*').execute()
            
            open_trades = {}
            for row in result.data:
                symbol = row['symbol']
                open_trades[symbol] = {
                    'symbol': symbol,
                    'type': row['trade_type'],
                    'entry_price': row['entry_price'],
                    'entry_time': row['entry_time'],
                    'status': row['status']
                }
            
            return open_trades
            
        except Exception as e:
            print(f"Supabase açık işlem getirme hatası: {e}")
            return {}
    
    def get_closed_trades(self) -> List[Dict]:
        """Kapalı işlemleri getir"""
        try:
            result = self.supabase.table('closed_trades').select('*').order('exit_time', desc=True).execute()
            
            closed_trades = []
            for row in result.data:
                closed_trades.append({
                    'symbol': row['symbol'],
                    'type': row['trade_type'],
                    'entry_price': row['entry_price'],
                    'entry_time': row['entry_time'],
                    'exit_price': row['exit_price'],
                    'exit_time': row['exit_time'],
                    'pnl_percent': row['pnl_percent'],
                    'status': row['status']
                })
            
            return closed_trades
            
        except Exception as e:
            print(f"Supabase kapalı işlem getirme hatası: {e}")
            return []
    
    def get_position_status(self, symbol: str, system: str = 'HYBRID_CRYPTO') -> str:
        """Sembol için pozisyon durumu - Sistem bazlı"""
        try:
            # Sistem filtresi ile sorgu yap
            result = self.supabase.table('open_trades').select('trade_type').eq('symbol', symbol).eq('system', system).execute()

            if result.data:
                return result.data[0]['trade_type']
            return 'NONE'

        except Exception as e:
            print(f"Supabase pozisyon durumu getirme hatası: {e}")
            return 'NONE'
    
    def get_summary(self) -> Dict:
        """Özet istatistikler"""
        try:
            closed_trades = self.get_closed_trades()
            
            if not closed_trades:
                return {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'win_rate': 0,
                    'total_pnl': 0,
                    'avg_pnl': 0
                }
            
            winning = [t for t in closed_trades if t['pnl_percent'] > 0]
            losing = [t for t in closed_trades if t['pnl_percent'] <= 0]
            total_pnl = sum(t['pnl_percent'] for t in closed_trades)
            
            return {
                'total_trades': len(closed_trades),
                'winning_trades': len(winning),
                'losing_trades': len(losing),
                'win_rate': round((len(winning) / len(closed_trades)) * 100, 2),
                'total_pnl': round(total_pnl, 2),
                'avg_pnl': round(total_pnl / len(closed_trades), 2)
            }
            
        except Exception as e:
            print(f"Supabase özet getirme hatası: {e}")
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_pnl': 0
            }
    
    def clear_old_signals(self, days: int = 7):
        """Eski sinyalleri temizle (varsayılan 7 gün)"""
        try:
            cutoff_date = datetime.now(pytz.utc) - timedelta(days=days)
            cutoff_iso = cutoff_date.isoformat()
            
            result = self.supabase.table('crypto_signals').delete().lt('timestamp', cutoff_iso).execute()
            print(f"{len(result.data)} eski sinyal temizlendi")
            
        except Exception as e:
            print(f"Supabase eski sinyal temizleme hatası: {e}")

# Test fonksiyonu
def test_supabase_connection():
    """Supabase bağlantısını test et"""
    try:
        manager = SupabaseManager()
        
        # Test sinyali ekle
        test_indicators = {
            'rsi': 65.5,
            'adx': 25.3,
            'vwap': 45000.123456
        }
        
        success = manager.add_signal(
            'TESTUSDT', 
            'LONG_ENTRY', 
            'Test Sinyali', 
            45000.0, 
            test_indicators
        )
        
        if success:
            print("✅ Supabase bağlantısı başarılı!")
            return True
        else:
            print("❌ Supabase bağlantısı başarısız!")
            return False
            
    except Exception as e:
        print(f"❌ Supabase test hatası: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Supabase Veri Yönetimi
Portfolio ve Trade yönetimi
"""

import os
from supabase import create_client, Client
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

load_dotenv()

class SupabaseManager:
    """Supabase veri yönetimi"""
    
    def __init__(self):
        # Supabase bağlantı bilgileri
        self.url = "https://rkjndkslanwyoyefsicd.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJram5ka3NsYW53eW95ZWZzaWNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzOTY2MDcsImV4cCI6MjA3NDk3MjYwN30.XZd3mmNDhKHj2zIBovsFasj1S7LEhkHNvO79_OGJHxo"
        
        # Supabase client oluştur
        self.supabase: Client = create_client(self.url, self.key)
        
    def get_portfolio_state(self) -> Dict:
        """Get current portfolio state with real-time calculations"""
        try:
            # Get base portfolio state
            result = self.supabase.table('portfolio_state').select('*').limit(1).execute()
            if not result.data:
                # Initialize with $1000
                init_data = {
                    'total_balance': 1000.0,
                    'available_balance': 1000.0,
                    'used_balance': 0.0,
                    'total_pnl': 0.0
                }
                self.supabase.table('portfolio_state').insert(init_data).execute()
                base_state = init_data
            else:
                base_state = result.data[0]
            
            # Calculate real-time used balance from open trades
            open_trades = self.supabase.table('open_trades').select('position_size').execute()
            used_balance = sum(trade.get('position_size', 50.0) for trade in open_trades.data)
            
            # Calculate total PnL from closed trades
            closed_trades = self.supabase.table('closed_trades').select('pnl_usd').execute()
            total_pnl = sum(trade.get('pnl_usd', 0.0) for trade in closed_trades.data)
            
            # Calculate available balance
            available_balance = base_state['total_balance'] + total_pnl - used_balance
            
            return {
                'total_balance': base_state['total_balance'] + total_pnl,
                'available_balance': max(0, available_balance),
                'used_balance': used_balance,
                'total_pnl': total_pnl
            }
            
        except Exception as e:
            print(f"Portfolio state error: {e}")
            return {
                'total_balance': 1000.0,
                'available_balance': 1000.0,
                'used_balance': 0.0,
                'total_pnl': 0.0
            }

    def update_portfolio_balance(self, pnl_usd: float, position_size: float, is_opening: bool):
        """Update portfolio after opening/closing position"""
        try:
            state = self.get_portfolio_state()
            if is_opening:
                state['available_balance'] -= position_size
                state['used_balance'] += position_size
            else:
                state['available_balance'] += position_size + pnl_usd
                state['used_balance'] -= position_size
                state['total_pnl'] += pnl_usd
                state['total_balance'] += pnl_usd
            
            self.supabase.table('portfolio_state').update(state).eq('id', state['id']).execute()
        except Exception as e:
            print(f"Portfolio update error: {e}")
        
    def add_signal(self, symbol: str, signal_type: str, message: str, 
                   price: float, indicators: Dict, system: str = None) -> bool:
        """Add signal only if not duplicate - Enhanced duplicate prevention"""
        try:
            # Check for recent identical signal (within 10 minutes for better prevention)
            ten_min_ago = (datetime.now(pytz.utc) - timedelta(minutes=10)).isoformat()
            
            # Check for any recent signal of same type for same symbol
            existing = self.supabase.table('crypto_signals')\
                .select('*')\
                .eq('symbol', symbol)\
                .eq('signal_type', signal_type)\
                .eq('system', system)\
                .gte('timestamp', ten_min_ago)\
                .execute()
            
            if existing.data:
                print(f"Duplicate signal skipped: {symbol} {signal_type} (found {len(existing.data)} recent signals)")
                return False
            
            # Additional check: If we have an open position, don't add entry signals
            if signal_type in ['LONG_ENTRY', 'SHORT_ENTRY']:
                open_positions = self.supabase.table('open_trades')\
                    .select('*')\
                    .eq('symbol', symbol)\
                    .eq('system', system)\
                    .execute()
                
                if open_positions.data:
                    print(f"Entry signal skipped: {symbol} {signal_type} (position already open)")
                    return False
            
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
            print(f"Signal added: {symbol} {signal_type} @ ${price:.6f}")
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Supabase sinyal ekleme hatası: {e}")
            return False
    
    def open_trade(self, symbol: str, trade_type: str, entry_price: float, 
                   atr_value: float = 0, stop_loss: float = 0, take_profit: float = 0, system: str = None) -> bool:
        """Open trade with capital management"""
        try:
            POSITION_SIZE = 50.0
            LEVERAGE = 5
            
            # Check available balance
            portfolio = self.get_portfolio_state()
            if portfolio['available_balance'] < POSITION_SIZE:
                print(f"Insufficient balance: ${portfolio['available_balance']:.2f} < ${POSITION_SIZE}")
                return False
            
            data = {
                'symbol': symbol,
                'trade_type': trade_type,
                'entry_price': entry_price,
                'entry_time': datetime.now(pytz.utc).isoformat(),
                'status': 'OPEN',
                'atr_value': atr_value,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'position_size': POSITION_SIZE,
                'leverage': LEVERAGE,
                'system': system
            }
            
            result = self.supabase.table('open_trades').upsert(data).execute()
            if len(result.data) > 0:
                self.update_portfolio_balance(0, POSITION_SIZE, is_opening=True)
                return True
            return False
            
        except Exception as e:
            print(f"Supabase işlem açma hatası: {e}")
            return False
    
    def close_trade(self, symbol: str, exit_price: float, system: str = 'HYBRID_CRYPTO') -> Optional[Dict]:
        """Close trade and calculate PnL with 5x leverage"""
        try:
            print(f"Attempting to close trade: {symbol} @ ${exit_price}")
            
            open_trade_result = self.supabase.table('open_trades')\
                .select('*')\
                .eq('symbol', symbol)\
                .eq('system', system)\
                .execute()
            
            if not open_trade_result.data:
                print(f"No open trade found for {symbol} in system {system}")
                return None
            
            trade = open_trade_result.data[0]
            print(f"Found open trade: {trade}")
            
            entry_price = float(trade['entry_price'])
            trade_type = trade['trade_type']
            position_size = trade.get('position_size', 50.0)
            leverage = trade.get('leverage', 5)
            
            print(f"Closing {trade_type} position: Entry ${entry_price}, Exit ${exit_price}")
            
            # Calculate percentage PnL
            if trade_type == 'LONG':
                pnl_percent = ((exit_price - entry_price) / entry_price) * 100
            else:
                pnl_percent = ((entry_price - exit_price) / entry_price) * 100
            
            # Calculate USD PnL with leverage
            pnl_usd = (pnl_percent / 100) * position_size * leverage
            
            print(f"Calculated P&L: {pnl_percent:.2f}% = ${pnl_usd:.2f}")
            
            closed_trade_data = {
                'symbol': symbol,
                'trade_type': trade_type,
                'entry_price': entry_price,
                'entry_time': trade['entry_time'],
                'exit_price': exit_price,
                'exit_time': datetime.now(pytz.utc).isoformat(),
                'pnl_percent': round(pnl_percent, 2),
                'pnl_usd': round(pnl_usd, 2),
                'position_size': position_size,
                'leverage': leverage,
                'status': 'CLOSED',
                'system': system
            }
            
            # Insert into closed trades
            self.supabase.table('closed_trades').insert(closed_trade_data).execute()
            print(f"Trade added to closed_trades: {closed_trade_data}")
            
            # Delete from open trades
            delete_result = self.supabase.table('open_trades').delete().eq('symbol', symbol).eq('system', system).execute()
            print(f"Deleted from open_trades: {delete_result.data}")
            
            # Update portfolio balance
            self.update_portfolio_balance(pnl_usd, position_size, is_opening=False)
            print(f"Portfolio balance updated: P&L ${pnl_usd:.2f}")
            
            return closed_trade_data
            
        except Exception as e:
            print(f"Error closing trade for {symbol}: {e}")
            return None
    
    def get_current_signals(self) -> Dict:
        """Mevcut sinyalleri getir (son 200 adet) - Sistem bazlı"""
        try:
            result = self.supabase.table('crypto_signals').select('*').order('timestamp', desc=True).limit(200).execute()
            
            signals = {}
            for row in result.data:
                key = f"{row['symbol']}_{row['timestamp']}"
                signals[key] = {
                    'symbol': row['symbol'],
                    'signal_type': row['signal_type'],
                    'message': row['message'],
                    'price': row['price'],
                    'timestamp': row['timestamp'],
                    'system': row['system'],
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
                    'status': row['status'],
                    'position_size': row.get('position_size', 50.0),
                    'leverage': row.get('leverage', 5),
                    'stop_loss': row.get('stop_loss', 0),
                    'take_profit': row.get('take_profit', 0),
                    'system': row.get('system', 'HYBRID_CRYPTO')
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
                    'pnl_usd': row.get('pnl_usd', 0.0),
                    'position_size': row.get('position_size', 50.0),
                    'leverage': row.get('leverage', 5),
                    'status': row['status'],
                    'system': row.get('system', 'HYBRID_CRYPTO')
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI Backend - Trading Signal Dashboard
Modern REST API for signal tracking
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import json
from pathlib import Path
from datetime import datetime
import pytz
from supabase_client import SupabaseManager
import asyncio
import threading
from typing import Optional as _Optional  # avoid shadowing

# Lazy import to avoid heavy module load during import time
scanner_thread = None
scanner_instance = None

app = FastAPI(
    title="Trading Signal API",
    description="Professional Trading Signal Tracking System",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da specific domain kullan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase manager
try:
    supabase = SupabaseManager()
    print("✅ Supabase connection established")
except Exception as e:
    print(f"⚠️ Supabase connection failed: {e}")
    supabase = None

# Scanner lifecycle hooks
@app.on_event("startup")
async def start_scanner_background():
    global scanner_thread, scanner_instance
    print("Starting scanner background thread...")
    try:
        from scanner_core import CryptoScanner  # local import to avoid circular issues
        scanner_instance = CryptoScanner()
        # Initialize synchronously
        if scanner_instance.initialize():
            # Start in background thread
            scanner_thread = threading.Thread(target=scanner_instance.start, daemon=True)
            scanner_thread.start()
            print("✓ Scanner started in background thread.")
        else:
            print("⚠️ Scanner initialization failed.")
    except Exception as e:
        print(f"⚠️ Scanner startup failed: {e}")
        import traceback
        traceback.print_exc()

@app.on_event("shutdown")
async def stop_scanner_background():
    global scanner_instance
    try:
        if scanner_instance is not None:
            scanner_instance.stop()
            print("✓ Scanner stop signal sent.")
    except Exception:
        pass

# WebSocket connections
active_connections: List[WebSocket] = []

# ----------------------------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------------------------

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Trading Signal API",
        "version": "2.0.0",
        "status": "online",
        "timestamp": datetime.now(pytz.utc).isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Scanner durumu kontrol et
        heartbeat_file = Path('heartbeat.json')
        scanner_status = "offline"
        last_scan = None
        
        if heartbeat_file.exists():
            data = json.loads(heartbeat_file.read_text())
            last_scan_time = datetime.fromisoformat(data['last_scan'])
            now = datetime.now(pytz.utc)
            diff = (now - last_scan_time).total_seconds()
            
            if diff < 120:  # Son 2 dakika içinde
                scanner_status = "online"
                last_scan = data['last_scan']
        
        return {
            "status": "healthy",
            "scanner": scanner_status,
            "last_scan": last_scan,
            "timestamp": datetime.now(pytz.utc).isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.post("/start-scanner")
async def start_scanner():
    """Manually start scanner"""
    global scanner_thread, scanner_instance
    try:
        if scanner_thread is None or not scanner_thread.is_alive():
            from scanner_core import CryptoScanner
            scanner_instance = CryptoScanner()
            scanner_instance.initialize()
            scanner_thread = threading.Thread(target=scanner_instance.start, daemon=True)
            scanner_thread.start()
            return {"success": True, "message": "Scanner started successfully"}
        else:
            return {"success": False, "message": "Scanner already running"}
    except Exception as e:
        return {"success": False, "message": f"Failed to start scanner: {str(e)}"}

@app.post("/close-trade/{symbol}")
async def close_trade_manual(symbol: str, exit_price: float):
    """Manually close a trade for debugging"""
    try:
        closed_trade = supabase.close_trade(symbol, exit_price, 'HYBRID_CRYPTO')
        if closed_trade:
            return {"success": True, "message": f"Trade closed for {symbol}", "trade": closed_trade}
        else:
            return {"success": False, "message": f"No open trade found for {symbol}"}
    except Exception as e:
        return {"success": False, "message": f"Failed to close trade: {str(e)}"}

# ----------------------------------------------------------------------
# SIGNALS ENDPOINTS
# ----------------------------------------------------------------------

@app.get("/api/signals")
async def get_signals(
    market: Optional[str] = None,
    system: Optional[str] = None,
    limit: Optional[int] = 50
):
    """
    Get trading signals
    
    Parameters:
    - market: CRYPTO, BIST, US (optional)
    - system: HYBRID, ELLIOTT (optional)
    - limit: Number of signals to return (default: 50)
    """
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    
    try:
        all_signals = supabase.get_current_signals()
        
        # Filtreleme
        filtered_signals = []
        seen_symbols = {}  # Sembol bazında en yeni sinyali tutmak için
        
        for signal_key, signal_data in all_signals.items():
            signal_system = signal_data.get('system', '')
            
            # Market filtresi
            if market and market.upper() not in signal_system:
                continue
            
            # System filtresi
            if system and system.upper() not in signal_system:
                continue
            
            # Aynı sembol için sadece en yeni sinyali ekle
            symbol_key = f"{signal_data['symbol']}_{signal_data['signal_type']}"
            existing_signal = seen_symbols.get(symbol_key)
            
            if existing_signal is None or signal_data['timestamp'] > existing_signal['timestamp']:
                seen_symbols[symbol_key] = signal_data
        
        # Sadece en yeni sinyalleri kullan
        filtered_signals = [
            {'id': f"{data['symbol']}_{data['signal_type']}", **data} 
            for data in seen_symbols.values()
        ]
        
        # Timestamp'e göre sırala (en yeni önce)
        filtered_signals.sort(
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        # Limit uygula
        if limit:
            filtered_signals = filtered_signals[:limit]
        
        return {
            "success": True,
            "count": len(filtered_signals),
            "signals": filtered_signals
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/signals/stats")
async def get_signal_stats():
    """Get signal statistics - Crypto Hybrid only"""
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    
    try:
        all_signals = supabase.get_current_signals()
        
        stats = {
            "CRYPTO": {"HYBRID": 0}
        }
        
        for signal_data in all_signals.values():
            system = signal_data.get('system', '')
            
            if 'HYBRID_CRYPTO' in system:
                stats["CRYPTO"]["HYBRID"] += 1
        
        return {
            "success": True,
            "stats": stats,
            "total": stats["CRYPTO"]["HYBRID"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------------------------------------
# TRADES ENDPOINTS
# ----------------------------------------------------------------------

@app.get("/api/trades/open")
async def get_open_trades(
    market: Optional[str] = None,
    system: Optional[str] = None
):
    """Get open trades"""
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    
    try:
        open_trades = supabase.get_open_trades()
        
        # Filtreleme
        filtered_trades = []
        for trade_key, trade_data in open_trades.items():
            trade_system = trade_data.get('system', '')
            
            # Market filtresi
            if market and market.upper() not in trade_system:
                continue
            
            # System filtresi
            if system and system.upper() not in trade_system:
                continue
            
            filtered_trades.append({
                'id': trade_key,
                **trade_data
            })
        
        return {
            "success": True,
            "count": len(filtered_trades),
            "trades": filtered_trades
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trades/closed")
async def get_closed_trades(
    market: Optional[str] = None,
    system: Optional[str] = None,
    limit: Optional[int] = 100
):
    """Get closed trades"""
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    
    try:
        closed_trades = supabase.get_closed_trades()
        
        # Filtreleme
        filtered_trades = []
        for trade_data in closed_trades:
            trade_system = trade_data.get('system', '')
            
            # Market filtresi
            if market and market.upper() not in trade_system:
                continue
            
            # System filtresi
            if system and system.upper() not in trade_system:
                continue
            
            filtered_trades.append(trade_data)
        
        # Timestamp'e göre sırala (en yeni önce)
        filtered_trades.sort(
            key=lambda x: x.get('exit_time', ''),
            reverse=True
        )
        
        # Limit uygula
        if limit:
            filtered_trades = filtered_trades[:limit]
        
        return {
            "success": True,
            "count": len(filtered_trades),
            "trades": filtered_trades
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trades/performance")
async def get_performance_stats():
    """Get performance statistics"""
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    
    try:
        closed_trades = supabase.get_closed_trades()
        
        # Sistem ve market bazlı gruplama
        stats = {}
        
        for trade in closed_trades:
            system = trade.get('system', 'UNKNOWN')
            
            if system not in stats:
                stats[system] = {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'total_pnl': 0,
                    'avg_pnl': 0,
                    'win_rate': 0,
                    'best_trade': 0,
                    'worst_trade': 0
                }
            
            pnl = trade.get('pnl', 0)
            stats[system]['total_trades'] += 1
            stats[system]['total_pnl'] += pnl
            
            if pnl > 0:
                stats[system]['winning_trades'] += 1
                if pnl > stats[system]['best_trade']:
                    stats[system]['best_trade'] = pnl
            else:
                stats[system]['losing_trades'] += 1
                if pnl < stats[system]['worst_trade']:
                    stats[system]['worst_trade'] = pnl
        
        # İstatistikleri hesapla
        for system in stats:
            total = stats[system]['total_trades']
            if total > 0:
                stats[system]['avg_pnl'] = stats[system]['total_pnl'] / total
                stats[system]['win_rate'] = (stats[system]['winning_trades'] / total) * 100
        
        return {
            "success": True,
            "performance": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------------------------------------
# WEBSOCKET FOR REAL-TIME UPDATES
# ----------------------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time signal updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Her 5 saniyede bir güncel veriyi gönder
            await asyncio.sleep(5)
            
            # Güncel sinyalleri al (Supabase bağlantısı yoksa boş döndür)
            if supabase is not None:
                signals = supabase.get_current_signals()
            else:
                signals = {}
            
            # WebSocket üzerinden gönder
            await websocket.send_json({
                "type": "signal_update",
                "data": {
                    "count": len(signals),
                    "timestamp": datetime.now(pytz.utc).isoformat()
                }
            })
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# ----------------------------------------------------------------------
# MARKET INFO
# ----------------------------------------------------------------------

@app.get("/api/portfolio")
async def get_portfolio():
    """Get portfolio state"""
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    
    try:
        portfolio = supabase.get_portfolio_state()
        return {
            "success": True,
            "portfolio": portfolio
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/markets")
async def get_markets():
    """Get available markets - Crypto only"""
    try:
        return {
            "success": True,
            "markets": {
                "CRYPTO": {
                    "name": "Cryptocurrency",
                    "status": "open",
                    "trading_hours": "24/7",
                    "timezone": "UTC"
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


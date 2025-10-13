# -*- coding: utf-8 -*-
"""
Kripto Sinyal Dashboard - Çoklu Sistem Versiyonu
Her iki sistemin sinyallerini ve performanslarını ayrı ayrı gösterir
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
from supabase_client import SupabaseManager
import pytz

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kripto Sinyal Takip Pro - Çoklu Sistem",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state başlatma
if 'last_signal_count' not in st.session_state:
    st.session_state.last_signal_count = 0
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'last_signals' not in st.session_state:
    st.session_state.last_signals = {}

# Dark Mode Toggle
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# CSS Stilleri - Dark Mode Desteği
def get_css():
    if st.session_state.dark_mode:
        # Dark Mode
        return """
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                text-align: center;
                color: #64B5F6;
                margin-bottom: 1rem;
            }
            .system-header {
                font-size: 1.8rem;
                font-weight: bold;
                color: #4CAF50;
                margin: 1rem 0;
            }
            .metric-card {
                background-color: #1E1E1E;
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #333;
                margin: 0.5rem 0;
            }
            .signal-card {
                background-color: #2D2D2D;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #4CAF50;
                margin: 0.5rem 0;
            }
            .hybrid-signal {
                border-left-color: #FF9800;
            }
            .elliott-signal {
                border-left-color: #2196F3;
            }
        </style>
        """
    else:
        # Light Mode
        return """
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                text-align: center;
                color: #1976D2;
                margin-bottom: 1rem;
            }
            .system-header {
                font-size: 1.8rem;
                font-weight: bold;
                color: #388E3C;
                margin: 1rem 0;
            }
            .metric-card {
                background-color: #FFFFFF;
                padding: 1rem;
                border-radius: 10px;
                border: 2px solid #E0E0E0;
                margin: 0.5rem 0;
                color: #212121;
            }
            .signal-card {
                background-color: #FFFFFF;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #4CAF50;
                margin: 0.5rem 0;
                color: #212121;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .signal-card strong {
                color: #1565C0;
                font-size: 1.1rem;
            }
            .hybrid-signal {
                border-left-color: #FF6F00;
                background-color: #FFF8E1;
            }
            .hybrid-signal strong {
                color: #E65100;
            }
            .elliott-signal {
                border-left-color: #1976D2;
                background-color: #E3F2FD;
            }
            .elliott-signal strong {
                color: #0D47A1;
            }
        </style>
        """

# Supabase manager
@st.cache_resource
def get_supabase_manager():
    return SupabaseManager()

def check_scanner_status():
    """Scanner'ın çalışıp çalışmadığını kontrol et"""
    try:
        heartbeat_file = Path('heartbeat.json')
        if heartbeat_file.exists():
            data = json.loads(heartbeat_file.read_text())
            last_scan = datetime.fromisoformat(data['last_scan'])
            now = datetime.now(pytz.utc)
            diff = (now - last_scan).total_seconds()
            
            # Son 2 dakika içinde tarama yapılmışsa çalışıyor
            is_running = diff < 120
            return is_running, last_scan, diff
        return False, None, None
    except Exception as e:
        return False, None, None

@st.cache_data(ttl=5)
def load_signals():
    """Sinyalleri yükle - Sistem bazlı"""
    try:
        supabase = get_supabase_manager()
        return supabase.get_current_signals()
    except Exception as e:
        st.error(f"Supabase bağlantı hatası: {e}")
        return {}

@st.cache_data(ttl=5)
def load_trades():
    """İşlemleri yükle - Sistem bazlı"""
    try:
        supabase = get_supabase_manager()
        open_trades = supabase.get_open_trades()
        closed_trades = supabase.get_closed_trades()
        return open_trades, closed_trades
    except Exception as e:
        st.error(f"Supabase bağlantı hatası: {e}")
        return {}, []

def calculate_system_stats(closed_trades):
    """Sistem bazlı istatistik hesapla"""
    if not closed_trades:
        return {
            'hybrid': {'total': 0, 'wins': 0, 'win_rate': 0, 'avg_pnl': 0, 'total_pnl': 0},
            'elliott': {'total': 0, 'wins': 0, 'win_rate': 0, 'avg_pnl': 0, 'total_pnl': 0}
        }
    
    # Sistem bazlı gruplama
    hybrid_trades = [t for t in closed_trades if t.get('system') == 'HYBRID']
    elliott_trades = [t for t in closed_trades if t.get('system') == 'ELLIOTT']
    
    def calc_stats(trades):
        if not trades:
            return {'total': 0, 'wins': 0, 'win_rate': 0, 'avg_pnl': 0, 'total_pnl': 0}
        
        wins = len([t for t in trades if t.get('pnl', 0) > 0])
        win_rate = (wins / len(trades)) * 100 if trades else 0
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        avg_pnl = total_pnl / len(trades) if trades else 0
        
        return {
            'total': len(trades),
            'wins': wins,
            'win_rate': win_rate,
            'avg_pnl': avg_pnl,
            'total_pnl': total_pnl
        }
    
    return {
        'hybrid': calc_stats(hybrid_trades),
        'elliott': calc_stats(elliott_trades)
    }

def calculate_signal_strength(signal_data):
    """Sinyal gücü skoru hesapla (0-100)"""
    score = 50  # Başlangıç skoru
    
    rsi = signal_data.get('rsi', 50)
    adx = signal_data.get('adx', 0)
    
    # RSI bazlı skor
    if signal_data.get('signal_type') in ['LONG_ENTRY']:
        # LONG için düşük RSI iyi
        if rsi < 30:
            score += 20
        elif rsi < 40:
            score += 15
        elif rsi < 50:
            score += 10
    elif signal_data.get('signal_type') in ['SHORT_ENTRY']:
        # SHORT için yüksek RSI iyi
        if rsi > 70:
            score += 20
        elif rsi > 60:
            score += 15
        elif rsi > 50:
            score += 10
    
    # ADX bazlı skor (trend gücü)
    if adx > 25:
        score += min(adx - 25, 20)  # Maksimum 20 puan
    
    return min(100, max(0, int(score)))

def get_strength_emoji(score):
    """Skor için emoji döndür"""
    if score >= 80:
        return "🔥"
    elif score >= 60:
        return "💪"
    elif score >= 40:
        return "👍"
    else:
        return "⚠️"

def filter_signals_by_system(signals, system, market_type='CRYPTO'):
    """Sistem ve market bazlı sinyal filtreleme"""
    if not signals:
        return {}
    
    filtered = {}
    system_key = f"{system}_{market_type}"
    
    for signal_key, signal_data in signals.items():
        signal_system = signal_data.get('system', '')
        # Eski format (HYBRID/ELLIOTT) veya yeni format (HYBRID_CRYPTO/ELLIOTT_BIST)
        if signal_system == system or signal_system == system_key:
            filtered[signal_key] = signal_data
    
    return filtered

def create_system_comparison_chart(stats):
    """Sistem karşılaştırma grafiği"""
    systems = ['HİBRİT', 'ELLİOTT']
    win_rates = [stats['hybrid']['win_rate'], stats['elliott']['win_rate']]
    avg_pnls = [stats['hybrid']['avg_pnl'], stats['elliott']['avg_pnl']]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Kazanma Oranı (%)', 'Ortalama PnL (%)'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Kazanma oranı
    fig.add_trace(
        go.Bar(x=systems, y=win_rates, name='Kazanma Oranı', marker_color=['#FF9800', '#2196F3']),
        row=1, col=1
    )
    
    # Ortalama PnL
    fig.add_trace(
        go.Bar(x=systems, y=avg_pnls, name='Ortalama PnL', marker_color=['#FF9800', '#2196F3']),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Sistem Performans Karşılaştırması",
        showlegend=False,
        height=400
    )
    
    return fig

# ----------------------------------------------------------------------
# ANA DASHBOARD
# ----------------------------------------------------------------------

def main():
    # CSS yükle
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Header
    mode_emoji = "🌙" if st.session_state.dark_mode else "☀️"
    st.markdown(f'<h1 class="main-header">{mode_emoji} KRİPTO SİNYAL TAKİP SİSTEMİ - ÇOKLU SİSTEM</h1>', unsafe_allow_html=True)
    
    # Veri yükle
    signals = load_signals()
    open_trades, closed_trades = load_trades()
    system_stats = calculate_system_stats(closed_trades)
    
    # Yeni sinyal bildirimi
    current_signal_count = len(signals)
    if current_signal_count > st.session_state.last_signal_count:
        new_count = current_signal_count - st.session_state.last_signal_count
        st.toast(f"🔔 {new_count} yeni sinyal geldi!", icon="📢")
    st.session_state.last_signal_count = current_signal_count
    
    # Sidebar
    with st.sidebar:
        st.image("https://cryptologos.cc/logos/bitcoin-btc-logo.png", width=80)
        st.title("⚙️ Kontrol Paneli")
        
        # Scanner Durumu
        is_running, last_scan, diff = check_scanner_status()
        if is_running:
            st.success("✅ Scanner Çalışıyor")
            if last_scan:
                st.caption(f"Son tarama: {int(diff)}s önce")
        else:
            st.error("❌ Scanner Durmuş")
            st.caption("Scanner başlatılıyor olabilir...")
        
        st.divider()
        
        # Dark Mode Toggle
        if st.button("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"):
            toggle_dark_mode()
            st.rerun()
        
        st.divider()
        
        # Sistem İstatistikleri
        st.subheader("📊 Sistem Performansı")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "HİBRİT Kazanma Oranı",
                f"{system_stats['hybrid']['win_rate']:.1f}%",
                f"{system_stats['hybrid']['total']} işlem"
            )
        
        with col2:
            st.metric(
                "ELLİOTT Kazanma Oranı", 
                f"{system_stats['elliott']['win_rate']:.1f}%",
                f"{system_stats['elliott']['total']} işlem"
            )
        
        # Arama ve Filtreleme
        st.divider()
        st.subheader("🔍 Arama & Filtreleme")
        
        search_symbol = st.text_input("Sembol Ara:", placeholder="BTCUSDT")
        signal_filter = st.selectbox("Sinyal Türü:", ["Tümü", "LONG_ENTRY", "SHORT_ENTRY", "LONG_EXIT", "SHORT_EXIT"])
        system_filter = st.selectbox("Sistem:", ["Tümü", "HYBRID", "ELLIOTT"])
    
    # Ana İçerik
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 KRİPTO", "🏛️ BIST", "📊 Sistem Karşılaştırması", "💼 Açık İşlemler", "📋 İşlem Geçmişi"])
    
    with tab1:
        st.markdown('<h2 class="system-header">💰 KRİPTO - Canlı Sinyaller (Son 10)</h2>', unsafe_allow_html=True)
        
        # Kripto sinyalleri
        all_hybrid_signals = filter_signals_by_system(signals, 'HYBRID', 'CRYPTO')
        all_elliott_signals = filter_signals_by_system(signals, 'ELLIOTT', 'CRYPTO')
        
        # Son 10 sinyali göster
        hybrid_signals = dict(list(all_hybrid_signals.items())[:10])
        elliott_signals = dict(list(all_elliott_signals.items())[:10])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 style="color: #FF9800;">🎯 HİBRİT SİSTEM SİNYALLERİ</h3>', unsafe_allow_html=True)
            if hybrid_signals:
                for signal_key, signal_data in hybrid_signals.items():
                    symbol = signal_data.get('symbol', 'N/A')
                    if search_symbol and search_symbol.upper() not in symbol.upper():
                        continue
                    if signal_filter != "Tümü" and signal_data.get('signal_type') != signal_filter:
                        continue
                    
                    # Sinyal gücü skoru hesapla
                    strength_score = calculate_signal_strength(signal_data)
                    strength_emoji = get_strength_emoji(strength_score)
                    
                    # Alım/Satım renk kodlaması (sadece giriş sinyalleri için)
                    signal_type = signal_data.get('signal_type', 'N/A')
                    if 'ENTRY' in signal_type:
                        if 'LONG' in signal_type:
                            signal_color = '#4CAF50'  # Yeşil - Alım
                            signal_bg = '#E8F5E9'
                        else:  # SHORT
                            signal_color = '#F44336'  # Kırmızı - Satım
                            signal_bg = '#FFEBEE'
                    else:  # EXIT - Hibrit sistem için turuncu
                        signal_color = '#FF9800'
                        signal_bg = '#FFF8E1'
                    
                    with st.container():
                        st.markdown(f'''
                        <div class="signal-card" style="background-color: {signal_bg}; border-left-color: {signal_color};">
                            <strong style="color: {signal_color};">{symbol}</strong> - 
                            <span style="color: {signal_color}; font-weight: bold;">{signal_type}</span>
                            <span style="float: right;">{strength_emoji} {strength_score}/100</span><br>
                            <em>{signal_data.get('message', 'N/A')}</em><br>
                            💰 ${signal_data.get('price', 0):.6f} | 
                            ⏰ {signal_data.get('timestamp', 'N/A')[:16]}
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.info("Hibrit sistem için sinyal bulunamadı.")
        
        with col2:
            st.markdown('<h3 style="color: #2196F3;">🌊 ELLİOTT SİSTEM SİNYALLERİ</h3>', unsafe_allow_html=True)
            if elliott_signals:
                for signal_key, signal_data in elliott_signals.items():
                    symbol = signal_data.get('symbol', 'N/A')
                    if search_symbol and search_symbol.upper() not in symbol.upper():
                        continue
                    if signal_filter != "Tümü" and signal_data.get('signal_type') != signal_filter:
                        continue
                    
                    # Sinyal gücü skoru hesapla
                    strength_score = calculate_signal_strength(signal_data)
                    strength_emoji = get_strength_emoji(strength_score)
                    
                    # Alım/Satım renk kodlaması (sadece giriş sinyalleri için)
                    signal_type = signal_data.get('signal_type', 'N/A')
                    if 'ENTRY' in signal_type:
                        if 'LONG' in signal_type:
                            signal_color = '#4CAF50'  # Yeşil - Alım
                            signal_bg = '#E8F5E9'
                        else:  # SHORT
                            signal_color = '#F44336'  # Kırmızı - Satım
                            signal_bg = '#FFEBEE'
                    else:  # EXIT - Elliott sistem için mavi
                        signal_color = '#2196F3'
                        signal_bg = '#E3F2FD'
                    
                    with st.container():
                        st.markdown(f'''
                        <div class="signal-card" style="background-color: {signal_bg}; border-left-color: {signal_color};">
                            <strong style="color: {signal_color};">{symbol}</strong> - 
                            <span style="color: {signal_color}; font-weight: bold;">{signal_type}</span>
                            <span style="float: right;">{strength_emoji} {strength_score}/100</span><br>
                            <em>{signal_data.get('message', 'N/A')}</em><br>
                            💰 ${signal_data.get('price', 0):.6f} | 
                            ⏰ {signal_data.get('timestamp', 'N/A')[:16]}
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.info("Elliott sistem için sinyal bulunamadı.")
    
    with tab2:
        st.markdown('<h2 class="system-header">🏛️ BIST - Canlı Sinyaller (Son 10)</h2>', unsafe_allow_html=True)
        
        # BIST sinyalleri
        all_hybrid_signals_bist = filter_signals_by_system(signals, 'HYBRID', 'BIST')
        all_elliott_signals_bist = filter_signals_by_system(signals, 'ELLIOTT', 'BIST')
        
        # Son 10 sinyali göster
        hybrid_signals_bist = dict(list(all_hybrid_signals_bist.items())[:10])
        elliott_signals_bist = dict(list(all_elliott_signals_bist.items())[:10])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 style="color: #FF9800;">🎯 HİBRİT SİSTEM SİNYALLERİ</h3>', unsafe_allow_html=True)
            if hybrid_signals_bist:
                for signal_key, signal_data in hybrid_signals_bist.items():
                    symbol = signal_data.get('symbol', 'N/A')
                    if search_symbol and search_symbol.upper() not in symbol.upper():
                        continue
                    if signal_filter != "Tümü" and signal_data.get('signal_type') != signal_filter:
                        continue
                    
                    strength_score = calculate_signal_strength(signal_data)
                    strength_emoji = get_strength_emoji(strength_score)
                    
                    signal_type = signal_data.get('signal_type', 'N/A')
                    if 'ENTRY' in signal_type:
                        if 'LONG' in signal_type:
                            signal_color = '#4CAF50'
                            signal_bg = '#E8F5E9'
                        else:
                            signal_color = '#F44336'
                            signal_bg = '#FFEBEE'
                    else:
                        signal_color = '#FF9800'
                        signal_bg = '#FFF8E1'
                    
                    with st.container():
                        st.markdown(f'''
                        <div class="signal-card" style="background-color: {signal_bg}; border-left-color: {signal_color};">
                            <strong style="color: {signal_color};">{symbol}</strong> - 
                            <span style="color: {signal_color}; font-weight: bold;">{signal_type}</span>
                            <span style="float: right;">{strength_emoji} {strength_score}/100</span><br>
                            <em>{signal_data.get('message', 'N/A')}</em><br>
                            💰 ₺{signal_data.get('price', 0):.2f} | 
                            ⏰ {signal_data.get('timestamp', 'N/A')[:16]}
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.info("BIST Hibrit sistem için sinyal bulunamadı.")
        
        with col2:
            st.markdown('<h3 style="color: #2196F3;">🌊 ELLİOTT SİSTEM SİNYALLERİ</h3>', unsafe_allow_html=True)
            if elliott_signals_bist:
                for signal_key, signal_data in elliott_signals_bist.items():
                    symbol = signal_data.get('symbol', 'N/A')
                    if search_symbol and search_symbol.upper() not in symbol.upper():
                        continue
                    if signal_filter != "Tümü" and signal_data.get('signal_type') != signal_filter:
                        continue
                    
                    strength_score = calculate_signal_strength(signal_data)
                    strength_emoji = get_strength_emoji(strength_score)
                    
                    signal_type = signal_data.get('signal_type', 'N/A')
                    if 'ENTRY' in signal_type:
                        if 'LONG' in signal_type:
                            signal_color = '#4CAF50'
                            signal_bg = '#E8F5E9'
                        else:
                            signal_color = '#F44336'
                            signal_bg = '#FFEBEE'
                    else:
                        signal_color = '#2196F3'
                        signal_bg = '#E3F2FD'
                    
                    with st.container():
                        st.markdown(f'''
                        <div class="signal-card" style="background-color: {signal_bg}; border-left-color: {signal_color};">
                            <strong style="color: {signal_color};">{symbol}</strong> - 
                            <span style="color: {signal_color}; font-weight: bold;">{signal_type}</span>
                            <span style="float: right;">{strength_emoji} {strength_score}/100</span><br>
                            <em>{signal_data.get('message', 'N/A')}</em><br>
                            💰 ₺{signal_data.get('price', 0):.2f} | 
                            ⏰ {signal_data.get('timestamp', 'N/A')[:16]}
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.info("BIST Elliott sistem için sinyal bulunamadı.")
    
    with tab3:
        st.markdown('<h2 class="system-header">📊 Sistem Performans Karşılaştırması</h2>', unsafe_allow_html=True)
        
        # Sistem karşılaştırma grafiği
        if system_stats['hybrid']['total'] > 0 or system_stats['elliott']['total'] > 0:
            fig = create_system_comparison_chart(system_stats)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detaylı istatistikler
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 style="color: #FF9800;">🎯 HİBRİT SİSTEM İSTATİSTİKLERİ</h3>', unsafe_allow_html=True)
            st.metric("Toplam İşlem", system_stats['hybrid']['total'])
            st.metric("Kazanılan İşlem", system_stats['hybrid']['wins'])
            st.metric("Kazanma Oranı", f"{system_stats['hybrid']['win_rate']:.1f}%")
            st.metric("Ortalama PnL", f"{system_stats['hybrid']['avg_pnl']:.2f}%")
            st.metric("Toplam PnL", f"${system_stats['hybrid']['total_pnl']:.2f}")
        
        with col2:
            st.markdown('<h3 style="color: #2196F3;">🌊 ELLİOTT SİSTEM İSTATİSTİKLERİ</h3>', unsafe_allow_html=True)
            st.metric("Toplam İşlem", system_stats['elliott']['total'])
            st.metric("Kazanılan İşlem", system_stats['elliott']['wins'])
            st.metric("Kazanma Oranı", f"{system_stats['elliott']['win_rate']:.1f}%")
            st.metric("Ortalama PnL", f"{system_stats['elliott']['avg_pnl']:.2f}%")
            st.metric("Toplam PnL", f"${system_stats['elliott']['total_pnl']:.2f}")
    
    with tab3:
        st.markdown('<h2 class="system-header">💼 Açık İşlemler</h2>', unsafe_allow_html=True)
        
        # EXIT sinyali olmayan ENTRY sinyallerini bul
        def find_open_positions_from_signals(all_signals, system_name):
            """Giriş sinyali var ama çıkış sinyali olmayan pozisyonları bul"""
            open_positions = {}
            
            for signal_key, signal_data in all_signals.items():
                symbol = signal_data.get('symbol')
                signal_type = signal_data.get('signal_type', '')
                
                # ENTRY sinyali mi?
                if 'ENTRY' in signal_type:
                    # Bu sembol için sonradan EXIT sinyali var mı kontrol et
                    has_exit = False
                    for exit_key, exit_data in all_signals.items():
                        if (exit_data.get('symbol') == symbol and 
                            'EXIT' in exit_data.get('signal_type', '') and
                            exit_data.get('timestamp') > signal_data.get('timestamp')):
                            has_exit = True
                            break
                    
                    # EXIT sinyali yoksa açık pozisyon olarak ekle
                    if not has_exit:
                        open_positions[signal_key] = {
                            'symbol': symbol,
                            'system': system_name,
                            'trade_type': 'LONG' if 'LONG' in signal_type else 'SHORT',
                            'entry_price': signal_data.get('price', 0),
                            'entry_time': signal_data.get('timestamp', 'N/A'),
                            'stop_loss': 0,  # Sinyalden hesaplanamaz
                            'take_profit': 0,
                            'status': 'OPEN',
                            'from_signal': True
                        }
            
            return open_positions
        
        # Tüm sinyalleri al
        all_hybrid_signals = filter_signals_by_system(signals, 'HYBRID')
        all_elliott_signals = filter_signals_by_system(signals, 'ELLIOTT')
        
        # Sinyal bazlı açık pozisyonları bul
        signal_based_hybrid = find_open_positions_from_signals(all_hybrid_signals, 'HYBRID')
        signal_based_elliott = find_open_positions_from_signals(all_elliott_signals, 'ELLIOTT')
        
        # Gerçek açık işlemlerle birleştir
        hybrid_trades = {k: v for k, v in open_trades.items() if v.get('system') == 'HYBRID'}
        elliott_trades = {k: v for k, v in open_trades.items() if v.get('system') == 'ELLIOTT'}
        
        # Sinyal bazlı açık pozisyonları ekle (gerçek işlemlerde yoksa)
        for key, signal_trade in signal_based_hybrid.items():
            # Aynı sembol gerçek işlemlerde var mı kontrol et
            symbol_exists = any(t.get('symbol') == signal_trade['symbol'] for t in hybrid_trades.values())
            if not symbol_exists:
                hybrid_trades[key] = signal_trade
        
        for key, signal_trade in signal_based_elliott.items():
            # Aynı sembol gerçek işlemlerde var mı kontrol et
            symbol_exists = any(t.get('symbol') == signal_trade['symbol'] for t in elliott_trades.values())
            if not symbol_exists:
                elliott_trades[key] = signal_trade
        
        if hybrid_trades or elliott_trades:
            # Sistem bazlı ayırma
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<h3 style="color: #FF9800;">🎯 HİBRİT SİSTEM İŞLEMLERİ</h3>', unsafe_allow_html=True)
                if hybrid_trades:
                    for trade_id, trade_data in hybrid_trades.items():
                        # SL/TP varsa göster
                        sl_tp_text = ""
                        if trade_data.get('stop_loss', 0) > 0 and trade_data.get('take_profit', 0) > 0:
                            sl_tp_text = f"🛑 SL: ${trade_data.get('stop_loss', 0):.6f} | 💰 TP: ${trade_data.get('take_profit', 0):.6f}<br>"
                        
                        st.markdown(f'''
                        <div class="metric-card" style="border-left: 4px solid #FF9800;">
                            <strong style="color: #FF9800;">{trade_data.get('symbol', 'N/A')}</strong><br>
                            📈 {trade_data.get('trade_type', 'N/A')} @ ${trade_data.get('entry_price', 0):.6f}<br>
                            {sl_tp_text}⏰ {trade_data.get('entry_time', 'N/A')[:16]}
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.info("Hibrit sistem için açık işlem yok")
            
            with col2:
                st.markdown('<h3 style="color: #2196F3;">🌊 ELLİOTT SİSTEM İŞLEMLERİ</h3>', unsafe_allow_html=True)
                if elliott_trades:
                    for trade_id, trade_data in elliott_trades.items():
                        # SL/TP varsa göster
                        sl_tp_text = ""
                        if trade_data.get('stop_loss', 0) > 0 and trade_data.get('take_profit', 0) > 0:
                            sl_tp_text = f"🛑 SL: ${trade_data.get('stop_loss', 0):.6f} | 💰 TP: ${trade_data.get('take_profit', 0):.6f}<br>"
                        
                        st.markdown(f'''
                        <div class="metric-card" style="border-left: 4px solid #2196F3;">
                            <strong style="color: #2196F3;">{trade_data.get('symbol', 'N/A')}</strong><br>
                            📈 {trade_data.get('trade_type', 'N/A')} @ ${trade_data.get('entry_price', 0):.6f}<br>
                            {sl_tp_text}⏰ {trade_data.get('entry_time', 'N/A')[:16]}
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.info("Elliott sistem için açık işlem yok")
        else:
            st.info("Hiç açık işlem bulunamadı.")
    
    with tab5:
        st.markdown('<h2 class="system-header">📋 İşlem Geçmişi</h2>', unsafe_allow_html=True)
        
        if closed_trades:
            df = pd.DataFrame(closed_trades)
            df['pnl_color'] = df['pnl'].apply(lambda x: 'green' if x > 0 else 'red')
            
            st.dataframe(
                df[['symbol', 'system', 'trade_type', 'entry_price', 'exit_price', 'pnl', 'pnl_pct', 'exit_time']],
                use_container_width=True
            )
        else:
            st.info("İşlem geçmişi bulunamadı.")
    
    # Auto refresh
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()

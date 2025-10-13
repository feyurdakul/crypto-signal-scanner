# -*- coding: utf-8 -*-
"""
Kripto Sinyal Dashboard V2 - Gelişmiş Özellikler
Canlı bildirimler, arama, filtreleme, sinyal gücü skoru, favoriler, dark mode
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

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kripto Sinyal Takip Pro",
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
if 'strategy_mode' not in st.session_state:
    st.session_state.strategy_mode = "HYBRID"

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
                text-shadow: 0 0 10px rgba(100, 181, 246, 0.5);
            }
            .kpi-card {
                background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                border: 1px solid #3b82f6;
            }
            .kpi-value {
                font-size: 2.5rem;
                font-weight: bold;
                margin: 0.5rem 0;
            }
            .kpi-label {
                font-size: 0.9rem;
                opacity: 0.8;
            }
            .signal-long {
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
            }
            .signal-short {
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
            }
            .signal-exit-long {
                background: linear-gradient(135deg, #f59e0b, #d97706);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
            }
            .signal-exit-short {
                background: linear-gradient(135deg, #06b6d4, #0891b2);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
            }
            .score-high { 
                color: #10b981; 
                font-weight: bold; 
                font-size: 1.2rem;
            }
            .score-medium { 
                color: #f59e0b; 
                font-weight: bold; 
                font-size: 1.2rem;
            }
            .score-low { 
                color: #ef4444; 
                font-weight: bold; 
                font-size: 1.2rem;
            }
            .profit { color: #10b981; font-weight: bold; }
            .loss { color: #ef4444; font-weight: bold; }
            .favorite-star { 
                color: #fbbf24; 
                font-size: 1.5rem; 
                cursor: pointer;
                text-shadow: 0 0 5px rgba(251, 191, 36, 0.5);
            }
            .stApp {
                background-color: #0f172a;
                color: #e2e8f0;
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
                color: #1f77b4;
                margin-bottom: 1rem;
            }
            .kpi-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .kpi-value {
                font-size: 2.5rem;
                font-weight: bold;
                margin: 0.5rem 0;
            }
            .kpi-label {
                font-size: 0.9rem;
                opacity: 0.9;
            }
            .signal-long {
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
            }
            .signal-short {
                background: linear-gradient(135deg, #dc3545, #c82333);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);
            }
            .signal-exit-long {
                background: linear-gradient(135deg, #ffc107, #ff9800);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
            }
            .signal-exit-short {
                background: linear-gradient(135deg, #17a2b8, #138496);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-weight: bold;
            }
            .score-high { color: #28a745; font-weight: bold; font-size: 1.2rem; }
            .score-medium { color: #ffc107; font-weight: bold; font-size: 1.2rem; }
            .score-low { color: #dc3545; font-weight: bold; font-size: 1.2rem; }
            .profit { color: #28a745; font-weight: bold; }
            .loss { color: #dc3545; font-weight: bold; }
            .favorite-star { color: #ffc107; font-size: 1.5rem; cursor: pointer; }
        </style>
        """

st.markdown(get_css(), unsafe_allow_html=True)

# Veri dosyaları
FAVORITES_FILE = Path('favorites.json')

# Supabase manager
@st.cache_resource
def get_supabase_manager():
    return SupabaseManager()

# ----------------------------------------------------------------------
# VERİ YÜKLEME
# ----------------------------------------------------------------------

@st.cache_data(ttl=5)
def load_signals():
    try:
        supabase = get_supabase_manager()
        return supabase.get_current_signals()
    except Exception as e:
        st.error(f"Supabase bağlantı hatası: {e}")
        return {}

@st.cache_data(ttl=5)
def load_trades():
    try:
        supabase = get_supabase_manager()
        open_trades = supabase.get_open_trades()
        closed_trades = supabase.get_closed_trades()
        return open_trades, closed_trades
    except Exception as e:
        st.error(f"Supabase bağlantı hatası: {e}")
        return {}, []

def load_favorites():
    if FAVORITES_FILE.exists():
        with open(FAVORITES_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_favorites():
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(list(st.session_state.favorites), f)

# Favorileri yükle
if not st.session_state.favorites:
    st.session_state.favorites = load_favorites()

# ----------------------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ----------------------------------------------------------------------

def calculate_signal_score(indicators):
    """Sinyal gücü skoru hesapla (1-100)"""
    score = 50  # Başlangıç
    
    rsi = indicators.get('rsi', 50)
    adx = indicators.get('adx', 25)
    
    # ADX katkısı (güçlü trend = yüksek skor)
    if adx < 20:
        score += 20
    elif adx < 25:
        score += 15
    elif adx < 30:
        score += 10
    
    # RSI katkısı (aşırı bölgeler = yüksek skor)
    if rsi > 60 or rsi < 40:
        score += 15
    if rsi > 65 or rsi < 35:
        score += 10
    
    # VWAP yakınlığı
    close = indicators.get('close', 0)
    vwap = indicators.get('vwap', 0)
    if close and vwap:
        diff_pct = abs((close - vwap) / vwap * 100)
        if diff_pct < 0.5:
            score += 15
        elif diff_pct < 1:
            score += 10
    
    return min(100, max(0, score))

def format_score_badge(score):
    """Skor badge'i formatla"""
    if score >= 70:
        return f'<span class="score-high">⭐ {score}</span>'
    elif score >= 50:
        return f'<span class="score-medium">🟡 {score}</span>'
    else:
        return f'<span class="score-low">🔴 {score}</span>'

def format_signal_badge(signal):
    """Sinyal badge'i formatla"""
    badges = {
        'LONG_ENTRY': '<span class="signal-long">📈 LONG</span>',
        'SHORT_ENTRY': '<span class="signal-short">📉 SHORT</span>',
        'LONG_EXIT': '<span class="signal-exit-long">🚪 LONG ÇIKIŞ</span>',
        'SHORT_EXIT': '<span class="signal-exit-short">🚪 SHORT ÇIKIŞ</span>'
    }
    return badges.get(signal, signal)

def format_pnl(pnl):
    """Kar/Zarar formatla"""
    if pnl > 0:
        return f'<span class="profit">+{pnl:.2f}%</span>'
    else:
        return f'<span class="loss">{pnl:.2f}%</span>'

def toggle_favorite(symbol):
    """Favorilere ekle/çıkar"""
    if symbol in st.session_state.favorites:
        st.session_state.favorites.remove(symbol)
    else:
        st.session_state.favorites.add(symbol)
    save_favorites()

def calculate_summary(closed_trades):
    """Özet istatistikler"""
    if not closed_trades:
        return {
            'total': 0, 'winning': 0, 'losing': 0,
            'win_rate': 0, 'total_pnl': 0, 'avg_pnl': 0,
            'best_trade': None, 'worst_trade': None
        }
    
    winning = [t for t in closed_trades if t['pnl_percent'] > 0]
    losing = [t for t in closed_trades if t['pnl_percent'] <= 0]
    total_pnl = sum(t['pnl_percent'] for t in closed_trades)
    
    best = max(closed_trades, key=lambda x: x['pnl_percent'])
    worst = min(closed_trades, key=lambda x: x['pnl_percent'])
    
    return {
        'total': len(closed_trades),
        'winning': len(winning),
        'losing': len(losing),
        'win_rate': (len(winning) / len(closed_trades)) * 100,
        'total_pnl': total_pnl,
        'avg_pnl': total_pnl / len(closed_trades),
        'best_trade': best,
        'worst_trade': worst
    }

# ----------------------------------------------------------------------
# ANA DASHBOARD
# ----------------------------------------------------------------------

def main():
    # Header
    mode_emoji = "🌙" if st.session_state.dark_mode else "☀️"
    st.markdown(f'<h1 class="main-header">{mode_emoji} KRİPTO SİNYAL TAKİP SİSTEMİ PRO</h1>', unsafe_allow_html=True)
    
    # Strateji Seçimi
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        strategy_options = {
            "HYBRID": "🌊 Hibrit Gün İçi Momentum Stratejisi",
            "ELLIOTT": "🌊 Elliott Dalga & Fibonacci Stratejisi"
        }
        
        selected_strategy = st.selectbox(
            "📊 Aktif Strateji Seçin:",
            options=list(strategy_options.keys()),
            format_func=lambda x: strategy_options[x],
            index=0 if st.session_state.strategy_mode == "HYBRID" else 1,
            key="strategy_selector"
        )
        
        if selected_strategy != st.session_state.strategy_mode:
            st.session_state.strategy_mode = selected_strategy
            # Strateji değişikliği için scanner'ı yeniden başlat
            st.warning("⚠️ Strateji değişikliği için sistem yeniden başlatılmalı!")
            if st.button("🔄 Sistemi Yeniden Başlat", type="primary"):
                st.success("✅ Strateji değiştirildi! Lütfen scanner'ı manuel olarak yeniden başlatın.")
                st.rerun()
        
        # Strateji açıklaması
        if st.session_state.strategy_mode == "HYBRID":
            st.info("🎯 **Hibrit Strateji**: VWAP + ADX + RSI ile gün içi momentum takibi")
        else:
            st.info("🌊 **Elliott Strateji**: Fibonacci retracement + SMA trend filtresi ile swing trading")
    
    # Veri yükle
    signals = load_signals()
    open_trades, closed_trades = load_trades()
    summary = calculate_summary(closed_trades)
    
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
        
        # Dark Mode Toggle
        if st.button(f"{mode_emoji} {'Light' if st.session_state.dark_mode else 'Dark'} Mode", width='stretch'):
            toggle_dark_mode()
            st.rerun()
        
        st.markdown("---")
        
        # Yenileme ayarları
        refresh_interval = st.slider("Otomatik Yenileme (saniye)", 5, 60, 10)
        
        st.markdown("---")
        st.subheader("📊 Performans Özeti")
        
        # KPI Kartları
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Toplam İşlem", summary['total'])
            st.metric("Kazanan", summary['winning'], delta=f"{summary['win_rate']:.1f}%")
        with col2:
            st.metric("Kaybeden", summary['losing'])
            st.metric("Toplam P/L", f"{summary['total_pnl']:.2f}%", 
                     delta=f"{summary['avg_pnl']:.2f}% Ort.")
        
        if summary['best_trade']:
            st.success(f"🏆 En İyi: {summary['best_trade']['symbol']} (+{summary['best_trade']['pnl_percent']:.2f}%)")
        if summary['worst_trade']:
            st.error(f"📉 En Kötü: {summary['worst_trade']['symbol']} ({summary['worst_trade']['pnl_percent']:.2f}%)")
        
        st.markdown("---")
        st.metric("Canlı Sinyal", len(signals))
        st.metric("Açık Pozisyon", len(open_trades))
        st.metric("⭐ Favoriler", len(st.session_state.favorites))
        
        st.markdown("---")
        st.info(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        
        if st.button("🔄 Manuel Yenile", width='stretch'):
            st.rerun()
    
    # Ana içerik
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔔 Canlı Sinyaller", 
        "⭐ Favoriler",
        "📊 Açık İşlemler", 
        "📋 Kapalı İşlemler",
        "📈 Analitik"
    ])
    
    # ===== SEKME 1: CANLI SİNYALLER =====
    with tab1:
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            search_term = st.text_input("🔍 Sembol Ara", placeholder="BTC, ETH, SOL...")
        
        with col2:
            signal_filter = st.selectbox("Sinyal Türü", 
                ["Tümü", "LONG_ENTRY", "SHORT_ENTRY", "LONG_EXIT", "SHORT_EXIT"])
        
        with col3:
            min_score = st.slider("Min. Skor", 0, 100, 0)
        
        st.subheader(f"🔔 Aktif Sinyaller ({len(signals)} adet)")
        
        if signals:
            # Filtreleme
            filtered_signals = {}
            for symbol, data in signals.items():
                # Arama filtresi
                if search_term and search_term.upper() not in symbol:
                    continue
                
                # Sinyal türü filtresi
                if signal_filter != "Tümü" and data['signal'] != signal_filter:
                    continue
                
                # Skor filtresi
                score = calculate_signal_score(data)
                if score < min_score:
                    continue
                
                filtered_signals[symbol] = data
            
            if filtered_signals:
                # Tablo
                signal_data = []
                for symbol, data in sorted(filtered_signals.items(), 
                                          key=lambda x: x[1]['timestamp'], reverse=True):
                    score = calculate_signal_score(data)
                    is_fav = "⭐" if symbol in st.session_state.favorites else "☆"
                    
                    signal_data.append({
                        'Fav': is_fav,
                        'Sembol': symbol,
                        'Sinyal': format_signal_badge(data['signal']),
                        'Skor': format_score_badge(score),
                        'Fiyat': f"${data['price']:.6f}",
                        'RSI': f"{data.get('rsi', 0):.1f}",
                        'ADX': f"{data.get('adx', 0):.1f}",
                        'Mesaj': data['message'],
                        'Zaman': datetime.fromisoformat(data['timestamp']).strftime('%H:%M:%S')
                    })
                
                df_signals = pd.DataFrame(signal_data)
                st.markdown(df_signals.to_html(escape=False, index=False), unsafe_allow_html=True)
                
                # Favorilere ekleme butonları
                st.markdown("---")
                cols = st.columns(5)
                for idx, symbol in enumerate(list(filtered_signals.keys())[:5]):
                    with cols[idx % 5]:
                        is_fav = symbol in st.session_state.favorites
                        btn_text = f"{'⭐' if is_fav else '☆'} {symbol[:6]}"
                        if st.button(btn_text, key=f"fav_{symbol}"):
                            toggle_favorite(symbol)
                            st.rerun()
            else:
                st.warning("🔍 Filtreye uygun sinyal bulunamadı.")
        else:
            st.info("📭 Henüz sinyal bulunmuyor.")
    
    # ===== SEKME 2: FAVORİLER =====
    with tab2:
        st.subheader(f"⭐ Favori Coinler ({len(st.session_state.favorites)} adet)")
        
        if st.session_state.favorites:
            fav_data = []
            for symbol in sorted(st.session_state.favorites):
                if symbol in signals:
                    data = signals[symbol]
                    score = calculate_signal_score(data)
                    fav_data.append({
                        'Sembol': symbol,
                        'Sinyal': format_signal_badge(data['signal']),
                        'Skor': format_score_badge(score),
                        'Fiyat': f"${data['price']:.6f}",
                        'RSI': f"{data.get('rsi', 0):.1f}",
                        'ADX': f"{data.get('adx', 0):.1f}",
                        'Zaman': datetime.fromisoformat(data['timestamp']).strftime('%H:%M:%S')
                    })
            
            if fav_data:
                df_fav = pd.DataFrame(fav_data)
                st.markdown(df_fav.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.info("Favori coinlerde henüz sinyal yok.")
            
            # Favorilerden çıkar
            if st.button("🗑️ Tüm Favorileri Temizle"):
                st.session_state.favorites.clear()
                save_favorites()
                st.rerun()
        else:
            st.info("⭐ Henüz favori eklenm emiş. Canlı Sinyaller sekmesinden yıldıza tıklayarak ekleyebilirsiniz.")
    
    # ===== SEKME 3: AÇIK İŞLEMLER =====
    with tab3:
        st.subheader(f"📊 Açık Pozisyonlar ({len(open_trades)} adet)")
        
        if open_trades:
            open_data = []
            for symbol, trade in sorted(open_trades.items()):
                entry_time = datetime.fromisoformat(trade['entry_time'])
                duration = datetime.now(entry_time.tzinfo) - entry_time
                is_fav = "⭐" if symbol in st.session_state.favorites else ""
                
                open_data.append({
                    'Fav': is_fav,
                    'Sembol': symbol,
                    'Tip': '📈 LONG' if trade['type'] == 'LONG' else '📉 SHORT',
                    'Giriş Fiyatı': f"${trade['entry_price']:.6f}",
                    'Giriş Zamanı': entry_time.strftime('%Y-%m-%d %H:%M'),
                    'Süre': str(duration).split('.')[0],
                    'Durum': '🟢 AÇIK'
                })
            
            df_open = pd.DataFrame(open_data)
            st.dataframe(df_open, width='stretch', hide_index=True)
        else:
            st.success("✅ Açık pozisyon bulunmuyor.")
    
    # ===== SEKME 4: KAPALI İŞLEMLER =====
    with tab3:
        st.subheader(f"📋 İşlem Geçmişi ({len(closed_trades)} adet)")
        
        if closed_trades:
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_type = st.selectbox("Tip Filtrele", ["Tümü", "LONG", "SHORT"], key="close_type")
            with col2:
                filter_result = st.selectbox("Sonuç", ["Tümü", "Kazanan", "Kaybeden"], key="close_result")
            with col3:
                days_filter = st.selectbox("Zaman", ["Tümü", "Son 24 Saat", "Son 7 Gün"], key="close_days")
            
            # Filtreleme
            filtered_trades = closed_trades
            if filter_type != "Tümü":
                filtered_trades = [t for t in filtered_trades if t['type'] == filter_type]
            if filter_result == "Kazanan":
                filtered_trades = [t for t in filtered_trades if t['pnl_percent'] > 0]
            elif filter_result == "Kaybeden":
                filtered_trades = [t for t in filtered_trades if t['pnl_percent'] <= 0]
            
            if days_filter != "Tümü":
                days = 1 if days_filter == "Son 24 Saat" else 7
                cutoff = datetime.now(tz=datetime.now().astimezone().tzinfo) - timedelta(days=days)
                filtered_trades = [t for t in filtered_trades 
                                  if datetime.fromisoformat(t['exit_time']) > cutoff]
            
            # Tablo
            closed_data = []
            for trade in reversed(filtered_trades):
                entry_time = datetime.fromisoformat(trade['entry_time'])
                exit_time = datetime.fromisoformat(trade['exit_time'])
                duration = exit_time - entry_time
                
                closed_data.append({
                    'Sembol': trade['symbol'],
                    'Tip': '📈 LONG' if trade['type'] == 'LONG' else '📉 SHORT',
                    'Giriş': f"${trade['entry_price']:.6f}",
                    'Çıkış': f"${trade['exit_price']:.6f}",
                    'Kar/Zarar': format_pnl(trade['pnl_percent']),
                    'Süre': str(duration).split('.')[0],
                    'Kapanış': exit_time.strftime('%Y-%m-%d %H:%M')
                })
            
            if closed_data:
                df_closed = pd.DataFrame(closed_data)
                st.markdown(df_closed.to_html(escape=False, index=False), unsafe_allow_html=True)
                
                # İndirme
                csv = df_closed.to_csv(index=False).encode('utf-8')
                st.download_button("📥 CSV İndir", csv, "trade_history.csv", "text/csv")
            else:
                st.warning("Filtreye uygun işlem yok.")
        else:
            st.info("📭 Henüz kapalı işlem yok.")
    
    # ===== SEKME 5: ANALİTİK =====
    with tab4:
        st.subheader("📈 Performans Analizi")
        
        if closed_trades:
            # Grafikler (önceki gibi)
            df_analytics = pd.DataFrame(closed_trades)
            df_analytics['exit_time'] = pd.to_datetime(df_analytics['exit_time'])
            df_analytics = df_analytics.sort_values('exit_time')
            df_analytics['cumulative_pnl'] = df_analytics['pnl_percent'].cumsum()
            
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Kümülatif Kar/Zarar', 'İşlem Dağılımı', 
                               'PnL Dağılımı', 'Tip Bazında Performans'),
                specs=[[{"type": "scatter"}, {"type": "pie"}],
                       [{"type": "histogram"}, {"type": "bar"}]]
            )
            
            fig.add_trace(
                go.Scatter(x=df_analytics['exit_time'], 
                          y=df_analytics['cumulative_pnl'],
                          mode='lines+markers',
                          name='Kümülatif PnL',
                          line=dict(color='#1f77b4', width=2)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Pie(labels=['Kazanan', 'Kaybeden'],
                      values=[summary['winning'], summary['losing']],
                      marker=dict(colors=['#28a745', '#dc3545'])),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Histogram(x=df_analytics['pnl_percent'],
                            name='PnL Dağılımı',
                            marker=dict(color='#17a2b8')),
                row=2, col=1
            )
            
            long_pnl = df_analytics[df_analytics['type'] == 'LONG']['pnl_percent'].sum()
            short_pnl = df_analytics[df_analytics['type'] == 'SHORT']['pnl_percent'].sum()
            
            fig.add_trace(
                go.Bar(x=['LONG', 'SHORT'],
                      y=[long_pnl, short_pnl],
                      marker=dict(color=['#28a745', '#dc3545'])),
                row=2, col=2
            )
            
            fig.update_layout(height=800, showlegend=False)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("📊 Yeterli veri yok.")
    
    # Otomatik yenileme
    time.sleep(refresh_interval)
    st.rerun()

if __name__ == "__main__":
    main()


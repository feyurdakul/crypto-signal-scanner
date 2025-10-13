# -*- coding: utf-8 -*-
"""
Kripto Sinyal Dashboard - Streamlit Arayüzü
Canlı sinyaller, açık/kapalı işlemler, kar/zarar takibi
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime
import threading
import time

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kripto Sinyal Takip",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .signal-long {
        background-color: #28a745;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .signal-short {
        background-color: #dc3545;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .signal-exit-long {
        background-color: #ffc107;
        color: black;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .signal-exit-short {
        background-color: #17a2b8;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .profit {
        color: #28a745;
        font-weight: bold;
    }
    .loss {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Veri dosyaları
SIGNALS_FILE = Path('trading_signals.json')
TRADES_FILE = Path('trade_history.json')

# ----------------------------------------------------------------------
# VERİ YÜKLEME FONKSİYONLARI
# ----------------------------------------------------------------------

@st.cache_data(ttl=5)
def load_signals():
    """Sinyalleri yükle"""
    if SIGNALS_FILE.exists():
        with open(SIGNALS_FILE, 'r') as f:
            return json.load(f)
    return {}

@st.cache_data(ttl=5)
def load_trades():
    """İşlemleri yükle"""
    if TRADES_FILE.exists():
        with open(TRADES_FILE, 'r') as f:
            data = json.load(f)
            return data.get('open', {}), data.get('closed', [])
    return {}, []

def calculate_summary(closed_trades):
    """Özet istatistikler hesapla"""
    if not closed_trades:
        return {
            'total': 0,
            'winning': 0,
            'losing': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_pnl': 0
        }
    
    winning = [t for t in closed_trades if t['pnl_percent'] > 0]
    losing = [t for t in closed_trades if t['pnl_percent'] <= 0]
    total_pnl = sum(t['pnl_percent'] for t in closed_trades)
    
    return {
        'total': len(closed_trades),
        'winning': len(winning),
        'losing': len(losing),
        'win_rate': (len(winning) / len(closed_trades)) * 100,
        'total_pnl': total_pnl,
        'avg_pnl': total_pnl / len(closed_trades)
    }

# ----------------------------------------------------------------------
# GÖRSEL YARDIMCI FONKSİYONLAR
# ----------------------------------------------------------------------

def format_signal_badge(signal):
    """Sinyal badge'i formatla"""
    if signal == 'LONG_ENTRY':
        return '<span class="signal-long">📈 LONG</span>'
    elif signal == 'SHORT_ENTRY':
        return '<span class="signal-short">📉 SHORT</span>'
    elif signal == 'LONG_EXIT':
        return '<span class="signal-exit-long">🚪 LONG ÇIKIŞ</span>'
    elif signal == 'SHORT_EXIT':
        return '<span class="signal-exit-short">🚪 SHORT ÇIKIŞ</span>'
    return signal

def format_pnl(pnl):
    """Kar/Zarar formatla"""
    if pnl > 0:
        return f'<span class="profit">+{pnl:.2f}%</span>'
    else:
        return f'<span class="loss">{pnl:.2f}%</span>'

# ----------------------------------------------------------------------
# ANA DASHBOARD
# ----------------------------------------------------------------------

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 KRİPTO SİNYAL TAKİP SİSTEMİ</h1>', unsafe_allow_html=True)
    
    # Veri yükle
    signals = load_signals()
    open_trades, closed_trades = load_trades()
    summary = calculate_summary(closed_trades)
    
    # Sidebar - Kontroller
    with st.sidebar:
        st.image("https://cryptologos.cc/logos/bitcoin-btc-logo.png", width=100)
        st.title("⚙️ Kontrol Paneli")
        
        refresh_interval = st.slider("Otomatik Yenileme (saniye)", 5, 60, 10)
        
        st.markdown("---")
        st.subheader("📈 Özet İstatistikler")
        st.metric("Toplam İşlem", summary['total'])
        st.metric("Kazanan İşlem", summary['winning'], delta=f"{summary['win_rate']:.1f}% Win Rate")
        st.metric("Kaybeden İşlem", summary['losing'])
        st.metric("Toplam Kar/Zarar", f"{summary['total_pnl']:.2f}%", 
                 delta=f"{summary['avg_pnl']:.2f}% Ortalama")
        
        st.markdown("---")
        st.info(f"🕐 Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
        
        if st.button("🔄 Manuel Yenile", width='stretch'):
            st.rerun()
    
    # Ana içerik - 3 sekme
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔔 Canlı Sinyaller", 
        "📊 Açık İşlemler", 
        "📋 Kapalı İşlemler",
        "📈 Analitik"
    ])
    
    # ===== SEKME 1: CANLI SİNYALLER =====
    with tab1:
        st.subheader(f"🔔 Aktif Sinyaller ({len(signals)} adet)")
        
        if signals:
            # Tabloyu oluştur
            signal_data = []
            for symbol, data in sorted(signals.items(), key=lambda x: x[1]['timestamp'], reverse=True):
                signal_data.append({
                    'Sembol': symbol,
                    'Sinyal': format_signal_badge(data['signal']),
                    'Mesaj': data['message'],
                    'Fiyat': f"${data['price']:.6f}",
                    'RSI': data.get('rsi', '-'),
                    'ADX': data.get('adx', '-'),
                    'VWAP': f"${data.get('vwap', 0):.6f}",
                    'Zaman': datetime.fromisoformat(data['timestamp']).strftime('%H:%M:%S')
                })
            
            df_signals = pd.DataFrame(signal_data)
            
            # HTML tablo olarak göster (badge'ler için)
            st.markdown(df_signals.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("📭 Henüz sinyal bulunmuyor. Tarayıcı aktif mi kontrol edin.")
    
    # ===== SEKME 2: AÇIK İŞLEMLER =====
    with tab2:
        st.subheader(f"📊 Açık Pozisyonlar ({len(open_trades)} adet)")
        
        if open_trades:
            open_data = []
            for symbol, trade in sorted(open_trades.items()):
                entry_time = datetime.fromisoformat(trade['entry_time'])
                duration = datetime.now(entry_time.tzinfo) - entry_time
                
                open_data.append({
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
    
    # ===== SEKME 3: KAPALI İŞLEMLER =====
    with tab3:
        st.subheader(f"📋 İşlem Geçmişi ({len(closed_trades)} adet)")
        
        if closed_trades:
            # Filtreleme
            col1, col2 = st.columns(2)
            with col1:
                filter_type = st.selectbox("Tip Filtrele", ["Tümü", "LONG", "SHORT"])
            with col2:
                filter_result = st.selectbox("Sonuç Filtrele", ["Tümü", "Kazanan", "Kaybeden"])
            
            # Filtrelenmiş veri
            filtered_trades = closed_trades
            if filter_type != "Tümü":
                filtered_trades = [t for t in filtered_trades if t['type'] == filter_type]
            if filter_result == "Kazanan":
                filtered_trades = [t for t in filtered_trades if t['pnl_percent'] > 0]
            elif filter_result == "Kaybeden":
                filtered_trades = [t for t in filtered_trades if t['pnl_percent'] <= 0]
            
            # Tablo
            closed_data = []
            for trade in reversed(filtered_trades):  # En son kapatılanlar üstte
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
            
            df_closed = pd.DataFrame(closed_data)
            st.markdown(df_closed.to_html(escape=False, index=False), unsafe_allow_html=True)
            
            # İndirme butonu
            csv = df_closed.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 CSV İndir",
                csv,
                "trade_history.csv",
                "text/csv",
                key='download-csv'
            )
        else:
            st.info("📭 Henüz kapalı işlem bulunmuyor.")
    
    # ===== SEKME 4: ANALİTİK =====
    with tab4:
        st.subheader("📈 Performans Analizi")
        
        if closed_trades:
            # Zaman içinde kümülatif kar/zarar
            df_analytics = pd.DataFrame(closed_trades)
            df_analytics['exit_time'] = pd.to_datetime(df_analytics['exit_time'])
            df_analytics = df_analytics.sort_values('exit_time')
            df_analytics['cumulative_pnl'] = df_analytics['pnl_percent'].cumsum()
            
            # Grafik
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Kümülatif Kar/Zarar', 'İşlem Dağılımı', 
                               'PnL Dağılımı', 'Tip Bazında Performans'),
                specs=[[{"type": "scatter"}, {"type": "pie"}],
                       [{"type": "histogram"}, {"type": "bar"}]]
            )
            
            # 1. Kümülatif PnL
            fig.add_trace(
                go.Scatter(x=df_analytics['exit_time'], 
                          y=df_analytics['cumulative_pnl'],
                          mode='lines+markers',
                          name='Kümülatif PnL',
                          line=dict(color='#1f77b4', width=2)),
                row=1, col=1
            )
            
            # 2. Kazanan/Kaybeden Pie
            fig.add_trace(
                go.Pie(labels=['Kazanan', 'Kaybeden'],
                      values=[summary['winning'], summary['losing']],
                      marker=dict(colors=['#28a745', '#dc3545'])),
                row=1, col=2
            )
            
            # 3. PnL Histogram
            fig.add_trace(
                go.Histogram(x=df_analytics['pnl_percent'],
                            name='PnL Dağılımı',
                            marker=dict(color='#17a2b8')),
                row=2, col=1
            )
            
            # 4. Tip bazında performans
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
            st.info("📊 Yeterli veri bulunmuyor. İşlemler kapandıkça grafikler görünecek.")
    
    # Otomatik yenileme
    time.sleep(refresh_interval)
    st.rerun()

# ----------------------------------------------------------------------
# ÇALIŞTIR
# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()


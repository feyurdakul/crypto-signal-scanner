'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, TrendingDown, Activity, DollarSign,
  Clock, BarChart3, Globe, Building2, Flag, RefreshCw,
  Search, Star, StarOff, ArrowUpDown, Moon, Sun, X, AlertCircle,
  Copy, Check, ChevronDown, Filter
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Signal {
  id: string;
  symbol: string;
  signal_type: string;
  message: string;
  price: number;
  timestamp: string;
  system: string;
  rsi?: number;
  adx?: number;
}

interface MarketStatus {
  name: string;
  status: string;
  trading_hours: string;
  current_time?: string;
}

export default function Dashboard() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [marketStats, setMarketStats] = useState<any>({});
  const [markets, setMarkets] = useState<Record<string, MarketStatus>>({});
  const [selectedMarket, setSelectedMarket] = useState('ALL');
  const [selectedSystem, setSelectedSystem] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [scannerStatus, setScannerStatus] = useState<string>('checking...');
  const [searchQuery, setSearchQuery] = useState('');
  const [signalScope, setSignalScope] = useState<'ALL' | 'ENTRY' | 'EXIT'>('ALL');
  const [sortBy, setSortBy] = useState<'timestamp' | 'symbol' | 'price'>('timestamp');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');
  const [watchlist, setWatchlist] = useState<Set<string>>(new Set());
  const [darkMode, setDarkMode] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [portfolio, setPortfolio] = useState<any>(null);
  const [openTrades, setOpenTrades] = useState<any[]>([]);
  const [openTradesWithPnl, setOpenTradesWithPnl] = useState<any[]>([]);
  const [closedTrades, setClosedTrades] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'signals' | 'open' | 'closed'>('signals');

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [selectedMarket, selectedSystem]);

  useEffect(() => {
    try {
      const raw = localStorage.getItem('watchlist');
      if (raw) setWatchlist(new Set(JSON.parse(raw)));
    } catch {}
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem('watchlist', JSON.stringify(Array.from(watchlist)));
    } catch {}
  }, [watchlist]);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('darkMode');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const isDark = stored ? stored === 'true' : prefersDark;
      setDarkMode(isDark);
      if (isDark) {
        document.documentElement.classList.add('dark');
      }
    } catch {}
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem('darkMode', String(darkMode));
      if (darkMode) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } catch {}
  }, [darkMode]);

  const fetchData = async () => {
    try {
      const [signalsRes, statsRes, marketsRes, healthRes, portfolioRes, openTradesRes, openTradesWithPnlRes, closedTradesRes] = await Promise.all([
        axios.get(`${API_URL}/api/signals`, {
          params: {
            market: selectedMarket !== 'ALL' ? selectedMarket : undefined,
            system: selectedSystem !== 'ALL' ? selectedSystem : undefined,
            limit: 50
          }
        }),
        axios.get(`${API_URL}/api/signals/stats`),
        axios.get(`${API_URL}/api/markets`),
        axios.get(`${API_URL}/health`),
        axios.get(`${API_URL}/api/portfolio`),
        axios.get(`${API_URL}/api/trades/open`),
        axios.get(`${API_URL}/api/trades/open-with-pnl`),
        axios.get(`${API_URL}/api/trades/closed`)
      ]);

      setSignals(signalsRes.data.signals || []);
      setMarketStats(statsRes.data.stats || {});
      setMarkets(marketsRes.data.markets || {});
      setScannerStatus(healthRes.data.scanner || 'offline');
      setPortfolio(portfolioRes.data.portfolio || null);
      setOpenTrades(openTradesRes.data.trades || []);
      setOpenTradesWithPnl(openTradesWithPnlRes.data.trades || []);
      setClosedTrades(closedTradesRes.data.trades || []);
      setLoading(false);
      setRefreshing(false);
      setError(null);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(axios.isAxiosError(error) ? 'Network error - Unable to connect to API' : 'An unexpected error occurred');
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
  };

  const toggleWatchlist = (symbol: string) => {
    setWatchlist(prev => {
      const next = new Set(prev);
      if (next.has(symbol)) next.delete(symbol); else next.add(symbol);
      return next;
    });
  };

  const copySignal = (signal: Signal) => {
    const text = `${signal.symbol} - ${signal.signal_type} @ $${signal.price.toFixed(6)} - ${signal.system}`;
    navigator.clipboard.writeText(text);
    setCopiedId(signal.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredSortedSignals = (() => {
    let data = signals.slice();
    if (signalScope === 'ENTRY') {
      data = data.filter(s => s.signal_type.includes('ENTRY'));
    } else if (signalScope === 'EXIT') {
      data = data.filter(s => s.signal_type.includes('EXIT'));
    }
    const q = searchQuery.trim().toLowerCase();
    if (q) {
      data = data.filter(s => s.symbol.toLowerCase().includes(q));
    }
    data.sort((a, b) => {
      let cmp = 0;
      if (sortBy === 'timestamp') {
        cmp = new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
      } else if (sortBy === 'symbol') {
        cmp = a.symbol.localeCompare(b.symbol);
      } else {
        cmp = (a.price || 0) - (b.price || 0);
      }
      return sortDir === 'asc' ? cmp : -cmp;
    });
    if (watchlist.size > 0) {
      data.sort((a, b) => {
        const ai = watchlist.has(a.symbol) ? 0 : 1;
        const bi = watchlist.has(b.symbol) ? 0 : 1;
        if (ai !== bi) return ai - bi;
        return 0;
      });
    }
    return data;
  })();

  const kpi = (() => {
    const total = signals.length;
    const entries = signals.filter(s => s.signal_type.includes('ENTRY')).length;
    const exits = signals.filter(s => s.signal_type.includes('EXIT')).length;
    const longEntries = signals.filter(s => s.signal_type.includes('LONG_ENTRY')).length;
    const shortEntries = signals.filter(s => s.signal_type.includes('SHORT_ENTRY')).length;
    return { total, entries, exits, longEntries, shortEntries };
  })();

  const getSignalBadgeClass = (signalType: string) => {
    if (signalType.includes('LONG_ENTRY')) return 'bg-emerald-500 text-white';
    if (signalType.includes('SHORT_ENTRY')) return 'bg-rose-500 text-white';
    if (signalType.includes('LONG_EXIT')) return 'bg-amber-500 text-white';
    if (signalType.includes('SHORT_EXIT')) return 'bg-sky-500 text-white';
    return 'bg-gray-500 text-white';
  };

  const getSystemBadge = (system: string) => {
    if (system.includes('HYBRID')) {
      return <span className="px-2 py-0.5 text-xs font-bold rounded bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-sm">HYBRID</span>;
    }
    if (system.includes('ELLIOTT')) {
      return <span className="px-2 py-0.5 text-xs font-bold rounded bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-sm">ELLIOTT</span>;
    }
    return null;
  };

  const getMarketBadge = (market: string) => {
    const colors: Record<string, string> = {
      'CRYPTO': 'bg-gradient-to-r from-purple-500 to-pink-500',
      'BIST': 'bg-gradient-to-r from-red-500 to-orange-500',
      'US': 'bg-gradient-to-r from-blue-600 to-indigo-600'
    };
    return <span className={`px-2 py-0.5 text-xs font-bold rounded ${colors[market] || 'bg-gray-500'} text-white shadow-sm`}>{market}</span>;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      <AnimatePresence>
        {error && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-gradient-to-r from-red-500 to-rose-600 border-b border-red-600 px-4 py-3 shadow-lg"
          >
            <div className="max-w-7xl mx-auto flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-white" />
                <span className="text-sm font-medium text-white">{error}</span>
              </div>
              <button 
                onClick={() => setError(null)} 
                className="text-white hover:text-red-100 transition-colors"
                aria-label="Dismiss error"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="bg-gradient-to-r from-slate-800 via-slate-700 to-slate-800 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 border-b border-slate-600 dark:border-slate-700 shadow-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl shadow-lg">
                <BarChart3 className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent">SIGNAL ▶ START</h1>
                <p className="text-xs text-slate-300">Professional Trading Signals</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 transition-colors border border-slate-600"
                aria-label="Toggle dark mode"
              >
                {darkMode ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-slate-300" />}
              </button>
              <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg border ${
                scannerStatus === 'online' 
                  ? 'bg-emerald-500/20 border-emerald-500/50' 
                  : 'bg-rose-500/20 border-rose-500/50'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  scannerStatus === 'online' ? 'bg-emerald-400 animate-pulse shadow-lg shadow-emerald-500/50' : 'bg-rose-400'
                }`}></div>
                <span className={`text-xs font-bold ${
                  scannerStatus === 'online' ? 'text-emerald-300' : 'text-rose-300'
                }`}>
                  {scannerStatus.toUpperCase()}
                </span>
              </div>
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg hover:from-blue-700 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg font-medium text-sm"
              >
                <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-6">
          {/* Total Balance */}
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl p-4 shadow-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-blue-100 uppercase">Balance</span>
              <DollarSign className="w-4 h-4 text-white" />
            </div>
            <div className="text-2xl font-bold text-white">${portfolio?.total_balance?.toFixed(2) || '1000.00'}</div>
            <div className="text-xs text-blue-100 mt-1">Current Capital</div>
          </motion.div>

          {/* Available Balance */}
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl p-4 shadow-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-green-100 uppercase">Available</span>
              <DollarSign className="w-4 h-4 text-white" />
            </div>
            <div className="text-2xl font-bold text-white">${portfolio?.available_balance?.toFixed(2) || '1000.00'}</div>
            <div className="text-xs text-green-100 mt-1">Free Capital</div>
          </motion.div>

          {/* Open Positions */}
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl p-4 shadow-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-amber-100 uppercase">In Use</span>
              <Activity className="w-4 h-4 text-white" />
            </div>
            <div className="text-2xl font-bold text-white">${portfolio?.used_balance?.toFixed(2) || '0.00'}</div>
            <div className="text-xs text-amber-100 mt-1">{openTrades.length} Positions</div>
          </motion.div>

          {/* Total PnL */}
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className={`bg-gradient-to-br ${(portfolio?.total_pnl || 0) >= 0 ? 'from-emerald-500 to-green-600' : 'from-rose-500 to-red-600'} rounded-xl p-4 shadow-lg`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-white uppercase">Total P&L</span>
              <TrendingUp className="w-4 h-4 text-white" />
            </div>
            <div className="text-2xl font-bold text-white">${portfolio?.total_pnl?.toFixed(2) || '0.00'}</div>
            <div className="text-xs text-white mt-1">{((portfolio?.total_pnl || 0) / 1000 * 100).toFixed(2)}% ROI</div>
          </motion.div>

          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl p-4 shadow-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-emerald-100 uppercase">Long Entries</span>
              <TrendingUp className="w-4 h-4 text-white" />
            </div>
            <div className="text-2xl font-bold text-white">{kpi.longEntries}</div>
            <div className="text-xs text-emerald-100 mt-1">Buy Signals</div>
          </motion.div>

          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-rose-500 to-red-600 rounded-xl p-4 shadow-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-rose-100 uppercase">Short Entries</span>
              <TrendingDown className="w-4 h-4 text-white" />
            </div>
            <div className="text-2xl font-bold text-white">{kpi.shortEntries}</div>
            <div className="text-xs text-rose-100 mt-1">Sell Signals</div>
          </motion.div>
        </div>

        {/* Search & Filters */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 p-4 mb-6">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <input
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search signals..."
                  className="w-full pl-10 pr-4 py-2.5 rounded-lg border-2 border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 text-sm font-medium outline-none focus:border-blue-500 dark:focus:border-blue-400 transition-colors"
                />
                <Search className="w-5 h-5 text-slate-400 absolute left-3 top-2.5" />
              </div>
            </div>

            {/* Info Badge */}
            <div className="flex items-center gap-2">
              <div className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-xs font-bold">
                CRYPTO
              </div>
              <div className="px-4 py-2 rounded-lg bg-gradient-to-r from-orange-500 to-amber-500 text-white text-xs font-bold">
                HYBRID
              </div>
            </div>

            {/* Signal Type Filter */}
            <div className="flex items-center gap-2">
              {['ALL', 'ENTRY', 'EXIT'].map(scope => (
                <button
                  key={scope}
                  onClick={() => setSignalScope(scope as any)}
                  className={`px-3 py-2 rounded-lg text-xs font-bold transition-all ${
                    signalScope === scope
                      ? 'bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 shadow-lg'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
                  }`}
                >
                  {scope}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 mb-6">
          <div className="flex border-b border-slate-200 dark:border-slate-700">
            <button
              onClick={() => setActiveTab('signals')}
              className={`flex-1 px-6 py-4 text-sm font-bold transition-colors ${
                activeTab === 'signals'
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700'
              }`}
            >
              Signals ({signals.length})
            </button>
            <button
              onClick={() => setActiveTab('open')}
              className={`flex-1 px-6 py-4 text-sm font-bold transition-colors ${
                activeTab === 'open'
                  ? 'bg-emerald-600 text-white'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700'
              }`}
            >
              Open Positions ({openTradesWithPnl.length})
            </button>
            <button
              onClick={() => setActiveTab('closed')}
              className={`flex-1 px-6 py-4 text-sm font-bold transition-colors ${
                activeTab === 'closed'
                  ? 'bg-slate-600 text-white'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700'
              }`}
            >
              Closed Trades ({closedTrades.length})
            </button>
          </div>
        </div>

        {/* Content based on active tab */}
        {activeTab === 'signals' && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="bg-gradient-to-r from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 px-6 py-4 border-b border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-white uppercase tracking-wide">Trading Signals</h2>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Real-time market opportunities</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-slate-600 dark:text-slate-400">
                  Showing <span className="text-blue-600 dark:text-blue-400 font-bold">{filteredSortedSignals.length}</span> signals
                </span>
              </div>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="relative">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-slate-200 dark:border-slate-700"></div>
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-t-blue-600 border-r-transparent border-b-transparent border-l-transparent absolute top-0 left-0"></div>
              </div>
            </div>
          ) : filteredSortedSignals.length === 0 ? (
            <div className="text-center py-20">
              <Activity className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
              <p className="text-lg font-semibold text-slate-600 dark:text-slate-400">No signals found</p>
              <p className="text-sm text-slate-500 dark:text-slate-500 mt-2">Try adjusting your filters</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-100 dark:bg-slate-900 border-b-2 border-slate-200 dark:border-slate-700">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider w-12">Rank</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Symbol</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Signal</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">System</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Market</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Price</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Time</th>
                    <th className="text-center px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider w-24">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {filteredSortedSignals.map((s, idx) => {
                    const isWatched = watchlist.has(s.symbol);
                    const market = s.system.split('_')[1] || 'CRYPTO';
                    return (
                      <motion.tr 
                        key={s.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.02 }}
                        className={`hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors ${isWatched ? 'bg-amber-50 dark:bg-amber-900/10' : ''}`}
                      >
                        <td className="px-4 py-4">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-bold text-slate-400 dark:text-slate-500">{idx + 1}</span>
                            <button 
                              onClick={() => toggleWatchlist(s.symbol)} 
                              className="hover:scale-110 transition-transform"
                              aria-label="Toggle watchlist"
                            >
                              {isWatched ? (
                                <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
                              ) : (
                                <StarOff className="w-4 h-4 text-slate-300 dark:text-slate-600" />
                              )}
                            </button>
                          </div>
                        </td>
                        <td className="px-4 py-4">
                          <span className="text-sm font-bold text-slate-900 dark:text-white">{s.symbol}</span>
                        </td>
                        <td className="px-4 py-4">
                          <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${getSignalBadgeClass(s.signal_type)} shadow-sm`}>
                            {s.signal_type.replace('_', ' ')}
                          </span>
                        </td>
                        <td className="px-4 py-4">
                          {getSystemBadge(s.system)}
                        </td>
                        <td className="px-4 py-4">
                          {getMarketBadge(market)}
                        </td>
                        <td className="px-4 py-4 text-right">
                          <span className="text-sm font-bold text-slate-900 dark:text-white">${s.price.toFixed(6)}</span>
                        </td>
                        <td className="px-4 py-4">
                          <span className="text-xs text-slate-500 dark:text-slate-400">
                            {new Date(s.timestamp).toLocaleString('en-US', { 
                              month: 'short', 
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <button
                            onClick={() => copySignal(s)}
                            className="inline-flex items-center gap-1 px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-xs font-bold transition-colors shadow-sm"
                          >
                            {copiedId === s.id ? (
                              <>
                                <Check className="w-3 h-3" />
                                <span>Copied</span>
                              </>
                            ) : (
                              <>
                                <Copy className="w-3 h-3" />
                                <span>Copy</span>
                              </>
                            )}
                          </button>
                        </td>
                      </motion.tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
        )}

        {activeTab === 'open' && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="bg-gradient-to-r from-slate-50 to-emerald-50 dark:from-slate-900 dark:to-slate-800 px-6 py-4 border-b border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-white uppercase tracking-wide">Open Positions</h2>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Active trading positions</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-slate-600 dark:text-slate-400">
                  Showing <span className="text-emerald-600 dark:text-emerald-400 font-bold">{openTradesWithPnl.length}</span> positions
                </span>
              </div>
            </div>
          </div>

          {openTradesWithPnl.length === 0 ? (
            <div className="text-center py-20">
              <Activity className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
              <p className="text-lg font-semibold text-slate-600 dark:text-slate-400">No open positions</p>
              <p className="text-sm text-slate-500 dark:text-slate-500 mt-2">Positions will appear here when trades are opened</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-100 dark:bg-slate-900 border-b-2 border-slate-200 dark:border-slate-700">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Symbol</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Type</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Entry Price</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Current Price</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Position Size</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Leverage</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">P&L %</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">P&L USD</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Entry Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {openTradesWithPnl.map((trade, idx) => (
                    <motion.tr 
                      key={trade.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.02 }}
                      className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="px-4 py-4">
                        <span className="text-sm font-bold text-slate-900 dark:text-white">{trade.symbol}</span>
                      </td>
                      <td className="px-4 py-4">
                        <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                          trade.type === 'LONG' ? 'bg-emerald-500 text-white' : 'bg-rose-500 text-white'
                        } shadow-sm`}>
                          {trade.type}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="text-sm font-bold text-slate-900 dark:text-white">${parseFloat(trade.entry_price).toFixed(6)}</span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="text-sm font-bold text-slate-900 dark:text-white">
                          {trade.current_price ? `$${trade.current_price.toFixed(6)}` : '--'}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="text-sm font-bold text-slate-900 dark:text-white">${trade.position_size?.toFixed(2) || '50.00'}</span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="text-sm font-bold text-slate-900 dark:text-white">{trade.leverage || 5}x</span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className={`text-sm font-bold ${(trade.pnl_percent || 0) >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {trade.current_price ? `${trade.pnl_percent?.toFixed(2) || '0.00'}%` : '--'}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className={`text-sm font-bold ${(trade.pnl_usd || 0) >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {trade.current_price ? `$${trade.pnl_usd?.toFixed(2) || '0.00'}` : '--'}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <span className="text-xs text-slate-500 dark:text-slate-400">
                          {new Date(trade.entry_time).toLocaleString('en-US', { 
                            month: 'short', 
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        )}

        {activeTab === 'closed' && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="bg-gradient-to-r from-slate-50 to-slate-50 dark:from-slate-900 dark:to-slate-800 px-6 py-4 border-b border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-white uppercase tracking-wide">Closed Trades</h2>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Completed trading history</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-slate-600 dark:text-slate-400">
                  Showing <span className="text-slate-600 dark:text-slate-400 font-bold">{closedTrades.length}</span> trades
                </span>
              </div>
            </div>
          </div>

          {closedTrades.length === 0 ? (
            <div className="text-center py-20">
              <Activity className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
              <p className="text-lg font-semibold text-slate-600 dark:text-slate-400">No closed trades</p>
              <p className="text-sm text-slate-500 dark:text-slate-500 mt-2">Trade history will appear here when positions are closed</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-100 dark:bg-slate-900 border-b-2 border-slate-200 dark:border-slate-700">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Symbol</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Type</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Entry Price</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Exit Price</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">P&L %</th>
                    <th className="text-right px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">P&L USD</th>
                    <th className="text-left px-4 py-3 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Duration</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {closedTrades.slice(0, 50).map((trade, idx) => {
                    const entryTime = new Date(trade.entry_time);
                    const exitTime = new Date(trade.exit_time);
                    const duration = exitTime.getTime() - entryTime.getTime();
                    const hours = Math.floor(duration / (1000 * 60 * 60));
                    const minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
                    
                    return (
                      <motion.tr 
                        key={`${trade.symbol}-${trade.exit_time}`}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.02 }}
                        className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                      >
                        <td className="px-4 py-4">
                          <span className="text-sm font-bold text-slate-900 dark:text-white">{trade.symbol}</span>
                        </td>
                        <td className="px-4 py-4">
                          <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                            trade.type === 'LONG' ? 'bg-emerald-500 text-white' : 'bg-rose-500 text-white'
                          } shadow-sm`}>
                            {trade.type}
                          </span>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <span className="text-sm font-bold text-slate-900 dark:text-white">${parseFloat(trade.entry_price).toFixed(6)}</span>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <span className="text-sm font-bold text-slate-900 dark:text-white">${parseFloat(trade.exit_price).toFixed(6)}</span>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <span className={`text-sm font-bold ${(trade.pnl_percent || 0) >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                            {(trade.pnl_percent || 0).toFixed(2)}%
                          </span>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <span className={`text-sm font-bold ${(trade.pnl_usd || 0) >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                            ${(trade.pnl_usd || 0).toFixed(2)}
                          </span>
                        </td>
                        <td className="px-4 py-4">
                          <span className="text-xs text-slate-500 dark:text-slate-400">
                            {hours}h {minutes}m
                          </span>
                        </td>
                      </motion.tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
        )}

        {/* Footer Info */}
        <div className="mt-6 text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Auto-refreshing every 5 seconds • Last update: {new Date().toLocaleTimeString()}
          </p>
        </div>
      </div>
    </div>
  );
}

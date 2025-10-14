'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, TrendingDown, Activity, DollarSign,
  Clock, BarChart3, Globe, Building2, Flag, RefreshCw,
  Search, Star, StarOff, ArrowUpDown
} from 'lucide-react';
import { motion } from 'framer-motion';

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
  const [selectedMarket, setSelectedMarket] = useState('CRYPTO');
  const [selectedSystem, setSelectedSystem] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [scannerStatus, setScannerStatus] = useState<string>('checking...');
  const [searchQuery, setSearchQuery] = useState('');
  const [signalScope, setSignalScope] = useState<'ALL' | 'ENTRY' | 'EXIT'>('ALL');
  const [sortBy, setSortBy] = useState<'timestamp' | 'symbol' | 'price'>('timestamp');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');
  const [watchlist, setWatchlist] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Her 5 saniyede güncelle
    return () => clearInterval(interval);
  }, [selectedMarket, selectedSystem]);

  // Load watchlist from localStorage
  useEffect(() => {
    try {
      const raw = localStorage.getItem('watchlist');
      if (raw) setWatchlist(new Set(JSON.parse(raw)));
    } catch {}
  }, []);

  // Persist watchlist
  useEffect(() => {
    try {
      localStorage.setItem('watchlist', JSON.stringify(Array.from(watchlist)));
    } catch {}
  }, [watchlist]);

  const fetchData = async () => {
    try {
      const [signalsRes, statsRes, marketsRes, healthRes] = await Promise.all([
        axios.get(`${API_URL}/api/signals`, {
          params: {
            market: selectedMarket !== 'ALL' ? selectedMarket : undefined,
            system: selectedSystem !== 'ALL' ? selectedSystem : undefined,
            limit: 20
          }
        }),
        axios.get(`${API_URL}/api/signals/stats`),
        axios.get(`${API_URL}/api/markets`),
        axios.get(`${API_URL}/health`)
      ]);

      setSignals(signalsRes.data.signals || []);
      setMarketStats(statsRes.data.stats || {});
      setMarkets(marketsRes.data.markets || {});
      setScannerStatus(healthRes.data.scanner || 'offline');
      setLoading(false);
      setRefreshing(false);
    } catch (error) {
      console.error('Error fetching data:', error);
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

  const filteredSortedSignals = (() => {
    let data = signals.slice();
    // scope
    if (signalScope === 'ENTRY') {
      data = data.filter(s => s.signal_type.includes('ENTRY'));
    } else if (signalScope === 'EXIT') {
      data = data.filter(s => s.signal_type.includes('EXIT'));
    }
    // search
    const q = searchQuery.trim().toLowerCase();
    if (q) {
      data = data.filter(s => s.symbol.toLowerCase().includes(q));
    }
    // sort
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
    // pin watchlist symbols to top
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
    return { total, entries, exits };
  })();

  const getSignalColor = (signalType: string) => {
    if (signalType.includes('LONG_ENTRY')) return 'text-green-600 bg-green-50 border-green-200';
    if (signalType.includes('SHORT_ENTRY')) return 'text-red-600 bg-red-50 border-red-200';
    if (signalType.includes('LONG_EXIT')) return 'text-orange-600 bg-orange-50 border-orange-200';
    if (signalType.includes('SHORT_EXIT')) return 'text-blue-600 bg-blue-50 border-blue-200';
    return 'text-gray-600 bg-gray-50 border-gray-200';
  };

  const getSystemBadge = (system: string) => {
    if (system.includes('HYBRID')) {
      return <span className="px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">HYBRID</span>;
    }
    if (system.includes('ELLIOTT')) {
      return <span className="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">ELLIOTT</span>;
    }
    return null;
  };

  const getMarketIcon = (market: string) => {
    switch (market) {
      case 'CRYPTO': return <Globe className="w-5 h-5" />;
      case 'BIST': return <Building2 className="w-5 h-5" />;
      case 'US': return <Flag className="w-5 h-5" />;
      default: return <Activity className="w-5 h-5" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">Trading Signal Dashboard</h1>
                <p className="text-sm text-slate-500">Real-time market analysis</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg ${
                scannerStatus === 'online' ? 'bg-green-50' : 'bg-red-50'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  scannerStatus === 'online' ? 'bg-green-500 animate-pulse' : 'bg-red-500'
                }`}></div>
                <span className={`text-sm font-medium ${
                  scannerStatus === 'online' ? 'text-green-700' : 'text-red-700'
                }`}>
                  Scanner: {scannerStatus}
                </span>
              </div>
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span className="text-sm font-medium">Yenile</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Market Tabs + KPIs */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            {['CRYPTO', 'BIST', 'US'].map(m => (
              <button
                key={m}
                onClick={() => setSelectedMarket(m)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium border ${selectedMarket === m ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'}`}
              >
                <span className="inline-flex items-center space-x-1">
                  {getMarketIcon(m)}
                  <span>{m}</span>
                </span>
              </button>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-white rounded-lg border border-slate-200 p-3">
              <div className="text-xs text-slate-500">Signals</div>
              <div className="text-lg font-semibold text-slate-900">{kpi.total}</div>
            </div>
            <div className="bg-white rounded-lg border border-slate-200 p-3">
              <div className="text-xs text-slate-500">Entries</div>
              <div className="text-lg font-semibold text-green-700">{kpi.entries}</div>
            </div>
            <div className="bg-white rounded-lg border border-slate-200 p-3">
              <div className="text-xs text-slate-500">Exits</div>
              <div className="text-lg font-semibold text-slate-700">{kpi.exits}</div>
            </div>
          </div>
        </div>

        {/* Filters Bar */}
        <div className="bg-white border border-slate-200 rounded-lg p-3 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div className="flex-1 flex items-center gap-2">
              <div className="relative w-full md:max-w-sm">
                <input
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search symbol..."
                  className="w-full pl-9 pr-3 py-2 rounded-md border border-slate-300 text-sm outline-none focus:ring-2 focus:ring-blue-200"
                />
                <Search className="w-4 h-4 text-slate-400 absolute left-2.5 top-2.5" />
              </div>
              <div className="flex items-center gap-2">
                {['ALL', 'ENTRY', 'EXIT'].map(scope => (
                  <button
                    key={scope}
                    onClick={() => setSignalScope(scope as any)}
                    className={`px-3 py-1.5 rounded-md text-sm border ${signalScope === scope ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}`}
                  >{scope}</button>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => { setSortBy('timestamp'); setSortDir(sortBy === 'timestamp' && sortDir === 'desc' ? 'asc' : 'desc'); }}
                className={`px-3 py-1.5 rounded-md text-sm border ${sortBy === 'timestamp' ? 'border-blue-600 text-blue-700' : 'border-slate-300 text-slate-700 hover:bg-slate-50'}`}
                title="Sort by time"
              >
                <span className="inline-flex items-center gap-1">Time <ArrowUpDown className="w-4 h-4" /></span>
              </button>
              <button
                onClick={() => { setSortBy('symbol'); setSortDir(sortBy === 'symbol' && sortDir === 'asc' ? 'desc' : 'asc'); }}
                className={`px-3 py-1.5 rounded-md text-sm border ${sortBy === 'symbol' ? 'border-blue-600 text-blue-700' : 'border-slate-300 text-slate-700 hover:bg-slate-50'}`}
                title="Sort by symbol"
              >
                <span className="inline-flex items-center gap-1">Symbol <ArrowUpDown className="w-4 h-4" /></span>
              </button>
              <button
                onClick={() => { setSortBy('price'); setSortDir(sortBy === 'price' && sortDir === 'asc' ? 'desc' : 'asc'); }}
                className={`px-3 py-1.5 rounded-md text-sm border ${sortBy === 'price' ? 'border-blue-600 text-blue-700' : 'border-slate-300 text-slate-700 hover:bg-slate-50'}`}
                title="Sort by price"
              >
                <span className="inline-flex items-center gap-1">Price <ArrowUpDown className="w-4 h-4" /></span>
              </button>
            </div>
          </div>
        </div>

        {/* System Filter */}
        <div className="flex items-center gap-2 mb-4">
          <span className="text-sm text-slate-600">System:</span>
          {['ALL', 'HYBRID', 'ELLIOTT'].map((system) => (
            <button
              key={system}
              onClick={() => setSelectedSystem(system)}
              className={`px-3 py-1.5 rounded-md text-sm border ${
                selectedSystem === system
                  ? 'bg-blue-600 text-white border-blue-600'
                  : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
              }`}
            >
              {system}
            </button>
          ))}
        </div>

        {/* Signals Table */}
        <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
          <div className="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-700">Live Signals ({filteredSortedSignals.length})</h2>
            <span className="text-xs text-slate-500">Sorted by {sortBy} · {sortDir}</span>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : filteredSortedSignals.length === 0 ? (
            <div className="text-center py-12">
              <Activity className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p className="text-slate-500">No signals for current filters.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                  <tr>
                    <th className="text-left px-4 py-2 w-10"></th>
                    <th className="text-left px-4 py-2">Time</th>
                    <th className="text-left px-4 py-2">Symbol</th>
                    <th className="text-left px-4 py-2">Type</th>
                    <th className="text-left px-4 py-2">System</th>
                    <th className="text-left px-4 py-2">Price</th>
                    <th className="text-left px-4 py-2">Message</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSortedSignals.map((s) => {
                    const isEntryLong = s.signal_type.includes('LONG_ENTRY');
                    const isEntryShort = s.signal_type.includes('SHORT_ENTRY');
                    const isExit = s.signal_type.includes('EXIT');
                    const rowColor = isEntryLong
                      ? 'text-green-700'
                      : isEntryShort
                      ? 'text-red-700'
                      : 'text-slate-700';
                    return (
                      <tr key={s.id} className="border-b last:border-0 hover:bg-slate-50">
                        <td className="px-4 py-2">
                          <button onClick={() => toggleWatchlist(s.symbol)} aria-label="Toggle watchlist">
                            {watchlist.has(s.symbol) ? (
                              <Star className="w-4 h-4 text-amber-500" />
                            ) : (
                              <StarOff className="w-4 h-4 text-slate-400" />
                            )}
                          </button>
                        </td>
                        <td className="px-4 py-2 text-slate-600">{new Date(s.timestamp).toLocaleString()}</td>
                        <td className="px-4 py-2 font-semibold text-slate-900">{s.symbol}</td>
                        <td className={`px-4 py-2 font-medium ${rowColor}`}>{s.signal_type.replace('_', ' ')}</td>
                        <td className="px-4 py-2">
                          {getSystemBadge(s.system)}
                        </td>
                        <td className="px-4 py-2">
                          <span className="inline-flex items-center gap-1 text-slate-800"><DollarSign className="w-3 h-3" />{s.price.toFixed(6)}</span>
                        </td>
                        <td className="px-4 py-2 max-w-[420px] truncate text-slate-600" title={s.message}>{s.message}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


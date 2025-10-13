'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, TrendingDown, Activity, DollarSign, 
  Clock, BarChart3, Globe, Building2, Flag 
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

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Her 5 saniyede güncelle
    return () => clearInterval(interval);
  }, [selectedMarket, selectedSystem]);

  const fetchData = async () => {
    try {
      const [signalsRes, statsRes, marketsRes] = await Promise.all([
        axios.get(`${API_URL}/api/signals`, {
          params: {
            market: selectedMarket !== 'ALL' ? selectedMarket : undefined,
            system: selectedSystem !== 'ALL' ? selectedSystem : undefined,
            limit: 20
          }
        }),
        axios.get(`${API_URL}/api/signals/stats`),
        axios.get(`${API_URL}/api/markets`)
      ]);

      setSignals(signalsRes.data.signals || []);
      setMarketStats(statsRes.data.stats || {});
      setMarkets(marketsRes.data.markets || {});
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">Trading Signal Dashboard</h1>
                <p className="text-sm text-slate-500">Real-time market analysis</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-2 px-3 py-1.5 bg-green-50 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-green-700">Live</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Market Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {Object.entries(markets).map(([key, market]) => (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-6 rounded-xl border-2 cursor-pointer transition-all ${
                selectedMarket === key
                  ? 'bg-blue-50 border-blue-300 shadow-lg'
                  : 'bg-white border-slate-200 hover:border-blue-200'
              }`}
              onClick={() => setSelectedMarket(key)}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  {getMarketIcon(key)}
                  <h3 className="font-semibold text-slate-900">{market.name}</h3>
                </div>
                <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                  market.status === 'open' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {market.status.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-slate-600 mb-1">{market.trading_hours}</p>
              {market.current_time && (
                <p className="text-xs text-slate-500">Current: {market.current_time}</p>
              )}
              <div className="mt-3 pt-3 border-t border-slate-200">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-600">Hybrid:</span>
                  <span className="font-semibold text-orange-600">
                    {marketStats[key]?.HYBRID || 0}
                  </span>
                </div>
                <div className="flex justify-between text-sm mt-1">
                  <span className="text-slate-600">Elliott:</span>
                  <span className="font-semibold text-blue-600">
                    {marketStats[key]?.ELLIOTT || 0}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* System Filter */}
        <div className="flex space-x-2 mb-6">
          {['ALL', 'HYBRID', 'ELLIOTT'].map((system) => (
            <button
              key={system}
              onClick={() => setSelectedSystem(system)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                selectedSystem === system
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-white text-slate-700 hover:bg-slate-50 border border-slate-200'
              }`}
            >
              {system}
            </button>
          ))}
        </div>

        {/* Signals Grid */}
        <div className="space-y-3">
          <h2 className="text-xl font-bold text-slate-900 mb-4">
            Live Signals ({signals.length})
          </h2>
          
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : signals.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-xl border border-slate-200">
              <Activity className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p className="text-slate-500">No signals yet. Waiting for market conditions...</p>
            </div>
          ) : (
            signals.map((signal, index) => (
              <motion.div
                key={signal.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`p-5 rounded-xl border-2 ${getSignalColor(signal.signal_type)}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-bold">{signal.symbol}</h3>
                      {getSystemBadge(signal.system)}
                      <span className="text-sm font-semibold">
                        {signal.signal_type.replace('_', ' ')}
                      </span>
                    </div>
                    <p className="text-sm mb-3">{signal.message}</p>
                    <div className="flex items-center space-x-4 text-sm">
                      <div className="flex items-center space-x-1">
                        <DollarSign className="w-4 h-4" />
                        <span className="font-semibold">${signal.price.toFixed(6)}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{new Date(signal.timestamp).toLocaleString()}</span>
                      </div>
                      {signal.rsi && (
                        <span>RSI: {signal.rsi.toFixed(1)}</span>
                      )}
                      {signal.adx && (
                        <span>ADX: {signal.adx.toFixed(1)}</span>
                      )}
                    </div>
                  </div>
                  {signal.signal_type.includes('LONG') ? (
                    <TrendingUp className="w-8 h-8" />
                  ) : (
                    <TrendingDown className="w-8 h-8" />
                  )}
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}


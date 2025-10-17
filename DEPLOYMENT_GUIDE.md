# Crypto Scanner - Deployment Guide

## Project Overview
This is a cryptocurrency signal scanning application that:
- Scans all USDT pairs on Binance every 10 minutes
- Applies a hybrid intraday trading strategy (VWAP + ADX + RSI)
- Stores signals and trades in Supabase
- Provides a FastAPI backend and Next.js frontend

## Deployment Architecture
- **Backend**: FastAPI app running on Railway (scans crypto signals every 10 minutes)
- **Frontend**: Next.js app running on Vercel (displays signals and performance)
- **Database**: Supabase (stores signals, trades, and portfolio data)

## Backend Deployment on Railway

### Step 1: Prepare Your Railway Account
1. Create a Railway account at https://railway.app
2. Install the Railway CLI (optional): `npm install -g @railway/cli`

### Step 2: Setup Supabase Database
1. Create a Supabase account at https://supabase.io
2. Create a new project
3. Note down your PROJECT URL and ANON KEY

### Step 3: Configure Database Tables
Execute these SQL commands in your Supabase SQL editor:

```sql
-- Crypto signals table
CREATE TABLE crypto_signals (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(20) NOT NULL,
  signal_type VARCHAR(20) NOT NULL,
  message TEXT,
  price DECIMAL(20, 10),
  rsi DECIMAL(5, 2),
  adx DECIMAL(5, 2),
  vwap DECIMAL(20, 10),
  atr DECIMAL(20, 10),
  system VARCHAR(50),
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Open trades table  
CREATE TABLE open_trades (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(20) NOT NULL,
  trade_type VARCHAR(10) NOT NULL,
  entry_price DECIMAL(20, 10),
  entry_time TIMESTAMPTZ DEFAULT NOW(),
  status VARCHAR(20) DEFAULT 'OPEN',
  atr_value DECIMAL(20, 10),
  stop_loss DECIMAL(20, 10),
  take_profit DECIMAL(20, 10),
  position_size DECIMAL(10, 2) DEFAULT 50.0,
  leverage INTEGER DEFAULT 5,
  system VARCHAR(50)
);

-- Closed trades table
CREATE TABLE closed_trades (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(20) NOT NULL,
  trade_type VARCHAR(10) NOT NULL,
  entry_price DECIMAL(20, 10),
  entry_time TIMESTAMPTZ,
  exit_price DECIMAL(20, 10),
  exit_time TIMESTAMPTZ DEFAULT NOW(),
  pnl_percent DECIMAL(8, 2),
  pnl_usd DECIMAL(10, 2),
  position_size DECIMAL(10, 2) DEFAULT 50.0,
  leverage INTEGER DEFAULT 5,
  status VARCHAR(20) DEFAULT 'CLOSED',
  system VARCHAR(50)
);

-- Portfolio state table
CREATE TABLE portfolio_state (
  id SERIAL PRIMARY KEY,
  total_balance DECIMAL(15, 2) DEFAULT 1000.0,
  available_balance DECIMAL(15, 2) DEFAULT 1000.0,
  used_balance DECIMAL(15, 2) DEFAULT 0.0,
  total_pnl DECIMAL(15, 2) DEFAULT 0.0
);
```

### Step 4: Deploy to Railway
1. Push this code to a GitHub repository
2. Connect your GitHub repo to Railway
3. Add these environment variables in Railway:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key
   - `SCAN_INTERVAL`: 600 (for 10-minute intervals, optional)
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `bash start_railway.sh`
6. Deploy the application

### Step 5: Verify Backend
1. Access your Railway deployment URL
2. Check the health endpoint: `https://your-app.railway.app/health`
3. Verify the scanner is running by checking the heartbeat

## Frontend Deployment on Vercel

### Step 1: Prepare Your Vercel Account
1. Create a Vercel account at https://vercel.com
2. Fork or push the repository containing the frontend

### Step 2: Deploy Frontend
1. Go to Vercel Dashboard → Add New Project
2. Import your GitHub repository
3. Change directory to `frontend` in the settings
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., https://your-app.railway.app)
5. Deploy the project

### Step 3: Verify Frontend
1. Access your Vercel deployment URL
2. Verify it can fetch data from the backend API
3. Test all dashboard functionality

## Environment Variables Reference

### Backend (Railway)
- `SUPABASE_URL` (required): Your Supabase project URL
- `SUPABASE_KEY` (required): Your Supabase anon key  
- `SCAN_INTERVAL` (optional): Scan interval in seconds (default: 600 for 10 minutes)
- `PORT` (optional): Port number (default: 8000)

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL` (required): Your backend API URL

## API Endpoints

### Backend API
- `GET /` - API root
- `GET /health` - Health check
- `GET /api/signals` - Get trading signals
- `GET /api/signals/stats` - Get signal statistics
- `GET /api/trades/open` - Get open trades
- `GET /api/trades/closed` - Get closed trades
- `GET /api/trades/performance` - Get performance stats
- `GET /api/markets` - Get market info
- `GET /api/portfolio` - Get portfolio state
- `POST /start-scanner` - Manually start scanner
- `POST /close-trade/{symbol}` - Manually close trade (debug)
- `WS /ws` - WebSocket for real-time updates

## Troubleshooting

### Common Issues
1. **Scanner not running**: Check Railway logs for errors
2. **Database connection**: Verify Supabase URL and key
3. **API calls failing**: Check backend URL in frontend
4. **Rate limits**: Reduce pairs in pairs.md if needed
5. **Memory issues**: Optimize the number of pairs being scanned

### Health Checks
- Check `/health` endpoint to verify scanner status
- Look for `heartbeat.json` file to confirm scanning activity
- Monitor Railway logs for any errors

## Maintenance

### Data Cleanup
The system automatically cleans old signals after 7 days. You can adjust this in `supabase_client.py`.

### Performance Monitoring
- Track API response times
- Monitor database query performance
- Check scanner execution times
- Review error logs regularly

## Security Notes

- Store API keys securely using environment variables
- Restrict database access with proper RLS policies if needed
- Use HTTPS for all API communications
- Regularly rotate API keys
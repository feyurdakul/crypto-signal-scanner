# Deployment Instructions for Railway and Vercel

## Backend Deployment on Railway

### Prerequisites
1. Railway account
2. Supabase account and project
3. Binance API keys (optional, for data fetching)

### Steps
1. Create a new Railway project
2. Connect your GitHub repository
3. Set up the following environment variables in Railway:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key
   - `SCAN_INTERVAL`: Interval in seconds (default: 600 for 10 minutes)
   - `PORT`: Port number (default: 8000)

4. Set the start command in Railway to: `bash start_railway.sh`

5. Deploy the application

### Configuration
- The scanner runs continuously every 10 minutes (600 seconds) by default
- All USDT pairs from `pairs.md` file are scanned
- Signals are stored in Supabase database
- The API exposes endpoints for signals, trades and performance data

## Frontend Deployment on Vercel

### Prerequisites
1. Vercel account
2. Backend API URL (from Railway deployment)

### Steps
1. Navigate to `frontend` directory
2. Create a `.env.local` file with the following content:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-app-url.up.railway.app
   ```
3. Push changes to GitHub
4. Import the project in Vercel
5. Make sure the build settings point to the `frontend` directory
6. Environment variables:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL

### API Endpoints Used
- `/api/signals` - Get trading signals
- `/api/signals/stats` - Get signal statistics
- `/api/trades/open` - Get open trades
- `/api/trades/closed` - Get closed trades
- `/api/trades/performance` - Get performance stats
- `/api/markets` - Get market information
- `/api/portfolio` - Get portfolio information
- `/health` - Health check

## Architecture

### Backend (Railway)
- FastAPI server with uvicorn
- Continuous scanning every 10 minutes
- Supabase database integration
- WebSocket support for real-time updates
- Multiple endpoints for data retrieval

### Frontend (Vercel)
- Next.js application
- Real-time data fetching from backend API
- Responsive dashboard interface
- Trading signal visualization
- Performance metrics display

## Environment Variables

### Backend (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SCAN_INTERVAL=600  # 10 minutes in seconds
PORT=8000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=your_backend_url
```

## Troubleshooting

1. **Scanner not running**: Check Railway logs for errors
2. **Database connection issues**: Verify Supabase URL and key
3. **API calls failing**: Ensure backend URL is correct in frontend
4. **Rate limits**: If getting rate limit errors, consider reducing the number of pairs in pairs.md

## Monitoring

The application includes a heartbeat file (`heartbeat.json`) that tracks the last scan time. You can check the health status at the `/health` endpoint.
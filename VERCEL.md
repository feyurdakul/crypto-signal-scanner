# Vercel Deployment Configuration

This project is designed to be deployed on Vercel with the following configuration:

## Frontend (Vercel)
1. Navigate to the `frontend` directory
2. Set the following environment variables in Vercel:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL

## Configuration

### Build Command
```
npm run build
```

### Output Directory
```
.next
```

### Framework
```
Next.js
```

## Environment Variables
- `NEXT_PUBLIC_API_URL`: URL of your deployed backend on Railway (e.g., https://your-app.railway.app)

## API Endpoints Used
The frontend expects the backend to provide these endpoints:
- `GET /api/signals` - Trading signals
- `GET /api/signals/stats` - Signal statistics  
- `GET /api/trades/open` - Open trades
- `GET /api/trades/closed` - Closed trades
- `GET /api/trades/performance` - Performance metrics
- `GET /api/markets` - Market information
- `GET /api/portfolio` - Portfolio data
- `GET /health` - Health check

## Verification Steps
1. Confirm the backend API is deployed and accessible
2. Verify the NEXT_PUBLIC_API_URL is correctly set
3. Deploy the frontend to Vercel
4. Test all functionality after deployment
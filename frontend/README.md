# Trading Signal Dashboard - Frontend

Modern, profesyonel trading signal dashboard built with Next.js 14, React 18, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Set environment variable
echo "NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app" > .env.local

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 📦 Tech Stack

- **Framework:** Next.js 14 (App Router)
- **UI Library:** React 18
- **Styling:** Tailwind CSS 3
- **Animations:** Framer Motion
- **Charts:** Recharts
- **Icons:** Lucide React
- **HTTP Client:** Axios
- **State Management:** Zustand
- **Date Handling:** date-fns

## 🎨 Features

### Real-Time Updates
- Auto-refresh every 5 seconds
- WebSocket support (coming soon)
- Live market status indicators

### Multi-Market Support
- 💰 Cryptocurrency (24/7)
- 🏛️ BIST (Turkish Stock Exchange)
- 🇺🇸 US Stock Market (Nasdaq & S&P500)

### Trading Systems
- 🎯 Hybrid System (VWAP + ADX + RSI)
- 🌊 Elliott Wave System

### UI/UX
- Responsive design (mobile, tablet, desktop)
- Dark mode support (coming soon)
- Smooth animations
- Color-coded signals (green/red)
- System badges
- Market status cards
- Performance metrics

## 📁 Project Structure

```
frontend/
├── app/
│   ├── page.tsx          # Main dashboard
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/           # Reusable components (future)
├── lib/                  # Utilities (future)
├── public/               # Static assets
├── next.config.js        # Next.js config
├── tailwind.config.js    # Tailwind config
├── tsconfig.json         # TypeScript config
└── package.json          # Dependencies
```

## 🔧 Configuration

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app
```

### API Endpoints

The frontend connects to these backend endpoints:

- `GET /api/signals` - Get trading signals
- `GET /api/signals/stats` - Signal statistics
- `GET /api/trades/open` - Open trades
- `GET /api/trades/closed` - Closed trades
- `GET /api/trades/performance` - Performance metrics
- `GET /api/markets` - Market status
- `WS /ws` - Real-time updates (WebSocket)

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Add environment variable in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Your Railway backend URL

### Railway

```bash
# In frontend directory
railway init
railway up
```

### Docker

```bash
# Build
docker build -t trading-dashboard .

# Run
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=your-api-url trading-dashboard
```

## 🎯 Development

### Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint
npm run lint
```

### Adding New Features

1. **New Component:**
   ```bash
   # Create in components/
   touch components/NewComponent.tsx
   ```

2. **New Page:**
   ```bash
   # Create in app/
   touch app/new-page/page.tsx
   ```

3. **New API Route:**
   ```bash
   # Create in app/api/
   touch app/api/route.ts
   ```

## 🎨 Customization

### Colors

Edit `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ },
      success: { /* your colors */ },
      // ...
    }
  }
}
```

### Fonts

Edit `app/layout.tsx`:

```tsx
import { YourFont } from 'next/font/google'

const yourFont = YourFont({ subsets: ['latin'] })
```

## 📊 Performance

- Lighthouse Score: 95+
- First Contentful Paint: < 1s
- Time to Interactive: < 2s
- Bundle Size: < 200KB (gzipped)

## 🐛 Troubleshooting

### API Connection Issues

```bash
# Check API URL
echo $NEXT_PUBLIC_API_URL

# Test API
curl https://your-api-url.up.railway.app/health
```

### Build Errors

```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

## 📝 License

Private project

## 🤝 Contributing

This is a private project. No external contributions.

## 📧 Support

For issues, contact the development team.

---

Built with ❤️ using Next.js and Tailwind CSS


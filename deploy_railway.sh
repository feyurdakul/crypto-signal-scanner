#!/bin/bash
# Deployment script for Railway

echo "🚀 Starting deployment preparation for Railway..."

# Check if required files exist
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

if [ ! -f "backend_api.py" ]; then
    echo "❌ backend_api.py not found"
    exit 1
fi

if [ ! -f "start_railway.sh" ]; then
    echo "❌ start_railway.sh not found"
    exit 1
fi

echo "✅ All required files present"

# Check environment variables
if [ -z "$SUPABASE_URL" ]; then
    echo "⚠️ SUPABASE_URL not set in environment"
else
    echo "✅ SUPABASE_URL is set"
fi

if [ -z "$SUPABASE_KEY" ]; then
    echo "⚠️ SUPABASE_KEY not set in environment"
else
    echo "✅ SUPABASE_KEY is set"
fi

echo "🔧 Deployment preparation complete"
echo "📋 Remember to set these environment variables in Railway:"
echo "   - SUPABASE_URL"
echo "   - SUPABASE_KEY"
echo "   - SCAN_INTERVAL (optional, default: 600)"
echo ""
echo "🔄 The scanner will run every 10 minutes (600 seconds) as configured"
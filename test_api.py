#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test FastAPI Endpoints
"""

import requests
import json

# Railway URL veya local
API_URL = "https://your-railway-url.up.railway.app"  # Railway URL'inizi buraya yazın
# API_URL = "http://localhost:8000"  # Local test için

def test_endpoints():
    """Tüm API endpoint'lerini test et"""
    
    print("🧪 API ENDPOINT TESTLERİ")
    print("="*70)
    print(f"API URL: {API_URL}\n")
    
    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
        ("GET", "/api/signals", "Get all signals"),
        ("GET", "/api/signals?market=CRYPTO&limit=5", "Get crypto signals"),
        ("GET", "/api/signals/stats", "Signal statistics"),
        ("GET", "/api/trades/open", "Open trades"),
        ("GET", "/api/trades/closed?limit=10", "Closed trades"),
        ("GET", "/api/trades/performance", "Performance stats"),
        ("GET", "/api/markets", "Market status"),
    ]
    
    results = []
    
    for method, endpoint, description in endpoints:
        try:
            print(f"Testing: {description}")
            print(f"  {method} {endpoint}")
            
            url = f"{API_URL}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Success - Status: {response.status_code}")
                
                # Önemli bilgileri göster
                if 'count' in data:
                    print(f"     Count: {data['count']}")
                if 'total' in data:
                    print(f"     Total: {data['total']}")
                if 'status' in data:
                    print(f"     Status: {data['status']}")
                
                results.append((description, "✅ PASS", response.status_code))
            else:
                print(f"  ❌ Failed - Status: {response.status_code}")
                results.append((description, "❌ FAIL", response.status_code))
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
            results.append((description, "❌ ERROR", str(e)[:30]))
        
        print()
    
    # Özet
    print("\n" + "="*70)
    print("📊 TEST SONUÇLARI")
    print("="*70)
    
    for desc, status, code in results:
        print(f"{status} {desc} ({code})")
    
    passed = sum(1 for _, status, _ in results if status == "✅ PASS")
    total = len(results)
    
    print(f"\n✅ Başarılı: {passed}/{total}")
    print(f"❌ Başarısız: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
    else:
        print("\n⚠️  Bazı testler başarısız oldu.")

if __name__ == "__main__":
    print("Not: API_URL değişkenini Railway URL'iniz ile güncelleyin!\n")
    test_endpoints()


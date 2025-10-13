"""
Health Check Endpoint
Railway'in uygulamanın çalıştığını kontrol etmesi için
"""

from flask import Flask, jsonify
from datetime import datetime
import threading
import os

app = Flask(__name__)

# Son tarama zamanı
last_scan_time = None

def update_scan_time():
    """Scanner'dan çağrılacak - son tarama zamanını güncelle"""
    global last_scan_time
    last_scan_time = datetime.now()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'scanner_running': last_scan_time is not None,
        'last_scan': last_scan_time.isoformat() if last_scan_time else None
    }
    return jsonify(status), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Crypto Signal Scanner',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    }), 200

def run_health_server(port=8000):
    """Health check server'ı başlat"""
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_health_server()


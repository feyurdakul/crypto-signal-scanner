# -*- coding: utf-8 -*-
"""
Sistem Performans İzleme
"""

import psutil
import time
from datetime import datetime
import json
from pathlib import Path

class PerformanceMonitor:
    """Sistem performansını izler"""

    def __init__(self):
        self.start_time = time.time()
        self.metrics_file = Path('performance_metrics.json')

    def get_system_metrics(self):
        """Sistem metriklerini al"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime_seconds': time.time() - self.start_time,
            'timestamp': datetime.now().isoformat()
        }

    def get_process_metrics(self):
        """Python process metrikleri"""
        process = psutil.Process()
        return {
            'process_cpu': process.cpu_percent(),
            'process_memory': process.memory_info().rss / 1024 / 1024,  # MB
            'threads': process.num_threads(),
            'open_files': len(process.open_files())
        }

    def log_metrics(self):
        """Metrikleri kaydet"""
        try:
            metrics = {
                'system': self.get_system_metrics(),
                'process': self.get_process_metrics()
            }

            # Önceki metrikleri yükle
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(metrics)

            # Sadece son 100 kaydı tut
            if len(data) > 100:
                data = data[-100:]

            with open(self.metrics_file, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Metrik kaydetme hatası: {e}")
            return False

    def get_performance_report(self):
        """Performans raporu oluştur"""
        try:
            if not self.metrics_file.exists():
                return {"error": "Henüz metrik verisi yok"}

            with open(self.metrics_file, 'r') as f:
                data = json.load(f)

            if not data:
                return {"error": "Metrik verisi boş"}

            # Son 10 kaydı analiz et
            recent = data[-10:]

            avg_cpu = sum(m['system']['cpu_percent'] for m in recent) / len(recent)
            avg_memory = sum(m['system']['memory_percent'] for m in recent) / len(recent)
            max_cpu = max(m['system']['cpu_percent'] for m in recent)
            max_memory = max(m['system']['memory_percent'] for m in recent)

            return {
                'average_cpu': round(avg_cpu, 2),
                'average_memory': round(avg_memory, 2),
                'max_cpu': round(max_cpu, 2),
                'max_memory': round(max_memory, 2),
                'total_records': len(data),
                'monitoring_duration': round(data[-1]['system']['uptime_seconds'], 2),
                'status': 'healthy' if avg_cpu < 80 and avg_memory < 80 else 'warning'
            }
        except Exception as e:
            return {"error": f"Analiz hatası: {e}"}

# Tek seferlik kullanım için
monitor = PerformanceMonitor()
monitor.log_metrics()
report = monitor.get_performance_report()
print("🚀 Sistem Performans Raporu:")
print(json.dumps(report, indent=2, ensure_ascii=False))
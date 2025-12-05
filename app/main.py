from flask import Flask,jsonify,request
from prometheus_client import Counter,Gauge,Histogram,Summary,Info,generate_latest,CONTENT_TYPE_LATEST
from functools import wraps
import time
import psutil
import random
import platform
import os

app = Flask(__name__)

# ============================================
# PROMETHEUS METRICS DEFINITIONS
# ============================================

app_info = Info('app','Application information')
app_info.info({
    'version': '1.0.0',
    'name': 'devops-dashboard',
    'python_version': platform.python_version(),
    'platform': platform.system()
})

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint","status"]
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method','endpoint'],
    buckets=[0.01,0.025,0.05,0.1,0.25,0.5,1.0,2.5,5.0,10.0]
)

http_request_size_bytes = Summary(
    'http_request_size_bytes',
    'HTTP request size in bytes',
    ['method','endpoint']
)

http_errors_total = Counter(
    "http_errors_total",
    "Total HTTP Errors",
    ["endpoint","error_type"]
)

active_requests = Gauge(
    'active_requests',
    'Number of requests currently being processed'
)

cpu_usage_percent = Gauge("cpu_usage_percent","CPU Usage Percentage")
cpu_count_total = Gauge("cpu_count_total","Total CPU cores")
cpu_frequency_mhz = Gauge("cpu_frequency_mhz","CPU Frequency in MHz")


memory_usage_bytes = Gauge("memory_usage_bytes","Memory Usage in Bytes")
memory_total_bytes = Gauge("memory_total_bytes","Total Memory in Bytes")
memory_usage_percent = Gauge("memory_usage_percent","Memory Usage Percentage")
memory_available_bytes = Gauge("memory_available_bytes","Available Memory in Bytes")

disk_usage_percent = Gauge("disk_usage_percent","Disk Usage Percentage")
disk_total_bytes = Gauge("disk_total_bytes","Total Disk Space in Bytes")
disk_used_bytes = Gauge("disk_used_bytes","Used Disk Space in Bytes")
disk_free_bytes = Gauge("disk_free_bytes","Free Disk Space in Bytes")

network_bytes_sent = Gauge("network_bytes_sent","Total Network Bytes Sent")
network_bytes_recv = Gauge("network_bytes_recv","Total Network Bytes Received")
network_connections = Gauge("network_connections","Number of Network Connections")

process_cpu_percent = Gauge("process_cpu_percent","Process CPU Percentage")
process_memory_bytes = Gauge("process_memory_bytes","Process Memory Usage in Bytes")
process_threads = Gauge("process_threads","Number of Process Threads")


app_uptime_seconds = Gauge("app_uptime_seconds", "Application Uptime in Seconds")
app_start_time = time.time()

api_calls_by_endpoint = Counter(
    'api_calls_by_endpoint',
    'API calls grouped by endpoint',
    ['endpoint']
)

# ============================================
# MIDDLEWARE - Request Tracking
# ============================================

def track_metrics(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        start_time = time.time()
        method = request.method
        endpoint = request.path
        
        active_requests.inc()
        
        try:
            response = f(*args,**kwargs)
            status = response[1] if isinstance(response, tuple) else 200
            http_requests_total.labels(method=method,endpoint=endpoint,status=status).inc()
            api_calls_by_endpoint.labels(endpoint=endpoint).inc()
            content_length = request.content_length or 0
            http_request_size_bytes.labels(method=method,endpoint=endpoint).observe(content_length)
            
            return response
            
        except Exception as e:
            http_errors_total.labels(endpoint=endpoint,error_type=type(e).__name__).inc()
            http_requests_total.labels(method=method,endpoint=endpoint,status=500).inc()
            raise
            
        finally:
            duration = time.time() - start_time
            http_request_duration_seconds.labels(method=method,endpoint=endpoint).observe(duration)
            active_requests.dec()
    
    return decorated_function


# ============================================
# SYSTEM METRICS UPDATE FUNCTION
# ============================================

def update_system_metrics():
    cpu_usage_percent.set(psutil.cpu_percent(interval=0.1))
    cpu_count_total.set(psutil.cpu_count())
    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            cpu_frequency_mhz.set(cpu_freq.current)
    except:
        pass
    
    mem = psutil.virtual_memory()
    memory_usage_bytes.set(mem.used)
    memory_total_bytes.set(mem.total)
    memory_usage_percent.set(mem.percent)
    memory_available_bytes.set(mem.available)
    
    try:
        disk = psutil.disk_usage('/')
    except:
        disk = psutil.disk_usage('C:')
    disk_usage_percent.set(disk.percent)
    disk_total_bytes.set(disk.total)
    disk_used_bytes.set(disk.used)
    disk_free_bytes.set(disk.free)
    
    net = psutil.net_io_counters()
    network_bytes_sent.set(net.bytes_sent)
    network_bytes_recv.set(net.bytes_recv)
    network_connections.set(len(psutil.net_connections()))
    
    process = psutil.Process()
    process_cpu_percent.set(process.cpu_percent())
    process_memory_bytes.set(process.memory_info().rss)
    process_threads.set(process.num_threads())
    app_uptime_seconds.set(time.time() - app_start_time)


# ============================================
# API ROUTES
# ============================================

@app.route("/")
@track_metrics
def home():
    return jsonify({
        "application": "DevOps Dashboard API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/": "API information",
            "/api/health": "Health check",
            "/api/data": "Sample data endpoint",
            "/api/stats": "System statistics",
            "/api/error": "Error simulation (for testing)",
            "/metrics": "Prometheus metrics"
        }
    }),200


@app.route("/api/health")
@track_metrics
def health():
    mem = psutil.virtual_memory()
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(time.time() - app_start_time, 2),
        "uptime_formatted": format_uptime(time.time() - app_start_time),
        "checks": {
            "cpu": "ok" if psutil.cpu_percent() < 90 else "warning",
            "memory": "ok" if mem.percent < 90 else "warning",
            "disk": "ok"
        }
    }),200


@app.route('/api/data')
@track_metrics
def get_data():
    # Simulate processing time
    delay = random.uniform(0.1,0.5)
    time.sleep(delay)
    
    return jsonify({
        "data": {
            "values": [random.randint(1,100) for _ in range(10)],
            "count": 10,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "processing_time_ms": round(delay * 1000,2),
        "timestamp": time.time()
    }),200


@app.route('/api/stats')
@track_metrics
def get_stats():
    mem = psutil.virtual_memory()
    try:
        disk = psutil.disk_usage('/')
    except:
        disk = psutil.disk_usage('C:')
    
    return jsonify({
        "system": {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "hostname": platform.node(),
            "processor": platform.processor()
        },
        "cpu": {
            "usage_percent": psutil.cpu_percent(),
            "cores": psutil.cpu_count(),
            "physical_cores": psutil.cpu_count(logical=False)
        },
        "memory": {
            "total_gb": round(mem.total/(1024**3),2),
            "used_gb": round(mem.used /(1024**3),2),
            "available_gb": round(mem.available/(1024**3),2),
            "percent": mem.percent
        },
        "disk": {
            "total_gb": round(disk.total/(1024**3),2),
            "used_gb": round(disk.used/(1024**3),2),
            "free_gb": round(disk.free/(1024**3),2),
            "percent": disk.percent
        },
        "application": {
            "uptime_seconds": round(time.time() - app_start_time, 2),
            "uptime_formatted": format_uptime(time.time() - app_start_time),
            "process_id": os.getpid()
        }
    }), 200


@app.route('/api/error')
@track_metrics
def trigger_error():
    error_type = request.args.get('type','general')
    
    if error_type == 'divide':
        result = 1/0
    elif error_type == 'value':
        raise ValueError("Sample value error")
    elif error_type == 'key':
        d = {}
        return d['nonexistent']
    else:
        raise Exception("Sample general error")


@app.route('/metrics')
def metrics():
    update_system_metrics()
    return generate_latest(),200,{'Content-Type': CONTENT_TYPE_LATEST}



def format_uptime(seconds):
    days = int(seconds//86400)
    hours = int((seconds%86400)//3600)
    minutes = int((seconds%3600)//60)
    secs = int(seconds%60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"




if __name__ == '__main__':
    print("=" * 50)
    print("🚀 DevOps Dashboard API")
    print("=" * 50)
    print(f"📊 Metrics: http://localhost:5000/metrics")
    print(f"🏥 Health:  http://localhost:5000/api/health")
    print(f"📈 Stats:   http://localhost:5000/api/stats")
    print("=" * 50)
    app.run(host='0.0.0.0',port=5000,debug=False)

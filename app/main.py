from flask import Flask,jsonify,request
from prometheus_client import Counter,Gauge,Histogram,generate_latest,CONTENT_TYPE_LATEST
from functools import wraps
import time
import psutil
import random

app = Flask(__name__)

#Prometheus Metrics

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method","endpoint","status"]
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_errors_total = Counter(
    "http_errors_total",
    "Total HTTP Errors",
    ["endpoint","error_type"]
)

#System Metrics
cpu_usage = Gauge("cpu_usage_percent","CPU Usage Percentage")
memory_usage_bytes = Gauge("memory_usage_bytes","Memory Usage in Bytes")
disk_usage = Gauge("disk_usage_percent","Disk Usage Percentage")

app_uptime = Gauge("app_uptime_seconds","Application Uptime in Seconds")
app_start_time = time.time()


def track_metrics(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        start_time = time.time()
        method = request.method
        endpoint = request.path
        try:
            response = f(*args,**kwargs)
            status = response[1] if isinstance(response,tuple) else 200
            http_requests_total.labels(method=method,endpoint=endpoint,status=status).inc()
            return response
        except Exception as e:
            http_errors_total.labels(endpoint=endpoint,error_type=type(e).__name__).inc()
            http_requests_total.labels(method=method,endpoint=endpoint,status=500).inc()
            raise
        finally:
            duration = time.time() - start_time
            http_request_duration_seconds.labels(method=method,endpoint=endpoint).observe(duration)
    return decorated_function


def update_system_metrics():
    cpu_usage.set(psutil.cpu_percent(interval=0.1))
    memory_usage_bytes.set(psutil.virtual_memory().used)
    disk_usage.set(psutil.disk_usage('/').percent)
    app_uptime.set(time.time() - app_start_time)
    
@app.route("/")
@track_metrics
def home():
    return jsonify({
        "message": "DevOps Dashboard API",
        "status": "running",
        "version": "1.0.0"
    }),200

@app.route("/api/health")
@track_metrics
def health():
    return jsonify({
        "status": "healthy",
        "uptime_seconds": time.time() - app_start_time
    }),200

@app.route('/api/data')
@track_metrics
def get_data():
    time.sleep(random.uniform(0.1,0.5))
    
    return jsonify({
        "data": [1,2,3,4,5],
        "timestamp": time.time()
    }),200
    
@app.route('/api/error')
@track_metrics
def trigger_error():
    error_type = request.args.get('type','general')
    
    if error_type == 'divide':
        result = 1/0
    elif error_type == 'value':
        raise ValueError("Sample value error")
    else:
        raise Exception("Sample general error")
    
@app.route('/metrics')
def metrics():
    update_system_metrics()
    return generate_latest(),200,{'Content-Type': CONTENT_TYPE_LATEST}
    
    
app.run(host='0.0.0.0',port=5000,debug=True)
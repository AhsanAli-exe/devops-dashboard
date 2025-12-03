# 🚀 DevOps Dashboard - Real-Time Monitoring System

A comprehensive DevOps monitoring dashboard that tracks CI/CD pipeline metrics, application health, and system performance using Flask, Prometheus, and Grafana with automated GitHub Actions workflows.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Prometheus](https://img.shields.io/badge/Prometheus-Latest-orange)
![Grafana](https://img.shields.io/badge/Grafana-Latest-yellow)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-success)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Monitoring Dashboards](#-monitoring-dashboards)
- [API Endpoints](#-api-endpoints)
- [Metrics Reference](#-metrics-reference)
- [Project Structure](#-project-structure)

---

## 🎯 Overview

This project demonstrates a complete DevOps monitoring solution that provides real-time visibility into:

- **Application Performance** - Request rates, response times, error tracking
- **System Resources** - CPU, memory, disk, network usage
- **CI/CD Metrics** - Build success rates, automated testing, pipeline health

The system automatically collects **20+ metrics** every 5 seconds, stores them in Prometheus, and visualizes them through professional Grafana dashboards.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              Flask Application (Port 5000)          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ REST API    │  │ Prometheus  │  │   System    │  │
│  │ Endpoints   │  │  Metrics    │  │  Monitor    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────┬───────────────────────────┘
                          │ HTTP /metrics
                          ▼
┌─────────────────────────────────────────────────────┐
│              Prometheus (Port 9090)                 │
│  • Time-series database                             │
│  • Scrapes every 5 seconds                          │
│  • PromQL query engine                              │
└─────────────────────────┬───────────────────────────┘
                          │ Data Source
                          ▼
┌─────────────────────────────────────────────────────┐
│               Grafana (Port 3000)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Application  │  │   System     │  │  DevOps   │  │
│  │   Health     │  │ Performance  │  │ Overview  │  │
│  └──────────────┘  └──────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              GitHub Actions CI/CD                   │
│  ┌──────────────────┐  ┌───────────────────────┐    │
│  │   CI Pipeline    │  │  Metrics Collection   │    │
│  │ • Linting        │  │ • Workflow tracking   │    │
│  │ • Testing        │  │ • Success rates       │    │
│  │ • Health checks  │  │ • Performance data    │    │
│  └──────────────────┘  └───────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🏥 Application Monitoring
- ✅ Real-time HTTP request tracking by endpoint/method/status
- ✅ Response time histograms with percentile calculations
- ✅ Error rate monitoring with categorization
- ✅ Active request counting
- ✅ Application uptime tracking
- ✅ Request size monitoring

### 💻 System Monitoring
- ✅ CPU usage percentage & core count
- ✅ Memory consumption (total, used, available)
- ✅ Disk space utilization
- ✅ Network I/O (bytes sent/received)
- ✅ Process-level metrics (threads, memory)
- ✅ Network connection count

### 🔄 CI/CD Automation
- ✅ Automated testing on every push
- ✅ Code linting with flake8
- ✅ Flask application health checks
- ✅ Workflow metrics collection
- ✅ Build success/failure tracking

### 📊 Professional Dashboards
- ✅ **Application Health Monitor** - Request rates, latency, uptime
- ✅ **System Performance Monitor** - CPU, memory, disk, network gauges
- ✅ **DevOps Overview Dashboard** - Pipeline health, service status

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.12, Flask 3.0.0 |
| **Metrics** | prometheus-client, psutil |
| **Monitoring** | Prometheus (time-series DB) |
| **Visualization** | Grafana (dashboards) |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, flake8 |

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- Git
- [Prometheus](https://prometheus.io/download/)
- [Grafana](https://grafana.com/grafana/download)

### Step 1: Clone Repository

```bash
git clone https://github.com/AhsanAli-exe/devops-dashboard.git
cd devops-dashboard
```

### Step 2: Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt
```

### Step 3: Start Services

```bash
# Terminal 1: Start Flask App
cd app
python main.py

# Terminal 2: Start Prometheus
cd /path/to/prometheus
./prometheus --config.file=/path/to/devops-dashboard/monitoring/prometheus.yml

# Terminal 3: Start Grafana
cd /path/to/grafana/bin
./grafana-server
```

### Step 4: Configure Grafana

1. Open http://localhost:3000 (login: admin/admin)
2. Add Data Source → Prometheus → URL: `http://localhost:9090`
3. Import dashboards from `monitoring/grafana/dashboards/`

---

## 🚀 Usage

### Start the Application

```bash
cd app
python main.py
```

Output:
```
==================================================
🚀 DevOps Dashboard API
==================================================
📊 Metrics: http://localhost:5000/metrics
🏥 Health:  http://localhost:5000/api/health
📈 Stats:   http://localhost:5000/api/stats
==================================================
```

### Generate Traffic

```bash
python load-test.py
```

This sends ~10 requests/second for 2 minutes to populate dashboards with real data.

### Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| Flask API | http://localhost:5000 | Application |
| Prometheus | http://localhost:9090 | Metrics DB |
| Grafana | http://localhost:3000 | Dashboards |

---

## 🔄 CI/CD Pipeline

### CI Pipeline (`ci.yml`)

**Triggers:** Push to main/master/develop, Pull requests

| Step | Description |
|------|-------------|
| Checkout | Clone repository |
| Setup Python | Install Python 3.12 |
| Cache | Cache pip dependencies |
| Install | Install requirements |
| Lint | Run flake8 code analysis |
| Test | Execute pytest suite |
| Health Check | Start app and verify endpoints |

### Metrics Collection (`metrics.yml`)

**Triggers:** After CI completion, Manual trigger, Scheduled

| Step | Description |
|------|-------------|
| Collect | Fetch workflow data via GitHub API |
| Calculate | Compute success rates |
| Report | Generate metrics summary |

---

## 📊 Monitoring Dashboards

### 1. Application Health Monitor

| Panel | Description |
|-------|-------------|
| App Status | UP/DOWN indicator |
| Total Requests | Cumulative request count |
| Total Errors | Error count with alerting |
| Requests/sec | Current throughput |
| Uptime | Application runtime |
| Request Rate Graph | Time-series by endpoint |
| Response Time (p95) | Latency percentiles |
| Endpoint Distribution | Pie chart of traffic |

### 2. System Performance Monitor

| Panel | Description |
|-------|-------------|
| CPU Gauge | Usage with thresholds |
| Memory Gauge | RAM utilization |
| Disk Gauge | Storage usage |
| Network Connections | Active connections |
| CPU & Memory Graph | Historical trends |
| Network I/O | Bytes sent/received |

### 3. DevOps Overview Dashboard

| Panel | Description |
|-------|-------------|
| App Status | Application health |
| Prometheus Status | Monitoring health |
| Total API Calls | Request counter |
| Error Count | Error monitoring |
| Traffic Distribution | Request breakdown |
| Process Metrics | Memory, threads |

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/api/health` | GET | Health check with system status |
| `/api/data` | GET | Sample data with processing delay |
| `/api/stats` | GET | Detailed system statistics |
| `/api/error` | GET | Error simulation (testing) |
| `/metrics` | GET | Prometheus metrics endpoint |

### Example Responses

**GET /api/health**
```json
{
  "status": "healthy",
  "uptime_seconds": 3600.5,
  "uptime_formatted": "1h 0m 0s",
  "checks": {
    "cpu": "ok",
    "memory": "ok",
    "disk": "ok"
  }
}
```

**GET /api/stats**
```json
{
  "system": {
    "platform": "Windows",
    "hostname": "DevMachine"
  },
  "cpu": {
    "usage_percent": 15.2,
    "cores": 16
  },
  "memory": {
    "total_gb": 16.0,
    "used_gb": 8.5,
    "percent": 53.1
  }
}
```

---

## 📈 Metrics Reference

### Application Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, endpoint, status | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | method, endpoint | Request latency |
| `http_errors_total` | Counter | endpoint, error_type | Error count |
| `active_requests` | Gauge | - | Current active requests |
| `app_uptime_seconds` | Gauge | - | Application uptime |

### System Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `cpu_usage_percent` | Gauge | CPU utilization |
| `cpu_count_total` | Gauge | Number of CPU cores |
| `memory_usage_bytes` | Gauge | Memory used |
| `memory_usage_percent` | Gauge | Memory percentage |
| `disk_usage_percent` | Gauge | Disk utilization |
| `network_bytes_sent` | Gauge | Network TX bytes |
| `network_bytes_recv` | Gauge | Network RX bytes |
| `process_memory_bytes` | Gauge | Process memory |
| `process_threads` | Gauge | Thread count |

---

## 📁 Project Structure

```
devops-dashboard/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline
│       └── metrics.yml         # Metrics collection
├── app/
│   ├── main.py                 # Flask application (200+ lines)
│   ├── test_main.py            # Unit tests (7 tests)
│   └── requirements.txt        # Dependencies
├── monitoring/
│   ├── prometheus.yml          # Prometheus config
│   └── grafana/
│       └── dashboards/
│           ├── application-health.json
│           ├── system-performance.json
│           └── cicd-metrics.json
├── load-test.py                # Load testing script
├── .gitignore
└── README.md
```

---

## 🧪 Testing

```bash
# Run unit tests
cd app
pytest test_main.py -v

# Run linting
flake8 app --max-line-length=127

# Load testing
python load-test.py
```

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Metrics | 20+ |
| Dashboard Panels | 30+ |
| API Endpoints | 6 |
| Unit Tests | 7 |
| CI/CD Workflows | 2 |
| Lines of Code | 1,500+ |

---

## 🎓 DevOps Concepts Demonstrated

1. **Observability** - Full visibility into application behavior
2. **Monitoring** - Real-time metrics collection
3. **CI/CD** - Automated testing pipelines
4. **Infrastructure as Code** - YAML configurations
5. **Time-Series Data** - Prometheus & PromQL
6. **Data Visualization** - Professional dashboards

---

## 👨‍💻 Author

**Ahsan Ali**
- GitHub: [@AhsanAli-exe](https://github.com/AhsanAli-exe)

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**⭐ If you found this project helpful, please give it a star!**

*Built with ❤️ for DevOps learning and demonstration*

# 🚀 DevOps Dashboard - Real-Time Monitoring System

A comprehensive DevOps monitoring dashboard that tracks CI/CD pipeline metrics, application health, and system performance using Flask, Prometheus, and Grafana with automated GitHub Actions workflows.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Prometheus](https://img.shields.io/badge/Prometheus-Latest-orange)
![Grafana](https://img.shields.io/badge/Grafana-Latest-yellow)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-success)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [CI/CD Pipelines](#cicd-pipelines)
- [Monitoring Dashboards](#monitoring-dashboards)
- [Project Structure](#project-structure)
- [Metrics Tracked](#metrics-tracked)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project demonstrates a complete DevOps monitoring solution that provides real-time visibility into:

- **Application Performance** - Request rates, response times, error tracking
- **System Resources** - CPU, memory, disk usage
- **CI/CD Metrics** - Build success rates, deployment frequency, pipeline health

The system automatically collects metrics every 5 seconds, stores them in Prometheus, and visualizes them through beautiful Grafana dashboards.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Flask Application (Port 5000)    │
│   - REST API endpoints              │
│   - Prometheus metrics exporter     │
│   - System monitoring (psutil)      │
└────────────┬────────────────────────┘
             │ HTTP scraping
             ↓
┌─────────────────────────────────────┐
│   Prometheus (Port 9090)            │
│   - Time-series database            │
│   - Metrics collection & storage    │
│   - Query engine (PromQL)           │
└────────────┬────────────────────────┘
             │ Data source
             ↓
┌─────────────────────────────────────┐
│   Grafana (Port 3000)               │
│   - 3 Custom Dashboards             │
│   - Real-time visualization         │
│   - Auto-refresh (5s interval)      │
└─────────────────────────────────────┘
             
             ┌─────────────────────┐
             │  GitHub Actions     │
             │  - CI Pipeline      │
             │  - Deploy Pipeline  │
             │  - Metrics Pipeline │
             └─────────────────────┘
```

---

## ✨ Features

### Application Monitoring
- ✅ Real-time HTTP request tracking
- ✅ Response time measurement (histograms)
- ✅ Error rate monitoring
- ✅ Endpoint-specific metrics
- ✅ Application uptime tracking

### System Monitoring
- ✅ CPU usage percentage
- ✅ Memory consumption
- ✅ Disk space utilization
- ✅ Historical performance graphs

### CI/CD Automation
- ✅ Automated testing on every push
- ✅ Code linting (flake8)
- ✅ Continuous deployment simulation
- ✅ Workflow metrics collection
- ✅ Build success/failure tracking

### Dashboards
- ✅ **Application Health Monitor** - Request rates, latency, uptime
- ✅ **System Performance Monitor** - CPU, memory, disk gauges
- ✅ **CI/CD Metrics Dashboard** - Pipeline health, error tracking

---

## 🛠️ Tech Stack

### Backend
- **Python 3.12** - Application runtime
- **Flask 3.0.0** - Web framework
- **prometheus-client** - Metrics exporter
- **psutil** - System monitoring

### Monitoring & Observability
- **Prometheus** - Metrics collection & storage
- **Grafana** - Data visualization & dashboards

### CI/CD
- **GitHub Actions** - Automated workflows
- **pytest** - Unit testing
- **flake8** - Code linting

### Tools
- **requests** - HTTP client for load testing
- **Docker** (optional) - Container orchestration

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- Git
- Prometheus ([Download](https://prometheus.io/download/))
- Grafana ([Download](https://grafana.com/grafana/download))

### Step 1: Clone the Repository

```bash
git clone https://github.com/AhsanAli-exe/devops-dashboard.git
cd devops-dashboard
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt
```

### Step 3: Configure Prometheus

1. Copy the Prometheus config:
```bash
cp monitoring/prometheus.yml /path/to/prometheus/prometheus.yml
```

2. Start Prometheus:
```bash
prometheus --config.file=prometheus.yml
```

3. Verify at: http://localhost:9090

### Step 4: Start Flask Application

```bash
cd app
python main.py
```

Access the application at: http://localhost:5000

**Available endpoints:**
- `/` - Home endpoint
- `/api/health` - Health check
- `/api/data` - Sample data endpoint
- `/metrics` - Prometheus metrics

### Step 5: Set Up Grafana

1. Start Grafana:
```bash
# Windows:
cd "C:\Program Files\GrafanaLabs\grafana\bin"
.\grafana-server.exe

# Linux/Mac:
grafana-server
```

2. Access Grafana at: http://localhost:3000
   - Default login: `admin` / `admin`

3. Add Prometheus data source:
   - Go to **Configuration** → **Data Sources**
   - Click **Add data source**
   - Select **Prometheus**
   - URL: `http://localhost:9090`
   - Click **Save & Test**

4. Import dashboards:
   - Go to **Create** (+) → **Import**
   - Upload JSON files from `monitoring/grafana/dashboards/`
   - Import all 3 dashboards

---

## 🚀 Usage

### Running the Application

```bash
# Start Flask app
python app/main.py
```

### Load Testing

Generate traffic to populate dashboards:

```bash
python load-test.py
```

This will:
- Send ~10 requests/second
- Run for 2 minutes
- Hit all endpoints randomly
- Display real-time statistics

### Viewing Dashboards

1. **Application Health**: http://localhost:3000/d/app-health
2. **System Performance**: http://localhost:3000/d/system-performance
3. **CI/CD Metrics**: http://localhost:3000/d/cicd-metrics

All dashboards auto-refresh every 5 seconds.

---

## 🔄 CI/CD Pipelines

### 1. CI Pipeline (`ci.yml`)

**Triggers:** Push to main/master/develop, Pull requests

**Steps:**
1. Checkout code
2. Set up Python 3.12
3. Cache dependencies
4. Install requirements
5. Lint with flake8
6. Run pytest tests
7. Test Flask startup
8. Build summary

### 2. Deploy Pipeline (`deploy.yml`)

**Triggers:** Push to main/master

**Steps:**
1. Checkout code
2. Set up Python
3. Pre-deployment checks
4. Simulate deployment
5. Post-deployment verification
6. Health checks
7. Deployment summary

### 3. Metrics Collection (`metrics.yml`)

**Triggers:** After CI/CD completion, Manual trigger

**Steps:**
1. Collect workflow data via GitHub API
2. Calculate success rates
3. Generate CI/CD metrics summary

---

## 📊 Monitoring Dashboards

### Dashboard 1: Application Health Monitor

**Panels:**
- HTTP Request Rate (time series)
- Total HTTP Requests (stat)
- Request Duration - 95th percentile (time series)
- Application Uptime (stat)

**Refresh:** 5 seconds

### Dashboard 2: System Performance Monitor

**Panels:**
- CPU Usage (gauge)
- Disk Usage (gauge)
- Memory Usage (gauge)
- CPU Usage Over Time (time series)

**Refresh:** 5 seconds

### Dashboard 3: CI/CD Metrics Dashboard

**Panels:**
- Request Volume (bar chart)
- Application Status (stat)
- Total Errors (stat)
- Requests by Endpoint (pie chart)

**Refresh:** 5 seconds

---

## 📁 Project Structure

```
devops-dashboard/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline
│       ├── deploy.yml          # Deployment pipeline
│       └── metrics.yml         # Metrics collection
├── app/
│   ├── main.py                 # Flask application
│   ├── test_main.py            # Unit tests
│   └── requirements.txt        # Python dependencies
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

## 📈 Metrics Tracked

### Application Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests by method, endpoint, status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `http_errors_total` | Counter | Total errors by endpoint and type |
| `app_uptime_seconds` | Gauge | Application uptime in seconds |

### System Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `cpu_usage_percent` | Gauge | Current CPU usage percentage |
| `memory_usage_bytes` | Gauge | Current memory usage in bytes |
| `disk_usage_percent` | Gauge | Current disk usage percentage |

### CI/CD Metrics

| Metric | Type | Description |
|--------|------|-------------|
| Workflow runs | Counter | Total workflow executions |
| Success rate | Gauge | Percentage of successful builds |
| Build duration | Histogram | Time taken for builds |

---

## 📸 Screenshots

### Application Health Monitor
Shows real-time request rates, response times, and application uptime.

### System Performance Monitor
Displays CPU, memory, and disk usage with color-coded gauges.

### CI/CD Metrics Dashboard
Tracks pipeline health, error rates, and request distribution.

---

## 🧪 Testing

### Run Unit Tests

```bash
cd app
pytest test_main.py -v
```

### Run Linting

```bash
flake8 app --max-line-length=127
```

### Load Testing

```bash
python load-test.py
```

---

## 🔧 Configuration

### Prometheus Configuration

Edit `monitoring/prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'devops-dashboard-app'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:5000']
```

### Grafana Data Source

- **Type:** Prometheus
- **URL:** http://localhost:9090
- **Access:** Server (default)

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Observability** - Full visibility into application behavior
2. **Monitoring** - Real-time metrics collection and alerting
3. **CI/CD** - Automated testing and deployment pipelines
4. **Infrastructure as Code** - YAML-based workflow definitions
5. **Time-Series Data** - Prometheus query language (PromQL)
6. **Data Visualization** - Professional dashboard design
7. **System Administration** - Service integration and management

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Ahsan Ali**
- GitHub: [@AhsanAli-exe](https://github.com/AhsanAli-exe)
- Project: [DevOps Dashboard](https://github.com/AhsanAli-exe/devops-dashboard)

---

## 🙏 Acknowledgments

- Prometheus community for excellent documentation
- Grafana for beautiful visualization tools
- Flask for the simple yet powerful web framework
- GitHub Actions for seamless CI/CD integration

---

## 📚 References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**⭐ If you found this project helpful, please give it a star!**

---

*Built with ❤️ for DevOps learning and demonstration*


# 🚀 DevOps Dashboard - Real-Time Monitoring System

A comprehensive DevOps monitoring dashboard that tracks **CI/CD pipeline metrics**, **application health**, and **system performance** using Flask, Prometheus, Grafana, and Pushgateway with automated GitHub Actions workflows.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Prometheus](https://img.shields.io/badge/Prometheus-Latest-orange)
![Grafana](https://img.shields.io/badge/Grafana-Latest-yellow)
![Pushgateway](https://img.shields.io/badge/Pushgateway-Enabled-purple)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-success)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Why CI/CD Simulation?](#-why-cicd-simulation)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [CI/CD Pipeline Metrics](#-cicd-pipeline-metrics)
- [Monitoring Dashboards](#-monitoring-dashboards)
- [API Endpoints](#-api-endpoints)
- [Metrics Reference](#-metrics-reference)
- [Project Structure](#-project-structure)

---

## 🎯 Overview

This project demonstrates a **complete DevOps monitoring solution** that provides real-time visibility into:

- **CI/CD Pipeline** - Build success rates, test results, deployment frequency
- **Application Performance** - Request rates, response times, error tracking
- **System Resources** - CPU, memory, disk, network usage

The system automatically collects **30+ metrics** every 5 seconds, stores them in Prometheus, and visualizes them through **4 professional Grafana dashboards**.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                            CLOUD (GitHub)                                │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                     GitHub Actions CI/CD                           │  │
│  │  ┌──────────────────┐        ┌───────────────────────┐            │  │
│  │  │   CI Pipeline    │        │  Metrics Collection   │            │  │
│  │  │ • Linting        │        │ • Workflow tracking   │            │  │
│  │  │ • Testing        │        │ • GitHub API calls    │            │  │
│  │  │ • Health checks  │        │ • Success rates       │            │  │
│  │  └──────────────────┘        └───────────────────────┘            │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
                                    ║
                     ═══════════════╬═══════════════
                        (Cannot directly communicate)
                     ═══════════════╬═══════════════
                                    ║
┌──────────────────────────────────────────────────────────────────────────┐
│                          LOCAL ENVIRONMENT                               │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              Flask Application (Port 5000)                       │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │    │
│  │  │ REST API    │  │ Prometheus  │  │   System    │              │    │
│  │  │ Endpoints   │  │  Metrics    │  │  Monitor    │              │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
│                             │                                            │
│  ┌──────────────────────────┼──────────────────────────────────────┐    │
│  │     CI/CD Metrics        │         Pushgateway (Port 9091)      │    │
│  │     Simulator            │         ┌─────────────────────┐      │    │
│  │  ┌─────────────────┐     │         │ Receives pushed     │      │    │
│  │  │ cicd_metrics.py │─────┼────────▶│ CI/CD metrics       │      │    │
│  │  │ • Build metrics │     │         │ from simulator      │      │    │
│  │  │ • Test results  │     │         └──────────┬──────────┘      │    │
│  │  │ • Deploy stats  │     │                    │                 │    │
│  │  └─────────────────┘     │                    │                 │    │
│  └──────────────────────────┼────────────────────┼─────────────────┘    │
│                             │                    │                      │
│                             ▼                    ▼                      │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                   Prometheus (Port 9090)                         │   │
│  │  • Scrapes Flask app metrics (every 5s)                          │   │
│  │  • Scrapes Pushgateway for CI/CD metrics                         │   │
│  │  • Time-series database with PromQL engine                       │   │
│  └──────────────────────────────┬───────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Grafana (Port 3000)                           │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────┐  │   │
│  │  │ Application  │ │   System     │ │   DevOps     │ │  CI/CD  │  │   │
│  │  │   Health     │ │ Performance  │ │  Overview    │ │Pipeline │  │   │
│  │  │  Dashboard   │ │  Dashboard   │ │  Dashboard   │ │Dashboard│  │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └─────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🤔 Why CI/CD Simulation?

### The Challenge: Cloud vs Local

| Component | Location | Network |
|-----------|----------|---------|
| **GitHub Actions** | Cloud (GitHub servers) | Internet |
| **Prometheus** | Local (your computer) | localhost |
| **Grafana** | Local (your computer) | localhost |

**Problem:** GitHub Actions runs in the **cloud** on GitHub's servers, while Prometheus runs **locally** on your computer. They **cannot directly communicate** because:

1. GitHub Actions has no access to your `localhost`
2. Your local Prometheus is behind your home network/firewall
3. There's no public endpoint for GitHub to push metrics to

### The Solution: CI/CD Metrics Simulator

Instead of trying to bridge the cloud-local gap, we created a **CI/CD Metrics Simulator** (`cicd_metrics.py`) that:

1. **Runs locally** alongside your Flask app
2. **Simulates real CI/CD pipeline behavior:**
   - Build durations (30-180 seconds)
   - Success/failure rates (90% success rate)
   - Test results (passed/failed counts)
   - Deployment frequency
3. **Pushes metrics to Pushgateway** (localhost:9091)
4. **Prometheus scrapes Pushgateway** and stores the metrics
5. **Grafana displays** CI/CD metrics in real-time

### How Real Companies Solve This

In production environments, companies use:
- **Self-hosted Prometheus** with public endpoints
- **Prometheus Cloud** services (Grafana Cloud, AWS Managed Prometheus)
- **Webhook-based systems** that receive data from CI/CD
- **CI/CD-specific tools** (GitLab built-in metrics, Jenkins Prometheus plugin)

Our simulation demonstrates the **same concepts** without requiring cloud infrastructure.

### What the Simulator Tracks

| Metric | Description | Type |
|--------|-------------|------|
| `ci_build_duration_seconds` | How long builds take | Gauge |
| `ci_build_total` | Total builds (success/failure) | Counter |
| `ci_build_success_rate` | Success percentage | Gauge |
| `ci_tests_total` | Number of tests run | Gauge |
| `ci_tests_passed` | Tests that passed | Gauge |
| `ci_tests_failed` | Tests that failed | Gauge |
| `ci_test_duration_seconds` | Test execution time | Gauge |
| `ci_pipeline_runs_total` | Total pipeline executions | Counter |
| `ci_deployments_total` | Deployment count | Counter |

---

## ✨ Features

### 🔄 CI/CD Pipeline Monitoring
- ✅ Build success rate tracking (gauge with thresholds)
- ✅ Build duration monitoring
- ✅ Test results (passed/failed/total)
- ✅ Pipeline run counting
- ✅ Deployment frequency tracking
- ✅ Real-time updates via Pushgateway

### 🏥 Application Monitoring
- ✅ Real-time HTTP request tracking by endpoint/method/status
- ✅ Response time histograms with percentile calculations
- ✅ Error rate monitoring with categorization
- ✅ Active request counting
- ✅ Application uptime tracking

### 💻 System Monitoring
- ✅ CPU usage percentage & core count
- ✅ Memory consumption (total, used, available)
- ✅ Disk space utilization
- ✅ Network I/O (bytes sent/received)
- ✅ Process-level metrics (threads, memory)

### 📊 Professional Dashboards (4 Total)
1. **Application Health Monitor** - Request rates, latency, uptime
2. **System Performance Monitor** - CPU, memory, disk, network gauges
3. **DevOps Overview Dashboard** - Service status, API metrics
4. **CI/CD Pipeline Metrics** - Build success rates, test results, deployments

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.12, Flask 3.0.0 |
| **Metrics** | prometheus-client, psutil |
| **Monitoring** | Prometheus (time-series DB) |
| **Metric Gateway** | Pushgateway (for CI/CD metrics) |
| **Visualization** | Grafana (dashboards) |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, flake8 |

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- Git
- [Prometheus](https://prometheus.io/download/)
- [Pushgateway](https://prometheus.io/download/#pushgateway)
- [Grafana](https://grafana.com/grafana/download)

### Step 1: Clone Repository

```bash
git clone https://github.com/AhsanAli-exe/devops-dashboard.git
cd devops-dashboard
```

### Step 2: Python Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r app/requirements.txt
```

### Step 3: Start All Services (5 Terminals)

```bash
# Terminal 1: Pushgateway
cd C:\pushgateway
.\pushgateway.exe

# Terminal 2: Prometheus
cd C:\prometheus
.\prometheus.exe

# Terminal 3: Flask App
cd devops-dashboard/app
python main.py

# Terminal 4: CI/CD Metrics Simulator
cd devops-dashboard/app
python cicd_metrics.py

# Terminal 5: Grafana
cd "C:\Program Files\GrafanaLabs\grafana\bin"
.\grafana-server.exe
```

### Step 4: Configure Grafana

1. Open http://localhost:3000 (login: admin/admin)
2. Add Data Source → Prometheus → URL: `http://localhost:9090`
3. Import all 4 dashboards from `monitoring/grafana/dashboards/`

---

## 🚀 Usage

### Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| Flask API | http://localhost:5000 | Application |
| Prometheus | http://localhost:9090 | Metrics DB |
| Pushgateway | http://localhost:9091 | CI/CD Metrics |
| Grafana | http://localhost:3000 | Dashboards |

### Verify Prometheus Targets

Go to http://localhost:9090/targets - You should see **3 targets UP:**
- ✅ `devops-dashboard-app` (localhost:5000)
- ✅ `prometheus` (localhost:9090)
- ✅ `pushgateway` (localhost:9091)

### Generate Traffic

```bash
python load-test.py  # Application traffic
python app/cicd_metrics.py  # CI/CD metrics (runs continuously)
```

---

## 🔄 CI/CD Pipeline Metrics

### Real GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push/PR to main | Automated testing, linting, health checks |
| `metrics.yml` | Push to main | Collects workflow data from GitHub API |

### Simulated CI/CD Metrics (Pushgateway)

The `cicd_metrics.py` simulator pushes metrics every 30 seconds:

```
🔄 Simulating CI/CD run #1...
   📦 Build: SUCCESS (45.2s)
   🧪 Tests: 7/7 passed
   🚀 Deploy to production: SUCCESS
   ✅ Metrics pushed to Pushgateway
```

### CI/CD Dashboard Panels

| Panel | Metric | Description |
|-------|--------|-------------|
| Build Success Rate | `ci_build_success_rate` | Gauge showing % (green >90%) |
| Total Builds | `ci_build_total` | Counter with trend |
| Build Duration | `ci_build_duration_seconds` | Time series graph |
| Tests Passed/Failed | `ci_tests_passed`, `ci_tests_failed` | Stats |
| Pipeline Runs | `ci_pipeline_runs_total` | Counter |
| Deployments | `ci_deployments_total` | By environment |

---

## 📊 Monitoring Dashboards

### 1. Application Health Monitor
- Request rate by endpoint
- Response time percentiles (p95)
- Error tracking
- Uptime monitoring
- Traffic distribution pie chart

### 2. System Performance Monitor
- CPU/Memory/Disk gauges with thresholds
- Network I/O graphs
- Process metrics
- Historical trends

### 3. DevOps Overview Dashboard
- Service status (App + Prometheus)
- API call volume
- Error rates
- Quick health overview

### 4. CI/CD Pipeline Metrics ⭐ NEW
- Build success rate gauge
- Build duration trends
- Test pass/fail stats
- Deployment tracking
- Pipeline run counter

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/api/health` | GET | Health check |
| `/api/data` | GET | Sample data |
| `/api/stats` | GET | System statistics |
| `/api/error` | GET | Error simulation |
| `/metrics` | GET | Prometheus metrics |

---

## 📈 Metrics Reference

### CI/CD Metrics (via Pushgateway)

| Metric | Type | Description |
|--------|------|-------------|
| `ci_build_success_rate` | Gauge | Build success percentage |
| `ci_build_total` | Counter | Total builds by status |
| `ci_build_duration_seconds` | Gauge | Build time |
| `ci_tests_total` | Gauge | Tests run |
| `ci_tests_passed` | Gauge | Passed tests |
| `ci_tests_failed` | Gauge | Failed tests |
| `ci_pipeline_runs_total` | Counter | Pipeline executions |
| `ci_deployments_total` | Counter | Deployments |

### Application Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | HTTP requests |
| `http_request_duration_seconds` | Histogram | Latency |
| `http_errors_total` | Counter | Errors |
| `app_uptime_seconds` | Gauge | Uptime |

### System Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `cpu_usage_percent` | Gauge | CPU usage |
| `memory_usage_percent` | Gauge | RAM usage |
| `disk_usage_percent` | Gauge | Disk usage |
| `network_bytes_sent/recv` | Gauge | Network I/O |

---

## 📁 Project Structure

```
devops-dashboard/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # CI pipeline (testing, linting)
│       └── metrics.yml               # GitHub API metrics collection
├── app/
│   ├── main.py                       # Flask application
│   ├── cicd_metrics.py               # CI/CD metrics simulator ⭐
│   ├── test_main.py                  # Unit tests
│   └── requirements.txt              # Dependencies
├── monitoring/
│   ├── prometheus.yml                # Prometheus config (3 targets)
│   └── grafana/
│       └── dashboards/
│           ├── application-health.json
│           ├── system-performance.json
│           ├── cicd-metrics.json
│           └── cicd-pipeline.json    # CI/CD dashboard ⭐
├── load-test.py                      # Load testing script
├── .gitignore
└── README.md
```

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Metrics | 30+ |
| Grafana Dashboards | 4 |
| Dashboard Panels | 40+ |
| API Endpoints | 6 |
| Unit Tests | 7 |
| CI/CD Workflows | 2 |

---

## 🎓 DevOps Concepts Demonstrated

1. **Observability** - Full visibility into application, system, and CI/CD
2. **Monitoring** - Real-time metrics collection with Prometheus
3. **Push vs Pull Metrics** - Pushgateway for ephemeral jobs
4. **CI/CD** - Automated testing with GitHub Actions
5. **Infrastructure as Code** - YAML configurations
6. **Time-Series Data** - Prometheus & PromQL queries
7. **Data Visualization** - Professional Grafana dashboards
8. **Metric Types** - Counters, Gauges, Histograms

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

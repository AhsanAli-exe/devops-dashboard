import time
import random
from prometheus_client import CollectorRegistry,Gauge,Counter,Histogram,push_to_gateway

PUSHGATEWAY_URL = 'localhost:9091'
registry = CollectorRegistry()

# ============================================
# CI/CD METRICS DEFINITIONS
# ============================================
ci_build_duration_seconds = Gauge(
    'ci_build_duration_seconds',
    'Duration of CI build in seconds',
    ['workflow','status'],
    registry=registry
)

ci_build_total = Counter(
    'ci_build_total',
    'Total number of CI builds',
    ['workflow','status'],
    registry=registry
)

ci_build_success_rate = Gauge(
    'ci_build_success_rate',
    'CI build success rate percentage',
    ['workflow'],
    registry=registry
)

# Test metrics
ci_tests_total = Gauge(
    'ci_tests_total',
    'Total number of tests run',
    ['workflow'],
    registry=registry
)

ci_tests_passed = Gauge(
    'ci_tests_passed',
    'Number of tests passed',
    ['workflow'],
    registry=registry
)

ci_tests_failed = Gauge(
    'ci_tests_failed',
    'Number of tests failed',
    ['workflow'],
    registry=registry
)

ci_test_duration_seconds = Gauge(
    'ci_test_duration_seconds',
    'Duration of test execution in seconds',
    ['workflow'],
    registry=registry
)

# Pipeline metrics
ci_pipeline_runs_total = Counter(
    'ci_pipeline_runs_total',
    'Total pipeline runs',
    ['pipeline'],
    registry=registry
)

ci_last_build_timestamp = Gauge(
    'ci_last_build_timestamp',
    'Timestamp of last build',
    ['workflow'],
    registry=registry
)

ci_deployments_total = Counter(
    'ci_deployments_total',
    'Total number of deployments',
    ['environment','status'],
    registry=registry
)

def simulate_ci_run():
    workflow = "CI Pipeline"
    build_duration = random.uniform(30,180)
    is_success = random.random() < 0.90
    status = "success" if is_success else "failure"
    ci_build_duration_seconds.labels(workflow=workflow,status=status).set(build_duration)
    ci_build_total.labels(workflow=workflow,status=status).inc()
    ci_last_build_timestamp.labels(workflow=workflow).set(time.time())
    ci_pipeline_runs_total.labels(pipeline=workflow).inc()
    
    total_tests = random.randint(5,10)
    if is_success:
        passed_tests = total_tests
        failed_tests = 0
    else:
        failed_tests = random.randint(1,3)
        passed_tests = total_tests - failed_tests
    
    ci_tests_total.labels(workflow=workflow).set(total_tests)
    ci_tests_passed.labels(workflow=workflow).set(passed_tests)
    ci_tests_failed.labels(workflow=workflow).set(failed_tests)
    ci_test_duration_seconds.labels(workflow=workflow).set(random.uniform(5,30))
    
    success_rate = 90 + random.uniform(-10,10)  # 80-100%
    ci_build_success_rate.labels(workflow=workflow).set(success_rate)
    
    return {
        'workflow': workflow,
        'status': status,
        'duration': round(build_duration, 2),
        'tests_total': total_tests,
        'tests_passed': passed_tests,
        'tests_failed': failed_tests
    }
    
    
def simulate_deployment():
    environment = random.choice(['staging','prod'])
    is_success = random.random() < 0.95
    status = 'success' if is_success else 'failure'
    
    ci_deployments_total.labels(environment=environment,status=status).inc()
    
    return {
        'environment': environment,
        'status': status
    }
    

def push_metrics():
    try:
        push_to_gateway(PUSHGATEWAY_URL,job='cicd_metrics',registry=registry)
        return True
    except Exception as e:
        print(f"Error pushing metrics: {e}")
        return False
    
def run_continuous_simulation(interval=30):
    print("=" * 50)
    print("🚀 CI/CD Metrics Simulator")
    print("=" * 50)
    print(f"📊 Pushgateway: http://{PUSHGATEWAY_URL}")
    print(f"⏱️  Simulation interval: {interval} seconds")
    print("=" * 50)
    
    build_count = 0
    while True:
        build_count += 1
        print(f"\n🔄 Simulating CI/CD run #{build_count}...")
        
        ci_result = simulate_ci_run()
        print(f" Build: {ci_result['status'].upper()} ({ci_result['duration']}s)")
        print(f" Tests: {ci_result['tests_passed']}/{ci_result['tests_total']} passed")
        if random.random() < 0.30:
            deploy_result = simulate_deployment()
            print(f" Deploy to {deploy_result['environment']}: {deploy_result['status'].upper()}")
        if push_metrics():
            print(f"  Metrics pushed to Pushgateway")
        else:
            print(f"  Failed to push metrics")
        
        print(f"\nNext simulation in {interval} seconds...")
        time.sleep(interval)
        
        
run_continuous_simulation(interval=30)
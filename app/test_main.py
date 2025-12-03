import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'running'
    assert 'endpoints' in data


def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'uptime_seconds' in data
    assert 'checks' in data


def test_data_endpoint(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'timestamp' in data
    assert len(data['data']['values']) == 10


def test_stats_endpoint(client):
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'system' in data
    assert 'cpu' in data
    assert 'memory' in data
    assert 'disk' in data


def test_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'http_requests_total' in response.data
    assert b'cpu_usage_percent' in response.data
    assert b'memory_usage_bytes' in response.data
    assert b'app_uptime_seconds' in response.data


def test_metrics_contain_system_info(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'cpu_count_total' in response.data
    assert b'memory_total_bytes' in response.data
    assert b'disk_usage_percent' in response.data

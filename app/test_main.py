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
    
def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    
def test_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'http_requests_total' in response.data

def test_data_endpoint(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'timestamp' in data
"""
Load Testing Script - Generate traffic for dashboard demo
"""
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:5000"

def make_request(endpoint):
    """Make a single request to an endpoint"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_traffic(duration=60, requests_per_second=5):
    """Generate continuous traffic"""
    print(f"🚀 Starting load test for {duration} seconds...")
    print(f"📊 Generating ~{requests_per_second} requests/second")
    print(f"🎯 Target: {BASE_URL}")
    print("-" * 50)
    
    endpoints = [
        "/",
        "/api/health",
        "/api/data",
        "/metrics"
    ]
    
    start_time = time.time()
    total_requests = 0
    successful_requests = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while time.time() - start_time < duration:
            # Submit multiple requests
            futures = []
            for _ in range(requests_per_second):
                endpoint = random.choice(endpoints)
                future = executor.submit(make_request, endpoint)
                futures.append(future)
            
            # Wait for responses
            for future in futures:
                status = future.result()
                total_requests += 1
                if status == 200:
                    successful_requests += 1
            
            # Display progress
            elapsed = int(time.time() - start_time)
            print(f"⏱️  {elapsed}s | Total: {total_requests} | Success: {successful_requests} | Rate: {total_requests/elapsed:.1f} req/s", end="\r")
            
            # Sleep to maintain rate
            time.sleep(1)
    
    print("\n" + "-" * 50)
    print(f"✅ Load test completed!")
    print(f"📈 Total requests: {total_requests}")
    print(f"✅ Successful: {successful_requests}")
    print(f"❌ Failed: {total_requests - successful_requests}")
    print(f"📊 Success rate: {(successful_requests/total_requests)*100:.1f}%")

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 DevOps Dashboard Load Tester")
    print("=" * 50)
    
    # Run load test
    generate_traffic(duration=120, requests_per_second=10)
    
    print("\n🎨 Now check your Grafana dashboards!")
    print("   They should be showing live data!")


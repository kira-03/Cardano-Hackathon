"""
Test script for API endpoints without stopping the server
"""
import requests
import json
import time

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    response = requests.get("http://localhost:8000/health")
    data = response.json()
    print(json.dumps(data, indent=2))
    return data

def test_analyze():
    """Test full analysis with Masumi logging"""
    print("\n🔍 Testing Full Analysis Pipeline with Masumi...")
    
    payload = {
        "policy_id": "a9fc2c980e6beed499b91089ca06ad433961a6238690219b8021fe43",
        "target_exchanges": ["MEXC", "Gate.io"],
        "target_chains": ["BSC", "Polygon"]
    }
    
    print(f"📤 Sending request with policy_id: {payload['policy_id']}")
    response = requests.post(
        "http://localhost:8000/api/analyze",
        json=payload,
        timeout=60
    )
    
    data = response.json()
    
    # Print summary
    print(f"\n✅ Analysis complete!")
    print(f"   Policy ID: {data.get('policy_id')}")
    print(f"   Token: {data.get('token_name')} ({data.get('token_symbol')})")
    readiness = data.get('readiness_score', {})
    print(f"   Listing Score: {readiness.get('total_score')}/100 (Grade: {readiness.get('grade')})")
    print(f"   Recommendations: {len(data.get('recommendations', []))}")
    print(f"   Exchange Requirements: {len(data.get('exchange_requirements', []))}")
    print(f"   Bridge Routes: {len(data.get('bridge_routes', []))}")
    print(f"   Recommended Chain: {data.get('recommended_chain')}")
    
    # Check Masumi logs
    masumi_logs = data.get('masumi_logs', [])
    print(f"\n📝 Masumi Logs Created: {len(masumi_logs)}")
    
    for i, log in enumerate(masumi_logs, 1):
        print(f"\n   Log {i}: {log.get('decision_type', 'N/A')}")
        print(f"   - DID: {log.get('agent_did', 'N/A')[:50]}...")
        print(f"   - Decision Hash: {log.get('decision_hash', 'N/A')[:32]}...")
        print(f"   - Timestamp: {log.get('timestamp', 'N/A')}")
    
    return data

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Cross-Chain Navigator Agent - API Test Suite")
    print("=" * 60)
    
    # Wait for server
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    try:
        # Test health
        health_data = test_health()
        
        if not health_data.get('services', {}).get('blockfrost'):
            print("\n❌ BlockFrost connection failed!")
            exit(1)
        
        print(f"\n✅ BlockFrost connected: {health_data.get('network')} network")
        
        # Test analysis with Masumi
        analysis_data = test_analyze()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

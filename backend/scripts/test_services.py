#!/usr/bin/env python3
"""
Test script to verify all services are working
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.cardano_service import CardanoService
from services.masumi_service import MasumiService
from config import settings

async def test_cardano_service():
    """Test Cardano service connection"""
    print("\n🔵 Testing Cardano Service...")
    try:
        service = CardanoService()
        connected = await service.check_connection()
        if connected:
            print("✅ Cardano service connection: OK")
            return True
        else:
            print("❌ Cardano service connection: FAILED")
            print(f"   Check your BLOCKFROST_API_KEY in .env")
            return False
    except Exception as e:
        print(f"❌ Cardano service error: {str(e)}")
        return False

async def test_masumi_service():
    """Test Masumi service"""
    print("\n🟣 Testing Masumi Service...")
    try:
        service = MasumiService()
        connected = service.check_connection()
        if connected:
            print("✅ Masumi service connection: OK")
        else:
            print("⚠️  Masumi node not running (this is OK for development)")
            print("   Agent decisions will be logged locally")
        return True
    except Exception as e:
        print(f"⚠️  Masumi service warning: {str(e)}")
        print("   Continuing with local logging...")
        return True

async def test_token_analysis():
    """Test token analysis with example policy ID"""
    print("\n📊 Testing Token Analysis...")
    try:
        service = CardanoService()
        
        # Test with a known Cardano policy (example)
        test_policy = "29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c6"
        
        print(f"   Analyzing policy: {test_policy[:20]}...")
        
        # Get token info
        info = await service.get_token_info(test_policy)
        print(f"✅ Token info retrieved: {info.get('asset_name', 'Unknown')}")
        
        # Get holders
        holders = await service.get_token_holders(test_policy)
        print(f"✅ Holders retrieved: {len(holders)} holders")
        
        # Get liquidity estimate
        liquidity = await service.get_dex_liquidity(test_policy)
        print(f"✅ Liquidity estimated: ${liquidity['total_liquidity_usd']:,.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Token analysis error: {str(e)}")
        print("   This might be due to an invalid test policy ID")
        return False

async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Cross-Chain Navigator Agent - System Test")
    print("=" * 60)
    
    print("\n📋 Configuration:")
    print(f"   BLOCKFROST_API_KEY: {'✓ Set' if settings.blockfrost_api_key else '✗ Missing'}")
    print(f"   BLOCKFROST_NETWORK: {settings.blockfrost_network}")
    print(f"   MASUMI_NODE_URL: {settings.masumi_node_url}")
    print(f"   DATABASE_URL: {settings.database_url}")
    
    results = []
    
    # Test services
    results.append(await test_cardano_service())
    results.append(await test_masumi_service())
    
    # If Cardano service is OK, test analysis
    if results[0]:
        results.append(await test_token_analysis())
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("\n🎉 System is ready! You can start the API server with:")
        print("   python -m uvicorn main:app --reload")
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
        print("\n💡 Please check:")
        print("   1. BLOCKFROST_API_KEY is set correctly in .env")
        print("   2. You have internet connection")
        print("   3. The test policy ID exists on Cardano")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

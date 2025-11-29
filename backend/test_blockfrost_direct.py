"""Test BlockFrost SDK directly"""
from blockfrost import BlockFrostApi, ApiUrls
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BLOCKFROST_API_KEY")
print(f"API Key: {api_key[:20]}...")

# Initialize API
api = BlockFrostApi(project_id=api_key, base_url=ApiUrls.preprod.value)

# Test health
print("\nTesting health...")
try:
    health = api.health()
    print(f"Health: {health.is_healthy}")
except Exception as e:
    print(f"Health Error: {e}")

# Test getting policy assets
policy_id = "a9fc2c980e6beed499b91089ca06ad433961a6238690219b8021fe43"
print(f"\nTesting assets_policy for {policy_id[:20]}...")
try:
    assets = api.assets_policy(policy_id)
    print(f"Found {len(assets)} assets")
    if assets:
        print(f"First asset: {assets[0].asset[:50]}...")
except Exception as e:
    print(f"Assets Error: {e}")

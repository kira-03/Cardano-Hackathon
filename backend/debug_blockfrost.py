import os
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

api_key = os.getenv("BLOCKFROST_API_KEY")
network = os.getenv("BLOCKFROST_NETWORK", "preprod")

print(f"Testing BlockFrost connection...")
print(f"Network: {network}")
print(f"API Key: {api_key[:8]}...{api_key[-4:] if api_key else 'None'}")

if not api_key:
    print("❌ Error: BLOCKFROST_API_KEY not found in .env")
    sys.exit(1)

# Determine base URL
if network.lower() == "mainnet":
    base_url = ApiUrls.mainnet.value
elif network.lower() == "preprod":
    base_url = ApiUrls.preprod.value
elif network.lower() == "preview":
    base_url = ApiUrls.preview.value
else:
    base_url = ApiUrls.testnet.value

print(f"Base URL: {base_url}")

try:
    api = BlockFrostApi(project_id=api_key, base_url=base_url)
    health = api.health()
    print(f"✅ Connection Successful!")
    print(f"Health Status: {health.is_healthy}")
    
    # Try to fetch a specific policy to verify permissions
    policy_id = "a9fc2c980e6beed499b91089ca06ad433961a6238690219b8021fe43" # The one used in tests
    print(f"\nFetching assets for policy {policy_id[:10]}...")
    assets = api.assets_policy(policy_id)
    print(f"✅ Found {len(assets)} assets.")
    if assets:
        print(f"First asset: {assets[0].asset}")

except ApiError as e:
    print(f"❌ BlockFrost API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Message: {e.message}")
except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}: {e}")

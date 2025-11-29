"""
Detailed test to see full response
"""
import requests
import json

payload = {
    "policy_id": "a9fc2c980e6beed499b91089ca06ad433961a6238690219b8021fe43",
    "target_exchanges": ["MEXC", "Gate.io"],
    "target_chains": ["BSC", "Polygon"]
}

print("Sending request...")
response = requests.post(
    "http://localhost:8000/api/analyze",
    json=payload,
    timeout=120
)

print(f"\nStatus Code: {response.status_code}")
print(f"\nFull Response:")
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)

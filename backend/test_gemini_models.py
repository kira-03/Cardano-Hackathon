"""
Test Gemini models availability
"""
import google.generativeai as genai
from config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)

print("🔍 Available Gemini Models:")
print("=" * 40)

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
        else:
            print(f"❌ {model.name} (no generateContent)")
except Exception as e:
    print(f"❌ Error listing models: {e}")

# Test with different model names
test_models = [
    'models/gemini-pro',
    'models/gemini-2.5-flash', 
    'gemini-pro',
    'gemini-1.5-pro'
]

print(f"\n🧪 Testing Model Names:")
print("=" * 40)

for model_name in test_models:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, respond with 'Working!'")
        print(f"✅ {model_name}: {response.text.strip()}")
        break  # Use the first working model
    except Exception as e:
        print(f"❌ {model_name}: {str(e)[:100]}...")
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: No API Key found in .env file.")
else:
    print(f"✅ Found API Key: {api_key[:5]}...")
    
    try:
        genai.configure(api_key=api_key)
        print("\n🔍 Checking available models for your key...")
        
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
                found_any = True
        
        if not found_any:
            print("⚠️ No content generation models found. Check your API key permissions.")
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
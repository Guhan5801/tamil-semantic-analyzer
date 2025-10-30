#!/usr/bin/env python3
"""Test to find correct Gemini model name"""

import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import Config

api_key = Config.GEMINI_API_KEY

# Try to list available models
print("Attempting to list available Gemini models...\n")

for api_version in ['v1', 'v1beta']:
    print(f"\n=== Testing API version: {api_version} ===")
    url = f'https://generativelanguage.googleapis.com/{api_version}/models?key={api_key}'
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Found {len(models)} models:")
            for model in models:
                model_name = model.get('name', '')
                supported_methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in supported_methods:
                    print(f"   • {model_name} - {supported_methods}")
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Exception: {e}")

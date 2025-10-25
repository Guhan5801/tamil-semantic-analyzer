#!/usr/bin/env python3
"""
Debug script to check full API response
"""

import requests
import json

def debug_api_response():
    """Debug the full API response"""
    
    text = "வணக்கம் நண்பர்களே"
    print(f"🔍 Testing with: {text}")
    
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            json={'text': text},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("📋 Full API Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_api_response()
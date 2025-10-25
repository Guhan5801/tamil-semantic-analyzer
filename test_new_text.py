#!/usr/bin/env python3
"""
Test with new text to bypass cache
"""

import requests
import json

def test_new_text():
    """Test with text that wasn't cached before"""
    
    # Use new text that wasn't tested before
    text = "மகிழ்ச்சியான பிறந்தநாள் வாழ்த்துக்கள்"
    print(f"🔍 Testing with new text: {text}")
    
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            json={'text': text},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            semantic = data.get('semantic_analysis', {})
            
            print(f"✅ Status: Success")
            print(f"📝 Text: {text}")
            print(f"🔤 Word Count: {semantic.get('word_count', 0)}")
            print(f"🏷️ Language: {semantic.get('language_detected', 'unknown')}")
            print(f"💡 Meaning: {semantic.get('meaning', 'No meaning field')}")
            print(f"⏱️ Time: {data.get('processing_time', 'unknown')}")
            print(f"📋 Cached: {data.get('cached', False)}")
            
            print("\n📋 Full semantic analysis:")
            print(json.dumps(semantic, indent=2, ensure_ascii=False))
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_new_text()
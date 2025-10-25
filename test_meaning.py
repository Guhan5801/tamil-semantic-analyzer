#!/usr/bin/env python3
"""
Test script to verify meaning extraction functionality
"""

import requests
import json

def test_meaning_extraction():
    """Test the meaning extraction with various Tamil texts"""
    
    test_cases = [
        "வணக்கம் நண்பர்களே",
        "நன்றி வாழ்த்துக்கள்",
        "குடும்பம் மிகவும் முக்கியம்",
        "இன்று நல்ல நாள்",
        "அன்பு என்பது உயர்ந்த உணர்வு"
    ]
    
    for text in test_cases:
        print(f"\n🔍 Testing: {text}")
        print("-" * 50)
        
        try:
            # API call
            response = requests.post(
                'http://localhost:5000/api/analyze',
                json={'text': text},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                semantic = data.get('semantic_analysis', {})
                meaning = semantic.get('meaning', 'No meaning found')
                
                print(f"✅ Status: Success")
                print(f"📝 Text: {text}")
                print(f"🔤 Word Count: {semantic.get('word_count', 0)}")
                print(f"🏷️ Language: {semantic.get('language_detected', 'unknown')}")
                print(f"💡 Meaning: {meaning}")
                print(f"⏱️ Time: {data.get('processing_time', 'unknown')}")
            else:
                print(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Tamil Text Meaning Extraction")
    print("=" * 60)
    test_meaning_extraction()
    print("\n✅ Testing completed!")
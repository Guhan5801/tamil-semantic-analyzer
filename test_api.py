#!/usr/bin/env python3
"""
Simple API Test Script to verify the semantic analysis endpoints
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints"""
    
    print("🧪 Testing Tamil Semantic Analysis API")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data.get('status', 'unknown')}")
            print(f"   📊 Engines status: {data.get('engines', {})}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            print(f"   📄 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Text analysis
    print("\n2. Testing Text Analysis...")
    test_text = "நான் மிகவும் மகிழ்ச்சியாக இருக்கிறேன்"
    
    try:
        response = requests.post(
            f"{base_url}/api/analyze",
            json={"text": test_text},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Analysis successful!")
            
            if data.get('status') == 'success':
                analysis = data.get('analysis', {})
                semantic = analysis.get('semantic_analysis', {})
                sentiment = analysis.get('sentiment_analysis', {})
                
                print(f"   📝 Input: {test_text}")
                print(f"   🧠 Word count: {semantic.get('word_count', 0)}")
                print(f"   💭 Sentiment: {sentiment.get('overall_sentiment', 'unknown')}")
                print(f"   🎯 Confidence: {sentiment.get('confidence', 0) * 100:.1f}%")
                print(f"   ⏱️ Processing time: {analysis.get('processing_time', 0):.2f}s")
                print(f"   Enhanced: {'✅' if analysis.get('enhanced_analysis', False) else '❌'}")
            else:
                print(f"   ❌ Analysis failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
    
    # Test 3: Web interface
    print("\n3. Testing Web Interface...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            if "Tamil Semantic & Sentiment Analysis" in response.text:
                print("   ✅ Web interface accessible")
            else:
                print("   ⚠️ Web interface loaded but content unexpected")
        else:
            print(f"   ❌ Web interface failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Web interface error: {e}")
    
    # Test 4: Test page
    print("\n4. Testing Debug Page...")
    try:
        response = requests.get(f"{base_url}/test", timeout=10)
        if response.status_code == 200:
            if "API Test" in response.text:
                print("   ✅ Debug page accessible")
            else:
                print("   ⚠️ Debug page loaded but content unexpected")
        else:
            print(f"   ❌ Debug page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Debug page error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API Testing Complete!")
    print(f"🌐 Main App: {base_url}")
    print(f"🧪 Test Page: {base_url}/test")
    print(f"🔍 Health: {base_url}/api/health")

if __name__ == "__main__":
    test_api()
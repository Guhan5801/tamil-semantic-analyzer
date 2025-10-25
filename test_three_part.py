#!/usr/bin/env python3
"""
Test Three-Part Tamil Text Analysis
Demonstrates the comprehensive analysis: Semantic Analysis, Tamil Translation, and Tamil Meaning
"""

import requests
import json
import time

def test_three_part_analysis():
    """Test the three-part analysis with sample texts"""
    
    # Test cases with different types of text
    test_cases = [
        {
            "text": "I am very happy today",
            "description": "Simple positive English sentence"
        },
        {
            "text": "The weather is beautiful and I feel peaceful",
            "description": "English sentence with emotions"
        },
        {
            "text": "நான் மிகவும் மகிழ்ச்சியாக இருக்கிறேன்",
            "description": "Tamil sentence - I am very happy"
        },
        {
            "text": "Life is full of challenges but we must stay strong",
            "description": "Motivational English sentence"
        }
    ]
    
    print("🎯 Testing Three-Part Tamil Text Analysis")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['description']}")
        print(f"Input Text: '{test_case['text']}'")
        print("-" * 40)
        
        try:
            # Call the three-part analysis API
            response = requests.post(
                'http://localhost:5000/api/three_part_analyze',
                json={'text': test_case['text']},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ Analysis Status:", data.get('status', 'unknown'))
                print("⏱️  Processing Time:", data.get('processing_time', 'N/A'))
                print("🌐 Language Detected:", data.get('language_detected', 'unknown'))
                
                # Part 1: Semantic Analysis
                semantic = data.get('semantic_analysis', {})
                print(f"\n🧠 PART 1: SEMANTIC ANALYSIS & TONE")
                print(f"   Meaning: {semantic.get('meaning', 'N/A')}")
                print(f"   Tone: {semantic.get('tone', 'N/A')}")
                print(f"   Sentiment: {semantic.get('sentiment', 'N/A')}")
                
                # Part 2: Tamil Translation
                translation = data.get('tamil_translation', {})
                print(f"\n🌏 PART 2: TAMIL TRANSLATION")
                print(f"   Primary: {translation.get('primary_translation', 'N/A')}")
                if translation.get('alternative_translation'):
                    print(f"   Alternative: {translation.get('alternative_translation')}")
                
                # Part 3: Simple Tamil Meaning
                meaning = data.get('tamil_meaning', {})
                print(f"\n💡 PART 3: SIMPLE TAMIL MEANING")
                print(f"   Simple Explanation: {meaning.get('simple_explanation', 'N/A')}")
                if meaning.get('key_message'):
                    print(f"   Key Message: {meaning.get('key_message')}")
                
                # Metrics
                metrics = data.get('text_metrics', {})
                print(f"\n📊 TEXT METRICS")
                print(f"   Characters: {metrics.get('character_count', 0)}")
                print(f"   Words: {metrics.get('word_count', 0)}")
                print(f"   Tamil Characters: {metrics.get('tamil_character_count', 0)}")
                
            else:
                print("❌ Error:", response.status_code, response.text)
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        print("\n" + "=" * 60)
        time.sleep(1)  # Brief pause between tests

if __name__ == "__main__":
    print("🚀 Starting Three-Part Analysis Test")
    print("Make sure the server is running at http://localhost:5000")
    print()
    
    try:
        # Check if server is running
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("✅ Server is running, starting tests...")
            test_three_part_analysis()
        else:
            print("❌ Server not responding. Please start the server first.")
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        print("Please make sure the server is running at http://localhost:5000")
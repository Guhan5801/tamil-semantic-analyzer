#!/usr/bin/env python3
"""
Comprehensive Gemini Integration Diagnostic
Tests the exact flow that's failing on Vercel
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*80)
print("🔍 COMPREHENSIVE GEMINI DIAGNOSTIC")
print("="*80)

# Test 1: Config
print("\n1️⃣ CONFIG CHECK")
print("-"*80)
try:
    from config import Config
    api_key = Config.GEMINI_API_KEY
    print(f"✅ Config loaded")
    print(f"   • API Key length: {len(api_key)}")
    print(f"   • API Key (last 10): ...{api_key[-10:]}")
    print(f"   • Model: {Config.GEMINI_MODEL}")
    print(f"   • Gemini enabled: {Config.ENABLE_GEMINI_ENHANCEMENT}")
    print(f"   • is_gemini_available(): {Config.is_gemini_available()}")
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

# Test 2: Gemini Integration
print("\n2️⃣ GEMINI INTEGRATION CHECK")
print("-"*80)
try:
    from gemini_integration import GeminiCulturalAnalyzer
    gemini = GeminiCulturalAnalyzer()
    print(f"✅ Gemini integration loaded")
    print(f"   • SDK available: {gemini.client is not None}")
    print(f"   • Model: {gemini.model_name}")
    print(f"   • Is available: {gemini.is_available}")
    print(f"   • API Key length: {len(gemini.api_key)}")
except Exception as e:
    print(f"❌ Gemini integration error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Direct Gemini API Call
print("\n3️⃣ DIRECT GEMINI API CALL")
print("-"*80)
try:
    test_text = "உரையின் தெளிவான விளக்கம்: இந்த உரை சுருக்கமாக ஒரு எண்ணத்தை விவரிக்கிறது."
    print(f"Test text: {test_text}")
    print(f"Length: {len(test_text)} characters")
    
    response = gemini.get_conversational_meaning(test_text)
    if response and response.get('text'):
        text_len = len(response['text'])
        print(f"\n✅ Gemini API responded!")
        print(f"   • Response length: {text_len} characters")
        print(f"   • Has பொருள்: {'பொருள்:' in response['text']}")
        print(f"   • Has சுருக்கமாக: {'சுருக்கமாக:' in response['text']}")
        print(f"\n   Preview (first 300 chars):")
        print(f"   {response['text'][:300]}...")
    else:
        print(f"❌ Gemini API returned empty response")
        print(f"   Response: {response}")
except Exception as e:
    print(f"❌ Direct API call error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Semantic Analyzer
print("\n4️⃣ SEMANTIC ANALYZER CHECK")
print("-"*80)
try:
    from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
    analyzer = SemanticSentimentAnalyzer()
    print(f"✅ Semantic analyzer initialized")
    print(f"   • Gemini enabled: {analyzer.gemini_enabled}")
    print(f"   • Gemini analyzer exists: {analyzer.gemini_analyzer is not None}")
    
    if analyzer.gemini_analyzer:
        print(f"   • Gemini model: {analyzer.gemini_analyzer.model_name}")
        print(f"   • Gemini available: {analyzer.gemini_analyzer.is_available}")
except Exception as e:
    print(f"❌ Semantic analyzer error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Full Analysis Flow
print("\n5️⃣ FULL ANALYSIS FLOW")
print("-"*80)
try:
    test_text = "உரையின் தெளிவான விளக்கம்: இந்த உரை சுருக்கமாக ஒரு எண்ணத்தை விவரிக்கிறது."
    print(f"Input: {test_text}\n")
    
    result = analyzer.analyze_semantic_sentiment(test_text)
    
    meaning = result['semantic_analysis'].get('meaning', '')
    enhanced = result.get('enhanced_analysis', False)
    
    print(f"✅ Analysis completed!")
    print(f"   • Enhanced: {enhanced}")
    print(f"   • Meaning length: {len(meaning)} characters")
    print(f"   • Has பொருள்: {'பொருள்:' in meaning}")
    print(f"   • Has சுருக்கமாக: {'சுருக்கமாக:' in meaning}")
    print(f"\n   Meaning preview (first 400 chars):")
    print(f"   {meaning[:400]}...")
    
    if enhanced and len(meaning) > 500:
        print(f"\n✅ FULL FLOW WORKING - Detailed meaning provided!")
    elif not enhanced:
        print(f"\n❌ PROBLEM: Gemini NOT being used (enhanced=False)")
    else:
        print(f"\n⚠️  PARTIAL: Gemini used but short output")
        
except Exception as e:
    print(f"❌ Full flow error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Environment Variables
print("\n6️⃣ ENVIRONMENT VARIABLES")
print("-"*80)
api_key_env = os.getenv('GEMINI_API_KEY', 'NOT SET')
print(f"GEMINI_API_KEY environment variable:")
if api_key_env == 'NOT SET':
    print(f"   ❌ NOT SET (will use config.py default)")
else:
    print(f"   ✅ SET in environment")
    print(f"   • Length: {len(api_key_env)} characters")
    print(f"   • Last 10: ...{api_key_env[-10:]}")

# Final Summary
print("\n" + "="*80)
print("📋 SUMMARY")
print("="*80)

if enhanced and len(meaning) > 500 and 'பொருள்:' in meaning:
    print("✅ ALL SYSTEMS GO!")
    print("✅ Local system working perfectly")
    print("✅ If Vercel shows generic output, update GEMINI_API_KEY there")
else:
    print("❌ ISSUES DETECTED:")
    if not enhanced:
        print("   • Gemini not being used (enhanced=False)")
    if len(meaning) < 500:
        print(f"   • Meaning too short: {len(meaning)} chars (expected 1000+)")
    if 'பொருள்:' not in meaning:
        print("   • No பொருள்: section found")

print("="*80)

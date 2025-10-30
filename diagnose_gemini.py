#!/usr/bin/env python3
"""
Quick test to check if Gemini is working locally vs what might be happening on Vercel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🔍 DIAGNOSING GEMINI ISSUE")
print("=" * 70)

# Test 1: Check imports
print("\n1️⃣ Testing imports...")
try:
    from config import Config
    print(f"   ✅ Config imported")
    print(f"   • GEMINI_API_KEY present: {bool(Config.GEMINI_API_KEY)}")
    print(f"   • GEMINI_MODEL: {Config.GEMINI_MODEL}")
    print(f"   • ENABLE_GEMINI_ENHANCEMENT: {Config.ENABLE_GEMINI_ENHANCEMENT}")
except Exception as e:
    print(f"   ❌ Config import failed: {e}")
    sys.exit(1)

# Test 2: Check Gemini availability
print("\n2️⃣ Testing Gemini availability...")
try:
    from gemini_integration import GeminiCulturalAnalyzer
    print(f"   ✅ GeminiCulturalAnalyzer imported")
    
    gemini = GeminiCulturalAnalyzer()
    print(f"   • is_available: {gemini.is_available}")
    print(f"   • model_name: {gemini.model_name}")
    print(f"   • base_url: {gemini.base_url}")
except Exception as e:
    print(f"   ❌ Gemini import/init failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check analyzer initialization
print("\n3️⃣ Testing SemanticSentimentAnalyzer initialization...")
try:
    from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
    analyzer = SemanticSentimentAnalyzer()
    print(f"   ✅ Analyzer created")
    print(f"   • gemini_enabled: {analyzer.gemini_enabled}")
    print(f"   • gemini_analyzer exists: {analyzer.gemini_analyzer is not None}")
except Exception as e:
    print(f"   ❌ Analyzer init failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Quick analysis test
print("\n4️⃣ Testing actual analysis...")
test_text = "யாதும் ஊரே யாவரும் கேளிர்"
try:
    result = analyzer.analyze_semantic_sentiment(test_text)
    
    is_enhanced = result.get('enhanced_analysis', False)
    meaning = result.get('semantic_analysis', {}).get('meaning', '')
    
    print(f"   • Input: {test_text}")
    print(f"   • Enhanced: {is_enhanced}")
    print(f"   • Meaning length: {len(meaning)} chars")
    print(f"   • Meaning preview: {meaning[:150]}...")
    
    if is_enhanced:
        print(f"\n   ✅ GEMINI IS WORKING!")
        source_book = result.get('semantic_analysis', {}).get('source_book', '')
        if source_book:
            print(f"   • Source identified: {source_book}")
    else:
        print(f"\n   ❌ GEMINI NOT ACTIVATED!")
        print(f"   • This is the basic fallback meaning")
        
        # Check for error
        if result.get('gemini_error'):
            print(f"   • Gemini error: {result['gemini_error']}")
            
except Exception as e:
    print(f"   ❌ Analysis failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)

# Summary
print("\n📊 SUMMARY:")
if analyzer.gemini_enabled and is_enhanced:
    print("✅ Everything is working correctly!")
    print("✅ Gemini AI is providing detailed literary analysis")
    print("✅ Your deployment should work once Vercel finishes building")
elif analyzer.gemini_enabled and not is_enhanced:
    print("⚠️ Gemini is enabled but not being used!")
    print("   Possible reasons:")
    print("   1. API call is failing (check network/API key)")
    print("   2. Response parsing is failing")
    print("   3. Error is being silently caught")
else:
    print("❌ Gemini is not enabled!")
    print("   Check:")
    print("   1. ENABLE_GEMINI_ENHANCEMENT = True")
    print("   2. GEMINI_API_KEY is set")
    print("   3. gemini_integration module imports correctly")

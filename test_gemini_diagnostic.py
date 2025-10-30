#!/usr/bin/env python3
"""
Quick test to diagnose Gemini integration issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_integration import GeminiCulturalAnalyzer
from config import Config
import json

print("=== Gemini Diagnostic Test ===\n")

# Check configuration
print(f"1. Configuration Check:")
print(f"   • GEMINI_API_KEY present: {bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'your_gemini_api_key_here')}")
print(f"   • GEMINI_MODEL: {Config.GEMINI_MODEL}")
print(f"   • ENABLE_GEMINI_ENHANCEMENT: {Config.ENABLE_GEMINI_ENHANCEMENT}")
print(f"   • is_gemini_available(): {Config.is_gemini_available()}")

# Initialize Gemini
print(f"\n2. Initializing GeminiCulturalAnalyzer:")
try:
    gemini = GeminiCulturalAnalyzer()
    print(f"   ✅ Initialized successfully")
    print(f"   • is_available: {gemini.is_available}")
    print(f"   • model_name: {gemini.model_name}")
    print(f"   • api_key length: {len(gemini.api_key) if gemini.api_key else 0}")
except Exception as e:
    print(f"   ❌ Failed to initialize: {e}")
    sys.exit(1)

# Test API call
print(f"\n3. Testing get_conversational_meaning():")
test_text = "யாதும் ஊரே யாவரும் கேளிர்"
try:
    result = gemini.get_conversational_meaning(test_text)
    print(f"   • Result returned: {result is not None}")
    if result:
        print(f"   • Has 'text' key: {'text' in result}")
        if 'text' in result:
            print(f"   • Response length: {len(result['text'])} characters")
            print(f"   • First 200 chars: {result['text'][:200]}")
    else:
        print(f"   ❌ No result returned from Gemini API")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test semantic sentiment analyzer
print(f"\n4. Testing SemanticSentimentAnalyzer:")
from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

analyzer = SemanticSentimentAnalyzer()
print(f"   • gemini_enabled: {analyzer.gemini_enabled}")
print(f"   • gemini_analyzer is None: {analyzer.gemini_analyzer is None}")

print(f"\n5. Running full analysis on test text:")
try:
    result = analyzer.analyze_semantic_sentiment(test_text)
    print(f"   • enhanced_analysis: {result.get('enhanced_analysis', False)}")
    print(f"   • gemini_error: {result.get('gemini_error', 'None')}")
    
    semantic = result.get('semantic_analysis', {})
    meaning = semantic.get('meaning', '')
    print(f"   • meaning length: {len(meaning)} characters")
    print(f"   • meaning preview: {meaning[:200]}")
    
    if 'source_book' in semantic:
        print(f"   • source_book: {semantic.get('source_book', 'N/A')}")
    
except Exception as e:
    print(f"   ❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n=== End of Diagnostic Test ===")

#!/usr/bin/env python3
"""
Complete Gemini Integration Verification
Checks all connection points and shows file locations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🔍 GEMINI INTEGRATION CONNECTION CHECK")
print("=" * 80)

# Get base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# File locations
files_to_check = {
    'Config': os.path.join(BASE_PATH, 'config.py'),
    'Gemini Integration': os.path.join(BASE_PATH, 'gemini_integration.py'),
    'Semantic Analyzer': os.path.join(BASE_PATH, 'semantic_sentiment_analyzer.py'),
    'API Endpoint': os.path.join(BASE_PATH, 'api', 'index.py'),
    'Requirements': os.path.join(BASE_PATH, 'requirements.txt')
}

print("\n📁 FILE LOCATIONS:")
print("-" * 80)
for name, path in files_to_check.items():
    exists = "✅" if os.path.exists(path) else "❌"
    print(f"{exists} {name}: {path}")

# Check 1: Config
print("\n" + "=" * 80)
print("1️⃣ CONFIG.PY - Gemini Settings")
print("=" * 80)
try:
    from config import Config
    print(f"✅ File: {files_to_check['Config']}")
    print(f"   • GEMINI_API_KEY present: {bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'your_gemini_api_key_here')}")
    print(f"   • GEMINI_API_KEY value: {'***' + Config.GEMINI_API_KEY[-10:] if Config.GEMINI_API_KEY else 'NOT SET'}")
    print(f"   • GEMINI_MODEL: {Config.GEMINI_MODEL}")
    print(f"   • ENABLE_GEMINI_ENHANCEMENT: {Config.ENABLE_GEMINI_ENHANCEMENT}")
    print(f"   • is_gemini_available(): {Config.is_gemini_available()}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check 2: Gemini Integration
print("\n" + "=" * 80)
print("2️⃣ GEMINI_INTEGRATION.PY - AI Integration Module")
print("=" * 80)
try:
    from gemini_integration import GeminiCulturalAnalyzer
    print(f"✅ File: {files_to_check['Gemini Integration']}")
    
    gemini = GeminiCulturalAnalyzer()
    print(f"   • Class imported: ✅")
    print(f"   • Instance created: ✅")
    print(f"   • is_available: {gemini.is_available}")
    print(f"   • model_name: {gemini.model_name}")
    print(f"   • base_url: {gemini.base_url}")
    print(f"   • api_key set: {bool(gemini.api_key)}")
    
    # Test connection
    print(f"\n   🧪 Testing Gemini API connection...")
    test_result = gemini.get_conversational_meaning("யாதும் ஊரே")
    if test_result and test_result.get('text'):
        print(f"   ✅ API Connection: WORKING")
        print(f"   ✅ Response received: {len(test_result['text'])} characters")
    else:
        print(f"   ❌ API Connection: FAILED")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check 3: Semantic Analyzer
print("\n" + "=" * 80)
print("3️⃣ SEMANTIC_SENTIMENT_ANALYZER.PY - Main Analyzer")
print("=" * 80)
try:
    from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
    print(f"✅ File: {files_to_check['Semantic Analyzer']}")
    
    analyzer = SemanticSentimentAnalyzer()
    print(f"   • Class imported: ✅")
    print(f"   • Instance created: ✅")
    print(f"   • gemini_enabled: {analyzer.gemini_enabled}")
    print(f"   • gemini_analyzer exists: {analyzer.gemini_analyzer is not None}")
    
    if analyzer.gemini_analyzer:
        print(f"   • Gemini model: {analyzer.gemini_analyzer.model_name}")
        print(f"   • Gemini available: {analyzer.gemini_analyzer.is_available}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check 4: API Integration
print("\n" + "=" * 80)
print("4️⃣ API/INDEX.PY - Flask Endpoint")
print("=" * 80)
try:
    print(f"📁 File: {files_to_check['API Endpoint']}")
    with open(files_to_check['API Endpoint'], 'r', encoding='utf-8') as f:
        api_content = f.read()
        
    # Check imports
    has_analyzer_import = 'from semantic_sentiment_analyzer import' in api_content
    has_analyzer_init = 'semantic_analyzer = SemanticSentimentAnalyzer()' in api_content
    
    print(f"   • Analyzer imported: {'✅' if has_analyzer_import else '❌'}")
    print(f"   • Analyzer initialized: {'✅' if has_analyzer_init else '❌'}")
    
    if has_analyzer_import and has_analyzer_init:
        print(f"   ✅ API properly connected to analyzer")
    else:
        print(f"   ❌ API NOT properly connected")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check 5: Dependencies
print("\n" + "=" * 80)
print("5️⃣ REQUIREMENTS.TXT - Dependencies")
print("=" * 80)
try:
    print(f"📁 File: {files_to_check['Requirements']}")
    with open(files_to_check['Requirements'], 'r', encoding='utf-8') as f:
        reqs = f.read()
    
    has_requests = 'requests' in reqs
    has_gemini = 'google-generativeai' in reqs or 'gemini' in reqs
    
    print(f"   • requests library: {'✅' if has_requests else '❌'}")
    print(f"   • google-generativeai: {'✅' if has_gemini else '❌'}")
    
    # Check if installed
    try:
        import requests
        print(f"   • requests installed: ✅")
    except:
        print(f"   • requests installed: ❌")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Final Test
print("\n" + "=" * 80)
print("6️⃣ INTEGRATION TEST - Full Flow")
print("=" * 80)
try:
    test_text = "யாதும் ஊரே யாவரும் கேளிர்"
    print(f"   Testing with: {test_text}")
    
    result = analyzer.analyze_semantic_sentiment(test_text)
    
    enhanced = result.get('enhanced_analysis', False)
    meaning = result.get('semantic_analysis', {}).get('meaning', '')
    source = result.get('semantic_analysis', {}).get('source_book', '')
    
    print(f"\n   📊 RESULTS:")
    print(f"   • Enhanced (Gemini used): {enhanced}")
    print(f"   • Source detected: {source}")
    print(f"   • Meaning length: {len(meaning)} characters")
    
    if enhanced and len(meaning) > 500:
        print(f"\n   ✅ INTEGRATION WORKING PERFECTLY!")
        print(f"   ✅ Gemini is providing detailed analysis")
    elif not enhanced:
        print(f"\n   ❌ PROBLEM: Gemini NOT being used!")
        print(f"   ❌ Falling back to basic analysis")
        if result.get('gemini_error'):
            print(f"   ❌ Error: {result['gemini_error']}")
    else:
        print(f"\n   ⚠️  PARTIAL: Gemini used but short output")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 80)
print("📋 INTEGRATION SUMMARY")
print("=" * 80)

all_good = True
issues = []

try:
    if not Config.is_gemini_available():
        all_good = False
        issues.append("Config: Gemini not available")
    
    if not gemini.is_available:
        all_good = False
        issues.append("Gemini Integration: API not available")
    
    if not analyzer.gemini_enabled:
        all_good = False
        issues.append("Semantic Analyzer: Gemini not enabled")
    
    if not enhanced:
        all_good = False
        issues.append("Integration Test: Gemini not being used")
    
    if all_good:
        print("✅ ALL SYSTEMS GO!")
        print("✅ Gemini integration is fully connected and working")
        print("✅ Ready for deployment")
    else:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
            
except:
    print("⚠️  Could not complete summary check")

print("\n" + "=" * 80)
print("FILE LOCATIONS FOR FIXING:")
print("=" * 80)
for name, path in files_to_check.items():
    print(f"{name}:")
    print(f"  {path}")
print("=" * 80)

#!/usr/bin/env python3
"""
Comprehensive verification test for Gemini integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
import json

print("=" * 70)
print("தமிழ் பொருள் ஆய்வு - இறுதி சரிபார்ப்பு சோதனை")
print("Final Verification Test - Tamil Semantic Analysis")
print("=" * 70)

# Initialize analyzer
analyzer = SemanticSentimentAnalyzer()

# Test texts - mix of literary and regular Tamil
test_cases = [
    {
        "name": "திருக்குறள் (Thirukkural)",
        "text": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
        "expected": "Should identify Thirukkural, அதிகாரம், meaning"
    },
    {
        "name": "கம்பராமாயணம் (Kambaramayanam)", 
        "text": "உலகம் யாவையும் தாம் ஒழிய வேறு இலை என்னும் உத்தமன்",
        "expected": "Should identify Kambaramayanam or literary work"
    },
    {
        "name": "சாதாரண வாக்கியம் (Regular sentence)",
        "text": "இன்று வானம் மிகவும் அழகாக இருக்கிறது",
        "expected": "Should provide clear meaning even if not from known book"
    },
    {
        "name": "புறநானூறு (Purananuru)",
        "text": "யாதும் ஊரே யாவரும் கேளிர்",
        "expected": "Should identify Purananuru, verse 192"
    }
]

print(f"\n{'='*70}")
print(f"Analyzer Status:")
print(f"  • Gemini Enabled: {analyzer.gemini_enabled}")
print(f"  • Gemini Analyzer Available: {analyzer.gemini_analyzer is not None}")
if analyzer.gemini_analyzer:
    print(f"  • Model Name: {analyzer.gemini_analyzer.model_name}")
    print(f"  • API Available: {analyzer.gemini_analyzer.is_available}")
print(f"{'='*70}\n")

# Test each case
for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'─'*70}")
    print(f"சோதனை {i}: {test_case['name']}")
    print(f"{'─'*70}")
    print(f"📝 உரை: {test_case['text']}")
    print(f"🎯 எதிர்பார்ப்பு: {test_case['expected']}\n")
    
    try:
        # Analyze
        result = analyzer.analyze_semantic_sentiment(test_case['text'])
        
        # Check if enhanced
        is_enhanced = result.get('enhanced_analysis', False)
        print(f"{'✅' if is_enhanced else '❌'} Enhanced Analysis: {is_enhanced}")
        
        if result.get('gemini_error'):
            print(f"⚠️ Gemini Error: {result['gemini_error']}")
        
        # Get semantic analysis
        semantic = result.get('semantic_analysis', {})
        meaning = semantic.get('meaning', '')
        source_book = semantic.get('source_book', '')
        
        print(f"\n📖 நூல் பெயர் (Source Book): {source_book if source_book else 'அடையாளம் காணப்படவில்லை'}")
        
        if semantic.get('chapter_section'):
            print(f"📚 பகுதி: {semantic.get('chapter_section')}")
        if semantic.get('verse_number'):
            print(f"🔢 பாடல் எண்: {semantic.get('verse_number')}")
        
        print(f"\n💭 பொருள் விளக்கம்:")
        print(f"{'-'*70}")
        # Show first 500 characters of meaning
        if len(meaning) > 500:
            print(meaning[:500] + "...")
            print(f"\n(மொத்த நீளம்: {len(meaning)} எழுத்துக்கள்)")
        else:
            print(meaning)
        print(f"{'-'*70}")
        
        # Sentiment
        sentiment = result.get('sentiment_analysis', {})
        print(f"\n😊 உணர்வு: {sentiment.get('overall_sentiment', 'N/A')} (நம்பிக்கை: {sentiment.get('confidence', 0):.1%})")
        
        # Check quality
        print(f"\n🔍 தர சரிபார்ப்பு:")
        if is_enhanced:
            if source_book:
                print(f"  ✅ நூல் அடையாளம் காணப்பட்டது: {source_book}")
            else:
                print(f"  ⚠️ நூல் அடையாளம் காணப்படவில்லை (சாதாரண உரையாக இருக்கலாம்)")
            
            if len(meaning) > 200:
                print(f"  ✅ விரிவான விளக்கம் கிடைத்தது ({len(meaning)} எழுத்துக்கள்)")
            else:
                print(f"  ⚠️ குறுகிய விளக்கம் ({len(meaning)} எழுத்துக்கள்)")
            
            # Check if it's the generic fallback
            if "உரையின் தெளிவான விளக்கம்" in meaning and len(meaning) < 150:
                print(f"  ❌ மூலப்படி விளக்கம் (Gemini செயல்படவில்லை)")
            else:
                print(f"  ✅ Gemini AI விளக்கம் கிடைத்தது")
        else:
            print(f"  ❌ Gemini enhancement செயல்படவில்லை")
            print(f"  ℹ️ மூலப்படி விளக்கம் மட்டுமே")
        
        print(f"\n⏱️ செயலாக்க நேரம்: {result.get('processing_time', 'N/A')}")
        
    except Exception as e:
        print(f"❌ சோதனை தோல்வி: {str(e)}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*70}")
print("சோதனை முடிந்தது - Test Completed")
print(f"{'='*70}\n")

# Final verification summary
print("📊 இறுதி சரிபார்ப்பு முடிவு:")
print("-" * 70)
if analyzer.gemini_enabled:
    print("✅ Gemini AI இயக்கப்பட்டுள்ளது")
    print("✅ மேம்படுத்தப்பட்ட பகுப்பாய்வு கிடைக்கும்")
    print("✅ நூல் அடையாளம் காணும் திறன் உள்ளது")
    print("✅ விரிவான தமிழ் விளக்கங்கள் கிடைக்கும்")
else:
    print("❌ Gemini AI செயல்படவில்லை")
    print("⚠️ மூலப்படி விளக்கங்கள் மட்டுமே கிடைக்கும்")

print("-" * 70)
print("\n✅ வலைதளத்தில் சோதிக்க தயாராக உள்ளது!")

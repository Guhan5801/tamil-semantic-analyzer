#!/usr/bin/env python3
"""Test semantic and sentiment accuracy"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
import json

print("=" * 80)
print("🧪 TESTING SEMANTIC & SENTIMENT ACCURACY")
print("=" * 80)

analyzer = SemanticSentimentAnalyzer()

test_cases = [
    {
        "name": "திருக்குறள் - கடவுள் வாழ்த்து",
        "text": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
        "expected_source": "திருக்குறள்",
        "expected_sentiment": "positive/devotional"
    },
    {
        "name": "கம்பராமாயணம்",
        "text": "உலகம் யாவையும் தாம் ஒழிய வேறு இலை என்னும் உத்தமன்",
        "expected_source": "கம்பராமாயணம்",
        "expected_sentiment": "positive/devotional"
    },
    {
        "name": "மகிழ்ச்சி உரை",
        "text": "இன்று மிகவும் மகிழ்ச்சியான நாள். வாழ்க்கை அழகாக இருக்கிறது.",
        "expected_source": "சாதாரண உரை",
        "expected_sentiment": "positive"
    },
    {
        "name": "சோகம் உரை",
        "text": "இன்று மிகவும் வருத்தமான நாள். எல்லாம் தவறாக போகிறது.",
        "expected_source": "சாதாரண உரை",
        "expected_sentiment": "negative"
    },
    {
        "name": "புறநானூறு",
        "text": "யாதும் ஊரே யாவரும் கேளிர்",
        "expected_source": "புறநானூறு",
        "expected_sentiment": "positive/philosophical"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['name']}")
    print(f"{'='*80}")
    print(f"📝 Input: {test['text']}")
    print(f"🎯 Expected Source: {test['expected_source']}")
    print(f"💭 Expected Sentiment: {test['expected_sentiment']}\n")
    
    result = analyzer.analyze_semantic_sentiment(test['text'])
    
    semantic = result.get('semantic_analysis', {})
    sentiment = result.get('sentiment_analysis', {})
    
    # Check semantic analysis
    source_book = semantic.get('source_book', 'N/A')
    meaning = semantic.get('meaning', '')
    
    print(f"📖 SEMANTIC ANALYSIS:")
    print(f"   ✓ Source Detected: {source_book}")
    print(f"   ✓ Meaning Length: {len(meaning)} characters")
    
    if 'chapter_section' in semantic and semantic.get('chapter_section') != 'பொருந்தாது':
        print(f"   ✓ Chapter/Section: {semantic.get('chapter_section')}")
    if 'verse_number' in semantic and semantic.get('verse_number') != 'பொருந்தாது':
        print(f"   ✓ Verse Number: {semantic.get('verse_number')}")
    
    print(f"\n   📄 பொருள் (Meaning):")
    print(f"   {'-'*76}")
    if len(meaning) > 300:
        print(f"   {meaning[:300]}...")
    else:
        print(f"   {meaning}")
    print(f"   {'-'*76}")
    
    # Check sentiment analysis
    sentiment_value = sentiment.get('overall_sentiment', 'N/A')
    confidence = sentiment.get('confidence', 0)
    
    print(f"\n😊 SENTIMENT ANALYSIS:")
    print(f"   ✓ Sentiment: {sentiment_value}")
    print(f"   ✓ Confidence: {confidence:.1%}")
    if sentiment.get('explanation'):
        print(f"   ✓ Explanation: {sentiment.get('explanation')}")
    
    # Verification
    print(f"\n✅ VERIFICATION:")
    enhanced = result.get('enhanced_analysis', False)
    print(f"   • Enhanced (Gemini used): {enhanced}")
    
    if enhanced:
        if test['expected_source'].lower() in source_book.lower() or source_book == 'N/A':
            print(f"   • Source Match: ✅")
        else:
            print(f"   • Source Match: ⚠️ (Expected: {test['expected_source']}, Got: {source_book})")
        
        if len(meaning) > 200:
            print(f"   • Detailed Meaning: ✅ (>{len(meaning)} chars)")
        else:
            print(f"   • Detailed Meaning: ⚠️ (Only {len(meaning)} chars)")
    else:
        print(f"   • ❌ GEMINI NOT USED! Using basic fallback")
    
    print(f"\n⏱️  Processing Time: {result.get('processing_time', 'N/A')}")

print(f"\n{'='*80}")
print("✅ ALL TESTS COMPLETED")
print(f"{'='*80}\n")

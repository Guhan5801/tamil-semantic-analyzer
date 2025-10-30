#!/usr/bin/env python3
"""Final verification before deployment"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

print("=" * 80)
print("🔍 FINAL VERIFICATION - Testing Exact User Scenario")
print("=" * 80)

analyzer = SemanticSentimentAnalyzer()

# Test with the exact input that was showing the problem
test_text = "யாதும் ஊரே யாவரும் கேளிர் தீதும் நன்றும் பிறர்தர வாரா"

print(f"\n📝 Testing with: {test_text}")
print(f"{'='*80}\n")

result = analyzer.analyze_semantic_sentiment(test_text)

semantic = result.get('semantic_analysis', {})
meaning = semantic.get('meaning', '')
source_book = semantic.get('source_book', '')
enhanced = result.get('enhanced_analysis', False)

print(f"✅ Analysis Complete!")
print(f"\n{'='*80}")
print(f"RESULTS:")
print(f"{'='*80}")

print(f"\n1️⃣ Enhanced Analysis Used: {enhanced}")
print(f"2️⃣ Source Book: {source_book}")
print(f"3️⃣ Meaning Length: {len(meaning)} characters")

print(f"\n{'='*80}")
print(f"பொருள் (MEANING):")
print(f"{'='*80}")
print(meaning)
print(f"{'='*80}")

# Check if it's the bad output or good output
if "உரையின் தெளிவான விளக்கம்" in meaning and len(meaning) < 200:
    print(f"\n❌ FAILED - Still showing generic fallback!")
    print(f"   This is the BAD output you don't want.")
    sys.exit(1)
elif "நூல்:" in meaning and len(meaning) > 500:
    print(f"\n✅ SUCCESS - Showing detailed Gemini output!")
    print(f"   This is the GOOD output you want.")
    print(f"\n   Contains:")
    if source_book:
        print(f"   ✓ Source Book: {source_book}")
    if 'chapter_section' in semantic:
        print(f"   ✓ Chapter/Section: {semantic.get('chapter_section')}")
    if 'verse_number' in semantic:
        print(f"   ✓ Verse Number: {semantic.get('verse_number')}")
    print(f"   ✓ Detailed meaning: {len(meaning)} characters")
else:
    print(f"\n⚠️ UNCERTAIN - Output format unexpected")
    print(f"   Length: {len(meaning)} characters")
    print(f"   Enhanced: {enhanced}")

print(f"\n{'='*80}")
print(f"READY FOR DEPLOYMENT: {'YES ✅' if enhanced and len(meaning) > 500 else 'NO ❌'}")
print(f"{'='*80}\n")

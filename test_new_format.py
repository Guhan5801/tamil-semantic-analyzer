#!/usr/bin/env python3
"""
Test the new பொருள் format with "பொருள்:" and "சுருக்கமாக:" sections
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

print("=" * 80)
print("🧪 TESTING NEW பொருள் FORMAT")
print("=" * 80)

# Initialize analyzer
analyzer = SemanticSentimentAnalyzer()

# Test with the exact input you provided
test_input = "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு"

print(f"\n📝 Input: {test_input}")
print("\n⏳ Analyzing with Gemini...")

result = analyzer.analyze_semantic_sentiment(test_input)

print("\n" + "=" * 80)
print("📊 RESULTS")
print("=" * 80)

# Check if Gemini was used
enhanced = result.get('enhanced_analysis', False)
print(f"\n✅ Gemini Used: {enhanced}")

# Get the semantic analysis
semantic = result.get('semantic_analysis', {})
meaning = semantic.get('meaning', '')
source = semantic.get('source_book', '')

print(f"\n📚 Source Book: {source}")
print(f"\n📏 Meaning Length: {len(meaning)} characters")

print("\n" + "=" * 80)
print("📖 தமிழ் பொருள் (TAMIL MEANING)")
print("=" * 80)
print(meaning)

# Check if it has the required format
has_porul = 'பொருள்:' in meaning
has_summary = 'சுருக்கமாக:' in meaning

print("\n" + "=" * 80)
print("✓ FORMAT VALIDATION")
print("=" * 80)
print(f"{'✅' if has_porul else '❌'} Contains 'பொருள்:' section")
print(f"{'✅' if has_summary else '❌'} Contains 'சுருக்கமாக:' section")

if has_porul and has_summary:
    print("\n🎉 SUCCESS! Format matches your requirement!")
else:
    print("\n⚠️  Format does not match. Checking what we got...")

# Show other fields
print("\n" + "=" * 80)
print("📋 OTHER ANALYSIS FIELDS")
print("=" * 80)
print(f"Sentiment: {result.get('sentiment_analysis', {}).get('overall_sentiment', 'N/A')}")
print(f"Theme: {semantic.get('theme', 'N/A')}")

if result.get('gemini_error'):
    print(f"\n❌ Gemini Error: {result['gemini_error']}")

print("\n" + "=" * 80)

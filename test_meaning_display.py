#!/usr/bin/env python3
"""
Test what's actually in the meaning field
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

print("=" * 80)
print("🧪 TESTING WHAT'S IN THE MEANING FIELD")
print("=" * 80)

# Initialize analyzer
analyzer = SemanticSentimentAnalyzer()

# Test with the exact input
test_input = "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு"

print(f"\n📝 Input: {test_input}")
print("\n⏳ Analyzing...")

result = analyzer.analyze_semantic_sentiment(test_input)

print("\n" + "=" * 80)
print("📊 FULL RESULT JSON")
print("=" * 80)
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\n" + "=" * 80)
print("📖 SEMANTIC ANALYSIS SECTION")
print("=" * 80)
semantic = result.get('semantic_analysis', {})
print(json.dumps(semantic, ensure_ascii=False, indent=2))

print("\n" + "=" * 80)
print("💡 MEANING FIELD VALUE")
print("=" * 80)
meaning = semantic.get('meaning', '')
print(f"Type: {type(meaning)}")
print(f"Length: {len(meaning)} characters")
print(f"\nContent:\n{meaning}")

print("\n" + "=" * 80)
print("✓ CHECKS")
print("=" * 80)
print(f"enhanced_analysis flag: {result.get('enhanced_analysis', False)}")
print(f"gemini_error present: {'gemini_error' in result}")
print(f"Has பொருள்: section: {'பொருள்:' in meaning}")
print(f"Has சுருக்கமாக: section: {'சுருக்கமாக:' in meaning}")
print(f"Has source book info: {'நூல்:' in meaning}")

print("\n" + "=" * 80)

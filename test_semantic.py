#!/usr/bin/env python3
"""
Test the semantic sentiment analyzer directly
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
import json

def test_semantic_sentiment():
    """Test the semantic sentiment analyzer"""
    
    print("🧪 தமிழ் பொருள் மற்றும் உணர்வு ஆய்வு சோதனை")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = SemanticSentimentAnalyzer()
    
    # Test with Tamil text
    test_texts = [
        "நான் மிகவும் மகிழ்ச்சியாக இருக்கிறேன்",  # I am very happy
        "இன்று மிகவும் சோகமான நாள்",  # Today is a very sad day
        "வானம் நீலமாக இருக்கிறது மற்றும் பறவைகள் பாடுகின்றன"  # The sky is blue and birds are singing
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 சோதனை {i}: {text}")
        print("-" * 40)
        
        try:
            result = analyzer.analyze_semantic_sentiment(text)
            
            # Display results
            print(f"🧠 பொருள் ஆய்வு:")
            semantic = result.get('semantic_analysis', {})
            print(f"   • வார்த்தைகள் எண்ணிக்கை: {semantic.get('word_count', 0)}")
            print(f"   • தமிழ் வார்த்தைகள்: {semantic.get('tamil_word_count', 0)}")
            print(f"   • மொழி: {semantic.get('language_detected', 'unknown')}")
            print(f"   • சிக்கலான தன்மை: {semantic.get('text_complexity', 'unknown')}")
            print(f"   • விषயங்கள்: {', '.join(semantic.get('key_themes', []))}")
            
            print(f"\n💭 உணர்வு ஆய்வு:")
            sentiment = result.get('sentiment_analysis', {})
            print(f"   • ஒட்டுமொத்த உணர்வு: {sentiment.get('overall_sentiment', 'unknown')}")
            print(f"   • நம்பிக்கை: {sentiment.get('confidence', 0):.2%}")
            
            print(f"\n⏱️ செயலாக்க நேரம்: {result.get('processing_time', '0.00s')}")
            print(f"🔧 மேம்பட்ட ஆய்வு: {'✅' if result.get('enhanced_analysis', False) else '❌'}")
            
        except Exception as e:
            print(f"❌ பிழை: {e}")
    
    print("\n" + "=" * 50)
    print("✅ சோதனை முடிந்தது!")

if __name__ == "__main__":
    test_semantic_sentiment()
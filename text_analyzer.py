#!/usr/bin/env python3
"""
Tamil Text Analysis - Command Line Interface
Direct text input for semantic and sentiment analysis
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

def print_banner():
    """Print application banner"""
    print("🧠💭 Tamil Semantic & Sentiment Analysis")
    print("=" * 50)
    print("📝 Enter Tamil text for instant analysis")
    print("💡 Type 'quit' or 'exit' to close")
    print("🚀 Type 'examples' to see sample texts")
    print("=" * 50)

def print_examples():
    """Print example texts"""
    examples = [
        ("😊 Happy", "நான் மிகவும் மகிழ்ச்சியாக இருக்கிறேன்"),
        ("😢 Sad", "இன்று மிகவும் சோகமான நாள்"),
        ("🌤️ Nature", "வானம் நீலமாக இருக்கிறது மற்றும் பறவைகள் பாடுகின்றன"),
        ("👨‍👩‍👧‍👦 Family", "என் குடும்பம் என்னுடைய வலிமை"),
        ("🙏 Spiritual", "கடவுள் அனைவரையும் காப்பாற்றுவார்"),
        ("📚 Education", "கல்வி என்பது வாழ்க்கையின் ஒளி"),
        ("💪 Motivation", "முயற்சி உடையார் இகழ்ச்சி அடையார்"),
        ("🌸 Beauty", "பூக்கள் மணம் வீசுகின்றன"),
    ]
    
    print("\n📚 Example Texts:")
    print("-" * 30)
    for i, (category, text) in enumerate(examples, 1):
        print(f"{i}. {category}: {text}")
    print("-" * 30)
    print("💡 Copy any example above to analyze")

def format_results(result):
    """Format analysis results for display"""
    semantic = result.get('semantic_analysis', {})
    sentiment = result.get('sentiment_analysis', {})
    
    print("\n📊 ANALYSIS RESULTS")
    print("=" * 50)
    
    # Semantic Analysis
    print("🧠 SEMANTIC ANALYSIS:")
    print(f"   • Word Count: {semantic.get('word_count', 0)}")
    print(f"   • Tamil Words: {semantic.get('tamil_word_count', 0)}")
    print(f"   • Language: {semantic.get('language_detected', 'unknown')}")
    print(f"   • Complexity: {semantic.get('text_complexity', 'unknown')}")
    
    themes = semantic.get('key_themes', [])
    if themes:
        print(f"   • Themes: {', '.join(themes)}")
    else:
        print("   • Themes: None detected")
    
    print(f"   • Semantic Density: {semantic.get('semantic_density', 0):.2%}")
    
    # Sentiment Analysis
    print("\n💭 SENTIMENT ANALYSIS:")
    overall = sentiment.get('overall_sentiment', 'unknown')
    confidence = sentiment.get('confidence', 0)
    intensity = sentiment.get('emotional_intensity', 0)
    
    # Color code sentiment
    sentiment_emoji = {
        'positive': '😊',
        'negative': '😢', 
        'neutral': '😐'
    }.get(overall, '❓')
    
    print(f"   • Overall Sentiment: {sentiment_emoji} {overall.upper()}")
    print(f"   • Confidence: {confidence:.1%}")
    print(f"   • Emotional Intensity: {intensity:.1%}")
    
    # Sentiment Distribution
    distribution = sentiment.get('sentiment_distribution', {})
    if distribution:
        print("   • Distribution:")
        print(f"     - Positive: {distribution.get('positive', 0):.1%}")
        print(f"     - Negative: {distribution.get('negative', 0):.1%}")
        print(f"     - Neutral: {distribution.get('neutral', 0):.1%}")
    
    # Processing Info
    processing_time = result.get('processing_time', 0)
    gemini_enhanced = result.get('gemini_enhanced', False)
    
    print(f"\n⏱️ Processing Time: {processing_time:.2f}s")
    print(f"Enhanced: {'✅ YES' if gemini_enhanced else '❌ NO'}")
    print("=" * 50)

def main():
    """Main interactive loop"""
    print_banner()
    
    # Initialize analyzer
    try:
        print("🔄 Initializing analyzer...")
        analyzer = SemanticSentimentAnalyzer()
        print("✅ Ready for analysis!")
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        return
    
    while True:
        try:
            # Get user input
            print(f"\n📝 Enter Tamil text (or command):")
            user_input = input(">>> ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            # Check for examples command
            if user_input.lower() in ['examples', 'example', 'ex']:
                print_examples()
                continue
            
            # Check for empty input
            if not user_input:
                print("⚠️ Please enter some text to analyze")
                continue
            
            # Perform analysis
            print(f"🔄 Analyzing: {user_input[:50]}...")
            result = analyzer.analyze_semantic_sentiment(user_input)
            
            # Display results
            format_results(result)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
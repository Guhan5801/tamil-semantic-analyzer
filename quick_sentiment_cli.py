#!/usr/bin/env python3
"""
Command Line Interface for Tamil Semantic & Sentiment Analysis
Quick text input and analysis tool
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
import json

def print_banner():
    """Print application banner"""
    print("🧠💭 Tamil Semantic & Sentiment Analysis CLI")
    print("=" * 50)
    print("📝 Enter Tamil text for instant analysis")
    print("🔤 Supports Tamil, Hindi, and English text")
    print("Enhanced with external model (if configured)")
    print("💡 Type 'quit', 'exit', or 'q' to exit")
    print("=" * 50)

def format_sentiment_output(analysis):
    """Format sentiment analysis output in a readable way"""
    
    semantic = analysis.get('semantic_analysis', {})
    sentiment = analysis.get('sentiment_analysis', {})
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)
    
    # Input text
    print(f"📝 Input Text: {analysis.get('input_text', '')}")
    print()
    
    # Semantic Analysis
    print("🧠 SEMANTIC ANALYSIS:")
    print(f"   📊 Word Count: {semantic.get('word_count', 0)}")
    print(f"   🔤 Tamil Words: {semantic.get('tamil_word_count', 0)}")
    print(f"   🌐 Language: {semantic.get('language_detected', 'unknown').title()}")
    print(f"   📈 Complexity: {semantic.get('text_complexity', 'unknown').title()}")
    
    themes = semantic.get('key_themes', [])
    if themes:
        print(f"   🎯 Themes: {', '.join(themes).title()}")
    else:
        print("   🎯 Themes: None detected")
    print()
    
    # Sentiment Analysis
    print("💭 SENTIMENT ANALYSIS:")
    
    # Overall sentiment with emoji
    overall = sentiment.get('overall_sentiment', 'neutral')
    sentiment_emoji = "😊" if overall == 'positive' else "😔" if overall == 'negative' else "😐"
    print(f"   {sentiment_emoji} Overall Sentiment: {overall.title()}")
    
    # Confidence with bar
    confidence = sentiment.get('confidence', 0) * 100
    print(f"   🎯 Confidence: {confidence:.1f}%")
    
    # Emotional intensity
    intensity = sentiment.get('emotional_intensity', 0) * 100
    print(f"   🔥 Emotional Intensity: {intensity:.1f}%")
    
    # Sentiment strength
    strength = sentiment.get('sentiment_strength', 'unknown')
    print(f"   💪 Sentiment Strength: {strength.title()}")
    
    # Detailed breakdown
    distribution = sentiment.get('sentiment_distribution', {})
    if distribution:
        print("\n   📊 Sentiment Breakdown:")
        print(f"      😊 Positive: {distribution.get('positive', 0) * 100:.1f}%")
        print(f"      😔 Negative: {distribution.get('negative', 0) * 100:.1f}%")
        print(f"      😐 Neutral: {distribution.get('neutral', 0) * 100:.1f}%")
    
    # Indicators found
    pos_indicators = sentiment.get('positive_indicators', 0)
    neg_indicators = sentiment.get('negative_indicators', 0)
    neutral_indicators = sentiment.get('neutral_indicators', 0)
    
    if pos_indicators > 0 or neg_indicators > 0 or neutral_indicators > 0:
        print("\n   🔍 Emotional Words Found:")
        if pos_indicators > 0:
            print(f"      😊 Positive words: {pos_indicators}")
        if neg_indicators > 0:
            print(f"      😔 Negative words: {neg_indicators}")
        if neutral_indicators > 0:
            print(f"      😐 Neutral words: {neutral_indicators}")
    
    # Intensifiers
    intensifiers = sentiment.get('intensifier_count', 0)
    if intensifiers > 0:
        print(f"\n   🚀 Intensifier words found: {intensifiers}")
    
    # Processing info
    processing_time = analysis.get('processing_time', 0)
    enhanced_analysis = analysis.get('enhanced_analysis', False)
    
    print(f"\n⏱️ Processing Time: {processing_time:.2f}s")
    print(f"Enhanced: {'✅ Yes' if enhanced_analysis else '❌ No'}")
    
    print("=" * 60)

def main():
    """Main CLI interface"""
    
    print_banner()
    
    # Initialize analyzer
    try:
        print("🔄 Initializing analyzer...")
        analyzer = SemanticSentimentAnalyzer()
        print("✅ Ready for analysis!\n")
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        return
    
    # Main input loop
    while True:
        try:
            # Get user input
            print("📝 Enter Tamil text (or 'quit' to exit):")
            text = input("➤ ").strip()
            
            # Check for exit commands
            if text.lower() in ['quit', 'exit', 'q', '']:
                print("\n👋 Thank you for using Tamil Semantic Analysis!")
                break
            
            # Analyze text
            print("\n🔄 Analyzing text...")
            try:
                result = analyzer.analyze_semantic_sentiment(text)
                format_sentiment_output(result)
                
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
            
            print("\n" + "-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
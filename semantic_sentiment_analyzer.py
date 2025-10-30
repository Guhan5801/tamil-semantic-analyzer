#!/usr/bin/env python3
"""
Optimized Semantic and Sentimental Analyzer for Tamil Text
Provides focused semantic and sentiment analysis with performance optimizations
"""

import logging
import time
from typing import Dict, Any
import re
import hashlib
from functools import lru_cache
from config import Config

# Import Gemini integration if available
try:
    from gemini_integration import GeminiCulturalAnalyzer
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    GeminiCulturalAnalyzer = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticSentimentAnalyzer:
    """Optimized analyzer for semantic and sentimental analysis with caching"""
    
    def __init__(self):
        self.gemini_analyzer = None
        self.gemini_enabled = Config.ENABLE_GEMINI_ENHANCEMENT and GEMINI_AVAILABLE and Config.is_gemini_available()
        self.analysis_cache = {}  # Simple in-memory cache
        self.cache_max_size = 100  # Maximum cache size
        
        if self.gemini_enabled and GeminiCulturalAnalyzer is not None:
            try:
                self.gemini_analyzer = GeminiCulturalAnalyzer()
                logger.info("✅ Enhanced Semantic Analyzer initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize enhanced analyzer: {str(e)}")
                self.gemini_enabled = False
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _clean_cache(self):
        """Clean cache if it exceeds maximum size"""
        if len(self.analysis_cache) > self.cache_max_size:
            # Remove oldest 20% of entries
            items_to_remove = len(self.analysis_cache) // 5
            keys_to_remove = list(self.analysis_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.analysis_cache[key]
    
    def analyze_semantic_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for semantic meaning and sentiment with caching
        Returns focused results without cultural context
        """
        # Check cache first
        cache_key = self._get_cache_key(text)
        if cache_key in self.analysis_cache:
            logger.info(f"Cache hit for analysis of {len(text)} characters")
            cached_result = self.analysis_cache[cache_key].copy()
            cached_result['cached'] = True
            cached_result['processing_time'] = "0.1s (cached)"
            return cached_result
        
        logger.info(f"Starting semantic and sentiment analysis for {len(text)} characters")
        start_time = time.time()
        
        # Initialize result structure
        analysis_result = {
            'input_text': text,
            'semantic_analysis': {},
            'sentiment_analysis': {},
            'enhanced_analysis': False,
            'processing_time': 0,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Basic semantic analysis
        analysis_result['semantic_analysis'] = self._basic_semantic_analysis(text)
        
        # Basic sentiment analysis
        analysis_result['sentiment_analysis'] = self._basic_sentiment_analysis(text)
        
        # Enhanced analysis with advanced NLP if available
        if self.gemini_enabled and self.gemini_analyzer:
            logger.info("Enhancing with conversational Gemini analysis...")
            try:
                enhanced_analysis = self._get_gemini_semantic_sentiment(text)
                if enhanced_analysis:
                    # Update with enhanced results
                    if enhanced_analysis.get('semantic'):
                        analysis_result['semantic_analysis'].update(enhanced_analysis['semantic'])
                    if enhanced_analysis.get('sentiment'):
                        analysis_result['sentiment_analysis'].update(enhanced_analysis['sentiment'])
                    analysis_result['enhanced_analysis'] = True
                    logger.info("✅ Conversational Gemini enhancement completed")
            except Exception as e:
                logger.warning(f"⚠️ Gemini enhancement failed: {str(e)}")
                analysis_result['gemini_error'] = str(e)
        
        processing_time = time.time() - start_time
        analysis_result['processing_time'] = f"{processing_time:.2f}s"
        
        # Cache the result for future use
        analysis_result['cached'] = False
        self.analysis_cache[cache_key] = analysis_result.copy()
        self._clean_cache()
        
        logger.info(f"Semantic and sentiment analysis completed in {processing_time:.2f}s")
        
        return analysis_result
    
    def _basic_semantic_analysis(self, text: str) -> Dict[str, Any]:
        """Basic semantic analysis without Gemini (Tamil-only outputs)"""
        
        # Improved word count for Tamil text
        # Split by spaces and punctuation, filter empty strings
        words = [word.strip() for word in re.split(r'[\s\.\,\!\?\;\:]+', text) if word.strip()]
        
        # Count Tamil words more accurately
        tamil_words = []
        for word in words:
            if re.search(r'[அ-ஹ]', word):  # Contains Tamil characters
                tamil_words.append(word)
        
        # Basic semantic categories
        semantic_analysis = {
            'word_count': len(words),
            'tamil_word_count': len(tamil_words),
            'character_count': len(text),
            'language_detected': 'tamil' if len(tamil_words) > len(words) / 2 else 'mixed',
            'text_complexity': 'simple' if len(words) < 10 else 'moderate' if len(words) < 25 else 'complex',
            'key_themes': self._extract_basic_themes(text),
            'semantic_density': len(tamil_words) / len(text) if len(text) > 0 else 0,
            # Produce a clearer Tamil-only explanation
            'meaning': self._generate_basic_meaning(text, words, tamil_words),
        }
        
        return semantic_analysis
    
    def _basic_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis without Gemini"""
        
        # Enhanced sentiment indicators for Tamil
        positive_indicators = [
            'நல்ல', 'அழগு', 'மகிழ்ச்சி', 'சந்தோஷம்', 'வெற்றி', 'பெருமை', 'அன்பு', 'நன்மை',
            'खुशी', 'प्रेम', 'सुंदर', 'अच्छा', 'खुश', 'प्रसन्न', 'सफलता', 'गर्व',  # Hindi
            'happy', 'love', 'beautiful', 'good', 'joy', 'success', 'pride', 'wonderful',
            'excellent', 'amazing', 'fantastic', 'great', 'awesome', 'brilliant',
            'வெற்றி', 'இனிமை', 'பாராட்டு', 'பாசம்', 'ஆனந்தம்', 'ஆரோக்கியம்', 'ஆசீர்வாதம்'
        ]
        
        negative_indicators = [
            'துன்பம்', 'கோபம்', 'வருத்தம்', 'பயம்', 'கஷ்டம்', 'தோல்வி', 'சோகம்', 'வேதனை',
            'दुख', 'गुस्सा', 'भय', 'चिंता', 'परेशान', 'गम', 'दर्द', 'कष्ट',  # Hindi
            'sad', 'angry', 'fear', 'worry', 'trouble', 'pain', 'sorrow', 'grief',
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'angry',
            'நோய்', 'வன்மை', 'எரிச்சல்', 'கவலை', 'அழுகை', 'குற்றம்', 'பாவம்'
        ]
        
        neutral_indicators = [
            'சாதாரண', 'நடுநிலை', 'சமம்', 'இயல்பு', 'सामान्य', 'normal', 'okay', 'fine',
            'regular', 'usual', 'typical', 'average', 'standard'
        ]
        
        # Sentiment intensifiers
        intensifiers = [
            'மிகவும்', 'மிக', 'வளரே', 'मिকुंती', 'बहुत', 'बेहद', 'बिल्कुल',
            'very', 'extremely', 'really', 'quite', 'so', 'too', 'much'
        ]
        
        # Count sentiment indicators
        text_lower = text.lower()
        positive_score = sum(1 for word in positive_indicators if word.lower() in text_lower)
        negative_score = sum(1 for word in negative_indicators if word.lower() in text_lower)
        neutral_score = sum(1 for word in neutral_indicators if word.lower() in text_lower)
        
        # Check for intensifiers
        intensifier_count = sum(1 for word in intensifiers if word.lower() in text_lower)
        intensity_multiplier = 1 + (intensifier_count * 0.3)  # 30% boost per intensifier
        
        total_score = positive_score + negative_score + neutral_score
        
        # Determine sentiment
        if total_score == 0:
            sentiment = 'neutral'
            confidence = 0.5
        elif positive_score > negative_score:
            sentiment = 'positive'
            confidence = (positive_score / total_score) * intensity_multiplier
        elif negative_score > positive_score:
            sentiment = 'negative' 
            confidence = (negative_score / total_score) * intensity_multiplier
        else:
            sentiment = 'neutral'
            confidence = (neutral_score / total_score) if neutral_score > 0 else 0.5
        
        # Cap confidence at 1.0
        confidence = min(1.0, confidence)
        
        # Basic sentiment analysis
        sentiment_analysis = {
            'overall_sentiment': sentiment,
            'confidence': confidence,
            'positive_indicators': positive_score,
            'negative_indicators': negative_score,
            'neutral_indicators': neutral_score,
            'intensifier_count': intensifier_count,
            'sentiment_strength': 'strong' if confidence > 0.7 else 'moderate' if confidence > 0.4 else 'weak',
            'detailed_analysis': {
                'has_intensifiers': intensifier_count > 0,
                'sentiment_words_found': positive_score + negative_score,
                'sentiment_clarity': 'clear' if abs(positive_score - negative_score) > 1 else 'mixed',
                'dominant_sentiment': sentiment if sentiment != 'neutral' else 'balanced'
            }
        }
        
        return sentiment_analysis
    
    def _generate_basic_meaning(self, text: str, words: list, tamil_words: list) -> str:
        """Generate a clearer Tamil-only explanation of the text.
        This is heuristic and lightweight to keep serverless fast. If Gemini is enabled,
        enhanced results will further improve clarity via _get_gemini_semantic_sentiment.
        """
        
        # Common Tamil greetings and their meanings
        meaning_patterns = {
            'வணக்கம்': 'வணக்கம் என்பது மரியாதையான வாழ்த்து',
            'நன்றி': 'நன்றி என்பது நன்றி தெரிவிக்கும் சொல்',
            'மன்னிக்கவும்': 'மன்னிப்பு கேட்கும் சொல்',
            'குடும்பம்': 'குடும்ப உறவுகளைப் பற்றிய உரை',
            'அன்பு': 'அன்பு மற்றும் பாசத்தை வெளிப்படுத்தும் உரை',
            'கல்வி': 'கல்வி மற்றும் கற்றல் பற்றிய உரை',
            'நண்பர்': 'நட்பு மற்றும் நண்பர்களைப் பற்றிய உரை',
            'இன்று': 'நாள் மற்றும் நேரத்தைப் பற்றிய குறிப்பு',
            'நல்ல': 'நேர்மறையான குணங்களை விவரிக்கும் உரை'
        }
        
        # Check for specific patterns (quick wins)
        for pattern, meaning in meaning_patterns.items():
            if pattern in text:
                return meaning
        
        # Construct a more explicit explanation in Tamil based on length & cues
        sentences = [s.strip() for s in re.split(r'[\.!?\n]+', text) if s.strip()]
        themes = self._extract_basic_themes(text)

        prefix = 'உரையின் தெளிவான விளக்கம்: '
        # Short texts
        if len(words) <= 5:
            return prefix + 'குறுகிய தமிழ் சொற்றொடர்/வாக்கியம். உரை சுருக்கமாக அதன் கருத்தை வெளிப்படுத்துகிறது.'
        # Medium texts
        if len(words) <= 20:
            detail = 'இந்த உரை சுருக்கமாக ஒரு எண்ணத்தை விவரிக்கிறது.'
            if themes:
                detail += f" இது முக்கியமாக {', '.join(themes)} தொடர்பான கருத்துகளைத் தொடுகிறது."
            if len(sentences) >= 2:
                detail += ' வாக்கியங்களின் ஒழுங்கு தெளிவாக உள்ளது.'
            return prefix + detail
        # Long texts
        detail = 'இந்த உரை விரிவாக ஒரு கருத்தை விளக்குகிறது.'
        if themes:
            detail += f" பிரதான தீம்கள்: {', '.join(themes)}."
        if len(sentences) >= 3:
            detail += f" மொத்தம் {len(sentences)} பகுதி/வாக்கியங்களாக தகவல் படிகட்டாக வழங்கப்பட்டுள்ளது."
        detail += ' உள்ளடக்கத்தின் பொருள், சூழல், நோக்கம் ஆகியவை தொடர்ச்சியாக விளக்கப்பட்டுள்ளன.'
        return prefix + detail
    
    def _extract_basic_themes(self, text: str) -> list:
        """Extract basic themes from text"""
        themes = []
        
        # Define theme keywords
        theme_keywords = {
            'family': ['குடும்பம்', 'தாய்', 'தந்தை', 'மகன்', 'மகள்', 'சகோதரன்', 'சகோதரி'],
            'nature': ['மரம்', 'நதி', 'மலை', 'கடல்', 'வானம்', 'மழை', 'காற்று', 'சூரியன்'],
            'spirituality': ['கடவுள்', 'பிரார்த்தனை', 'வணக்கம்', 'பக்தி', 'தர்மம்'],
            'society': ['மக்கள்', 'நாடு', 'கிராமம்', 'நகரம்', 'சமுதாயம்']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def _get_gemini_semantic_sentiment(self, text: str) -> Dict[str, Any]:
        """Get enhanced semantic and sentiment analysis from Gemini using conversational approach"""
        if not self.gemini_analyzer or not self.gemini_analyzer.is_available:
            return {}
        
        try:
            # Use the conversational meaning method
            response = self.gemini_analyzer.get_conversational_meaning(text)
            # If response has text content, process it
            if response and response.get('text'):
                response_text = response['text']
                # Clean the response text
                import json
                try:
                    clean_response = response_text.strip()
                    if clean_response.startswith('```json'):
                        clean_response = clean_response[7:-3]
                    elif clean_response.startswith('```'):
                        clean_response = clean_response[3:-3]
                    
                    parsed_response = json.loads(clean_response)
                    
                    # Convert to expected format with bilingual support
                    result = {
                        'semantic': {
                            # Tamil-only mapping; ignore any english field
                            'meaning': parsed_response.get('tamil_meaning', parsed_response.get('meaning', '')),
                            'explanation': parsed_response.get('explanation', ''),
                            'cultural_context': parsed_response.get('cultural_context', ''),
                            'themes': []
                        },
                        'sentiment': {
                            'overall_sentiment': parsed_response.get('sentiment', 'neutral'),
                            'confidence': 0.8,
                            'explanation': 'Gemini வழங்கிய உணர்வு ஆய்வு'
                        }
                    }
                    return result
                    
                except json.JSONDecodeError:
                    logger.warning("Failed to parse Gemini JSON response, using raw text")
                    # If JSON parsing fails, use the raw response as meaning
                    return {
                        'semantic': {
                            'meaning': response_text,  # Tamil text expected from Gemini configuration
                            'explanation': response_text,
                            'cultural_context': 'சூழல் பகுப்பாய்வு பெற இயலவில்லை',
                            'themes': []
                        },
                        'sentiment': {
                            'overall_sentiment': 'neutral',
                            'confidence': 0.7,
                            'explanation': 'அடிப்படை பகுப்பாய்வு'
                        }
                    }
            
        except Exception as e:
            logger.error(f"Enhanced semantic analysis failed: {e}")
            
        return {}
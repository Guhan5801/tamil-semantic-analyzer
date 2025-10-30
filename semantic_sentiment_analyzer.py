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
        
        logger.info(f"Initializing SemanticSentimentAnalyzer:")
        logger.info(f"  ENABLE_GEMINI_ENHANCEMENT = {Config.ENABLE_GEMINI_ENHANCEMENT}")
        logger.info(f"  GEMINI_AVAILABLE = {GEMINI_AVAILABLE}")
        logger.info(f"  is_gemini_available() = {Config.is_gemini_available()}")
        logger.info(f"  gemini_enabled = {self.gemini_enabled}")
        
        if self.gemini_enabled and GeminiCulturalAnalyzer is not None:
            try:
                self.gemini_analyzer = GeminiCulturalAnalyzer()
                logger.info("✅ Enhanced Semantic Analyzer initialized with Gemini")
            except Exception as e:
                logger.error(f"❌ Failed to initialize enhanced analyzer: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                self.gemini_enabled = False
        else:
            logger.warning("⚠️ Gemini enhancement disabled")
    
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
        try:
            sentences = [s.strip() for s in re.split(r'[\.!?\n]+', text) if s.strip()]
            themes = self._extract_basic_themes(text)
        except Exception:
            # Fallback in case regex or theme extraction fails
            sentences = []
            themes = []

        prefix = 'உரையின் தெளிவான விளக்கம்: '
        # Short texts
        if len(words) <= 5:
            return prefix + 'குறுகிய தமிழ் சொற்றொடர்/வாக்கியம். உரை சுருக்கமாக அதன் கருத்தை வெளிப்படுத்துகிறது.'
        # Medium texts
        if len(words) <= 20:
            detail = 'இந்த உரை சுருக்கமாக ஒரு எண்ணத்தை விவரிக்கிறது.'
            if themes:
                detail += " இது முக்கியமாக " + ", ".join(str(t) for t in themes) + " தொடர்பான கருத்துகளைத் தொடுகிறது."
            if len(sentences) >= 2:
                detail += ' வாக்கியங்களின் ஒழுங்கு தெளிவாக உள்ளது.'
            return prefix + detail
        # Long texts
        detail = 'இந்த உரை விரிவாக ஒரு கருத்தை விளக்குகிறது.'
        if themes:
            detail += " பிரதான தீம்கள்: " + ", ".join(str(t) for t in themes) + "."
        if len(sentences) >= 3:
            detail += " மொத்தம் " + str(len(sentences)) + " பகுதி/வாக்கியங்களாக தகவல் படிகட்டாக வழங்கப்பட்டுள்ளது."
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
        """Get enhanced semantic and sentiment analysis from Gemini with literary source identification"""
        if not self.gemini_analyzer or not self.gemini_analyzer.is_available:
            return {}
        
        try:
            # Use the conversational meaning method for literary analysis
            response = self.gemini_analyzer.get_conversational_meaning(text)
            # If response has text content, process it
            if response and response.get('text'):
                response_text = response['text']
                # Clean the response text
                import json
                import re
                try:
                    clean_response = response_text.strip()
                    
                    # Remove markdown code blocks if present
                    if '```json' in clean_response:
                        # Extract content between ```json and ```
                        match = re.search(r'```json\s*(.*?)\s*```', clean_response, re.DOTALL)
                        if match:
                            clean_response = match.group(1)
                    elif '```' in clean_response:
                        # Extract content between ``` and ```
                        match = re.search(r'```\s*(.*?)\s*```', clean_response, re.DOTALL)
                        if match:
                            clean_response = match.group(1)
                    
                    clean_response = clean_response.strip()
                    parsed_response = json.loads(clean_response)
                    
                    # Build detailed meaning with literary source information
                    detailed_meaning = parsed_response.get('tamil_meaning', '')
                    
                    # Add source book information if available
                    source_parts = []
                    if parsed_response.get('source_book'):
                        source_parts.append("நூல்: " + parsed_response.get('source_book'))
                    if parsed_response.get('chapter_section'):
                        source_parts.append("பகுதி: " + parsed_response.get('chapter_section'))
                    if parsed_response.get('verse_number'):
                        source_parts.append("பாடல்: " + str(parsed_response.get('verse_number')))
                    
                    if source_parts:
                        detailed_meaning = " | ".join(source_parts) + "\n\n" + detailed_meaning
                    
                    # Add line-by-line if available (handle different data types)
                    if parsed_response.get('line_by_line'):
                        line_by_line = parsed_response.get('line_by_line')
                        if isinstance(line_by_line, str):
                            detailed_meaning += "\n\nவரிக்கு வரி விளக்கம்:\n" + line_by_line
                        elif isinstance(line_by_line, list):
                            detailed_meaning += "\n\nவரிக்கு வரி விளக்கம்:\n" + json.dumps(line_by_line, ensure_ascii=False, indent=2)
                        elif isinstance(line_by_line, dict):
                            detailed_meaning += "\n\nவரிக்கு வரி விளக்கம்:\n" + json.dumps(line_by_line, ensure_ascii=False, indent=2)
                    
                    # Add explanation if available
                    if parsed_response.get('explanation'):
                        explanation = parsed_response.get('explanation')
                        if isinstance(explanation, str):
                            detailed_meaning += "\n\nவிரிவான விளக்கம்:\n" + explanation
                        else:
                            detailed_meaning += "\n\nவிரிவான விளக்கம்:\n" + json.dumps(explanation, ensure_ascii=False, indent=2)
                    
                    # Add theme if available
                    if parsed_response.get('theme'):
                        theme = parsed_response.get('theme')
                        if isinstance(theme, str):
                            detailed_meaning += "\n\nகருத்து: " + theme
                        else:
                            detailed_meaning += "\n\nகருத்து: " + json.dumps(theme, ensure_ascii=False, indent=2)
                    
                    # Convert to expected format (Tamil-only)
                    result = {
                        'semantic': {
                            'meaning': detailed_meaning,
                            'source_book': parsed_response.get('source_book', ''),
                            'chapter_section': parsed_response.get('chapter_section', ''),
                            'verse_number': parsed_response.get('verse_number', ''),
                            'explanation': parsed_response.get('explanation', ''),
                            'theme': parsed_response.get('theme', ''),
                            'themes': []
                        },
                        'sentiment': {
                            'overall_sentiment': parsed_response.get('sentiment', 'neutral'),
                            'confidence': 0.9,
                            'explanation': 'Gemini AI மூலம் பகுப்பாய்வு செய்யப்பட்டது'
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
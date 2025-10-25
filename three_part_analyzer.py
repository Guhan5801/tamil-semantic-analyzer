#!/usr/bin/env python3
"""
Enhanced Three-Part Tamil Text Analyzer
Provides: Semantic Analysis, Tamil Translation, and Tamil Meaning Explanation
"""

import logging
import time
import re
import hashlib
from typing import Dict, Any, Optional
import google.generativeai as genai
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreePartTamilAnalyzer:
    """Enhanced analyzer providing semantic analysis, Tamil translation, and meaning explanation"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = 'gemini-2.5-flash'
        self.analysis_cache = {}
        self.cache_max_size = 100
        
        # Configure Gemini API
        if self.api_key:
            genai.configure(api_key=self.api_key)
            try:
                self.model = genai.GenerativeModel(self.model_name)
                self.is_available = True
                logger.info("✅ Three-Part Tamil Analyzer initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini model: {str(e)}")
                self.is_available = False
                self.model = None
        else:
            self.is_available = False
            self.model = None
            logger.warning("⚠️ Gemini API key not configured")
    
    def analyze_text_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive three-part analysis:
        1. Semantic analysis and tone
        2. Tamil translation
        3. Simple Tamil meaning explanation
        """
        
        start_time = time.time()
        
        # Check cache first
        cache_key = self._get_cache_key(text)
        if cache_key in self.analysis_cache:
            cached_result = self.analysis_cache[cache_key].copy()
            cached_result['cached'] = True
            cached_result['processing_time'] = "0.01s (cached)"
            logger.info("📋 Returning cached three-part analysis")
            return cached_result
        
        try:
            # Perform three-part analysis
            result = self._perform_three_part_analysis(text)
            
            processing_time = time.time() - start_time
            result['processing_time'] = f"{processing_time:.2f}s"
            result['cached'] = False
            
            # Cache the result
            self.analysis_cache[cache_key] = result.copy()
            self._clean_cache()
            
            logger.info(f"✅ Three-part analysis completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Three-part analysis failed: {str(e)}")
            return self._fallback_analysis(text)
    
    def _perform_three_part_analysis(self, text: str) -> Dict[str, Any]:
        """Perform enhanced three-part analysis"""
        
        if not self.is_available:
            return self._fallback_analysis(text)
        
        # Create comprehensive prompt for three-part analysis
        prompt = self._create_three_part_prompt(text)
        
        try:
            # Generate content using Gemini
            generation_config = genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=2000,
                top_p=0.8,
                top_k=40
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response.text:
                # Parse the structured response
                return self._parse_three_part_response(response.text, text)
            else:
                logger.warning("No response from Gemini - using fallback")
                return self._fallback_analysis(text)
                
        except Exception as e:
            logger.error(f"Model API error: {str(e)}")
            return self._fallback_analysis(text)
    
    def _create_three_part_prompt(self, text: str) -> str:
        """Create prompt for three-part analysis"""
        
        return f"""
Analyze the following text and provide a comprehensive three-part analysis with academic precision and cultural understanding.

**Input Text:** "{text}"

Please provide your analysis in the following structured format:

**PART 1: SEMANTIC ANALYSIS & TONE**
- Accurate meaning and interpretation of the text
- Emotional tone (positive, negative, neutral, mixed)
- Context and implied messages
- Literary devices or special language features
- Overall sentiment and mood

**PART 2: TAMIL TRANSLATION**
- Accurate Tamil translation of the input text
- Preserve the original meaning and tone
- Use appropriate Tamil vocabulary and grammar
- If the input is already in Tamil, provide alternative phrasing or formal version

**PART 3: SIMPLE TAMIL MEANING**
- Simple, easy-to-understand explanation in Tamil
- Break down complex concepts into basic terms
- Cultural context if relevant
- Practical everyday meaning
- Key message in simple Tamil words

Requirements for accuracy:
- Maintain semantic precision in translations
- Provide culturally appropriate interpretations
- Ensure grammatical correctness
- Use evidence-based analysis

---

Please structure your response exactly as shown above with clear sections.
"""
    
    def _parse_three_part_response(self, response_text: str, original_text: str) -> Dict[str, Any]:
        """Parse the structured response from Gemini"""
        
        try:
            # Initialize result structure
            result = {
                'input_text': original_text,
                'analysis_type': 'three_part_comprehensive',
                'timestamp': time.time()
            }
            
            # Split response into sections
            sections = response_text.split('**PART')
            
            if len(sections) >= 4:  # Original + 3 parts
                # Parse Part 1: Semantic Analysis & Tone
                part1 = sections[1] if len(sections) > 1 else ""
                result['semantic_analysis'] = self._extract_semantic_analysis(part1)
                
                # Parse Part 2: Tamil Translation
                part2 = sections[2] if len(sections) > 2 else ""
                result['tamil_translation'] = self._extract_tamil_translation(part2)
                
                # Parse Part 3: Simple Tamil Meaning
                part3 = sections[3] if len(sections) > 3 else ""
                result['tamil_meaning'] = self._extract_tamil_meaning(part3)
                
            else:
                # If structured parsing fails, extract from full text
                result = self._extract_from_full_text(response_text, original_text)
            
            # Add basic metrics
            result['text_metrics'] = self._calculate_text_metrics(original_text)
            result['language_detection'] = self._detect_language(original_text)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {str(e)}")
            return self._fallback_analysis(original_text)
    
    def _extract_semantic_analysis(self, part1_text: str) -> Dict[str, Any]:
        """Extract semantic analysis from Part 1"""
        
        # Clean up the text
        clean_text = part1_text.replace('1: SEMANTIC ANALYSIS & TONE**', '').strip()
        
        # Extract key information
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        
        semantic_info = {
            'meaning': '',
            'tone': 'neutral',
            'context': '',
            'sentiment': 'neutral',
            'literary_features': [],
            'raw_analysis': clean_text
        }
        
        # Parse the content for specific information
        for line in lines:
            line_lower = line.lower()
            if any(word in line_lower for word in ['meaning', 'interpretation']):
                semantic_info['meaning'] = line
            elif any(word in line_lower for word in ['tone', 'emotional']):
                semantic_info['tone'] = self._extract_tone(line)
            elif any(word in line_lower for word in ['context', 'implies']):
                semantic_info['context'] = line
            elif any(word in line_lower for word in ['sentiment', 'mood']):
                semantic_info['sentiment'] = self._extract_sentiment(line)
        
        # If no specific meaning found, use first substantial line
        if not semantic_info['meaning'] and lines:
            semantic_info['meaning'] = lines[0]
        
        return semantic_info
    
    def _extract_tamil_translation(self, part2_text: str) -> Dict[str, Any]:
        """Extract Tamil translation from Part 2"""
        
        clean_text = part2_text.replace('2: TAMIL TRANSLATION**', '').strip()
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        
        translation_info = {
            'translation': '',
            'alternative_translation': '',
            'translation_notes': '',
            'raw_translation': clean_text
        }
        
        # Extract Tamil text (contains Tamil Unicode characters)
        tamil_lines = []
        other_lines = []
        
        for line in lines:
            if re.search(r'[அ-ஹ]', line):  # Contains Tamil characters
                tamil_lines.append(line)
            else:
                other_lines.append(line)
        
        # Set primary translation
        if tamil_lines:
            translation_info['translation'] = tamil_lines[0]
            if len(tamil_lines) > 1:
                translation_info['alternative_translation'] = ' | '.join(tamil_lines[1:])
        
        # Set translation notes
        if other_lines:
            translation_info['translation_notes'] = ' '.join(other_lines)
        
        return translation_info
    
    def _extract_tamil_meaning(self, part3_text: str) -> Dict[str, Any]:
        """Extract simple Tamil meaning from Part 3"""
        
        clean_text = part3_text.replace('3: SIMPLE TAMIL MEANING**', '').strip()
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        
        meaning_info = {
            'simple_meaning': '',
            'cultural_context': '',
            'practical_meaning': '',
            'key_message': '',
            'raw_meaning': clean_text
        }
        
        # Extract Tamil explanations
        tamil_explanations = []
        english_explanations = []
        
        for line in lines:
            if re.search(r'[அ-ஹ]', line):
                tamil_explanations.append(line)
            else:
                english_explanations.append(line)
        
        # Set meanings
        if tamil_explanations:
            meaning_info['simple_meaning'] = tamil_explanations[0]
            if len(tamil_explanations) > 1:
                meaning_info['key_message'] = tamil_explanations[-1]
        
        if english_explanations:
            for line in english_explanations:
                line_lower = line.lower()
                if 'cultural' in line_lower:
                    meaning_info['cultural_context'] = line
                elif 'practical' in line_lower or 'everyday' in line_lower:
                    meaning_info['practical_meaning'] = line
        
        return meaning_info
    
    def _extract_tone(self, text: str) -> str:
        """Extract tone from text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['positive', 'happy', 'joyful', 'optimistic']):
            return 'positive'
        elif any(word in text_lower for word in ['negative', 'sad', 'angry', 'pessimistic']):
            return 'negative'
        elif any(word in text_lower for word in ['neutral', 'balanced', 'objective']):
            return 'neutral'
        elif any(word in text_lower for word in ['mixed', 'complex', 'varied']):
            return 'mixed'
        else:
            return 'neutral'
    
    def _extract_sentiment(self, text: str) -> str:
        """Extract sentiment from text"""
        return self._extract_tone(text)  # Same logic for now
    
    def _calculate_text_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate basic text metrics"""
        
        words = re.findall(r'\b\w+\b', text)
        tamil_chars = re.findall(r'[அ-ஹ]', text)
        
        return {
            'character_count': len(text),
            'word_count': len(words),
            'tamil_character_count': len(tamil_chars),
            'sentence_count': len(re.split(r'[.!?]+', text)),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0
        }
    
    def _detect_language(self, text: str) -> str:
        """Detect primary language of text"""
        
        tamil_chars = len(re.findall(r'[அ-ஹ]', text))
        total_chars = len(re.findall(r'[a-zA-Zஅ-ஹ]', text))
        
        if total_chars == 0:
            return 'unknown'
        
        tamil_ratio = tamil_chars / total_chars
        
        if tamil_ratio > 0.7:
            return 'tamil'
        elif tamil_ratio > 0.3:
            return 'mixed'
        else:
            return 'english'
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Provide fallback analysis when enhancement model is not available"""
        
        return {
            'input_text': text,
            'analysis_type': 'fallback_basic',
            'semantic_analysis': {
                'meaning': f"Basic analysis of: {text}",
                'tone': 'neutral',
                'sentiment': 'neutral',
                'raw_analysis': 'enhancement not available - basic analysis provided'
            },
            'tamil_translation': {
                'translation': text if re.search(r'[அ-ஹ]', text) else 'மொழிபெயர்ப்பு தேவை',
                'translation_notes': 'enhanced translation not available',
                'raw_translation': 'Fallback translation'
            },
            'tamil_meaning': {
                'simple_meaning': 'எளிய விளக்கம் கிடைக்கவில்லை',
                'key_message': 'விளக்கம் தற்போது கிடைக்கவில்லை',
                'raw_meaning': 'enhanced explanation not available'
            },
            'text_metrics': self._calculate_text_metrics(text),
            'language_detection': self._detect_language(text),
            'processing_time': '0.01s',
            'cached': False,
            'timestamp': time.time()
        }
    
    def _extract_from_full_text(self, response_text: str, original_text: str) -> Dict[str, Any]:
        """Extract information from full response text when structured parsing fails"""
        
        # Split by paragraphs and try to identify sections
        paragraphs = [p.strip() for p in response_text.split('\n\n') if p.strip()]
        
        result = {
            'input_text': original_text,
            'analysis_type': 'unstructured_extraction',
            'semantic_analysis': {
                'meaning': paragraphs[0] if paragraphs else 'Analysis unavailable',
                'tone': 'neutral',
                'raw_analysis': response_text
            },
            'tamil_translation': {
                'translation': self._find_tamil_in_text(response_text) or 'மொழிபெயர்ப்பு கிடைக்கவில்லை',
                'raw_translation': response_text
            },
            'tamil_meaning': {
                'simple_meaning': paragraphs[-1] if paragraphs else 'விளக்கம் கிடைக்கவில்லை',
                'raw_meaning': response_text
            },
            'text_metrics': self._calculate_text_metrics(original_text),
            'language_detection': self._detect_language(original_text),
            'timestamp': time.time()
        }
        
        return result
    
    def _find_tamil_in_text(self, text: str) -> str:
        """Find Tamil text in response"""
        
        lines = text.split('\n')
        for line in lines:
            if re.search(r'[அ-ஹ]', line):
                return line.strip()
        return ""
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _clean_cache(self):
        """Clean cache if it exceeds maximum size"""
        if len(self.analysis_cache) > self.cache_max_size:
            # Remove oldest entries (simple FIFO)
            keys_to_remove = list(self.analysis_cache.keys())[:-self.cache_max_size//2]
            for key in keys_to_remove:
                del self.analysis_cache[key]
            logger.info(f"🧹 Cache cleaned, removed {len(keys_to_remove)} entries")

# Initialize the analyzer
three_part_analyzer = ThreePartTamilAnalyzer()
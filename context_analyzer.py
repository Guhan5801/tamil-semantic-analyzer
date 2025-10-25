#!/usr/bin/env python3
"""
Context Analyzer for Tamil Literary Text
Analyzes extracted text and provides cultural context (Seiyul/Vilakkam)
"""

import logging
import time
from typing import Dict, List, Any, Optional
import re
from kambaramayanam_database import KambaramayanamDatabase
from config import Config

# Import external enhancement integration if available
try:
    from gemini_integration import GeminiCulturalAnalyzer
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    GeminiCulturalAnalyzer = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TamilContextAnalyzer:
    """Analyzes Tamil text and provides cultural context for Kambaramayanam content"""
    
    def __init__(self):
        self.database = KambaramayanamDatabase()
        self.confidence_threshold = Config.KAMBARAMAYANAM_CONFIDENCE_THRESHOLD
        
    # Initialize enhancement analyzer if available and configured
        self.gemini_analyzer = None
        self.gemini_enabled = Config.ENABLE_GEMINI_ENHANCEMENT and GEMINI_AVAILABLE and Config.is_gemini_available()
        
        if self.gemini_enabled and GeminiCulturalAnalyzer is not None:
            try:
                self.gemini_analyzer = GeminiCulturalAnalyzer()
                logger.info("✅ Cultural Analyzer integrated")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize enhancement analyzer: {str(e)}")
                self.gemini_enabled = False
        else:
            if not GEMINI_AVAILABLE:
                logger.info("ℹ️ enhancement integration not available (module not found)")
            elif not Config.is_gemini_available():
                logger.info("ℹ️ enhancement API not configured")
            else:
                logger.info("ℹ️ enhancement disabled in config")
        
        self.famous_keywords = {
            'அறம்': 'தர்மம், நீதி, நல்லொழுக்கம்',
            'இராமன்': 'அயோத்தி இளவரசன், மரியாதை புருஷோத்தமன்',
            'சீதை': 'இராமனின் மனைவி, பொறுமையின் அடையாளம்',
            'அனுமன்': 'இராமனின் பக்தன், வானர வீரன்',
            'ராவணன்': 'இலங்கை அரசன், வல்லமை மிக்கவன்',
            'கம்பன்': 'கம்பராமாயணத்தின் ஆசிரியர், மகாகவி',
            'வனவாசம்': 'காட்டில் வாழ்வு, துறவு நிலை',
            'அயோத்தி': 'இராமனின் தலைநகரம், நீதியின் இருப்பிடம்',
            'இலங்கை': 'ராவணனின் நாடு, செல்வச் செழிப்பின் இடம்'
        }
        logger.info("Tamil Context Analyzer initialized with cultural database")
    
    def analyze_text_context(self, extracted_text: str) -> Dict[str, Any]:
        """
        Main function to analyze extracted text and provide cultural context
        """
        logger.info(f"Analyzing text context for {len(extracted_text)} characters")
        start_time = time.time()
        
        if not extracted_text.strip():
            return {
                'is_kambaramayanam': False,
                'confidence': 0.0,
                'analysis': 'No text provided for analysis',
                'cultural_context': {},
                'processing_time': 0.0
            }
        
        # Step 1: Find matching verses
        verse_matches = self.database.find_matching_verses(extracted_text)
        
        # Step 2: Identify key cultural elements
        cultural_elements = self.identify_cultural_elements(extracted_text)
        
        # Step 3: Determine if it's Kambaramayanam content
        is_kambaramayanam, confidence = self.determine_kambaramayanam_content(
            verse_matches, cultural_elements, extracted_text
        )
        
        # Step 4: Generate comprehensive analysis
        analysis_result = self.generate_analysis(
            extracted_text, verse_matches, cultural_elements, is_kambaramayanam, confidence
        )
        
        # Step 5: Enhance with external model if available
        if self.gemini_enabled and self.gemini_analyzer:
            logger.info("Enhancing analysis with configured enhancement...")
            try:
                analysis_result = self.gemini_analyzer.enhance_cultural_context(
                    extracted_text, analysis_result
                )
                logger.info("✅ Enhancement completed")
            except Exception as e:
                logger.warning(f"⚠️ Enhancement failed: {str(e)}")
                analysis_result['enhancement_error'] = str(e)
        
        processing_time = time.time() - start_time
        analysis_result['processing_time'] = processing_time
        
        logger.info(f"Context analysis completed: {is_kambaramayanam} with {confidence:.2%} confidence")
        
        return analysis_result
    
    def identify_cultural_elements(self, text: str) -> Dict[str, Any]:
        """Identify cultural elements, characters, and concepts in the text"""
        
        elements = {
            'characters': [],
            'places': [],
            'concepts': [],
            'keywords': [],
            'literary_significance': []
        }
        
        # Clean text for analysis
        clean_text = text.lower()
        
        # Check for famous keywords
        for keyword, meaning in self.famous_keywords.items():
            if keyword in text:
                elements['keywords'].append({
                    'word': keyword,
                    'meaning': meaning,
                    'context': 'kambaramayanam'
                })
        
        # Character identification
        characters = ['இராமன்', 'சீதை', 'லட்சுமணன்', 'அனுமன்', 'ராவணன்', 'தசரதன்', 'கைகேயி', 'பரதன்', 'சத்துருக்னன்']
        for char in characters:
            if char in text:
                elements['characters'].append(char)
        
        # Place identification  
        places = ['அயோத்தி', 'இலங்கை', 'மிதிலை', 'கிஷ்கிந்தை', 'பஞ்சவடி']
        for place in places:
            if place in text:
                elements['places'].append(place)
        
        # Concept identification
        concepts = ['அறம்', 'தர்மம்', 'பக்தி', 'வீரம்', 'காதல்', 'கடமை', 'நீதி']
        for concept in concepts:
            if concept in text:
                elements['concepts'].append(concept)
        
        # Literary device identification
        if 'என்று' in text or 'எனக்' in text:
            elements['literary_significance'].append('உரையாடல்')
        if any(word in text for word in ['போல', 'மாதிரி', 'சமம்']):
            elements['literary_significance'].append('உவமை')
        if text.count('\n') > 1:
            elements['literary_significance'].append('பாடல் வடிவம்')
        
        return elements
    
    def determine_kambaramayanam_content(self, verse_matches: List[Dict], 
                                       cultural_elements: Dict, 
                                       text: str) -> tuple[bool, float]:
        """Determine if the text belongs to Kambaramayanam and calculate confidence"""
        
        confidence_factors = []
        
        # Factor 1: Direct verse matches (highest weight)
        if verse_matches:
            best_match_score = max(match['similarity_score'] for match in verse_matches)
            confidence_factors.append(('verse_match', best_match_score, 0.5))
        
        # Factor 2: Character presence
        character_score = len(cultural_elements['characters']) * 0.1
        confidence_factors.append(('characters', min(character_score, 0.3), 0.2))
        
        # Factor 3: Keyword presence
        keyword_score = len(cultural_elements['keywords']) * 0.05
        confidence_factors.append(('keywords', min(keyword_score, 0.2), 0.15))
        
        # Factor 4: Literary structure
        if cultural_elements['literary_significance']:
            literary_score = len(cultural_elements['literary_significance']) * 0.05
            confidence_factors.append(('literary', min(literary_score, 0.15), 0.1))
        
        # Factor 5: Text length and complexity
        text_length_score = min(len(text) / 200, 0.1)  # Longer text gets slightly higher score
        confidence_factors.append(('text_length', text_length_score, 0.05))
        
        # Calculate weighted confidence
        total_confidence = 0
        total_weight = 0
        
        for factor_name, score, weight in confidence_factors:
            total_confidence += score * weight
            total_weight += weight
        
        final_confidence = total_confidence / total_weight if total_weight > 0 else 0
        
        # Determine if it's Kambaramayanam (threshold-based decision)
        is_kambaramayanam = final_confidence >= self.confidence_threshold
        
        return is_kambaramayanam, final_confidence
    
    def generate_analysis(self, text: str, verse_matches: List[Dict], 
                         cultural_elements: Dict, is_kambaramayanam: bool, 
                         confidence: float) -> Dict[str, Any]:
        """Generate comprehensive analysis with cultural context"""
        
        analysis = {
            'is_kambaramayanam': is_kambaramayanam,
            'confidence': confidence,
            'extracted_text': text,
            'text_length': len(text),
            'cultural_context': {},
            'verse_matches': [],
            'seiyul_explanations': [],
            'literary_analysis': {},
            'recommendations': []
        }
        
        # Add verse matches with detailed context
        if verse_matches:
            for match in verse_matches[:3]:  # Top 3 matches
                verse_context = self.database.get_cultural_context(match['verse_id'])
                
                match_info = {
                    'verse_reference': f"Volume {match['volume']}, {match['chapter']}, Verse {match['verse_number']}",
                    'original_text': match['original_text'],
                    'meaning': match['meaning'],
                    'seiyul': match['seiyul'],
                    'similarity_score': match['similarity_score'],
                    'famous_level': match['famous_level'],
                    'moral_teaching': match.get('moral_teaching', ''),
                    'characters_involved': verse_context.get('characters', []),
                    'literary_devices': verse_context.get('literary_devices', [])
                }
                
                analysis['verse_matches'].append(match_info)
                
                # Add Seiyul explanations
                if match['seiyul']:
                    analysis['seiyul_explanations'].append({
                        'verse_reference': match_info['verse_reference'],
                        'explanation': match['seiyul'],
                        'cultural_significance': verse_context.get('historical_significance', ''),
                        'modern_relevance': self.get_modern_relevance(match['seiyul'])
                    })
        
        # Add cultural context details
        analysis['cultural_context'] = {
            'identified_characters': cultural_elements['characters'],
            'mentioned_places': cultural_elements['places'],
            'key_concepts': cultural_elements['concepts'],
            'cultural_keywords': cultural_elements['keywords'],
            'literary_elements': cultural_elements['literary_significance']
        }
        
        # Literary analysis
        analysis['literary_analysis'] = {
            'text_type': self.determine_text_type(text, cultural_elements),
            'poetic_elements': self.identify_poetic_elements(text),
            'narrative_style': self.analyze_narrative_style(text),
            'emotional_tone': self.analyze_emotional_tone(text, cultural_elements)
        }
        
        # Generate recommendations
        analysis['recommendations'] = self.generate_recommendations(
            is_kambaramayanam, confidence, verse_matches, cultural_elements
        )
        
        return analysis
    
    def get_modern_relevance(self, seiyul: str) -> str:
        """Extract modern relevance from traditional Seiyul"""
        
        # Simple keyword-based modern relevance mapping
        relevance_map = {
            'அறம்': 'நவீன நெறிமுறைகள் மற்றும் சமூக நீதி',
            'பக்தி': 'நம்பிக்கை மற்றும் ஆன்மீக வளர்ச்சி',
            'வீரம்': 'தைரியம் மற்றும் தலைமைத்துவம்',
            'காதல்': 'உண்மையான அன்பு மற்றும் அர்ப்பணம்',
            'கடமை': 'பொறுப்பு மற்றும் கடமை உணர்வு',
            'நீதி': 'சட்ட ஒழுங்கு மற்றும் நியாயம்'
        }
        
        for concept, relevance in relevance_map.items():
            if concept in seiyul:
                return f"நவீன கால பொருத்தம்: {relevance}"
        
        return "இக்கால வாழ்க்கையில் பயன்படுத்தக்கூடிய அறநெறி"
    
    def determine_text_type(self, text: str, elements: Dict) -> str:
        """Determine the type of text (verse, prose, dialogue, etc.)"""
        
        if '\n' in text and any(char in text for char in elements['characters']):
            return 'காவிய பாடல்'
        elif 'என்று' in text or 'எனக்' in text:
            return 'உரையாடல்'
        elif any(concept in text for concept in elements['concepts']):
            return 'தத்துவப் பகுதி'
        else:
            return 'வர்ணனை'
    
    def identify_poetic_elements(self, text: str) -> List[str]:
        """Identify poetic elements in the text"""
        
        elements = []
        
        # Check for rhyme patterns
        lines = text.split('\n')
        if len(lines) > 1:
            elements.append('பாடல் வடிவம்')
        
        # Check for alliteration
        if re.search(r'(\S)\1+', text):
            elements.append('அணிநிலை')
        
        # Check for repetition
        words = text.split()
        if len(set(words)) < len(words) * 0.8:
            elements.append('மறுதளை')
        
        return elements
    
    def analyze_narrative_style(self, text: str) -> str:
        """Analyze the narrative style of the text"""
        
        if 'என்று' in text:
            return 'உரையாடல் நடை'
        elif any(word in text for word in ['அவன்', 'அவள்', 'அவர்']):
            return 'விவரண நடை'
        elif any(word in text for word in ['நான்', 'நாம்', 'என்']):
            return 'சுய கதை நடை'
        else:
            return 'பாடல் நடை'
    
    def analyze_emotional_tone(self, text: str, elements: Dict) -> str:
        """Analyze the emotional tone of the text"""
        
        positive_words = ['மகிழ்', 'இன்ப', 'அழக', 'அற', 'நல்ல', 'வெற்றி']
        negative_words = ['துன்ப', 'வருத்த', 'கோப', 'அழுத', 'போர்', 'பிரிவ']
        devotional_words = ['பக்தி', 'வணக்க', 'தொழு', 'ஏத்த']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        devotional_count = sum(1 for word in devotional_words if word in text)
        
        if devotional_count > 0:
            return 'பக்தி ரச நிலை'
        elif positive_count > negative_count:
            return 'மகிழ்ச்சி நிலை'
        elif negative_count > positive_count:
            return 'துன்ப நிலை'
        else:
            return 'நடுநிலை'
    
    def generate_recommendations(self, is_kambaramayanam: bool, confidence: float,
                               verse_matches: List[Dict], elements: Dict) -> List[str]:
        """Generate recommendations for further exploration"""
        
        recommendations = []
        
        if is_kambaramayanam:
            if confidence > 0.8:
                recommendations.append("இது கம்பராமாயணத்தின் பகுதி என்று உறுதியாகக் கூறலாம்")
            elif confidence > 0.6:
                recommendations.append("இது கம்பராமாயணத்துடன் தொடர்புடையதாக இருக்கலாம்")
            else:
                recommendations.append("கம்பராமாயணத்தின் தாக்கம் இருக்கலாம், மேலும் சரிபார்ப்பு தேவை")
            
            if verse_matches:
                recommendations.append(f"குறிப்பாக {verse_matches[0]['chapter']} என்ற பகுதியைப் படியுங்கள்")
            
            if elements['characters']:
                char_list = ', '.join(elements['characters'])
                recommendations.append(f"இந்த பாத்திரங்களைப் பற்றி மேலும் அறிய: {char_list}")
        
        else:
            recommendations.append("இது கம்பராமாயணத்தின் பகுதி அல்ல")
            
            if elements['keywords']:
                recommendations.append("ஆனால் சில தமிழ் இலக்கிய கூறுகள் உள்ளன")
                recommendations.append("பிற தமிழ் கிளாசிக்கல் இலக்கியங்களை ஆராயுங்கள்")
        
        return recommendations
    
    def close(self):
        """Close database connections"""
        if self.database:
            self.database.close()

# Usage example
if __name__ == "__main__":
    print("🔍 Tamil Context Analyzer with Cultural Context")
    print("=" * 55)
    
    # Initialize analyzer
    analyzer = TamilContextAnalyzer()
    
    # Test with sample text
    test_texts = [
        "அறம் செய விரும்பு அறம் செய விரும்பு",
        "இராமன் சீதையுடன் வனவாசம் சென்றான்",
        "அனுமன் வீரம் பெற்ற வானர சேனை",
        "இன்று ஒரு நல்ல நாள்"  # Non-Kambaramayanam text
    ]
    
    for i, test_text in enumerate(test_texts, 1):
        print(f"\n{i}. Testing: '{test_text}'")
        print("-" * 40)
        
        result = analyzer.analyze_text_context(test_text)
        
        print(f"📊 Is Kambaramayanam: {'✅ Yes' if result['is_kambaramayanam'] else '❌ No'}")
        print(f"📈 Confidence: {result['confidence']:.1%}")
        
        if result['verse_matches']:
            print(f"📖 Best match: {result['verse_matches'][0]['verse_reference']}")
            print(f"🎯 Similarity: {result['verse_matches'][0]['similarity_score']:.1%}")
        
        if result['seiyul_explanations']:
            print(f"📚 Seiyul: {result['seiyul_explanations'][0]['explanation'][:100]}...")
        
        print(f"⏱️ Processing time: {result['processing_time']:.3f}s")
    
    analyzer.close()
    print("\n✅ Context analysis completed!")
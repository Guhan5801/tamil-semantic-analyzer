"""
Gemini integration for enhanced cultural context analysis
Uses an external generative model to provide cultural explanations
"""

import logging
import time
import json
import requests
from typing import Dict, Any, List, Optional
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiCulturalAnalyzer:
    """Enhanced cultural analysis using an external model"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        self.temperature = Config.GEMINI_TEMPERATURE
        self.max_tokens = Config.GEMINI_MAX_TOKENS
        self.base_url = 'https://generativelanguage.googleapis.com/v1/models'
        
        # Configure Gemini API
        if self.api_key and self.api_key != 'your_gemini_api_key_here':
            try:
                # Test API availability with a simple request
                self.is_available = True
                logger.info("✅ Cultural Analyzer initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini model: {str(e)}")
                self.is_available = False
        else:
            self.is_available = False
            logger.warning("⚠️ Enhanced NLP API key not configured - advanced analysis disabled")
    
    def _make_request(self, prompt: str) -> Optional[str]:
        """Make HTTP request to Gemini API"""
        if not self.is_available:
            logger.warning("_make_request called but is_available=False")
            return None
            
        try:
            url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"
            logger.info(f"Making Gemini API request to: {self.base_url}/{self.model_name}")
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": self.temperature,
                    "maxOutputTokens": self.max_tokens
                }
            }
            
            logger.info(f"Sending request with timeout=60s...")
            response = requests.post(url, json=payload, timeout=60)
            logger.info(f"Received response with status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Response JSON keys: {list(data.keys())}")
                
                if 'candidates' in data and len(data['candidates']) > 0:
                    content = data['candidates'][0]['content']['parts'][0]['text']
                    logger.info(f"✅ Successfully extracted content ({len(content)} chars)")
                    return content.strip()
                else:
                    logger.error(f"No candidates in response: {data}")
                    return None
            elif response.status_code == 503:
                logger.warning("Gemini API is temporarily overloaded - will provide fallback analysis")
                return None
            else:
                logger.error(f"Gemini API error: {response.status_code}")
                logger.error(f"Response text: {response.text[:500]}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("❌ Gemini request timed out after 60 seconds")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Gemini request exception: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error in Gemini request: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def enhance_cultural_context(self, extracted_text: str, 
                                basic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance cultural context analysis using an external model

        Args:
            extracted_text: OCR extracted Tamil text
            basic_analysis: Basic analysis from context_analyzer

        Returns:
            Enhanced cultural analysis with model insights
        """
        
        if not self.is_available:
            logger.warning("Gemini API not available - returning basic analysis")
            return basic_analysis
        
        try:
            start_time = time.time()
            
            # Create enhanced prompt for Gemini
            prompt = self._create_cultural_analysis_prompt(extracted_text, basic_analysis)
            
            # Call Gemini API
            gemini_response = self._call_gemini_api(prompt)
            
            if gemini_response and gemini_response.get('success'):
                # Parse and integrate Gemini insights
                enhanced_analysis = self._integrate_gemini_insights(
                    basic_analysis, gemini_response['content']
                )
                
                processing_time = time.time() - start_time
                enhanced_analysis['gemini_analysis'] = {
                    'processing_time': processing_time,
                    'model_used': self.model_name,
                    'enhanced': True,
                    'raw_response': gemini_response['content']
                }
                
                logger.info(f"✅ Cultural enhancement completed in {processing_time:.2f}s")
                return enhanced_analysis
            
            else:
                logger.warning("❌ Model call failed - returning basic analysis")
                return basic_analysis
                
        except Exception as e:
            logger.error(f"❌ Enhancement failed: {str(e)}")
            return basic_analysis
    
    def _create_cultural_analysis_prompt(self, text: str, basic_analysis: Dict[str, Any]) -> str:
        """Create detailed prompt for cultural analysis"""
        
        prompt = f"""
Analyze the following Tamil text with careful attention to cultural context, literary devices, and historical significance. Provide accurate, evidence-based insights.

**Tamil Text to Analyze:**
"{text}"

**Basic Analysis Results:**
- Is Kambaramayanam: {basic_analysis.get('is_kambaramayanam', False)}
- Confidence: {basic_analysis.get('confidence', 0):.1%}
- Characters identified: {basic_analysis.get('cultural_context', {}).get('identified_characters', [])}
- Places mentioned: {basic_analysis.get('cultural_context', {}).get('mentioned_places', [])}
- Key concepts: {basic_analysis.get('cultural_context', {}).get('key_concepts', [])}

**Please provide enhanced analysis in the following JSON format:**

{{
    "literary_significance": {{
        "is_kambaramayanam_verse": boolean,
        "confidence_explanation": "detailed explanation of why this is/isn't from Kambaramayanam",
        "verse_context": "if it's from Kambaramayanam, provide the story context",
        "literary_devices": ["list of literary devices used"],
        "meter_and_rhythm": "analysis of poetic meter if applicable"
    }},
    "cultural_context": {{
        "historical_significance": "historical and cultural importance",
        "philosophical_themes": ["key philosophical concepts"],
        "moral_teachings": "moral or ethical lessons",
        "character_analysis": "deep analysis of characters mentioned",
        "symbolism": "symbolic meanings and metaphors"
    }},
    "enhanced_seiyul": {{
        "traditional_interpretation": "classical commentary understanding",
        "modern_relevance": "how this applies to contemporary life",
        "cultural_values": "Tamil cultural values reflected",
        "spiritual_significance": "spiritual or devotional aspects"
    }},
    "linguistic_analysis": {{
        "language_register": "formal/classical/devotional etc.",
        "vocabulary_significance": "notable word choices and their meanings",
        "grammatical_features": "important grammatical or syntactic elements",
        "regional_variations": "any regional or dialectal features"
    }},
    "recommendations": {{
        "further_reading": ["suggested related texts or verses"],
        "study_approach": "how to best understand this text",
        "cultural_learning": "cultural aspects to explore further"
    }}
}}

Please ensure your analysis is culturally authentic, academically sound, and respects the sacred nature of these texts. Focus on educational value and cultural preservation.
"""
        
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Gemini API with the cultural analysis prompt"""
        
        if not self.is_available:
            return {'success': False, 'error': 'Model not initialized'}
        
        try:
            response = self._make_request(prompt)
            
            if response:
                return {
                    'success': True,
                    'content': response,
                    'model': self.model_name
                }
            else:
                logger.warning("Gemini API returned no content - providing fallback")
                return {'success': False, 'error': 'No content generated'}
                
        except Exception as e:
            logger.error(f"Model API error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _integrate_gemini_insights(self, basic_analysis: Dict[str, Any], 
                                  gemini_content: str) -> Dict[str, Any]:
        """Integrate Gemini insights with basic analysis"""
        
        try:
            # Try to parse JSON response from Gemini
            gemini_insights = self._parse_gemini_response(gemini_content)
            
            if gemini_insights:
                # Create enhanced analysis by merging basic and Gemini insights
                enhanced_analysis = basic_analysis.copy()
                
                # Update confidence based on Gemini analysis
                if 'literary_significance' in gemini_insights:
                    lit_sig = gemini_insights['literary_significance']
                    if 'is_kambaramayanam_verse' in lit_sig:
                        enhanced_analysis['is_kambaramayanam'] = lit_sig['is_kambaramayanam_verse']
                        enhanced_analysis['confidence_explanation'] = lit_sig.get('confidence_explanation', '')
                
                # Add enhanced cultural context
                if 'cultural_context' in enhanced_analysis:
                    enhanced_analysis['cultural_context']['nlp_enhanced'] = True
                    
                    # Add Gemini cultural insights
                    if 'cultural_context' in gemini_insights:
                        enhanced_analysis['cultural_context'].update({
                            'historical_significance': gemini_insights['cultural_context'].get('historical_significance', ''),
                            'philosophical_themes': gemini_insights['cultural_context'].get('philosophical_themes', []),
                            'moral_teachings': gemini_insights['cultural_context'].get('moral_teachings', ''),
                            'symbolism': gemini_insights['cultural_context'].get('symbolism', '')
                        })
                
                # Add enhanced Seiyul explanations
                if 'enhanced_seiyul' in gemini_insights:
                    enhanced_analysis['enhanced_seiyul'] = gemini_insights['enhanced_seiyul']
                
                # Add linguistic analysis
                if 'linguistic_analysis' in gemini_insights:
                    enhanced_analysis['linguistic_analysis'] = gemini_insights['linguistic_analysis']
                
                # Add enhanced recommendations
                if 'recommendations' in gemini_insights:
                    existing_recs = enhanced_analysis.get('recommendations', [])
                    gemini_recs = gemini_insights['recommendations']
                    
                    if 'further_reading' in gemini_recs:
                        existing_recs.extend(gemini_recs['further_reading'])
                    
                    enhanced_analysis['recommendations'] = existing_recs
                    enhanced_analysis['study_recommendations'] = gemini_recs
                
                return enhanced_analysis
            
            else:
                # If JSON parsing fails, add raw Gemini response
                basic_analysis['gemini_raw_insights'] = gemini_content
                return basic_analysis
                
        except Exception as e:
            logger.error(f"Error integrating Gemini insights: {str(e)}")
            basic_analysis['gemini_error'] = str(e)
            return basic_analysis
    
    def _parse_gemini_response(self, content: str) -> Optional[Dict[str, Any]]:
        """Parse JSON response from Gemini"""
        
        try:
            # Try to find JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            
            else:
                logger.warning("No JSON found in model response")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse model JSON response: {str(e)}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error parsing model response: {str(e)}")
            return None
    
    def get_verse_elaboration(self, verse_text: str, basic_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed elaboration for a specific verse using Gemini"""
        
        if not self.is_available:
            return {'error': 'Gemini API not available'}
        
        prompt = f"""
As a Tamil literature scholar specializing in Kambaramayanam, provide a detailed elaboration of this verse:

"{verse_text}"

Please provide:
1. **Line-by-line explanation** in Tamil and English
2. **Historical context** within Kambaramayanam
3. **Literary devices** used by Kamban
4. **Philosophical significance**
5. **Cultural relevance** then and now
6. **Connection to Sanskrit Ramayana** (if applicable)
7. **Moral teachings** embedded in the verse

Format your response as detailed explanatory text, focusing on educational value and cultural appreciation.
"""
        
        try:
            response = self._call_gemini_api(prompt)
            
            if response and response.get('success'):
                return {
                    'success': True,
                    'elaboration': response['content'],
                    'processing_time': time.time()
                }
            else:
                return {'success': False, 'error': 'Failed to get verse elaboration'}
                
        except Exception as e:
            logger.error(f"Error getting verse elaboration: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_conversational_meaning(self, text: str) -> Optional[Dict[str, Any]]:
        """Get accurate literary meaning with book/source identification in Tamil only"""
        if not self.is_available:
            return None
            
        try:
            # Enhanced prompt for accurate literary analysis with source identification
            conversational_prompt = f"""நீங்கள் ஒரு தமிழ் இலக்கிய வல்லுநர் மற்றும் பொருள் விளக்க நிபுணர். கீழே கொடுக்கப்பட்ட தமிழ் உரையின் துல்லியமான, அசல் நூல் பொருளை விளக்கவும்.

உரை: "{text}"

**மிக முக்கியமான வழிகாட்டுதல்கள்:**
1. இது இலக்கிய நூலிலிருந்து வந்ததா என துல்லியமாக கண்டறியவும் (திருக்குறள், கம்பராமாயணம், புறநானூறு, அகநானூறு, சங்க இலக்கியம், திருவாசகம், தேவாரம், நாலடியார், சிலப்பதிகாரம், திருமந்திரம் போன்றவை)
2. நூலிலிருந்து வந்ததென்றால், **அந்த நூலின் அசல் உரையாசிரியர்கள் கூறிய பொருளை மட்டுமே** குறிப்பிடவும் (எ.கா: பரிமேலழகர், மணக்குடவர், கல்லாடனார், வீரமாமுனிவர் போன்றோரின் உரை)
3. **உங்கள் சொந்த கருத்துகளை சேர்க்க வேண்டாம் - அசல் நூல் பொருளை மட்டும் தரவும்**
4. **பொருள் இரண்டு பகுதிகளாக இருக்க வேண்டும்:**
   - **பொருள்:** அசல் நூல் உரையாசிரியர்கள் கூறிய துல்லியமான விளக்கம் (2-4 வாக்கியங்கள்)
   - **சுருக்கமாக:** ஒரு வரியில் அசல் பொருளின் சாரம்
5. சாதாரண உரை என்றால், அதன் நேரடி பொருளை மட்டும் தெளிவாக விளக்கவும்
6. வரிக்கு வரி பொருள் - **அசல் நூலின் சொல்லுரையை** அடிப்படையாக கொண்டு தரவும்

**கட்டாய JSON வடிவம்:**
{{
  "tamil_meaning": "பொருள்:\\n[அசல் நூல் உரையாசிரியர்கள் கூறிய துல்லியமான பொருள் 2-4 வாக்கியங்களில்]\\n\\nசுருக்கமாக:\\n[ஒரு வரியில் அசல் பொருளின் சாரம்]",
  "source_book": "நூலின் பெயர் அல்லது 'சாதாரண உரை'",
  "chapter_section": "அதிகாரம்/காண்டம்/படலம் அல்லது 'பொருந்தாது'",
  "verse_number": "பாடல் எண் அல்லது 'பொருந்தாது'",
  "commentary_reference": "உரையாசிரியர் பெயர் (பரிமேலழகர், மணக்குடவர், கல்லாடனார் போன்றோர்) அல்லது 'பொருந்தாது'",
  "line_by_line": "அசல் சொல்லுரை அடிப்படையில் ஒவ்வொரு வரியின்/சொல்லின் பொருள்",
  "explanation": "அசல் நூல் உரையில் கூறப்பட்ட சூழல், பின்னணி, முக்கியத்துவம்",
  "theme": "அசல் நூல் குறிப்பிடும் முக்கிய கருத்து மற்றும் செய்தி",
  "sentiment": "positive/negative/neutral/devotional/philosophical"
}}

**துல்லியமான எடுத்துக்காட்டு:**
உள்ளீடு: "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு"

tamil_meaning (பரிமேலழகர் உரை அடிப்படையில்):
"பொருள்:
அகரம் எல்லா எழுத்துகளுக்கும் முதலாவது ஆதலின், அதனை முதலாகக் கொண்டு எழுத்துக்களை எழுதுதல் போல், ஆதி பகவன் என்னும் கடவுள் உலகத்திற்கு முதற்காரணமாக இருக்கிறார். எனவே, அவரை முதலாகக் கொண்டே நூல்களை இயற்ற வேண்டும்.

சுருக்கமாக:
எழுத்துக்கு அகரம் முதல் போல, உலகிற்கு ஆதிபகவன் முதல்."

**மிக முக்கியம்:** 
- அசல் நூலில் உள்ள பொருளை மட்டும் தரவும் - உங்கள் விளக்கங்களை சேர்க்க வேண்டாம்
- உரையாசிரியர்கள் கூறிய வார்த்தைகளையும் பொருளையும் பின்பற்றவும்
- நவீன விளக்கங்கள் வேண்டாம் - பாரம்பரிய உரைகளை பின்பற்றவும்
- பொருள் பகுதி துல்லியமாக அசல் நூல் உரையை பிரதிபலிக்க வேண்டும்"""
            
            api_response = self._call_gemini_api(conversational_prompt)
            if api_response and api_response.get('success'):
                return {'text': api_response.get('content', '')}
            return None
        except Exception as e:
            logger.error(f"Literary meaning analysis failed: {e}")
            return None

    def analyze_semantic_sentiment(self, text: str, prompt: str) -> Optional[Dict[str, Any]]:
        """Analyze text for semantic and sentiment analysis using conversational approach"""
        if not self.is_available:
            return None
            
        try:
            # Create a conversational prompt for better meaning extraction
            conversational_prompt = f"""
நீங்கள் ஒரு தமிழ் மொழி நிபுணர். கீழே கொடுக்கப்பட்ட தமிழ் உரையைப் படித்து, எளிமையான மற்றும் தெளிவான முறையில் பதிலளிக்கவும்.

உரை: "{text}"

தயவுசெய்து இந்த உரையைப் பற்றி எனக்குச் சொல்லுங்கள்:
1. இந்த உரை என்ன பற்றி பேசுகிறது?
2. இதில் என்ன உணர்வு வெளிப்படுகிறது?
3. இதன் பொருள் என்ன?

உங்கள் பதிலை JSON வடிவத்தில் கொடுக்கவும்:
{{
  "semantic": {{
    "meaning": "உரையின் முக்கிய பொருள் தமிழில்",
    "themes": ["முக்கிய விषயங்கள்"],
    "explanation": "விரிவான விளக்கம் தமிழில்"
  }},
  "sentiment": {{
    "overall_sentiment": "positive/negative/neutral",
    "confidence": 0.8,
    "explanation": "உணர்வு விளக்கம் தமிழில்"
  }}
}}
"""
            
            api_response = self._call_gemini_api(conversational_prompt)
            if api_response and api_response.get('success'):
                return {'text': api_response.get('content', '')}
            return None
        except Exception as e:
            logger.error(f"Semantic sentiment analysis failed: {e}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """Check model API health and configuration"""
        
        status = {
            'gemini_configured': self.is_available,
            'api_key_present': bool(self.api_key),
            'model': self.model_name,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
        
        if self.is_available:
            # Test API with simple prompt
            try:
                test_response = self._call_gemini_api("Say 'Tamil OCR system test successful' in Tamil.")
                status['api_accessible'] = test_response.get('success', False) if test_response else False
                status['test_response'] = test_response.get('content', 'No response') if test_response else 'API call failed'
            except Exception as e:
                status['api_accessible'] = False
                status['error'] = str(e)
        else:
            status['api_accessible'] = False
            status['error'] = 'API key not configured or model not initialized'
        
        return status

# Usage example
if __name__ == "__main__":
    print("Cultural Analyzer Test")
    print("=" * 40)
    
    # Initialize analyzer
    analyzer = GeminiCulturalAnalyzer()
    
    # Health check
    health = analyzer.health_check()
    print(f"🏥 Model Status: {'✅ Ready' if health['api_accessible'] else '❌ Not Ready'}")
    
    if health['api_accessible']:
        # Test with sample analysis
        sample_text = "அறம் செய விரும்பு"
        sample_basic = {
            'is_kambaramayanam': True,
            'confidence': 0.8,
            'cultural_context': {
                'identified_characters': [],
                'mentioned_places': [],
                'key_concepts': ['அறம்']
            }
        }
        
        print(f"\n🧪 Testing with: '{sample_text}'")
        enhanced = analyzer.enhance_cultural_context(sample_text, sample_basic)
        
        print(f"📊 Enhanced analysis available: {'✅' if 'nlp_analysis' in enhanced else '❌'}")
        
        if 'enhanced_seiyul' in enhanced:
            print(f"📚 Enhanced Seiyul available: ✅")
        
        print(f"⏱️ Processing time: {enhanced.get('gemini_analysis', {}).get('processing_time', 0):.2f}s")
    
    else:
        print("💡 To enable enhancement model:")
        print("   1. Get an API key from your model provider")
        print("   2. Set it in config.py: Config.set_gemini_api_key('your-key')")
        print("   3. Or set environment variable: GEMINI_API_KEY='your-key'")
    
    print("\n✅ Gemini integration test completed!")
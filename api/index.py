import os
import sys
import re
import logging
import hashlib
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force cache bust for new பொருள் format - v2.0
logger.info("🔄 API Version 2.0 - Updated பொருள் format with structured sections")

# Ensure project root is on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, 'templates'),
    static_folder=None
)
CORS(app)

# Optional analyzer import
semantic_analyzer = None
try:
    from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
    semantic_analyzer = SemanticSentimentAnalyzer()
    logger.info("✅ Semantic analyzer initialized")
except Exception as e:
    logger.error(f"❌ Analyzer initialization failed: {e}")
    semantic_analyzer = None


def _file_md5(path: str) -> str | None:
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


@app.route('/')
def root():
    app_info = {
        'name': 'Tamil Semantic & Sentiment Analyzer',
        'version': '1.0.0',
        'features': [
            'Tamil-only validation (English blocked)',
            'Semantic and Sentiment analysis',
            'Optional Gemini enhancement'
        ]
    }
    return render_template('dashboard_prod.html', app_info=app_info)


@app.route('/api/health')
def health():
    gemini_status = {}
    if semantic_analyzer:
        gemini_status = {
            'gemini_enabled': semantic_analyzer.gemini_enabled,
            'gemini_analyzer_exists': semantic_analyzer.gemini_analyzer is not None,
            'model_name': semantic_analyzer.gemini_analyzer.model_name if semantic_analyzer.gemini_analyzer else None,
            'api_available': semantic_analyzer.gemini_analyzer.is_available if semantic_analyzer.gemini_analyzer else False
        }
    
    return jsonify({
        'status': 'healthy',
        'analyzer': 'ready' if semantic_analyzer else 'not initialized',
        'gemini_status': gemini_status,
        'timestamp': datetime.now().isoformat(),
        'commit': os.getenv('VERCEL_GIT_COMMIT_SHA') or os.getenv('GIT_COMMIT_SHA'),
        'environment': os.getenv('VERCEL_ENV') or os.getenv('ENV'),
        'file_md5': _file_md5(__file__),
        'python_version': sys.version.split()[0]
    })


@app.route('/api/debug')
def debug():
    """Debug endpoint to check configuration"""
    try:
        from config import Config
        
        # Check environment variable
        env_key = os.getenv('GEMINI_API_KEY', '')
        
        debug_info = {
            'environment': {
                'GEMINI_API_KEY_in_env': bool(env_key),
                'GEMINI_API_KEY_env_length': len(env_key) if env_key else 0,
                'env_key_valid': len(env_key) == 39 if env_key else False,
                'using_hardcoded_key': len(env_key) != 39 or not env_key
            },
            'config': {
                'GEMINI_API_KEY_set': bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'your_gemini_api_key_here'),
                'GEMINI_API_KEY_length': len(Config.GEMINI_API_KEY) if Config.GEMINI_API_KEY else 0,
                'GEMINI_API_KEY_last10': f"***{Config.GEMINI_API_KEY[-10:]}" if Config.GEMINI_API_KEY else '',
                'GEMINI_MODEL': Config.GEMINI_MODEL,
                'ENABLE_GEMINI_ENHANCEMENT': Config.ENABLE_GEMINI_ENHANCEMENT,
                'is_gemini_available': Config.is_gemini_available()
            },
            'analyzer': {
                'exists': semantic_analyzer is not None,
                'gemini_enabled': semantic_analyzer.gemini_enabled if semantic_analyzer else None,
                'gemini_analyzer_exists': semantic_analyzer.gemini_analyzer is not None if semantic_analyzer else None
            },
            'environment': {
                'VERCEL_ENV': os.getenv('VERCEL_ENV'),
                'VERCEL_GIT_COMMIT_SHA': os.getenv('VERCEL_GIT_COMMIT_SHA'),
                'FLASK_ENV': os.getenv('FLASK_ENV'),
                'python_version': sys.version
            },
            'imports': {
                'semantic_sentiment_analyzer_imported': 'semantic_sentiment_analyzer' in sys.modules,
                'gemini_integration_imported': 'gemini_integration' in sys.modules,
                'requests_available': 'requests' in sys.modules
            }
        }
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': str(e.__traceback__)}), 500


@app.route('/api/test-gemini')
def test_gemini():
    """Test Gemini API directly"""
    try:
        if not semantic_analyzer:
            return jsonify({'status': 'error', 'error': 'Analyzer not available'}), 503
        
        test_text = "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு"
        
        result = {
            'gemini_enabled': semantic_analyzer.gemini_enabled,
            'gemini_analyzer_exists': semantic_analyzer.gemini_analyzer is not None,
            'test_input': test_text
        }
        
        if semantic_analyzer.gemini_analyzer:
            result['gemini_available'] = semantic_analyzer.gemini_analyzer.is_available
            
            try:
                logger.info("Testing Gemini API call...")
                gemini_response = semantic_analyzer.gemini_analyzer.get_conversational_meaning(test_text)
                result['gemini_response_received'] = bool(gemini_response)
                result['gemini_response_has_text'] = bool(gemini_response and gemini_response.get('text'))
                
                if gemini_response and gemini_response.get('text'):
                    response_text = gemini_response.get('text', '')
                    result['response_length'] = len(response_text)
                    result['response_preview'] = response_text[:500] + '...' if len(response_text) > 500 else response_text
                    result['has_porul'] = 'பொருள்:' in response_text
                    result['has_summary'] = 'சுருக்கமாக:' in response_text
                else:
                    result['error'] = 'Gemini returned empty response'
            except Exception as e:
                result['gemini_call_error'] = str(e)
                import traceback
                result['gemini_traceback'] = traceback.format_exc()
        else:
            result['error'] = 'Gemini analyzer not initialized'
        
        return jsonify(result)
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if not semantic_analyzer:
            return jsonify({'status': 'error', 'error': 'Analyzer not available'}), 503

        data = request.get_json(silent=True) or {}
        text = (data.get('text') or '').strip()

        if not text:
            return jsonify({'status': 'error', 'error': 'உரை தேவை (Text is required)'}), 400

        # Tamil-only validation: reject any English words
        english_words = re.findall(r'\b[a-zA-Z]+\b', text)
        if english_words:
            return jsonify({
                'status': 'error',
                'error': f'ஆங்கில வார்த்தைகள் கண்டறியப்பட்டன: {", ".join(english_words)}. தமிழ் உரை மட்டுமே அனுமதிக்கப்படுகிறது.',
                'english_words_found': english_words
            }), 400

        logger.info(f"Analyze request: {len(text)} chars")
        result = semantic_analyzer.analyze_semantic_sentiment(text)
        
        # Log enhancement status and meaning details
        semantic_data = result.get('semantic_analysis', {})
        meaning_length = len(semantic_data.get('meaning', ''))
        has_porul = 'பொருள்:' in semantic_data.get('meaning', '')
        has_summary = 'சுருக்கமாக:' in semantic_data.get('meaning', '')
        
        logger.info(f"Analysis complete: enhanced={result.get('enhanced_analysis', False)}, " +
                   f"gemini_error={result.get('gemini_error', 'none')}, " +
                   f"meaning_length={meaning_length}, has_porul={has_porul}, has_summary={has_summary}")

        # Do not return any english_meaning key and ensure Tamil-only fields
        semantic_out = dict(result.get('semantic_analysis', {}) or {})
        if 'english_meaning' in semantic_out:
            semantic_out.pop('english_meaning', None)
        # If Gemini added any nested fields inadvertently
        for k in list(semantic_out.keys()):
            if 'english' in k.lower():
                semantic_out.pop(k, None)

        response = {
            'status': 'success',
            'text': text,
            'semantic_analysis': semantic_out,
            'sentiment_analysis': result.get('sentiment_analysis', {}),
            'processing_time': result.get('processing_time', '0s'),
            'enhanced_analysis': result.get('enhanced_analysis', False),
            'timestamp': result.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        return jsonify(response)

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'status': 'error', 'error': f'பகுப்பாய்வு பிழை: {str(e)}'}), 500


# Local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
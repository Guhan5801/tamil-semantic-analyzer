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
        
        # Log enhancement status
        logger.info(f"Analysis complete: enhanced={result.get('enhanced_analysis', False)}, " +
                   f"gemini_error={result.get('gemini_error', 'none')}")

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
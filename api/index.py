import sys"""import sys

import os

import reTamil Semantic Analyzer - Vercel Serverless APIimport os

import logging

from datetime import datetimeSimplified version to fix deployment issuesimport re



# Add parent directory to Python path"""import logging

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, parent_dir)import sysfrom datetime import datetime



from flask import Flask, request, jsonifyimport os

from flask_cors import CORS

# Configure logging

# Configure logging

logging.basicConfig(level=logging.INFO)# Add parent directory to Python pathlogging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))logger = logging.getLogger(__name__)

# Create Flask app

app = Flask(__name__)sys.path.insert(0, parent_dir)

CORS(app)

# Import Flask

# Initialize analyzer with error handling

semantic_analyzer = Nonefrom flask import Flask, request, jsonifyfrom flask import Flask, request, jsonify

try:

    from semantic_sentiment_analyzer import SemanticSentimentAnalyzerfrom flask_cors import CORSfrom flask_cors import CORS

    semantic_analyzer = SemanticSentimentAnalyzer()

    logger.info("Analyzer initialized successfully")from datetime import datetime

except Exception as e:

    logger.error(f"Analyzer initialization failed: {e}")import re# Initialize Flask app



@app.route('/')import loggingapp = Flask(__name__)

def home():

    return jsonify({CORS(app)

        'service': 'Tamil Semantic Analyzer API',

        'status': 'running',# Configure logging

        'version': '1.0.0',

        'analyzer': 'available' if semantic_analyzer else 'unavailable',logging.basicConfig(level=logging.INFO)# Try to import analyzer (but don't crash if it fails)

        'endpoints': {

            'health': '/api/health',logger = logging.getLogger(__name__)semantic_analyzer = None

            'analyze': '/api/analyze (POST)'

        }try:

    })

# Create Flask app    # Add parent directory to path

@app.route('/api/health')

def health():app = Flask(__name__)    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return jsonify({

        'status': 'healthy',CORS(app)    sys.path.insert(0, parent_dir)

        'analyzer': 'ready' if semantic_analyzer else 'not initialized',

        'timestamp': datetime.now().isoformat()    

    })

# Initialize analyzer (with error handling)    from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

@app.route('/api/analyze', methods=['POST'])

def analyze():semantic_analyzer = None    semantic_analyzer = SemanticSentimentAnalyzer()

    try:

        if not semantic_analyzer:try:    logger.info("✅ Semantic analyzer initialized")

            return jsonify({'error': 'Analyzer not available'}), 503

            from semantic_sentiment_analyzer import SemanticSentimentAnalyzerexcept Exception as e:

        data = request.get_json() or {}

        text = data.get('text', '').strip()    semantic_analyzer = SemanticSentimentAnalyzer()    logger.error(f"❌ Analyzer initialization failed: {e}")

        

        if not text:    logger.info("✅ Analyzer initialized")    logger.error(f"Current path: {os.getcwd()}")

            return jsonify({'error': 'Text required'}), 400

        except Exception as e:    logger.error(f"Python path: {sys.path}")

        # Check for English words

        english_words = re.findall(r'\b[a-zA-Z]+\b', text)    logger.error(f"❌ Analyzer failed: {e}")

        if english_words:

            return jsonify({@app.route('/')

                'error': f'English words detected: {", ".join(english_words)}',

                'english_words': english_words@app.route('/')def index():

            }), 400

        def home():    """Main route - simple response"""

        # Analyze

        result = semantic_analyzer.analyze_semantic_sentiment(text)    """Root endpoint"""    return jsonify({

        

        return jsonify({    return jsonify({        'status': 'running',

            'status': 'success',

            'text': text,        'service': 'Tamil Semantic Analyzer API',        'message': 'Tamil Semantic Analyzer API',

            'semantic_analysis': result.get('semantic_analysis', {}),

            'sentiment_analysis': result.get('sentiment_analysis', {}),        'status': 'running',        'version': '1.0.0',

            'processing_time': result.get('processing_time', '0s'),

            'timestamp': datetime.now().isoformat()        'version': '1.0.0',        'analyzer_available': semantic_analyzer is not None,

        })

                'analyzer': 'available' if semantic_analyzer else 'unavailable',        'endpoints': {

    except Exception as e:

        logger.error(f"Analysis error: {e}")        'endpoints': {            'health': '/api/health',

        return jsonify({'error': str(e)}), 500

            'health': '/api/health',            'analyze': '/api/analyze (POST)'

if __name__ == '__main__':

    app.run(debug=True, port=5000)            'analyze': '/api/analyze (POST with JSON: {"text": "your tamil text"})'        }


        }    })

    })

@app.route('/api/health')

@app.route('/api/health')def health_check():

def health():    """Health check endpoint"""

    """Health check"""    try:

    return jsonify({        import sys

        'status': 'healthy',        return jsonify({

        'analyzer': 'ready' if semantic_analyzer else 'not initialized',            'status': 'healthy',

        'timestamp': datetime.now().isoformat()            'service': 'Tamil Semantic Analyzer',

    })            'version': '1.0.0',

            'analyzer_status': 'available' if semantic_analyzer else 'unavailable',

@app.route('/api/analyze', methods=['POST'])            'python_version': sys.version,

def analyze():            'timestamp': datetime.now().isoformat()

    """Analyze Tamil text"""        })

    try:    except Exception as e:

        if not semantic_analyzer:        return jsonify({

            return jsonify({'error': 'Analyzer not available'}), 503            'status': 'error',

                    'error': str(e)

        data = request.get_json() or {}        }), 500

        text = data.get('text', '').strip()

        @app.route('/api/analyze', methods=['POST'])

        if not text:def api_analyze():

            return jsonify({'error': 'Text required'}), 400    """Optimized API endpoint for Tamil text analysis"""

            try:

        # Check for English words        if not semantic_analyzer:

        english_words = re.findall(r'\b[a-zA-Z]+\b', text)            return jsonify({

        if english_words:                'status': 'error',

            return jsonify({                'error': 'செமாண்டிக் பகுப்பாய்வி கிடைக்கவில்லை (Semantic analyzer not available)'

                'error': f'English words detected: {", ".join(english_words)}. Tamil only.',            }), 500

                'english_words': english_words

            }), 400        # Get JSON data

                data = request.get_json()

        # Analyze        

        result = semantic_analyzer.analyze_semantic_sentiment(text)        if not data or 'text' not in data:

                    return jsonify({

        return jsonify({                'status': 'error',

            'status': 'success',                'error': 'உரை தேவை (Text is required)'

            'text': text,            }), 400

            'semantic_analysis': result.get('semantic_analysis', {}),        

            'sentiment_analysis': result.get('sentiment_analysis', {}),        text = data['text'].strip()

            'processing_time': result.get('processing_time', '0s'),        if not text:

            'timestamp': datetime.now().isoformat()            return jsonify({

        })                'status': 'error',

                        'error': 'வெற்று உரை அனுமதிக்கப்படவில்லை (Empty text not allowed)'

    except Exception as e:            }), 400

        logger.error(f"Error: {e}")

        return jsonify({'error': str(e)}), 500        # Check for English words - Tamil only validation

        english_words = re.findall(r'\b[a-zA-Z]+\b', text)

# For local testing        if english_words:

if __name__ == '__main__':            return jsonify({

    app.run(debug=True, port=5000)                'status': 'error',

                'error': f'ஆங்கில வார்த்தைகள் கண்டறியப்பட்டன: {", ".join(english_words)}. தமிழ் உரை மட்டுமே அனுமதிக்கப்படுகிறது.',
                'english_words_found': english_words
            }), 400

        logger.info(f"API Analysis request for {len(text)} characters")
        
        # Perform analysis
        result = semantic_analyzer.analyze_semantic_sentiment(text)
        
        # Return full semantic and sentiment analysis structure
        response_data = {
            'status': 'success',
            'text': text,
            'semantic_analysis': result.get('semantic_analysis', {}),
            'sentiment_analysis': result.get('sentiment_analysis', {}),
            'processing_time': result.get('processing_time', '0s'),
            'enhanced_analysis': result.get('enhanced_analysis', False),
            'timestamp': result.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'analysis_type': 'semantic_sentiment'
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"API analysis error: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': f'பகுப்பாய்வு பிழை (Analysis error): {str(e)}'
        }), 500

# Vercel serverless function handler
def handler(request, response):
    """Vercel serverless function handler"""
    return app(request, response)

# For local testing
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
import sys
import os
import re
import logging
from datetime import datetime

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path to import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
logger.info(f"Added to path: {parent_dir}")

# Import Flask first
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Initialize Flask app for Vercel
app = Flask(__name__, 
           template_folder=os.path.join(parent_dir, 'templates'),
           static_folder=os.path.join(parent_dir, 'static'))
CORS(app)

# Try to import and initialize analyzer
semantic_analyzer = None
try:
    from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
    semantic_analyzer = SemanticSentimentAnalyzer()
    logger.info("✅ Semantic analyzer initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize semantic analyzer: {e}")
    # Continue without analyzer - will return error messages

@app.route('/')
def dashboard():
    """Main dashboard route"""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        # Fallback to simple HTML if template not found
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tamil Semantic Analyzer</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>🌟 Tamil Semantic Analyzer API</h1>
            <p>API is running! Use POST /api/analyze to analyze Tamil text.</p>
            <p>Health check: <a href="/api/health">/api/health</a></p>
        </body>
        </html>
        '''

@app.route('/api/health')
def health_check():
    """Health check endpoint for Vercel"""
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'Tamil Semantic Sentiment Analysis API',
            'version': '1.0.0',
            'analyzer_status': 'available' if semantic_analyzer else 'unavailable',
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Optimized API endpoint for Tamil text analysis"""
    try:
        if not semantic_analyzer:
            return jsonify({
                'status': 'error',
                'error': 'செமாண்டிக் பகுப்பாய்வி கிடைக்கவில்லை (Semantic analyzer not available)'
            }), 500

        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'status': 'error',
                'error': 'உரை தேவை (Text is required)'
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'status': 'error',
                'error': 'வெற்று உரை அனுமதிக்கப்படவில்லை (Empty text not allowed)'
            }), 400

        # Check for English words - Tamil only validation
        english_words = re.findall(r'\b[a-zA-Z]+\b', text)
        if english_words:
            return jsonify({
                'status': 'error',
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
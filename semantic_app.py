#!/usr/bin/env python3
"""
Tamil Text Analyzer Web Application
Provides three-part analysis: Semantic Analysis, Tamil Translation, and Tamil Meaning
"""

import os
import logging
import re
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_cors import CORS

import tempfile
import json
from datetime import datetime
from semantic_sentiment_analyzer import SemanticSentimentAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'tamil_text_analyzer_2024'
CORS(app)

# Global variables
semantic_analyzer = None
simple_ocr_engine = None

# Configuration
# File upload functionality removed - text input only

class SimpleTamilOCR:
    """Simplified Tamil OCR using only Tesseract"""
    
    def __init__(self):
        logger.info("Initializing Simple Tamil OCR...")
        try:
            import pytesseract
            # Test Tesseract
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            test_result = pytesseract.get_tesseract_version()
            logger.info(f"✅ Tesseract initialized: {test_result}")
            self.available = True
        except Exception as e:
            logger.error(f"❌ Tesseract initialization failed: {e}")
            self.available = False
    
    def extract_text(self, image_path):
        """Extract text from image using Tesseract"""
        if not self.available:
            return {"error": "OCR engine not available"}
        
        try:
            import pytesseract
            from PIL import Image
            
            # Load and process image
            image = Image.open(image_path)
            
            # Configure Tesseract for Tamil
            config = r'--oem 3 --psm 6 -l tam+eng'
            
            # Extract text
            text = pytesseract.image_to_string(image, config=config)
            
            return {
                "text": text.strip(),
                "confidence": 75.0,
                "engine": "tesseract",
                "language": "tamil+english"
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {"error": f"Text extraction failed: {str(e)}"}

def initialize_engines():
    """Initialize semantic analyzer, three-part analyzer and OCR engine"""
    global semantic_analyzer, simple_ocr_engine
    
    logger.info("🚀 Initializing Tamil Text Analysis System...")
    
    try:
        # Initialize Semantic Analyzer
        logger.info("🧠 Initializing Semantic & Sentiment Analyzer...")
        semantic_analyzer = SemanticSentimentAnalyzer()
        
        # Initialize Simple OCR (optional)
        logger.info("📖 Initializing OCR Engine...")
        simple_ocr_engine = SimpleTamilOCR()
        
        logger.info("✅ All engines initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Engine initialization failed: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    """Optimized dashboard page"""
    return render_template('dashboard.html')

@app.route('/test')
def test_page():
    """API test page for debugging"""
    return render_template('test_api.html')

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Analyze text input for semantic and sentiment"""
    try:
        if not semantic_analyzer:
            flash('Semantic analyzer not available. Please check system setup.', 'error')
            return redirect(url_for('index'))
        
        # Get text input
        text_input = request.form.get('text', '').strip()
        
        if not text_input:
            flash('Please provide text to analyze', 'error')
            return redirect(url_for('index'))
        
        # Perform semantic and sentiment analysis
        logger.info(f"Analyzing text: {text_input[:50]}...")
        analysis_result = semantic_analyzer.analyze_semantic_sentiment(text_input)
        
        # Prepare clean results with proper error handling
        results = {
            'input_text': text_input,
            'semantic_analysis': analysis_result.get('semantic_analysis', {}),
            'sentiment_analysis': analysis_result.get('sentiment_analysis', {}),
            'processing_time': analysis_result.get('processing_time', 0),
            'enhanced_analysis': analysis_result.get('enhanced_analysis', False),
            'timestamp': analysis_result.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
        
        # Ensure all required fields exist
        if not results['semantic_analysis']:
            results['semantic_analysis'] = {
                'word_count': 0,
                'tamil_word_count': 0,
                'language_detected': 'unknown',
                'text_complexity': 'unknown',
                'key_themes': []
            }
        
        if not results['sentiment_analysis']:
            results['sentiment_analysis'] = {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'emotional_intensity': 0.0,
                'positive_indicators': 0,
                'negative_indicators': 0,
                'neutral_indicators': 0,
                'sentiment_distribution': {
                    'positive': 0.0,
                    'negative': 0.0,
                    'neutral': 1.0
                }
            }
        
        return render_template('semantic_analysis.html', results=results)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        flash(f'Analysis failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/quick_analyze', methods=['POST'])
def quick_analyze():
    """Quick API endpoint for immediate text analysis"""
    try:
        if not semantic_analyzer:
            return jsonify({'error': 'Semantic analyzer not available'})
        
        # Get text from form data or JSON
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '').strip() if data else ''
        else:
            text = request.form.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text input required'})
        
        # Perform analysis
        result = semantic_analyzer.analyze_semantic_sentiment(text)
        
        return jsonify({
            'status': 'success',
            'analysis': {
                'semantic': result.get('semantic_analysis', {}),
                'sentiment': result.get('sentiment_analysis', {}),
                'processing_time': result.get('processing_time', 0),
                'enhanced_analysis': result.get('enhanced_analysis', False)
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        })

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Optimized API endpoint for semantic and sentiment analysis"""
    try:
        if not semantic_analyzer:
            return jsonify({
                'status': 'error',
                'error': 'Semantic analyzer not available'
            }), 500

        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'status': 'error',
                'error': 'No text provided in request'
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'status': 'error',
                'error': 'Empty text provided'
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
            'error': f'Analysis failed: {str(e)}'
        }), 500



@app.route('/api/analyze_legacy', methods=['POST'])
def api_analyze_legacy():
    """Legacy API endpoint for backward compatibility"""
    try:
        if not semantic_analyzer:
            return jsonify({
                'status': 'error',
                'error': 'Semantic analyzer not available'
            }), 500
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({
                    'status': 'error',
                    'error': 'Text input required in JSON body'
                }), 400
            text = data['text'].strip()
        else:
            text = request.form.get('text', '').strip()
            if not text:
                return jsonify({
                    'status': 'error',
                    'error': 'Text input required'
                }), 400
        
        if not text:
            return jsonify({
                'status': 'error',
                'error': 'Empty text provided'
            }), 400
        
        # Perform analysis
        result = semantic_analyzer.analyze_semantic_sentiment(text)
        
        return jsonify({
            'status': 'success',
            'analysis': result
        })
        
    except Exception as e:
        logger.error(f"API analysis error: {e}")
        return jsonify({
            'status': 'error', 
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "engines": {
                "semantic_analyzer": semantic_analyzer is not None,
                "ocr": simple_ocr_engine.available if simple_ocr_engine else False
            }
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Tamil Semantic & Sentiment Analysis System")
    print("=======================================================")
    
    # Initialize engines
    if initialize_engines():
        print("✅ Engines initialized successfully")
        print("🌐 Starting web server...")
        print("📱 Access the application at: http://localhost:5000")
        print("🔍 API health check: http://localhost:5000/api/health")
        print("-------------------------------------------------------")
        print("📝 Features available:")
        print("   • Semantic analysis of Tamil text")
        print("   • Sentiment analysis and emotion detection")
        print("   • Text input analysis")
        print("   • Enhanced analysis (external model integration)")
        print("   • Clean, focused results only")
        print("=======================================================")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    else:
        print("❌ Failed to initialize engines. Please check dependencies.")
        print("💡 Make sure enhanced NLP API is configured for advanced analysis")
        exit(1)
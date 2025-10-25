#!/usr/bin/env python3
"""
Tamil Semantic & Sentiment Analyzer - Production Web Application
Advanced Tamil text analysis with bilingual meaning extraction and AI integration
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
from production_config import ProductionConfig

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern for production deployment"""
    app = Flask(__name__)
    
    # Production configuration
    app.config.from_object(ProductionConfig)
    app.config['MAX_CONTENT_LENGTH'] = ProductionConfig.MAX_CONTENT_LENGTH
    
    # Enable CORS for cross-origin requests
    CORS(app, origins=['*'])
    
    # Initialize semantic analyzer
    semantic_analyzer = SemanticSentimentAnalyzer()
    
    @app.route('/')
    def index():
        """Main dashboard route"""
        app_info = ProductionConfig.get_app_info()
        return render_template('dashboard.html', app_info=app_info)
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': ProductionConfig.get_app_info()['version'],
            'gemini_available': ProductionConfig.is_gemini_available()
        })
    
    @app.route('/api/analyze', methods=['POST'])
    def analyze_text():
        """Analyze Tamil text for semantic meaning and sentiment"""
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({'error': 'No text provided'}), 400
            
            text = data['text'].strip()
            
            if not text:
                return jsonify({'error': 'Empty text provided'}), 400
            
            if len(text) > 5000:  # Limit text length
                return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
            
            logger.info(f"API Analysis request for {len(text)} characters")
            
            # Perform analysis
            analysis_result = semantic_analyzer.analyze_semantic_sentiment(text)
            
            # Add metadata
            analysis_result['api_version'] = '2.0'
            analysis_result['features_used'] = ['semantic_analysis', 'sentiment_analysis']
            
            if analysis_result.get('enhanced_analysis'):
                analysis_result['features_used'].append('gemini_enhancement')
            
            return jsonify(analysis_result)
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return jsonify({
                'error': 'Analysis failed',
                'message': 'Please try again with different text',
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/api/info')
    def app_info():
        """Get application information"""
        return jsonify(ProductionConfig.get_app_info())
    
    @app.errorhandler(404)
    def not_found(error):
        """Custom 404 handler"""
        return jsonify({
            'error': 'Endpoint not found',
            'available_endpoints': [
                '/ - Main dashboard',
                '/api/health - Health check',
                '/api/analyze - Text analysis (POST)',
                '/api/info - Application information'
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Custom 500 handler"""
        return jsonify({
            'error': 'Internal server error',
            'message': 'Please try again later',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    return app

def print_startup_banner():
    """Print startup information"""
    app_info = ProductionConfig.get_app_info()
    print("🚀 Starting Tamil Semantic & Sentiment Analysis System")
    print("=" * 63)
    print(f"📱 Application: {app_info['name']}")
    print(f"🔢 Version: {app_info['version']}")
    print(f"🧠 AI Enhancement: {'✅ Enabled' if ProductionConfig.is_gemini_available() else '❌ Disabled'}")
    print(f"🌐 Host: {ProductionConfig.HOST}:{ProductionConfig.PORT}")
    print(f"🔧 Debug Mode: {'ON' if ProductionConfig.DEBUG else 'OFF'}")
    print("=" * 63)
    print("📝 Features available:")
    for feature in app_info['features']:
        print(f"   • {feature}")
    print("=" * 63)

if __name__ == '__main__':
    # Initialize application
    print_startup_banner()
    
    app = create_app()
    
    # Run application
    app.run(
        host=ProductionConfig.HOST,
        port=ProductionConfig.PORT,
        debug=ProductionConfig.DEBUG
    )
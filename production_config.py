"""
Production Configuration for Tamil Semantic Sentiment Analyzer
Environment variables and production settings
"""
import os
from typing import Optional

class ProductionConfig:
    """Production configuration with environment variables"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tamil-sentiment-analyzer-2024-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your_gemini_api_key_here')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    GEMINI_TEMPERATURE = float(os.environ.get('GEMINI_TEMPERATURE', '0.7'))
    GEMINI_MAX_TOKENS = int(os.environ.get('GEMINI_MAX_TOKENS', '1000'))
    
    # Feature Flags
    ENABLE_GEMINI_ENHANCEMENT = os.environ.get('ENABLE_GEMINI', 'True').lower() == 'true'
    ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'False').lower() == 'true'
    
    # Performance Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '30'))
    
    @classmethod
    def is_gemini_available(cls) -> bool:
        """Check if Gemini API is properly configured"""
        api_key = cls.GEMINI_API_KEY
        return bool(api_key and api_key != 'AIzaSyDToXd7MR-Vir-ILIYKQ4lmTdKlJH5GAkY' and len(api_key) > 10)
    
    @classmethod
    def get_app_info(cls) -> dict:
        """Get application information for display"""
        return {
            'name': 'Tamil Semantic & Sentiment Analyzer',
            'version': '2.0.0',
            'description': 'Advanced Tamil text analysis with bilingual meaning extraction',
            'author': 'Tamil NLP Team',
            'features': [
                'Semantic analysis of Tamil text',
                'Sentiment analysis and emotion detection',
                'Bilingual meaning extraction (Tamil + English)',
                'Cultural context analysis',
                'AI-powered explanations'
            ]
        }
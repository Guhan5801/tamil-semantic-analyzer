# Configuration file for Tamil Handwritten OCR System
# Store your API keys and system settings here

import os
from typing import Dict, Any

class Config:
    """Configuration class for managing API keys and system settings"""
    
    # Gemini API Configuration
    # Get from environment, but validate it's the correct length (39 chars)
    _env_key = os.getenv('GEMINI_API_KEY', '')
    _correct_key = 'AIzaSyDToXd7MR-Vir-ILIYKQ4lmTdKlJH5GAkY'
    
    # Use environment key only if it's valid (39 characters), otherwise use hardcoded
    if _env_key and len(_env_key) == 39:
        GEMINI_API_KEY = _env_key
    else:
        GEMINI_API_KEY = _correct_key
        if _env_key and len(_env_key) != 39:
            print(f"⚠️ WARNING: Invalid GEMINI_API_KEY in environment (length: {len(_env_key)}). Using hardcoded key.")
    
    GEMINI_MODEL = 'gemini-2.5-flash'  # Stable model for production
    GEMINI_TEMPERATURE = 0.3  # Lower for more consistent cultural analysis
    GEMINI_MAX_TOKENS = 2048
    
    # OCR Configuration
    OCR_CONFIDENCE_THRESHOLD = 0.5
    USE_MULTIPLE_OCR_ENGINES = True
    
    # Cultural Analysis Configuration
    KAMBARAMAYANAM_CONFIDENCE_THRESHOLD = 0.5
    ENABLE_GEMINI_ENHANCEMENT = True  # Use Gemini for enhanced cultural analysis
    
    # Web Interface Configuration
    FLASK_SECRET_KEY = 'tamil_ocr_cultural_context_2024'
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = True
    
    # File Upload Configuration
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'tiff', 'bmp'}
    
    # Database Configuration
    DATABASE_PATH = 'kambaramayanam.db'
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def set_gemini_api_key(cls, api_key: str):
        """Set Gemini API key"""
        cls.GEMINI_API_KEY = api_key
        os.environ['GEMINI_API_KEY'] = api_key
    
    @classmethod
    def get_gemini_config(cls) -> Dict[str, Any]:
        """Get Gemini API configuration"""
        return {
            'api_key': cls.GEMINI_API_KEY,
            'model': cls.GEMINI_MODEL,
            'temperature': cls.GEMINI_TEMPERATURE,
            'max_tokens': cls.GEMINI_MAX_TOKENS
        }
    
    @classmethod
    def is_gemini_available(cls) -> bool:
        """Check if Gemini API is configured and available"""
        return bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY.strip())
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration settings"""
        return {
            'gemini_api_configured': cls.is_gemini_available(),
            'database_path_valid': bool(cls.DATABASE_PATH),
            'flask_config_valid': bool(cls.FLASK_SECRET_KEY),
            'ocr_config_valid': 0 <= cls.OCR_CONFIDENCE_THRESHOLD <= 1,
            'cultural_config_valid': 0 <= cls.KAMBARAMAYANAM_CONFIDENCE_THRESHOLD <= 1
        }

# Example usage - Gemini API key is now configured!
# The API key is already set above: AIzaSyDToXd7MR-Vir-ILIYKQ4lmTdKlJH5GAkY

# You can also set via environment variable if preferred:
# export GEMINI_API_KEY='AIzaSyDToXd7MR-Vir-ILIYKQ4lmTdKlJH5GAkY'

# Or update programmatically:
# Config.set_gemini_api_key('AIzaSyDToXd7MR-Vir-ILIYKQ4lmTdKlJH5GAkY')
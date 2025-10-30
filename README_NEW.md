# Tamil Semantic Analyzer - Reorganized Project Structure

## 🎯 Project Overview
A professional Tamil text analysis system with semantic analysis, sentiment detection, and AI-powered insights using Google Gemini.

## 📁 Project Structure

```
tamil-semantic-analyzer/
│
├── 📁 src/                          # All source code
│   ├── core/                        # Core analysis engines
│   ├── analyzers/                   # Specialized analyzers  
│   ├── web/                         # Web application
│   ├── api/                         # Serverless API
│   └── utils/                       # Utilities
│
├── 📁 config/                       # Configuration
├── 📁 tests/                        # Test suite
├── 📁 scripts/                      # CLI & utilities
├── 📁 deployment/                   # Deployment configs
├── 📁 docs/                         # Documentation
├── 📁 data/                         # Data & uploads
│
└── 📄 Core Files
    ├── README.md
    ├── requirements.txt
    ├── vercel.json
    └── pyproject.toml
```

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the app
python scripts/quick_start.py
```

### Access the Application
- **Dashboard**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **API Docs**: http://localhost:5000/api/docs

## 📚 Features

### ✨ Core Features
- **Semantic Analysis**: Deep understanding of Tamil text meaning
- **Sentiment Analysis**: Emotion and sentiment detection
- **AI Enhancement**: Gemini AI integration for advanced insights
- **Tamil-Only Validation**: Ensures pure Tamil text input
- **Real-time Analysis**: Instant results

### 🔧 Technical Features
- Flask web framework
- RESTful API
- Serverless deployment (Vercel)
- Responsive UI
- Clean architecture

## 📖 Documentation

Detailed documentation available in `docs/`:
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture](docs/ARCHITECTURE.md)

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask
- **AI**: Google Gemini API
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Deployment**: Vercel (Serverless)
- **Database**: SQLite (optional)

## 📦 Directory Details

### `/src/core/`
Core analysis engines and AI integration
- `semantic_sentiment_analyzer.py` - Main analyzer
- `gemini_integration.py` - AI integration

### `/src/analyzers/`
Specialized analysis modules
- `text_analyzer.py` - Text processing
- `context_analyzer.py` - Context understanding

### `/src/web/`
Web application (Flask)
- `app.py` - Main application
- `templates/` - HTML templates
- `routes/` - API routes

### `/src/api/`
Serverless API for Vercel
- `index.py` - Entry point

### `/config/`
Configuration files
- `config.py` - Base config
- `production_config.py` - Production settings

### `/tests/`
Test suite
- Unit tests
- Integration tests
- API tests

### `/scripts/`
Utility scripts
- `quick_start.py` - Quick start app
- `quick_sentiment_cli.py` - CLI tool

### `/deployment/`
Deployment configurations
- Docker
- Vercel
- Railway
- Heroku

### `/docs/`
Documentation
- Setup guides
- API docs
- Architecture diagrams

### `/data/`
Data and uploads
- Upload directory
- Sample images
- Databases

## 🌐 Deployment

### Vercel (Recommended)
```bash
# Already configured!
git push origin main
# Auto-deploys to Vercel
```

### Environment Variables
Required in Vercel dashboard:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `FLASK_ENV` - production

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this project

## 🙏 Acknowledgments

- Google Gemini AI for advanced analysis
- Tamil language processing community
- Open source contributors

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs/` folder
- **API**: See API documentation

---

**Made with ❤️ for Tamil language processing**

**Version**: 2.0.0  
**Status**: Production Ready ✅  
**Last Updated**: October 2025

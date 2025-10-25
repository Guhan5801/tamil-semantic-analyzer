# Tamil Semantic & Sentiment Analyzer

## 🚀 Live Web Application for Tamil Text Analysis

A production-ready web application that provides advanced semantic analysis, sentiment detection, and AI-powered bilingual meaning extraction for Tamil text. Built with Flask and enhanced with Gemini AI integration.

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/your-username/tamil-sentiment-analyzer)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## ✨ Features

- **🧠 Semantic Analysis**: Deep understanding of Tamil text structure and meaning
- **💗 Sentiment Detection**: Emotion and mood analysis with confidence scoring
- **🌍 Bilingual Meanings**: AI-powered explanations in both Tamil and English
- **🎨 Modern UI**: Professional, responsive web interface
- **🚀 Production Ready**: Optimized for cloud deployment
- **🤖 AI Enhanced**: Powered by Google Gemini for cultural context
- **📱 Mobile Friendly**: Works seamlessly on all device sizes

## 🎯 Live Demo

Try the live application: **[Tamil Analyzer](https://your-app-name.herokuapp.com)**

### Sample Texts to Try:
- `வணக்கம் நண்பர்களே. எப்படி இருக்கீங்க?`
- `இன்று மிகவும் மகிழ்ச்சியான நாள்`
- `கல்வி என்பது மனிதனின் மிக முக்கியமான சொத்து`

## 🏗️ Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/tamil-sentiment-analyzer.git
   cd tamil-sentiment-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements-prod.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

## 🌐 Deployment Options

### Option 1: Heroku (Recommended)

1. **One-Click Deploy**
   - Click the "Deploy to Heroku" button above
   - Set your `GEMINI_API_KEY` in the environment variables
   - Deploy!

2. **Manual Deploy**
   ```bash
   # Install Heroku CLI
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_api_key_here
   git push heroku main
   ```

### Option 2: Railway

1. **One-Click Deploy**
   - Click the "Deploy on Railway" button above
   - Connect your GitHub repository
   - Set environment variables
   - Deploy!

2. **Manual Deploy**
   ```bash
   # Install Railway CLI
   railway login
   railway new
   railway add
   railway up
   ```

### Option 3: Vercel

```bash
# Install Vercel CLI
npm i -g vercel
vercel --prod
```

### Option 4: Docker

```bash
# Build and run with Docker
docker build -t tamil-analyzer .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key tamil-analyzer
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI features | - | ✅ |
| `SECRET_KEY` | Flask secret key for sessions | auto-generated | ❌ |
| `PORT` | Application port | 5000 | ❌ |
| `FLASK_ENV` | Flask environment | production | ❌ |
| `ENABLE_GEMINI` | Enable AI enhancement | True | ❌ |

### Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your environment variables

## 📊 API Endpoints

### `POST /api/analyze`
Analyze Tamil text for semantic meaning and sentiment.

**Request:**
```json
{
  "text": "வணக்கம் நண்பர்களே"
}
```

**Response:**
```json
{
  "semantic_analysis": {
    "meaning": "தமிழ் பொருள்",
    "english_meaning": "English explanation",
    "word_count": 5,
    "language_detected": "tamil"
  },
  "sentiment_analysis": {
    "overall_sentiment": "positive",
    "confidence": 0.85,
    "explanation": "உணர்வு விளக்கம்"
  },
  "enhanced_analysis": true
}
```

### `GET /api/health`
Health check endpoint for monitoring.

### `GET /api/info`
Application information and version.

## 🏗️ Architecture

```
tamil-sentiment-analyzer/
├── app.py                    # Main Flask application
├── production_config.py      # Production configuration
├── semantic_sentiment_analyzer.py  # Core analysis engine
├── gemini_integration.py     # AI integration
├── templates/
│   └── dashboard_prod.html   # Production UI
├── requirements-prod.txt     # Production dependencies
├── Procfile                  # Heroku configuration
├── Dockerfile                # Container configuration
├── railway.toml              # Railway configuration
├── vercel.json              # Vercel configuration
└── .env.example             # Environment template
```

## 🔍 How It Works

1. **Text Input**: User enters Tamil text through the web interface
2. **Semantic Analysis**: Core engine analyzes text structure, words, and themes
3. **Sentiment Detection**: Identifies emotional content and confidence levels
4. **AI Enhancement**: Gemini AI provides cultural context and bilingual meanings
5. **Results Display**: Professional dashboard shows all analysis results

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Analysis**: Instant feedback with loading animations
- **Bilingual Display**: Tamil and English results side by side
- **Professional Styling**: Modern gradient design with smooth animations
- **Error Handling**: Graceful error messages and retry options

## 🔒 Security Features

- Input validation and sanitization
- Rate limiting protection
- Secure environment variable handling
- Production-ready configuration
- Health check monitoring

## 📈 Performance

- **Fast Analysis**: Optimized processing pipeline
- **Caching**: Smart caching for repeated requests
- **CDN Assets**: Bootstrap and FontAwesome from CDN
- **Lightweight**: Minimal dependencies for faster startup
- **Scalable**: Multi-worker configuration for high traffic

## 🛠️ Development

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install development dependencies
pip install -r requirements-prod.txt

# Run in development mode
export FLASK_DEBUG=True
python app.py
```

### Testing
```bash
# Test the API
curl -X POST http://localhost:5000/api/analyze \\
  -H "Content-Type: application/json" \\
  -d '{"text": "வணக்கம் நண்பர்களே"}'

# Health check
curl http://localhost:5000/api/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for advanced language understanding
- **Bootstrap** for responsive UI components
- **Flask** for the web framework
- **Tamil NLP Community** for inspiration and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/tamil-sentiment-analyzer/issues)
- **Documentation**: [Wiki](https://github.com/your-username/tamil-sentiment-analyzer/wiki)
- **Email**: your-email@example.com

---

**Made with ❤️ for the Tamil NLP community**

[![Tamil](https://img.shields.io/badge/Language-Tamil-red)](https://en.wikipedia.org/wiki/Tamil_language)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![AI](https://img.shields.io/badge/AI-Gemini-purple)](https://ai.google.dev)
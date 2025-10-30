import os
import sys
import re
import logging
import hashlib
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure project root is on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

app = Flask(__name__)
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
        html = """<!DOCTYPE html>
<html lang=\"ta\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Tamil Semantic & Sentiment Analyzer</title>
    <link href=\"https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/css/bootstrap.min.css\" rel=\"stylesheet\">
    <link href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\" rel=\"stylesheet\">
    <style>
        body{font-family: system-ui, -apple-system, Segoe UI, Roboto, 'Noto Sans Tamil', sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);margin:0;color:#374151}
        .container{max-width:1000px;margin:32px auto;background:#fff;border-radius:12px;box-shadow:0 10px 20px rgba(0,0,0,.08);overflow:hidden}
        .header{padding:24px 28px;background:linear-gradient(135deg,#2563eb,#1e40af);color:#fff}
        .content{padding:24px 28px}
        .section{background:#f8fafc;border:1px solid #eef2f7;border-radius:10px;padding:16px;margin-top:16px}
        textarea{width:100%;border:2px solid #e5e7eb;border-radius:8px;padding:12px}
    </style>
    <script defer src=\"https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/js/bootstrap.bundle.min.js\"></script>
    <script defer src=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js\"></script>
    <meta name=\"robots\" content=\"noindex\" />
    <meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; connect-src 'self' https:; img-src 'self' data:;\" />
    <meta name=\"color-scheme\" content=\"light\" />
    <meta name=\"description\" content=\"Tamil-only text analyzer running on Vercel\" />
</head>
<body>
    <div class=\"container\"> 
        <div class=\"header\">
            <h2 class=\"mb-1\"><i class=\"fa fa-language\"></i> Tamil Semantic & Sentiment Analyzer</h2>
            <div style=\"opacity:.9\">Tamil-only input. English is rejected.</div>
        </div>
        <div class=\"content\">
            <div class=\"section\">
                <label for=\"text\" class=\"form-label\">Enter Tamil Text</label>
                <textarea id=\"text\" rows=\"6\" placeholder=\"உங்கள் தமிழ் உரையை இங்கே தட்டச்சு செய்யவும்...\"></textarea>
                <button id=\"go\" class=\"btn btn-primary mt-3\"><i class=\"fa fa-search\"></i> Analyze</button>
            </div>
            <div id=\"out\" class=\"section\" style=\"display:none\"></div>
        </div>
    </div>
    <script>
        const btn = document.getElementById('go');
        const ta = document.getElementById('text');
        const out = document.getElementById('out');
        btn.addEventListener('click', async () => {
            const text = (ta.value || '').trim();
            if(!text){ alert('Please enter Tamil text.'); return; }
            btn.disabled = true; btn.innerHTML = '<i class=\"fa fa-spinner fa-spin\"></i> Analyzing...';
            try{
                const r = await fetch('/api/analyze', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text})});
                const data = await r.json();
                out.style.display = 'block';
                if(!r.ok){
                    out.innerHTML = '<div class=\"text-danger\">' + (data.error || 'Error') + '</div>';
                }else{
                    const sem = data.semantic_analysis || {}; const sen = data.sentiment_analysis || {};
                    out.innerHTML = `
                        <div><strong>Language:</strong> ${sem.language_detected || 'unknown'}</div>
                        <div><strong>Words:</strong> ${sem.word_count || 0}</div>
                        <div><strong>Complexity:</strong> ${sem.text_complexity || 'unknown'}</div>
                        ${sem.meaning ? `<div class=\"mt-2\"><strong>Meaning:</strong> ${sem.meaning}</div>` : ''}
                        <hr/>
                        <div><strong>Sentiment:</strong> ${sen.overall_sentiment || 'neutral'} (${Math.round((sen.confidence||0)*100)}%)</div>
                    `;
                }
            }catch(e){ out.style.display='block'; out.innerHTML = '<div class=\"text-danger\">Request failed.</div>'; }
            finally{ btn.disabled = false; btn.innerHTML = '<i class=\"fa fa-search\"></i> Analyze'; }
        });
    </script>
</body>
</html>`"""
        return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'analyzer': 'ready' if semantic_analyzer else 'not initialized',
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

        # Do not return any english_meaning key
        semantic_out = dict(result.get('semantic_analysis', {}) or {})
        if 'english_meaning' in semantic_out:
            semantic_out.pop('english_meaning', None)

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
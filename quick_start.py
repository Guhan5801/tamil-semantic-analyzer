"""
Quick Start Script for Tamil Handwritten OCR System
Run this to quickly test the system with sample images
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'PIL', 'cv2', 'numpy', 'easyocr', 'pytesseract', 
        'flask', 'flask_cors'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'cv2':
                import cv2
            elif package == 'flask_cors':
                import flask_cors
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("🔧 Installing required dependencies...")
    
    # Install packages
    packages_to_install = [
        'opencv-python',
        'easyocr', 
        'pytesseract',
        'Pillow',
        'numpy',
        'flask',
        'flask-cors',
        'scikit-image',
        'fuzzywuzzy',
        'python-Levenshtein'
    ]
    
    for package in packages_to_install:
        try:
            os.system(f'pip install {package}')
            print(f"✅ {package} installed")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

def create_sample_images_dir():
    """Create directory for sample images"""
    sample_dir = Path("sample_images")
    sample_dir.mkdir(exist_ok=True)
    
    # Create a README for sample images
    readme_content = """# Sample Images Directory

Place your Tamil handwritten images here for testing.

Supported formats:
- PNG
- JPG/JPEG
- WebP

For best results:
- Use clear, well-lit images
- Ensure text is readable
- Avoid excessive skew or rotation
- Higher resolution is better

Example filenames:
- kambaramayanam_verse.jpg
- tamil_handwriting.png
- manuscript_page.jpg
"""
    
    with open(sample_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    return sample_dir

def check_tesseract():
    """Check if Tesseract OCR is installed on the system"""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

def main():
    """Main quick start function"""
    print("🚀 Tamil Handwritten OCR System - Quick Start")
    print("=" * 55)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right directory
    required_files = ['app.py', 'main_system.py', 'handwritten_ocr_engine.py']
    missing_files = [f for f in required_files if not (current_dir / f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        print("💡 Make sure you're in the tamil-handwritten-ocr-system directory")
        return
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"❌ Missing dependencies: {missing_deps}")
        
        response = input("Would you like to install them now? (y/n): ").lower().strip()
        if response == 'y':
            install_dependencies()
            print("\n🔄 Rechecking dependencies...")
            missing_deps = check_dependencies()
            
            if missing_deps:
                print(f"❌ Still missing: {missing_deps}")
                print("💡 You may need to install them manually:")
                print(f"   pip install {' '.join(missing_deps)}")
                return
        else:
            print("💡 Install dependencies manually with: pip install -r requirements.txt")
            return
    
    print("✅ All Python dependencies are available")
    
    # Check Tesseract
    print("\n🔍 Checking Tesseract OCR...")
    if check_tesseract():
        print("✅ Tesseract OCR is installed and accessible")
    else:
        print("❌ Tesseract OCR not found")
        print("💡 Please install Tesseract OCR:")
        print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   Linux: sudo apt-get install tesseract-ocr tesseract-ocr-tam")
        print("   macOS: brew install tesseract")
        
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            return
    
    # Create sample images directory
    print("\n📁 Setting up sample images directory...")
    sample_dir = create_sample_images_dir()
    print(f"✅ Sample images directory created: {sample_dir}")
    
    # Test the system
    print("\n🧪 Testing the system...")
    try:
        from main_system import TamilLiteraryOCRSystem
        
        print("🔄 Initializing system...")
        system = TamilLiteraryOCRSystem()
        
        if system.system_ready:
            print("✅ System initialized successfully!")
            
            # Test with sample text
            print("\n🧪 Testing with sample text...")
            if hasattr(system, "context_analyzer") and system.context_analyzer is not None and hasattr(system.context_analyzer, "analyze_text_context"):
                test_result = system.context_analyzer.analyze_text_context("அறம் செய விரும்பு")
                
                print(f"📊 Test result:")
                print(f"   Kambaramayanam detection: {'✅' if test_result['is_kambaramayanam'] else '❌'}")
                print(f"   Confidence: {test_result['confidence']:.1%}")
            else:
                print("❌ context_analyzer is not available or not initialized in TamilLiteraryOCRSystem.")
            
            # Show system stats
            stats = system.get_system_stats()
            print(f"\n📈 System statistics:")
            print(f"   Ready for processing: ✅")
            print(f"   Processing time: {test_result.get('processing_time', 0):.3f}s")
            
            system.close()
            
        else:
            print("❌ System initialization failed")
            return
            
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return
    
    # Provide next steps
    print("\n🎯 System is ready! Next steps:")
    print("-" * 30)
    print("1. 📸 Place Tamil handwritten images in the 'sample_images' directory")
    print("2. 🤖 Configure enhancement model (optional but recommended):")
    print("   • Get free API key: https://aistudio.google.com/app/apikey")
    print("   • Visit: http://localhost:5000/configure")
    print("   • Or set: Config.set_gemini_api_key('your-key') in config.py")
    print("3. 🌐 Start the web interface:")
    print("   python app.py")
    print("4. 📱 Open your browser to: http://localhost:5000")
    print("5. 🔬 Or test directly with:")
    print("   python main_system.py")
    
    print("\n📚 What the system can do:")
    print("   • Extract text from handwritten Tamil images")
    print("   • Identify Kambaramayanam verses")
    print("   • Provide cultural context (Seiyul/Vilakkam)")
    print("   • Analyze literary elements")
    print("   • Handle mediocre handwriting quality")
    print("   🔧 WITH ENHANCEMENT: Advanced cultural analysis & deeper insights")
    
    print("\n✨ Ready to preserve Tamil literary heritage!")
    
    # Option to start web server immediately
    response = input("\nWould you like to start the web server now? (y/n): ").lower().strip()
    if response == 'y':
        print("\n🌐 Starting web server...")
        try:
            os.system("python app.py")
        except KeyboardInterrupt:
            print("\n👋 Web server stopped")
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")

if __name__ == "__main__":
    main()
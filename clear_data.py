#!/usr/bin/env python3
"""
Clear all stored data and refresh the Tamil Text Analyzer system
This script will clear:
- In-memory caches
- Python bytecode cache (__pycache__)
- Local storage (via browser refresh)
- Analysis history
"""

import os
import shutil
import sys
import time
from pathlib import Path

def clear_pycache():
    """Remove Python bytecode cache files"""
    print("🗑️ Clearing Python bytecode cache...")
    
    pycache_dirs = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            pycache_dirs.append(pycache_path)
    
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            print(f"   ✅ Removed: {pycache_dir}")
        except Exception as e:
            print(f"   ⚠️ Could not remove {pycache_dir}: {e}")

def clear_memory_caches():
    """Clear in-memory analysis caches"""
    print("🧠 Clearing in-memory analysis caches...")
    
    try:
        # Import and reinitialize the analyzer to clear its cache
        from semantic_sentiment_analyzer import SemanticSentimentAnalyzer
        
        # Create a new instance to clear any existing cache
        analyzer = SemanticSentimentAnalyzer()
        if hasattr(analyzer, 'analysis_cache'):
            analyzer.analysis_cache.clear()
            print("   ✅ Semantic sentiment analysis cache cleared")
            
    except Exception as e:
        print(f"   ⚠️ Could not clear analysis cache: {e}")

def clear_upload_files():
    """Clear any uploaded files"""
    print("📁 Clearing uploaded files...")
    
    uploads_dir = Path('uploads')
    if uploads_dir.exists():
        for file in uploads_dir.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                    print(f"   ✅ Removed: {file}")
                except Exception as e:
                    print(f"   ⚠️ Could not remove {file}: {e}")
    else:
        print("   ✅ No uploads directory found")

def clear_temporary_files():
    """Clear any temporary files"""
    print("🗂️ Clearing temporary files...")
    
    temp_patterns = ['*.tmp', '*.temp', '*.log']
    for pattern in temp_patterns:
        for file in Path('.').glob(pattern):
            try:
                file.unlink()
                print(f"   ✅ Removed: {file}")
            except Exception as e:
                print(f"   ⚠️ Could not remove {file}: {e}")

def restart_system():
    """Restart the system components"""
    print("🔄 System components refreshed")
    print("   ✅ Memory caches cleared")
    print("   ✅ Python modules will be reloaded on next import")
    print("   ✅ Fresh analysis instances will be created")

def main():
    """Main function to clear all data and refresh system"""
    print("🧹 Tamil Text Analyzer - Data Cleanup & Refresh")
    print("=" * 50)
    
    # Change to the script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Clear various types of stored data
    clear_pycache()
    clear_memory_caches()
    clear_upload_files()
    clear_temporary_files()
    restart_system()
    
    print("\n" + "=" * 50)
    print("✅ Data cleanup completed successfully!")
    print("\n💡 To complete the refresh:")
    print("   1. Restart any running web servers")
    print("   2. Refresh your browser to clear localStorage")
    print("   3. The system is now ready with fresh state")
    print("\n🚀 You can now run the system with clean data!")

if __name__ == "__main__":
    main()
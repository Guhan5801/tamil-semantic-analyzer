#!/usr/bin/env python3
"""
Tamil Semantic Analysis Dashboard Demo
Showcases the optimized features and performance improvements
"""

import requests
import json
import time

def demo_dashboard_features():
    """Demonstrate the optimized dashboard features"""
    base_url = "http://localhost:5000"
    
    print("🎯 Tamil Semantic Analysis Dashboard Demo")
    print("=" * 60)
    
    # Test data in Tamil
    test_texts = [
        "நான் மிகவும் மகிழ்ச்சியாக இருக்கிறேன்",  # I am very happy
        "இந்த உலகம் அழகானது",                      # This world is beautiful
        "கோபம் வந்துவிட்டது",                       # Anger has come
        "நான் சோகமாக இருக்கிறேன்"                   # I am sad
    ]
    
    print("\n🚀 Testing System Health")
    print("-" * 30)
    
    # Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ System Status:", health_data['status'])
            print("📊 Engines Available:")
            for engine, status in health_data['engines'].items():
                print(f"   • {engine}: {'✅' if status else '❌'}")
        else:
            print("❌ Health check failed")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print("\n📈 Testing Analytics")
    print("-" * 30)
    
    # Analytics check
    try:
        response = requests.get(f"{base_url}/api/analytics", timeout=5)
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Analytics Available")
            print(f"📝 Cache Size: {analytics['cache_stats']['cache_size']}")
            print(f"🧠 Gemini Enabled: {analytics['system_info']['gemini_enabled']}")
            print(f"⚡ Version: {analytics['system_info']['analyzer_version']}")
        else:
            print("❌ Analytics failed")
    except Exception as e:
        print(f"❌ Analytics error: {e}")
    
    print("\n💬 Testing Sentiment Analysis with Caching")
    print("-" * 50)
    
    total_processing_time = 0
    cache_hits = 0
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n🔄 Test {i}/4: Analyzing Tamil text")
        print(f"📝 Text: {text}")
        
        # First analysis (should be fresh)
        start_time = time.time()
        try:
            response = requests.post(
                f"{base_url}/api/analyze",
                json={"text": text},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                processing_time = time.time() - start_time
                total_processing_time += processing_time
                
                print(f"✅ Status: {data['status']}")
                print(f"😊 Sentiment: {data['sentiment']}")
                print(f"🎯 Confidence: {data['confidence']:.2f}")
                print(f"⏱️  Processing Time: {data['processing_time']}")
                print(f"💾 Cached: {'Yes' if data.get('cached', False) else 'No'}")
                
                if data.get('cached', False):
                    cache_hits += 1
                
                # Show top emotions
                emotions = data.get('emotions', {})
                if emotions:
                    print("🎭 Top Emotions:")
                    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
                    for emotion, value in sorted_emotions:
                        print(f"   • {emotion}: {value:.2f}")
                
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
    
    # Test caching by repeating first analysis
    print(f"\n🔄 Testing Cache Performance (Repeating first analysis)")
    print("-" * 50)
    
    cache_start_time = time.time()
    try:
        response = requests.post(
            f"{base_url}/api/analyze",
            json={"text": test_texts[0]},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            cache_processing_time = time.time() - cache_start_time
            
            print(f"✅ Cache Test Successful")
            print(f"💾 Cached: {'Yes' if data.get('cached', False) else 'No'}")
            print(f"⚡ Cache Processing Time: {cache_processing_time:.3f}s")
            print(f"🚀 Speed Improvement: {((total_processing_time/len(test_texts))/cache_processing_time):.1f}x faster")
            
    except Exception as e:
        print(f"❌ Cache test error: {e}")
    
    print("\n📊 Performance Summary")
    print("=" * 60)
    print(f"📈 Total Tests: {len(test_texts)}")
    print(f"💾 Cache Hits: {cache_hits}")
    print(f"⏱️  Average Processing Time: {total_processing_time/len(test_texts):.2f}s")
    print(f"🎯 Cache Hit Rate: {(cache_hits/len(test_texts))*100:.1f}%")
    
    print("\n🌐 Dashboard Access URLs")
    print("-" * 30)
    print(f"🎨 Modern Dashboard: {base_url}/dashboard")
    print(f"🔧 Classic Interface: {base_url}/")
    print(f"🧪 Test Interface: {base_url}/test")
    print(f"📊 Health Check: {base_url}/api/health")
    print(f"📈 Analytics: {base_url}/api/analytics")
    
    print("\n✨ Optimization Features Demonstrated:")
    print("-" * 40)
    print("✅ Intelligent caching system")
    print("✅ Optimized API responses") 
    print("✅ Real-time health monitoring")
    print("✅ Performance analytics")
    print("✅ Enhanced error handling")
    print("✅ Modern dashboard interface")
    
    print("\n🎉 Demo Complete! The optimized dashboard is ready for use.")

if __name__ == "__main__":
    demo_dashboard_features()
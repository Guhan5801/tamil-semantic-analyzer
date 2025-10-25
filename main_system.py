"""
Main Integration Module - Complete Tamil Handwritten OCR System
Combines all components for end-to-end processing
"""

import logging
import time
import os
import sys
from typing import Dict, Any, Optional
from PIL import Image
import json

# Import our modules
try:
    from handwritten_ocr_engine import TamilHandwrittenOCR
    from context_analyzer import TamilContextAnalyzer
    from kambaramayanam_database import KambaramayanamDatabase
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all modules are in the same directory")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TamilLiteraryOCRSystem:
    """
    Complete Tamil Handwritten OCR System with Cultural Context
    Main class that orchestrates all components
    """
    
    def __init__(self):
        logger.info("🚀 Initializing Tamil Literary OCR System...")
        
        # Initialize components
        self.ocr_engine = None
        self.context_analyzer = None
        self.database = None
        self.system_ready = False
        
        # Performance metrics
        self.stats = {
            'total_images_processed': 0,
            'successful_extractions': 0,
            'kambaramayanam_detections': 0,
            'average_processing_time': 0.0,
            'total_processing_time': 0.0
        }
        
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize all system components"""
        try:
            # Initialize OCR Engine
            logger.info("📖 Initializing OCR Engine...")
            self.ocr_engine = TamilHandwrittenOCR()
            
            # Initialize Context Analyzer
            logger.info("🧠 Initializing Context Analyzer...")
            self.context_analyzer = TamilContextAnalyzer()
            
            # Initialize Database
            logger.info("🗄️ Initializing Database...")
            self.database = KambaramayanamDatabase()
            
            self.system_ready = True
            logger.info("✅ System initialization complete!")
            logger.info("🎯 Ready to process Tamil handwritten images")
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {str(e)}")
            self.system_ready = False
            raise
    
    def process_image(self, image_path_or_pil: str | Image.Image, 
                     save_results: bool = False,
                     output_dir: str = "results") -> Dict[str, Any]:
        """
        Main processing function - complete pipeline
        
        Args:
            image_path_or_pil: Path to image file or PIL Image object
            save_results: Whether to save results to file
            output_dir: Directory to save results
            
        Returns:
            Complete analysis results
        """
        
        if not self.system_ready:
            raise RuntimeError("System not properly initialized")
        
        start_time = time.time()
        
        try:
            # Step 1: Load and validate image
            logger.info("📸 Loading image...")
            if isinstance(image_path_or_pil, str):
                if not os.path.exists(image_path_or_pil):
                    raise FileNotFoundError(f"Image file not found: {image_path_or_pil}")
                image = Image.open(image_path_or_pil)
                image_source = os.path.basename(image_path_or_pil)
            else:
                image = image_path_or_pil
                image_source = "PIL_Image_Object"
            
            logger.info(f"📊 Image loaded: {image.size} pixels, {image.mode} mode")
            
            # Step 2: OCR Processing
            logger.info("🔤 Starting OCR processing...")
            ocr_start = time.time()
            ocr_result = self.ocr_engine.extract_text_from_image(image)
            ocr_time = time.time() - ocr_start
            
            if not ocr_result['success']:
                raise RuntimeError(f"OCR failed: {ocr_result['error']}")
            
            extracted_text = ocr_result['text']
            logger.info(f"📝 OCR completed: {len(extracted_text)} characters in {ocr_time:.2f}s")
            
            # Step 3: Cultural Context Analysis
            logger.info("🎭 Analyzing cultural context...")
            context_start = time.time()
            context_result = self.context_analyzer.analyze_text_context(extracted_text)
            context_time = time.time() - context_start
            
            logger.info(f"🧠 Context analysis completed in {context_time:.2f}s")
            
            # Step 4: Compile comprehensive results
            total_time = time.time() - start_time
            
            results = {
                'system_info': {
                    'processing_timestamp': time.time(),
                    'image_source': image_source,
                    'system_version': '1.0.0',
                    'components_used': ['TamilHandwrittenOCR', 'TamilContextAnalyzer', 'KambaramayanamDatabase']
                },
                'image_info': {
                    'size': image.size,
                    'mode': image.mode,
                    'format': getattr(image, 'format', 'Unknown')
                },
                'ocr_results': {
                    'extracted_text': extracted_text,
                    'text_length': len(extracted_text),
                    'engine_used': ocr_result.get('engine_used', 'Unknown'),
                    'confidence': ocr_result.get('confidence', 0.0),
                    'enhancements_applied': ocr_result.get('enhancements_applied', []),
                    'processing_time': ocr_time
                },
                'cultural_analysis': {
                    'is_kambaramayanam': context_result['is_kambaramayanam'],
                    'confidence': context_result['confidence'],
                    'cultural_context': context_result['cultural_context'],
                    'verse_matches': context_result['verse_matches'],
                    'seiyul_explanations': context_result['seiyul_explanations'],
                    'literary_analysis': context_result['literary_analysis'],
                    'recommendations': context_result['recommendations'],
                    'processing_time': context_time
                },
                'performance_metrics': {
                    'total_processing_time': total_time,
                    'ocr_time_percentage': (ocr_time / total_time) * 100,
                    'analysis_time_percentage': (context_time / total_time) * 100,
                    'words_per_second': len(extracted_text.split()) / total_time if extracted_text else 0
                },
                'success': True
            }
            
            # Update system statistics
            self._update_stats(results)
            
            # Save results if requested
            if save_results:
                self._save_results(results, output_dir, image_source)
            
            logger.info(f"✅ Processing completed successfully in {total_time:.2f}s")
            logger.info(f"🎯 Kambaramayanam: {'Yes' if context_result['is_kambaramayanam'] else 'No'} ({context_result['confidence']:.1%} confidence)")
            
            return results
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time,
                'system_info': {
                    'processing_timestamp': time.time(),
                    'image_source': image_source if 'image_source' in locals() else 'Unknown'
                }
            }
            
            logger.error(f"❌ Processing failed: {str(e)}")
            return error_result
    
    def process_batch(self, image_paths: list, 
                     output_dir: str = "batch_results") -> Dict[str, Any]:
        """Process multiple images in batch"""
        
        logger.info(f"📦 Starting batch processing of {len(image_paths)} images")
        
        batch_start = time.time()
        results = []
        successful_count = 0
        kambaramayanam_count = 0
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"🔄 Processing image {i}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            try:
                result = self.process_image(image_path, save_results=True, output_dir=output_dir)
                results.append(result)
                
                if result['success']:
                    successful_count += 1
                    if result['cultural_analysis']['is_kambaramayanam']:
                        kambaramayanam_count += 1
                        
            except Exception as e:
                logger.error(f"❌ Failed to process {image_path}: {str(e)}")
                results.append({
                    'success': False,
                    'error': str(e),
                    'image_path': image_path
                })
        
        batch_time = time.time() - batch_start
        
        # Compile batch summary
        batch_summary = {
            'batch_info': {
                'total_images': len(image_paths),
                'successful_extractions': successful_count,
                'kambaramayanam_detections': kambaramayanam_count,
                'success_rate': (successful_count / len(image_paths)) * 100,
                'kambaramayanam_rate': (kambaramayanam_count / successful_count) * 100 if successful_count > 0 else 0,
                'total_processing_time': batch_time,
                'average_time_per_image': batch_time / len(image_paths)
            },
            'individual_results': results,
            'summary_statistics': self.get_system_stats()
        }
        
        # Save batch summary
        summary_path = os.path.join(output_dir, 'batch_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(batch_summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Batch processing completed:")
        logger.info(f"   📊 Success rate: {batch_summary['batch_info']['success_rate']:.1f}%")
        logger.info(f"   🎯 Kambaramayanam rate: {batch_summary['batch_info']['kambaramayanam_rate']:.1f}%")
        logger.info(f"   ⏱️ Total time: {batch_time:.2f}s")
        logger.info(f"   📁 Results saved to: {output_dir}")
        
        return batch_summary
    
    def _update_stats(self, results: Dict[str, Any]):
        """Update system performance statistics"""
        
        if results['success']:
            self.stats['total_images_processed'] += 1
            self.stats['successful_extractions'] += 1
            self.stats['total_processing_time'] += results['performance_metrics']['total_processing_time']
            
            if results['cultural_analysis']['is_kambaramayanam']:
                self.stats['kambaramayanam_detections'] += 1
            
            # Update average processing time
            self.stats['average_processing_time'] = (
                self.stats['total_processing_time'] / self.stats['successful_extractions']
            )
    
    def _save_results(self, results: Dict[str, Any], 
                     output_dir: str, image_source: str):
        """Save results to JSON file"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(image_source)[0]
        filename = f"{base_name}_results_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save results
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Results saved to: {filepath}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system performance statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset system statistics"""
        self.stats = {
            'total_images_processed': 0,
            'successful_extractions': 0,
            'kambaramayanam_detections': 0,
            'average_processing_time': 0.0,
            'total_processing_time': 0.0
        }
        logger.info("📊 System statistics reset")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        
        health_status = {
            'system_ready': self.system_ready,
            'components': {
                'ocr_engine': self.ocr_engine is not None,
                'context_analyzer': self.context_analyzer is not None,
                'database': self.database is not None
            },
            'stats': self.get_system_stats(),
            'timestamp': time.time()
        }
        
        return health_status
    
    def close(self):
        """Clean up system resources"""
        logger.info("🔄 Closing system components...")
        
        if self.context_analyzer:
            self.context_analyzer.close()
        
        if self.database:
            self.database.close()
        
        logger.info("✅ System shutdown complete")

# Demo function
def demo_system():
    """Demonstrate the complete system with sample usage"""
    
    print("🎭 Tamil Literary OCR System Demo")
    print("=" * 50)
    
    # Initialize system
    system = TamilLiteraryOCRSystem()
    
    # Check system health
    health = system.health_check()
    print(f"🏥 System Health: {'✅ Ready' if health['system_ready'] else '❌ Not Ready'}")
    
    # Test with sample text (simulating OCR result)
    test_scenarios = [
        {
            'name': 'Kambaramayanam Verse',
            'text': 'அறம் செய விரும்பு அறம் செய விரும்பு',
            'description': 'Famous moral teaching from Kambaramayanam'
        },
        {
            'name': 'Character Reference',
            'text': 'இராமன் சீதையுடன் வனவாசம் சென்றான்',
            'description': 'Reference to Rama and Sita'
        },
        {
            'name': 'Non-Kambaramayanam',
            'text': 'இன்று ஒரு நல்ல நாள் அழகான வானிலை',
            'description': 'General Tamil text'
        }
    ]
    
    print("\n🧪 Testing with sample texts:")
    print("-" * 30)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   Text: '{scenario['text']}'")
        print(f"   Description: {scenario['description']}")
        
        # Simulate processing by using context analyzer directly
        result = system.context_analyzer.analyze_text_context(scenario['text'])
        
        print(f"   🎯 Kambaramayanam: {'✅ Yes' if result['is_kambaramayanam'] else '❌ No'}")
        print(f"   📊 Confidence: {result['confidence']:.1%}")
        
        if result['verse_matches']:
            print(f"   📖 Best match: {result['verse_matches'][0]['verse_reference']}")
        
        if result['seiyul_explanations']:
            print(f"   📚 Has Seiyul explanation: ✅")
    
    # Display system statistics
    stats = system.get_system_stats()
    print(f"\n📈 System Statistics:")
    print(f"   Images processed: {stats['total_images_processed']}")
    print(f"   Successful extractions: {stats['successful_extractions']}")
    print(f"   Kambaramayanam detections: {stats['kambaramayanam_detections']}")
    
    # Close system
    system.close()
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    demo_system()
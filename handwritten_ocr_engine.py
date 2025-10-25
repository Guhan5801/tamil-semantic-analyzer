#!/usr/bin/env python3
"""
Advanced Tamil Handwritten OCR Engine
Specialized for converting handwritten Tamil text (including mediocre handwriting) to digital format
"""

import cv2
import numpy as np
import logging
from typing import Dict, List, Tuple, Any
import time
import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TamilHandwrittenOCR:
    """Advanced OCR engine specifically designed for Tamil handwritten text"""
    
    def __init__(self):
        self.engines = []
        self.initialized = False
        self.preprocessing_params = {
            'gaussian_blur': (1, 1),
            'contrast_factor': 1.5,
            'brightness_factor': 1.2,
            'sharpness_factor': 2.0
        }
        self.initialize_engines()
    
    def initialize_engines(self):
        """Initialize multiple OCR engines for better accuracy"""
        logger.info("Initializing Tamil handwritten OCR engines...")
        
        # Engine 1: EasyOCR (Primary for Tamil)
        try:
            import easyocr
            self.easyocr_reader = easyocr.Reader(['ta', 'en'], gpu=False)
            self.engines.append('easyocr')
            logger.info("✅ EasyOCR initialized for Tamil handwriting")
        except Exception as e:
            logger.warning(f"EasyOCR not available: {e}")
        
        # Engine 2: Tesseract (Fallback)
        try:
            # Configure Tesseract for Tamil
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.engines.append('tesseract')
            logger.info("✅ Tesseract initialized for Tamil fallback")
        except Exception as e:
            logger.warning(f"Tesseract not available: {e}")
        
        # Engine 3: Custom preprocessing for difficult handwriting
        self.engines.append('enhanced_preprocessing')
        
        self.initialized = len(self.engines) > 0
        logger.info(f"Initialized {len(self.engines)} OCR engines: {self.engines}")
    
    def enhance_image_for_handwriting(self, image_path: str) -> List[str]:
        """Advanced image preprocessing specifically for handwritten Tamil text"""
        
        enhanced_images = []
        
        try:
            # Load image
            original_image = Image.open(image_path)
            
            # Convert to grayscale if needed
            if original_image.mode != 'L':
                gray_image = original_image.convert('L')
            else:
                gray_image = original_image
            
            # Enhancement 1: Standard preprocessing
            enhanced1 = self.standard_enhancement(gray_image)
            enhanced1_path = image_path.replace('.', '_enhanced1.')
            enhanced1.save(enhanced1_path)
            enhanced_images.append(enhanced1_path)
            
            # Enhancement 2: High contrast for faded handwriting
            enhanced2 = self.high_contrast_enhancement(gray_image)
            enhanced2_path = image_path.replace('.', '_enhanced2.')
            enhanced2.save(enhanced2_path)
            enhanced_images.append(enhanced2_path)
            
            # Enhancement 3: Noise reduction for rough handwriting
            enhanced3 = self.noise_reduction_enhancement(gray_image)
            enhanced3_path = image_path.replace('.', '_enhanced3.')
            enhanced3.save(enhanced3_path)
            enhanced_images.append(enhanced3_path)
            
            # Enhancement 4: Morphological operations for thick handwriting
            enhanced4 = self.morphological_enhancement(gray_image)
            enhanced4_path = image_path.replace('.', '_enhanced4.')
            enhanced4.save(enhanced4_path)
            enhanced_images.append(enhanced4_path)
            
            logger.info(f"Created {len(enhanced_images)} enhanced versions for handwriting recognition")
            
        except Exception as e:
            logger.error(f"Image enhancement failed: {e}")
            enhanced_images = [image_path]  # Fallback to original
        
        return enhanced_images
    
    def standard_enhancement(self, image: Image.Image) -> Image.Image:
        """Standard enhancement for typical handwriting"""
        # Increase contrast
        contrast_enhancer = ImageEnhance.Contrast(image)
        enhanced = contrast_enhancer.enhance(self.preprocessing_params['contrast_factor'])
        
        # Increase brightness slightly
        brightness_enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = brightness_enhancer.enhance(self.preprocessing_params['brightness_factor'])
        
        # Sharpen the image
        sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = sharpness_enhancer.enhance(self.preprocessing_params['sharpness_factor'])
        
        return enhanced
    
    def high_contrast_enhancement(self, image: Image.Image) -> Image.Image:
        """High contrast enhancement for faded handwriting"""
        # Convert to numpy array
        img_array = np.array(image)
        
        # Apply histogram equalization
        img_eq = cv2.equalizeHist(img_array)
        
        # Apply adaptive threshold
        img_thresh = cv2.adaptiveThreshold(
            img_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return Image.fromarray(img_thresh)
    
    def noise_reduction_enhancement(self, image: Image.Image) -> Image.Image:
        """Noise reduction for rough/unclear handwriting"""
        # Apply Gaussian blur to reduce noise
        blurred = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Apply median filter
        img_array = np.array(blurred)
        denoised = cv2.medianBlur(img_array, 3)
        
        # Apply bilateral filter for edge preservation
        bilateral = cv2.bilateralFilter(denoised, 9, 75, 75)
        
        return Image.fromarray(bilateral)
    
    def morphological_enhancement(self, image: Image.Image) -> Image.Image:
        """Morphological operations for thick handwriting"""
        img_array = np.array(image)
        
        # Apply threshold
        _, thresh = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY)
        
        # Define kernel for morphological operations
        kernel = np.ones((2,2), np.uint8)
        
        # Apply erosion to thin thick lines
        eroded = cv2.erode(thresh, kernel, iterations=1)
        
        # Apply dilation to connect broken characters
        dilated = cv2.dilate(eroded, kernel, iterations=1)
        
        return Image.fromarray(dilated)
    
    def extract_text_from_image(self, image_path_or_pil) -> Dict[str, Any]:
        """
        Main text extraction method that handles both file paths and PIL images
        Tries multiple engines and enhancements for best results
        """
        try:
            # Handle different input types
            if isinstance(image_path_or_pil, str):
                # File path provided
                image_path = image_path_or_pil
                image = Image.open(image_path)
            else:
                # PIL Image object provided
                image = image_path_or_pil
                # Save temporarily for OCR engines that need file paths
                temp_path = "temp_ocr_image.png"
                image.save(temp_path)
                image_path = temp_path
            
            start_time = time.time()
            best_result = None
            best_confidence = 0
            enhancement_attempts = []
            
            # Try different enhancement combinations
            enhancement_methods = [
                ('original', lambda img: img),
                ('standard', self.standard_enhancement),
                ('high_contrast', self.high_contrast_enhancement),
                ('noise_reduction', self.noise_reduction_enhancement),
                ('morphological', self.morphological_enhancement)
            ]
            
            for method_name, enhancement_func in enhancement_methods:
                try:
                    # Apply enhancement
                    enhanced_image = enhancement_func(image)
                    
                    # Save enhanced image temporarily
                    enhanced_path = f"temp_enhanced_{method_name}.png"
                    enhanced_image.save(enhanced_path)
                    
                    # Try EasyOCR first
                    easyocr_result = self.extract_text_easyocr(enhanced_path)
                    if easyocr_result['success'] and easyocr_result['confidence'] > best_confidence:
                        best_result = easyocr_result
                        best_confidence = easyocr_result['confidence']
                        best_result['enhancements_applied'] = [method_name]
                        enhancement_attempts.append(f"{method_name}_easyocr")
                    
                    # Try Tesseract as backup
                    tesseract_result = self.extract_text_tesseract(enhanced_path)
                    if tesseract_result['success'] and tesseract_result['confidence'] > best_confidence:
                        best_result = tesseract_result
                        best_confidence = tesseract_result['confidence']
                        best_result['enhancements_applied'] = [method_name]
                        enhancement_attempts.append(f"{method_name}_tesseract")
                    
                    # Clean up temporary file
                    if os.path.exists(enhanced_path):
                        os.remove(enhanced_path)
                        
                except Exception as e:
                    logger.warning(f"Enhancement {method_name} failed: {str(e)}")
                    continue
            
            # Clean up temporary original file if created
            if isinstance(image_path_or_pil, Image.Image) and os.path.exists(temp_path):
                os.remove(temp_path)
            
            processing_time = time.time() - start_time
            
            if best_result:
                best_result['total_processing_time'] = processing_time
                best_result['enhancement_attempts'] = enhancement_attempts
                logger.info(f"✅ Text extraction successful: {best_confidence:.1%} confidence in {processing_time:.2f}s")
                return best_result
            else:
                logger.warning("❌ No successful text extraction with any method")
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'error': 'Failed to extract text with any enhancement method',
                    'enhancement_attempts': enhancement_attempts,
                    'processing_time': processing_time
                }
                
        except Exception as e:
            logger.error(f"❌ Text extraction failed: {str(e)}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'processing_time': time.time() - start_time if 'start_time' in locals() else 0
            }
    
    def extract_text_easyocr(self, image_path: str) -> Dict[str, Any]:
        """Extract text using EasyOCR (primary engine)"""
        try:
            start_time = time.time()
            
            # Process with EasyOCR
            results = self.easyocr_reader.readtext(image_path)
            
            # Extract text and calculate confidence
            extracted_lines = []
            total_confidence = 0
            
            for result in results:
                bbox, text, confidence = result
                if confidence > 0.3:  # Filter low confidence results
                    extracted_lines.append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
                    total_confidence += confidence
            
            # Combine all text
            full_text = ' '.join([line['text'] for line in extracted_lines])
            avg_confidence = total_confidence / len(extracted_lines) if extracted_lines else 0
            
            processing_time = time.time() - start_time
            
            return {
                'text': full_text,
                'lines': extracted_lines,
                'confidence': avg_confidence,
                'processing_time': processing_time,
                'engine': 'easyocr',
                'character_count': len(full_text),
                'line_count': len(extracted_lines)
            }
            
        except Exception as e:
            logger.error(f"EasyOCR extraction failed: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'engine': 'easyocr'
            }
    
    def extract_text_tesseract(self, image_path: str) -> Dict[str, Any]:
        """Extract text using Tesseract (fallback engine)"""
        try:
            start_time = time.time()
            
            # Configure Tesseract for Tamil
            custom_config = r'--oem 3 --psm 6 -l tam'
            
            # Extract text
            text = pytesseract.image_to_string(Image.open(image_path), config=custom_config)
            
            # Get confidence data
            try:
                data = pytesseract.image_to_data(Image.open(image_path), config=custom_config, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                avg_confidence = avg_confidence / 100  # Convert to 0-1 scale
            except:
                avg_confidence = 0.5  # Default confidence
            
            processing_time = time.time() - start_time
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'processing_time': processing_time,
                'engine': 'tesseract',
                'character_count': len(text.strip())
            }
            
        except Exception as e:
            logger.error(f"Tesseract extraction failed: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'engine': 'tesseract'
            }
    
    def process_handwritten_image(self, image_path: str) -> Dict[str, Any]:
        """
        Main function to process handwritten Tamil image
        Uses multiple engines and preprocessing techniques
        """
        
        if not self.initialized:
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'OCR engines not initialized',
                'processing_details': {}
            }
        
        logger.info(f"Processing handwritten Tamil image: {image_path}")
        start_time = time.time()
        
        # Step 1: Create enhanced versions of the image
        enhanced_images = self.enhance_image_for_handwriting(image_path)
        
        # Step 2: Process with multiple engines and images
        all_results = []
        
        for img_path in enhanced_images:
            # Try EasyOCR first (best for Tamil)
            if 'easyocr' in self.engines:
                easyocr_result = self.extract_text_easyocr(img_path)
                easyocr_result['image_variant'] = os.path.basename(img_path)
                all_results.append(easyocr_result)
            
            # Try Tesseract as backup
            if 'tesseract' in self.engines:
                tesseract_result = self.extract_text_tesseract(img_path)
                tesseract_result['image_variant'] = os.path.basename(img_path)
                all_results.append(tesseract_result)
        
        # Step 3: Select best result based on confidence and text quality
        best_result = self.select_best_result(all_results)
        
        # Step 4: Post-process and clean up
        self.cleanup_enhanced_images(enhanced_images, image_path)
        
        total_processing_time = time.time() - start_time
        
        # Step 5: Prepare final result
        final_result = {
            'extracted_text': best_result.get('text', ''),
            'confidence': best_result.get('confidence', 0.0),
            'best_engine': best_result.get('engine', 'none'),
            'best_variant': best_result.get('image_variant', 'original'),
            'character_count': len(best_result.get('text', '')),
            'total_processing_time': total_processing_time,
            'engines_tried': len(all_results),
            'all_results': all_results,
            'handwriting_quality': self.assess_handwriting_quality(best_result),
            'success': len(best_result.get('text', '').strip()) > 0
        }
        
        logger.info(f"Handwritten OCR completed: {final_result['character_count']} characters extracted with {final_result['confidence']:.2%} confidence")
        
        return final_result
    
    def select_best_result(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best OCR result based on confidence and text quality"""
        
        if not results:
            return {'text': '', 'confidence': 0.0, 'engine': 'none'}
        
        # Filter out empty results
        valid_results = [r for r in results if r.get('text', '').strip()]
        
        if not valid_results:
            return {'text': '', 'confidence': 0.0, 'engine': 'none'}
        
        # Score each result based on multiple factors
        scored_results = []
        
        for result in valid_results:
            text = result.get('text', '').strip()
            confidence = result.get('confidence', 0.0)
            
            # Calculate quality score
            score = confidence * 0.7  # Base confidence weight
            
            # Bonus for text length (longer text often means better recognition)
            length_bonus = min(len(text) / 100, 0.2)  # Max 20% bonus
            score += length_bonus
            
            # Bonus for Tamil characters
            tamil_char_count = sum(1 for char in text if ord(char) >= 0x0B80 and ord(char) <= 0x0BFF)
            tamil_ratio = tamil_char_count / len(text) if text else 0
            score += tamil_ratio * 0.1  # Max 10% bonus for Tamil content
            
            scored_results.append((score, result))
        
        # Sort by score and return the best
        scored_results.sort(key=lambda x: x[0], reverse=True)
        best_result = scored_results[0][1]
        
        logger.info(f"Selected best result: {best_result.get('engine')} with score {scored_results[0][0]:.3f}")
        
        return best_result
    
    def assess_handwriting_quality(self, result: Dict[str, Any]) -> str:
        """Assess the quality of handwriting based on OCR results"""
        confidence = result.get('confidence', 0.0)
        
        if confidence >= 0.8:
            return "Excellent - Clear handwriting"
        elif confidence >= 0.6:
            return "Good - Readable handwriting"
        elif confidence >= 0.4:
            return "Moderate - Some unclear characters"
        elif confidence >= 0.2:
            return "Poor - Difficult handwriting"
        else:
            return "Very Poor - Barely readable"
    
    def cleanup_enhanced_images(self, enhanced_images: List[str], original_path: str):
        """Clean up temporary enhanced image files"""
        for img_path in enhanced_images:
            if img_path != original_path and os.path.exists(img_path):
                try:
                    os.remove(img_path)
                except:
                    pass  # Ignore cleanup errors

# Usage example and testing
if __name__ == "__main__":
    print("🚀 Tamil Handwritten OCR Engine")
    print("=" * 50)
    
    # Initialize the OCR engine
    ocr_engine = TamilHandwrittenOCR()
    
    if ocr_engine.initialized:
        print("✅ OCR engine initialized successfully")
        print(f"📊 Available engines: {ocr_engine.engines}")
        print("\n📝 Ready to process handwritten Tamil images!")
        print("💡 This engine is optimized for mediocre handwriting quality")
        print("🎯 Specialized for Kambaramayanam and classical Tamil literature")
    else:
        print("❌ OCR engine initialization failed")
        print("Please install required dependencies: easyocr, opencv-python, pillow")
#!/usr/bin/env python3
"""
Kambaramayanam Database with Cultural Context (Seiyul/Vilakkam)
Complete verse database with meanings and cultural explanations
"""

import sqlite3
import logging
import json
from typing import Dict, List, Tuple, Any, Optional
import time
import re
from difflib import SequenceMatcher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KambaramayanamDatabase:
    """Complete Kambaramayanam database with Seiyul (cultural context) system"""
    
    def __init__(self, db_path: str = "kambaramayanam_with_context.db"):
        self.db_path = db_path
        self.connection = None
        self.initialize_database()
        self.populate_sample_data()
    
    def initialize_database(self):
        """Initialize the database with comprehensive schema"""
        logger.info("Initializing Kambaramayanam database with cultural context...")
        
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            # Main verses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kambaramayanam_verses (
                    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    volume_number INTEGER NOT NULL,
                    chapter_name TEXT NOT NULL,
                    verse_number INTEGER NOT NULL,
                    original_text TEXT NOT NULL,
                    transliteration TEXT,
                    word_meaning TEXT,
                    verse_meaning TEXT,
                    cultural_context TEXT,
                    seiyul_explanation TEXT,
                    famous_level INTEGER DEFAULT 0,  -- 0-5 scale of how famous the line is
                    character_references TEXT,  -- JSON array of characters mentioned
                    literary_devices TEXT,  -- JSON array of literary devices used
                    moral_teaching TEXT,
                    historical_significance TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Individual lines table for precise matching
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS verse_lines (
                    line_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    verse_id INTEGER,
                    line_number INTEGER,
                    line_text TEXT NOT NULL,
                    line_meaning TEXT,
                    key_words TEXT,  -- Important words in this line
                    FOREIGN KEY (verse_id) REFERENCES kambaramayanam_verses (verse_id)
                )
            """)
            
            # Cultural context lookup table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cultural_contexts (
                    context_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context_type TEXT NOT NULL,  -- 'character', 'place', 'concept', 'tradition'
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    significance TEXT,
                    related_verses TEXT  -- JSON array of verse_ids
                )
            """)
            
            # Famous quotes and their explanations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS famous_quotes (
                    quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    verse_id INTEGER,
                    quote_text TEXT NOT NULL,
                    modern_relevance TEXT,
                    usage_context TEXT,
                    similar_quotes TEXT,  -- Similar quotes from other literature
                    FOREIGN KEY (verse_id) REFERENCES kambaramayanam_verses (verse_id)
                )
            """)
            
            self.connection.commit()
            logger.info("✅ Database schema created successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def populate_sample_data(self):
        """Populate database with sample Kambaramayanam verses and context"""
        logger.info("Populating database with Kambaramayanam verses and cultural context...")
        
        try:
            cursor = self.connection.cursor()
            
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM kambaramayanam_verses")
            if cursor.fetchone()[0] > 0:
                logger.info("Database already contains data, skipping population")
                return
            
            # Sample verses with cultural context
            sample_verses = [
                {
                    'volume': 1,
                    'chapter': 'பாலகாண்டம்',
                    'verse_number': 1,
                    'text': 'உலகம் யாவையும் ஏத்த நின்ற\nஉயர்ந்த முத்தமிழ் ஞான வேலவன்\nநிலவு மென்முலை நீல மேனி\nநேர்மை யான பிரான் நம்பிக்கு',
                    'transliteration': 'ulagam yaavaiyum etta ninra uyarnda muttamizh gnaana velavan nilavu menumulai neela meni nermai yaana piraan nambikku',
                    'meaning': 'கம்பன் தமிழ், வடமொழி, பிராகிருதம் என்ற முத்தமிழில் வல்லவனான முருகனை வணங்குகிறார்',
                    'seiyul': 'இது கம்பராமாயணத்தின் அறிமுக பாடல். கம்பன் முருகப் பெருமானை முதலில் வணங்குகிறார். "முத்தமிழ்" என்பது தமிழ், வடமொழி, பிராகிருதம் மூன்றையும் குறிக்கும். கம்பன் தன் காவியத்தை தொடங்கும் முன் இறைவனை வணங்கும் பாரம்பரியத்தை பின்பற்றுகிறார்.',
                    'famous_level': 5,
                    'characters': '["முருகன்", "கம்பன்"]',
                    'devices': '["வணக்கம்", "அணிநிலை", "உவமை"]',
                    'moral': 'இறைவன் துணையுடன் எந்த நல்ல காரியத்தையும் தொடங்க வேண்டும்',
                    'significance': 'கம்பராமாயணத்தின் முதல் பாடல் - தமிழ் இலக்கிய வரலாற்றில் மிக முக்கியமான தொடக்கம்'
                },
                {
                    'volume': 2,
                    'chapter': 'அயோத்தியா காண்டம்',
                    'verse_number': 45,
                    'text': 'அறம் செய விரும்பு\nஅறம் செய விரும்பு\nஅறம் செய விரும்பு',
                    'transliteration': 'aram seiya virumbu aram seiya virumbu aram seiya virumbu',
                    'meaning': 'நீதியைச் செய்ய விரும்பு, நீதியைச் செய்ய விரும்பு, நீதியைச் செய்ய விரும்பு',
                    'seiyul': 'இராமன் தன் வாழ்க்கையின் முக்கிய கொள்கையை மூன்று முறை வலியுறுத்துகிறார். "அறம்" என்பது தர்மம், நீதி, நல்லொழுக்கம் ஆகியவற்றைக் குறிக்கும். மூன்று முறை சொல்வது அதன் முக்கியத்துவத்தை வலியுறுத்துவதற்காக.',
                    'famous_level': 4,
                    'characters': '["இராமன்"]',
                    'devices': '["மறுதளை", "வலியுறுத்தல்"]',
                    'moral': 'அறநெறியில் நிலைத்திருப்பதே வாழ்க்கையின் முதன்மை நோக்கம்',
                    'significance': 'தமிழ் மக்களின் அறநெறி வாழ்க்கைக்கு வழிகாட்டும் பாடல்'
                },
                {
                    'volume': 3,
                    'chapter': 'ஆரண்ய காண்டம்',
                    'verse_number': 23,
                    'text': 'சீதை இராமன் இருவரும்\nசேர்ந்து வாழ்ந்த இன்ப நாள்\nவாதை வந்த போதும்\nவாழ்வின் அர்த்தம் அறிந்தனர்',
                    'transliteration': 'seethai iraaman iruvarum serndu vaazhda inba naal vaadhai vanda podum vaazhvin artham arindanar',
                    'meaning': 'சீதையும் இராமனும் இருவரும் சேர்ந்து வாழ்ந்த மகிழ்ச்சியான நாட்களில், துன்பம் வந்த போதும் வாழ்க்கையின் பொருளை உணர்ந்தனர்',
                    'seiyul': 'இது இராமனும் சீதையும் வனவாசத்தில் எதிர்கொண்ட சவால்களைப் பற்றிய பாடல். துன்பத்தில் உண்மையான அன்பு வெளிப்படும் என்ற கருத்தை உணர்த்துகிறது. "வாழ்வின் அர்த்தம்" என்பது இன்பதுன்பங்களைத் தாண்டிய ஆழமான வாழ்க்கை புரிதலைக் குறிக்கும்.',
                    'famous_level': 3,
                    'characters': '["சீதை", "இராமன்"]',
                    'devices': '["இணையல்", "வேறுபாடு"]',
                    'moral': 'உண்மையான அன்பு துன்பத்திலும் நிலைத்திருக்கும்',
                    'significance': 'தமிழ் இலக்கியத்தில் கணவன்-மனைவி அன்பின் சிறந்த உதாரணம்'
                },
                {
                    'volume': 4,
                    'chapter': 'கிஷ்கிந்தா காண்டம்',
                    'verse_number': 67,
                    'text': 'அனுமன் வீரம் பெற்ற\nஅற்புத வானர சேனை\nநனுமன் நம்பிக்கை கொண்டு\nநல்ல வழி காட்டினான்',
                    'transliteration': 'anuman veeram perra arbudha vaanara senai nanuman nambikkai kondu nalla vazhi kaattinaan',
                    'meaning': 'அனுமன் வீரம் பெற்ற அற்புதமான வானர சேனையுடன், நம்பிக்கை கொண்டு நல்ல வழியைக் காட்டினான்',
                    'seiyul': 'அனுமன் இராமனுக்கு உதவ தன் வீரத்தையும் ஞானத்தையும் பயன்படுத்துகிறார். "வானர சேனை" என்பது அனுமனின் தலைமையில் உள்ள வானரப் படைகளைக் குறிக்கும். அனுமன் கணவாய் - அதாவது வீரம், பக்தி, ஞானம் மூன்றும் கொண்ட ஆளுமையின் சிறந்த உதாரணம்.',
                    'famous_level': 4,
                    'characters': '["அனுமன்", "வானர சேனை"]',
                    'devices': '["குணச்சிறப்பு", "வீரகாவியம்"]',
                    'moral': 'உண்மையான பக்தர்கள் தங்கள் திறமைகளை நல்ல நோக்கத்திற்காக பயன்படுத்துவர்',
                    'significance': 'அனுமன் வழிபாட்டின் அடிப்படை - வீரம் மற்றும் பக்தியின் சேர்க்கை'
                },
                {
                    'volume': 6,
                    'chapter': 'யுத்த காண்டம்',
                    'verse_number': 234,
                    'text': 'இராவணன் அழிந்து போனான்\nஇராமன் வெற்றி பெற்றான்\nஅறம் வென்றது\nஅன்று முதல் அகிலம் மகிழ்ந்தது',
                    'transliteration': 'iraavanan azhindu ponaan iraaman vetri petraan aram vendradu andru mudal agilam magizhndadu',
                    'meaning': 'இராவணன் அழிந்து போனான், இராமன் வெற்றி பெற்றான், அறம் வென்றது, அன்று முதல் உலகமே மகிழ்ந்தது',
                    'seiyul': 'இது இராமாயணத்தின் முக்கிய செய்தி - அறம் அதர்மத்தின் மீது வெற்றி பெறுவது. இராவணன் மிகுந்த வல்லமை படைத்தவனாக இருந்தும், அறநெறி தவறியதால் அழிந்தான். இராமன் நீதி வழியில் நின்று வென்றான். "அகிலம்" என்பது முழு உலகத்தையும் குறிக்கும் - அறம் வெற்றி பெறும்போது உலகமே மகிழும்.',
                    'famous_level': 5,
                    'characters': '["இராவணன்", "இராமன்"]',
                    'devices': '["எதிர்நிலை", "வெற்றிக்காவியம்"]',
                    'moral': 'அறம் எத்தனை பெரிய எதிர்ப்பை சந்தித்தாலும் இறுதியில் வெற்றி பெறும்',
                    'significance': 'நல்லதின் வெற்றி குறித்த தமிழ் மக்களின் நம்பிக்கையின் அடிப்படை'
                }
            ]
            
            # Insert sample verses
            for verse in sample_verses:
                cursor.execute("""
                    INSERT INTO kambaramayanam_verses 
                    (volume_number, chapter_name, verse_number, original_text, transliteration, 
                     verse_meaning, seiyul_explanation, famous_level, character_references, 
                     literary_devices, moral_teaching, historical_significance)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    verse['volume'], verse['chapter'], verse['verse_number'], verse['text'],
                    verse['transliteration'], verse['meaning'], verse['seiyul'], verse['famous_level'],
                    verse['characters'], verse['devices'], verse['moral'], verse['significance']
                ))
                
                verse_id = cursor.lastrowid
                
                # Insert individual lines
                lines = verse['text'].split('\n')
                for i, line in enumerate(lines, 1):
                    if line.strip():
                        cursor.execute("""
                            INSERT INTO verse_lines (verse_id, line_number, line_text)
                            VALUES (?, ?, ?)
                        """, (verse_id, i, line.strip()))
            
            # Insert cultural contexts
            cultural_data = [
                {
                    'type': 'character',
                    'name': 'இராமன்',
                    'description': 'அயோத்தி இளவரசன், மரியாதை புருஷோத்தமன், இராமாயணத்தின் முக்கிய நாயகன்',
                    'significance': 'தர்மத்தின் உருவகம், இலட்சியமான மனிதனின் எடுத்துக்காட்டு'
                },
                {
                    'type': 'character',
                    'name': 'சீதை',
                    'description': 'இராமனின் மனைவி, பொறுமை மற்றும் தூய்மையின் அடையாளம்',
                    'significance': 'தமிழ் மண்ணின் இலட்சிய மாதின் உதாரணம்'
                },
                {
                    'type': 'character',
                    'name': 'அனுமன்',
                    'description': 'இராமனின் மிகச் சிறந்த பக்தன், வானர வீரன், பலசாலி',
                    'significance': 'பக்தி, வீரம், விவேகம் ஆகியவற்றின் சேர்க்கை'
                },
                {
                    'type': 'concept',
                    'name': 'அறம்',
                    'description': 'நீதி, தர்மம், நல்லொழுக்கம், கடமை உணர்வு',
                    'significance': 'இராமாயணத்தின் மையக் கருத்து, வாழ்க்கையின் அடிப்படை கொள்கை'
                },
                {
                    'type': 'place',
                    'name': 'அயோத்தி',
                    'description': 'இராமனின் தலைநகரம், நீதியின் இருப்பிடம்',
                    'significance': 'இலட்சியமான அரசாட்சியின் சின்னம்'
                }
            ]
            
            for context in cultural_data:
                cursor.execute("""
                    INSERT INTO cultural_contexts (context_type, name, description, significance)
                    VALUES (?, ?, ?, ?)
                """, (context['type'], context['name'], context['description'], context['significance']))
            
            self.connection.commit()
            logger.info(f"✅ Successfully populated database with {len(sample_verses)} verses and cultural context")
            
        except Exception as e:
            logger.error(f"Data population failed: {e}")
            raise
    
    def find_matching_verses(self, text: str, similarity_threshold: float = 0.6) -> List[Dict[str, Any]]:
        """Find verses that match the input text with cultural context"""
        
        if not text.strip():
            return []
        
        try:
            cursor = self.connection.cursor()
            
            # Search in verses and lines
            cursor.execute("""
                SELECT v.verse_id, v.volume_number, v.chapter_name, v.verse_number, 
                       v.original_text, v.verse_meaning, v.seiyul_explanation, 
                       v.famous_level, v.character_references, v.moral_teaching,
                       l.line_text, l.line_number
                FROM kambaramayanam_verses v
                LEFT JOIN verse_lines l ON v.verse_id = l.verse_id
            """)
            
            results = cursor.fetchall()
            matches = []
            
            # Clean input text
            clean_input = self.clean_text(text)
            
            for row in results:
                verse_id, volume, chapter, verse_num, original, meaning, seiyul, famous_level, chars, moral, line_text, line_num = row
                
                # Check similarity with full verse
                verse_similarity = self.calculate_similarity(clean_input, self.clean_text(original))
                
                # Check similarity with individual line if available
                line_similarity = 0
                if line_text:
                    line_similarity = self.calculate_similarity(clean_input, self.clean_text(line_text))
                
                # Use the higher similarity
                best_similarity = max(verse_similarity, line_similarity)
                
                if best_similarity >= similarity_threshold:
                    matches.append({
                        'verse_id': verse_id,
                        'volume': volume,
                        'chapter': chapter,
                        'verse_number': verse_num,
                        'original_text': original,
                        'meaning': meaning,
                        'seiyul': seiyul,
                        'famous_level': famous_level,
                        'characters': chars,
                        'moral_teaching': moral,
                        'similarity_score': best_similarity,
                        'match_type': 'line' if line_similarity > verse_similarity else 'verse',
                        'matched_line': line_text if line_similarity > verse_similarity else None,
                        'line_number': line_num if line_similarity > verse_similarity else None
                    })
            
            # Remove duplicates and sort by similarity
            unique_matches = {}
            for match in matches:
                verse_id = match['verse_id']
                if verse_id not in unique_matches or match['similarity_score'] > unique_matches[verse_id]['similarity_score']:
                    unique_matches[verse_id] = match
            
            final_matches = list(unique_matches.values())
            final_matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            logger.info(f"Found {len(final_matches)} matching verses for input text")
            return final_matches
            
        except Exception as e:
            logger.error(f"Verse matching failed: {e}")
            return []
    
    def get_cultural_context(self, verse_id: int) -> Dict[str, Any]:
        """Get detailed cultural context for a specific verse"""
        
        try:
            cursor = self.connection.cursor()
            
            # Get verse details
            cursor.execute("""
                SELECT * FROM kambaramayanam_verses WHERE verse_id = ?
            """, (verse_id,))
            
            verse = cursor.fetchone()
            if not verse:
                return {}
            
            # Get related cultural contexts
            cursor.execute("""
                SELECT * FROM cultural_contexts
            """)
            
            contexts = cursor.fetchall()
            
            # Parse character references
            characters = []
            if verse[9]:  # character_references column
                try:
                    char_names = json.loads(verse[9])
                    for char_name in char_names:
                        for context in contexts:
                            if context[1] == 'character' and context[2] == char_name:
                                characters.append({
                                    'name': context[2],
                                    'description': context[3],
                                    'significance': context[4]
                                })
                except:
                    pass
            
            return {
                'verse_id': verse[0],
                'volume': verse[1],
                'chapter': verse[2],
                'verse_number': verse[3],
                'original_text': verse[4],
                'transliteration': verse[5],
                'word_meaning': verse[6],
                'verse_meaning': verse[7],
                'seiyul_explanation': verse[9],
                'famous_level': verse[10],
                'characters': characters,
                'moral_teaching': verse[12],
                'historical_significance': verse[13],
                'literary_devices': json.loads(verse[11]) if verse[11] else []
            }
            
        except Exception as e:
            logger.error(f"Cultural context retrieval failed: {e}")
            return {}
    
    def clean_text(self, text: str) -> str:
        """Clean text for better matching"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Remove punctuation but keep Tamil characters
        cleaned = re.sub(r'[^\u0B80-\u0BFF\u0020a-zA-Z]', '', cleaned)
        
        return cleaned.lower()
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using multiple methods"""
        
        if not text1 or not text2:
            return 0.0
        
        # Method 1: Sequence matching
        seq_similarity = SequenceMatcher(None, text1, text2).ratio()
        
        # Method 2: Word overlap
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            word_similarity = 0.0
        else:
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            word_similarity = intersection / union if union > 0 else 0.0
        
        # Method 3: Character overlap
        chars1 = set(text1)
        chars2 = set(text2)
        
        if not chars1 or not chars2:
            char_similarity = 0.0
        else:
            char_intersection = len(chars1.intersection(chars2))
            char_union = len(chars1.union(chars2))
            char_similarity = char_intersection / char_union if char_union > 0 else 0.0
        
        # Weighted average
        final_similarity = (seq_similarity * 0.5 + word_similarity * 0.3 + char_similarity * 0.2)
        
        return final_similarity
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM kambaramayanam_verses")
            total_verses = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM verse_lines")
            total_lines = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM cultural_contexts")
            total_contexts = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(famous_level) FROM kambaramayanam_verses")
            avg_fame = cursor.fetchone()[0] or 0
            
            return {
                'total_verses': total_verses,
                'total_lines': total_lines,
                'cultural_contexts': total_contexts,
                'average_fame_level': round(avg_fame, 2),
                'database_path': self.db_path
            }
            
        except Exception as e:
            logger.error(f"Statistics retrieval failed: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

# Usage example
if __name__ == "__main__":
    print("📚 Kambaramayanam Database with Cultural Context")
    print("=" * 55)
    
    # Initialize database
    db = KambaramayanamDatabase()
    
    # Get statistics
    stats = db.get_statistics()
    print(f"📊 Database Statistics:")
    print(f"   Total verses: {stats['total_verses']}")
    print(f"   Total lines: {stats['total_lines']}")
    print(f"   Cultural contexts: {stats['cultural_contexts']}")
    print(f"   Average fame level: {stats['average_fame_level']}")
    
    # Test with sample text
    test_text = "அறம் செய விரும்பு"
    print(f"\n🔍 Testing with text: '{test_text}'")
    
    matches = db.find_matching_verses(test_text)
    
    if matches:
        print(f"✅ Found {len(matches)} matches:")
        for match in matches[:2]:  # Show top 2 matches
            print(f"\n📖 Volume {match['volume']}, {match['chapter']}, Verse {match['verse_number']}")
            print(f"   Text: {match['original_text'][:100]}...")
            print(f"   Meaning: {match['meaning'][:100]}...")
            print(f"   Seiyul: {match['seiyul'][:150]}...")
            print(f"   Similarity: {match['similarity_score']:.2%}")
            print(f"   Fame Level: {match['famous_level']}/5")
    else:
        print("❌ No matches found")
    
    db.close()
    print("\n✅ Database operations completed!")
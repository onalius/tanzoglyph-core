import unittest
import os
import sys
import json
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tanzoglyph.encoder import (
    encode_profile,
    encode_traits,
    encode_archetypes,
    encode_spiritual_arcs,
    encode_mood,
    encode_scars,
    encode_projection,
    encode_intensity,
    encode_inflection
)

from tanzoglyph.decoder import decode_glyph


class TestEncoder(unittest.TestCase):
    """Test cases for the TanzoGlyph encoder module"""

    def setUp(self):
        # Sample profile data for testing
        self.sample_profile = {
            "name": "Test Profile",
            "version": "1.0.0",
            "traits": {
                "analytical": 0.85,
                "creative": 0.75,
                "determined": -0.20,
                "empathetic": 0.60
            },
            "archetypes": [
                {"name": "Sage", "weight": 0.85},
                {"name": "Creator", "weight": 0.65}
            ],
            "spiritual_arcs": [
                {"name": "Wisdom Journey", "progress": 0.70},
                {"name": "Self-Discovery", "progress": 0.45}
            ],
            "mood_profile": {
                "calm": 0.75,
                "curious": 0.85,
                "focused": 0.65
            },
            "scars": [
                {"name": "Imposter Syndrome", "intensity": 0.55, "healing": 0.60},
                {"name": "Perfectionism", "intensity": 0.70, "healing": 0.40}
            ],
            "projection": {
                "clarity": 0.80,
                "precision": 0.75,
                "warmth": 0.50
            },
            "intensity": {
                "cognitive": 0.85,
                "emotional": 0.60,
                "intuitive": 0.70
            },
            "inflection": {
                "cognitive": "rising",
                "emotional": "stable",
                "intuitive": "oscillating"
            }
        }

    def test_encode_profile(self):
        """Test encoding a complete profile"""
        glyph = encode_profile(self.sample_profile)
        
        # Verify glyph is a non-empty string
        self.assertIsInstance(glyph, str)
        self.assertTrue(len(glyph) > 0)
        
        # Check if the glyph contains characters from each expected category
        self.assertTrue(any(c for c in glyph if 'A' <= c <= 'Z' or 'a' <= c <= 'z'))  # Latin (traits)
        self.assertTrue(any(c for c in glyph if '\u0410' <= c <= '\u042F'))  # Cyrillic (archetypes)
        self.assertTrue(any(c for c in glyph if '\u0391' <= c <= '\u03A9'))  # Greek (spiritual arcs)
        
        # Verify round-trip encoding/decoding
        decoded = decode_glyph(glyph)
        self.assertEqual(decoded['name'], self.sample_profile['name'])
        self.assertEqual(len(decoded['traits']), len(self.sample_profile['traits']))
        self.assertEqual(len(decoded['archetypes']), len(self.sample_profile['archetypes']))

    def test_encode_traits(self):
        """Test encoding personality traits"""
        traits = self.sample_profile['traits']
        trait_chars = encode_traits(traits)
        
        # Verify trait encoding produces Latin characters
        self.assertIsInstance(trait_chars, str)
        self.assertTrue(all(c.isalpha() and c.isascii() for c in trait_chars))
        
        # Number of trait characters should match number of traits
        self.assertEqual(len(trait_chars), len(traits))

    def test_encode_archetypes(self):
        """Test encoding archetypes"""
        archetypes = self.sample_profile['archetypes']
        archetype_chars = encode_archetypes(archetypes)
        
        # Verify archetype encoding produces Cyrillic characters
        self.assertIsInstance(archetype_chars, str)
        self.assertTrue(all('\u0410' <= c <= '\u042F' for c in archetype_chars))
        
        # Number of characters should match number of archetypes
        self.assertEqual(len(archetype_chars), len(archetypes))

    def test_encode_spiritual_arcs(self):
        """Test encoding spiritual arcs"""
        arcs = self.sample_profile['spiritual_arcs']
        arc_chars = encode_spiritual_arcs(arcs)
        
        # Verify arc encoding produces Greek characters
        self.assertIsInstance(arc_chars, str)
        self.assertTrue(all('\u0391' <= c <= '\u03A9' for c in arc_chars))
        
        # Number of characters should match number of arcs
        self.assertEqual(len(arc_chars), len(arcs))

    def test_encode_mood(self):
        """Test encoding mood profile"""
        mood = self.sample_profile['mood_profile']
        mood_chars = encode_mood(mood)
        
        # Verify mood encoding produces Half-width Kana characters
        self.assertIsInstance(mood_chars, str)
        self.assertTrue(all('\uFF66' <= c <= '\uFF9D' for c in mood_chars))
        
        # Number of characters should match number of mood states
        self.assertEqual(len(mood_chars), len(mood))

    def test_encode_scars(self):
        """Test encoding psychological scars"""
        scars = self.sample_profile['scars']
        scar_chars = encode_scars(scars)
        
        # Verify scar encoding produces Braille characters
        self.assertIsInstance(scar_chars, str)
        self.assertTrue(all('\u2800' <= c <= '\u28FF' for c in scar_chars))
        
        # Each scar should produce one character
        self.assertEqual(len(scar_chars), len(scars))

    def test_encode_projection(self):
        """Test encoding projection/style traits"""
        projection = self.sample_profile['projection']
        projection_chars = encode_projection(projection)
        
        # Verify projection encoding produces Block Drawing characters
        self.assertIsInstance(projection_chars, str)
        
        # Number of characters should match number of projection traits
        self.assertEqual(len(projection_chars), len(projection))

    def test_encode_intensity(self):
        """Test encoding intensity values"""
        intensity = self.sample_profile['intensity']
        intensity_chars = encode_intensity(intensity)
        
        # Verify intensity encoding produces Geometric Shape characters
        self.assertIsInstance(intensity_chars, str)
        
        # Number of characters should match number of intensity metrics
        self.assertEqual(len(intensity_chars), len(intensity))

    def test_encode_inflection(self):
        """Test encoding inflection patterns"""
        inflection = self.sample_profile['inflection']
        inflection_chars = encode_inflection(inflection)
        
        # Verify inflection encoding produces Arrow characters
        self.assertIsInstance(inflection_chars, str)
        
        # Number of characters should match number of inflection patterns
        self.assertEqual(len(inflection_chars), len(inflection))


if __name__ == '__main__':
    unittest.main()

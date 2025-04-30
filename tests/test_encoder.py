"""
Test suite for TanzoGlyph encoder module
"""

import os
import sys
import unittest
import yaml
import json
from pathlib import Path

# Add the parent directory to the Python path to import tanzoglyph modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tanzoglyph.encoder import (
    encode_profile, encode_file, validate_against_schema,
    serialize_tomoglyph, generate_visual_stream
)
from tanzoglyph.decoder import decode_glyph

class TestEncoder(unittest.TestCase):
    """Test cases for TanzoGlyph encoder functions"""
    
    def setUp(self):
        # Set up test data
        self.example_profile = {
            "name": "Test Profile",
            "version": "1.0.0",
            "traits": {
                "analytical": 0.8,
                "creative": 0.6
            },
            "archetypes": [
                {"name": "Teacher", "weight": 0.7},
                {"name": "Explorer", "weight": 0.4}
            ],
            "mood_profile": {
                "calm": 0.6,
                "curious": 0.8
            }
        }
        
        # Create a temporary test file
        self.test_dir = Path("./tests/temp")
        self.test_dir.mkdir(exist_ok=True)
        
        # Save example profile as YAML
        self.yaml_path = self.test_dir / "test_profile.yaml"
        with open(self.yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(self.example_profile, f)
            
        # Save example profile as JSON
        self.json_path = self.test_dir / "test_profile.json"
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.example_profile, f, indent=2)
        
    def tearDown(self):
        # Clean up temporary files
        if self.yaml_path.exists():
            self.yaml_path.unlink()
        if self.json_path.exists():
            self.json_path.unlink()
        # Remove temp directory if empty
        try:
            self.test_dir.rmdir()
        except OSError:
            pass
    
    def test_encode_profile(self):
        """Test encoding a profile dictionary to TanzoGlyph"""
        glyph = encode_profile(self.example_profile)
        
        # Check that the result is a non-empty string
        self.assertIsInstance(glyph, str)
        self.assertTrue(len(glyph) > 0)
        
        # Check that the glyph contains characters from different Unicode blocks
        # (You'll need to have at least one character from each encoded section)
        has_latin = any(ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z') for c in glyph)
        self.assertTrue(has_latin, "Glyph should contain Latin characters for traits")
    
    def test_encode_file(self):
        """Test encoding a file to TanzoGlyph"""
        # Test YAML file
        yaml_glyph = encode_file(str(self.yaml_path))
        self.assertIsInstance(yaml_glyph, str)
        self.assertTrue(len(yaml_glyph) > 0)
        
        # Test JSON file
        json_glyph = encode_file(str(self.json_path))
        self.assertIsInstance(json_glyph, str)
        self.assertTrue(len(json_glyph) > 0)
        
        # Both encodings should be identical
        self.assertEqual(yaml_glyph, json_glyph)
    
    def test_round_trip(self):
        """Test encoding and then decoding results in the original data"""
        # Encode the profile
        glyph = encode_profile(self.example_profile)
        
        # Decode it back
        decoded = decode_glyph(glyph)
        
        # Check that key elements are preserved
        self.assertEqual(decoded.get("name"), self.example_profile.get("name"))
        
        # Check that traits are preserved (allowing for small float differences)
        for trait, value in self.example_profile.get("traits", {}).items():
            self.assertIn(trait, decoded.get("traits", {}))
            decoded_value = decoded.get("traits", {}).get(trait)
            self.assertIsNotNone(decoded_value)
            self.assertAlmostEqual(value, decoded_value, delta=0.2)
    
    def test_serialize_tomoglyph(self):
        """Test the serialize_tomoglyph function"""
        # This would normally validate against the schema, but we need to mock that
        # for testing without setting up the full schema validation
        try:
            glyph = serialize_tomoglyph(str(self.yaml_path))
            self.assertIsInstance(glyph, str)
            self.assertTrue(len(glyph) > 0)
        except FileNotFoundError:
            # If the schema file is not found, we skip this test
            self.skipTest("Schema file not found, skipping test")
    
    def test_generate_visual_stream(self):
        """Test generating a visual stream from a glyph"""
        # Encode a profile
        glyph = encode_profile(self.example_profile)
        
        # Generate visual stream
        visual = generate_visual_stream(glyph)
        
        # Check that it returns a non-empty string
        self.assertIsInstance(visual, str)
        self.assertTrue(len(visual) > 0)
        
        # Check that it contains at least some of the glyph characters
        for c in glyph[:5]:  # Check first 5 chars
            self.assertIn(c, visual)


if __name__ == "__main__":
    unittest.main()

"""
Test suite for TanzoGlyph schema validation
"""

import os
import sys
import unittest
import json
import yaml
from pathlib import Path

# Add the parent directory to the Python path to import tanzoglyph modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tanzoglyph.encoder import (
    validate_against_schema, get_schema_path, load_schema
)

class TestGlyphSchema(unittest.TestCase):
    """Test cases for TanzoGlyph schema validation"""
    
    def setUp(self):
        # Create a temporary test directory
        self.test_dir = Path("./tests/temp")
        self.test_dir.mkdir(exist_ok=True)
        
        # Create a valid profile
        self.valid_profile = {
            "name": "Valid Test Profile",
            "version": "1.0.0",
            "glyph_string": "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂",
            "created_at": "2025-04-30T16:00:00Z",
            "updated_at": "2025-04-30T16:00:00Z",
            "description": "A valid test profile",
            "traits": {
                "analytical": 0.8,
                "creative": 0.6
            },
            "archetypes": [
                {"name": "Teacher", "weight": 0.7},
                {"name": "Explorer", "weight": 0.4}
            ]
        }
        
        # Save valid profile as YAML
        self.valid_yaml_path = self.test_dir / "valid_profile.yaml"
        with open(self.valid_yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(self.valid_profile, f)
        
        # Create an invalid profile (missing required fields)
        self.invalid_profile = {
            "name": "Invalid Test Profile"
            # Missing version and glyph_string (required fields)
        }
        
        # Save invalid profile as YAML
        self.invalid_yaml_path = self.test_dir / "invalid_profile.yaml"
        with open(self.invalid_yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(self.invalid_profile, f)
    
    def tearDown(self):
        # Clean up temporary files
        if self.valid_yaml_path.exists():
            self.valid_yaml_path.unlink()
        if self.invalid_yaml_path.exists():
            self.invalid_yaml_path.unlink()
        # Remove temp directory if empty
        try:
            self.test_dir.rmdir()
        except OSError:
            pass
    
    def test_schema_loading(self):
        """Test loading the schema files"""
        try:
            # Try to get the schema path
            schema_path = get_schema_path('tomoglyph')
            self.assertTrue(os.path.exists(schema_path))
            
            # Try to load the schema
            schema = load_schema(schema_path)
            self.assertIsInstance(schema, dict)
            self.assertIn('properties', schema)
            
            # Check some essential schema properties
            self.assertIn('name', schema['properties'])
            self.assertIn('glyph_string', schema['properties'])
            self.assertIn('version', schema['properties'])
        except FileNotFoundError:
            self.skipTest("Schema files not found, skipping test")
    
    def test_validate_valid_profile(self):
        """Test validating a valid profile against the schema"""
        try:
            # This should pass without raising an exception
            result = validate_against_schema(str(self.valid_yaml_path))
            self.assertTrue(result)
        except FileNotFoundError:
            self.skipTest("Schema files not found, skipping test")
        except Exception as e:
            self.fail(f"Validation raised an unexpected exception: {str(e)}")
    
    def test_validate_invalid_profile(self):
        """Test that an invalid profile fails validation"""
        try:
            # This should raise a validation error
            with self.assertRaises(Exception):
                validate_against_schema(str(self.invalid_yaml_path))
        except FileNotFoundError:
            self.skipTest("Schema files not found, skipping test")


if __name__ == "__main__":
    unittest.main()

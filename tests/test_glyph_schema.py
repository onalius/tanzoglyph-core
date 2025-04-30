import unittest
import os
import sys
import json
import yaml
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGlyphSchema(unittest.TestCase):
    """Test cases for the TanzoGlyph JSON schema validation"""

    def setUp(self):
        # Load the schema
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'tomoglyph.schema.json')
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
            
        # Sample valid profile for testing
        self.valid_profile = {
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
            "created_at": "2025-04-30T12:00:00Z",
            "description": "A test profile for schema validation"
        }

    def test_valid_profile(self):
        """Test that a valid profile passes schema validation"""
        try:
            validate(instance=self.valid_profile, schema=self.schema)
            validation_success = True
        except ValidationError:
            validation_success = False
            
        self.assertTrue(validation_success)

    def test_missing_required_fields(self):
        """Test that profiles missing required fields fail validation"""
        # Test missing name
        invalid_profile = self.valid_profile.copy()
        del invalid_profile['name']
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test missing version
        invalid_profile = self.valid_profile.copy()
        del invalid_profile['version']
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test missing traits
        invalid_profile = self.valid_profile.copy()
        del invalid_profile['traits']
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test missing archetypes
        invalid_profile = self.valid_profile.copy()
        del invalid_profile['archetypes']
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)

    def test_invalid_types(self):
        """Test that profiles with wrong field types fail validation"""
        # Test invalid name type
        invalid_profile = self.valid_profile.copy()
        invalid_profile['name'] = 123  # Should be string
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test invalid version format
        invalid_profile = self.valid_profile.copy()
        invalid_profile['version'] = "not-semver"  # Should match pattern
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test invalid traits type
        invalid_profile = self.valid_profile.copy()
        invalid_profile['traits'] = [1, 2, 3]  # Should be object
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test invalid archetypes type
        invalid_profile = self.valid_profile.copy()
        invalid_profile['archetypes'] = "not-array"  # Should be array
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)

    def test_value_constraints(self):
        """Test that values outside allowed ranges fail validation"""
        # Test trait value outside range
        invalid_profile = self.valid_profile.copy()
        invalid_profile['traits']['over_range'] = 1.5  # Should be -1 to 1
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)
            
        # Test archetype weight outside range
        invalid_profile = self.valid_profile.copy()
        invalid_profile['archetypes'][0]['weight'] = 1.2  # Should be 0 to 1
        
        with self.assertRaises(ValidationError):
            validate(instance=invalid_profile, schema=self.schema)

    def test_example_profiles(self):
        """Test that the example profiles in the repo pass validation"""
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'glyphs')
        example_files = [f for f in os.listdir(examples_dir) if f.endswith('.yaml')]
        
        for example_file in example_files:
            file_path = os.path.join(examples_dir, example_file)
            with open(file_path, 'r') as f:
                profile = yaml.safe_load(f)
                
            try:
                validate(instance=profile, schema=self.schema)
                validation_success = True
            except ValidationError as e:
                validation_success = False
                print(f"Validation error in {example_file}: {e}")
                
            self.assertTrue(validation_success, f"Example profile {example_file} failed validation")


if __name__ == '__main__':
    unittest.main()

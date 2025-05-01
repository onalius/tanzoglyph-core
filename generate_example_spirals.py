#!/usr/bin/env python
"""Script to generate example spiral visualizations for TanzoGlyph profiles"""

import os
import yaml
from tanzoglyph.spiral_encoder import save_spiral_image, SpiralType

# Directory paths
EXAMPLES_DIR = "examples/glyphs"
SPIRALS_DIR = "examples/spirals"

# Ensure the spirals directory exists
os.makedirs(SPIRALS_DIR, exist_ok=True)

# List of example glyph profiles
profiles = [
    "healer_archetype.yaml",
    "explorer_archetype.yaml",
    "sage_archetype.yaml"
]

# Generate spiral visualizations for each profile
for profile_file in profiles:
    # Load the profile from YAML
    with open(os.path.join(EXAMPLES_DIR, profile_file), 'r') as f:
        profile = yaml.safe_load(f)
    
    # Get the glyph string
    glyph = profile.get('glyph_string', '')
    name = profile.get('name', 'Unnamed')
    
    if glyph:
        # Generate Archimedean spiral
        output_path = os.path.join(SPIRALS_DIR, f"{profile_file.split('.')[0]}_archimedean.png")
        save_spiral_image(
            glyph,
            output_path,
            spiral_type=SpiralType.ARCHIMEDEAN,
            title=f"{name} - Archimedean Spiral",
            background_color="#222222",
            figure_size=(10, 10),
            dpi=150
        )
        print(f"Generated Archimedean spiral for {name}: {output_path}")
        
        # Generate Logarithmic spiral
        output_path = os.path.join(SPIRALS_DIR, f"{profile_file.split('.')[0]}_logarithmic.png")
        save_spiral_image(
            glyph,
            output_path,
            spiral_type=SpiralType.LOGARITHMIC,
            title=f"{name} - Logarithmic Spiral",
            background_color="#222222",
            figure_size=(10, 10),
            dpi=150
        )
        print(f"Generated Logarithmic spiral for {name}: {output_path}")
    else:
        print(f"Warning: No glyph string found in {profile_file}")

print("All example spirals have been generated.")

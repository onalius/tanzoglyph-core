#!/usr/bin/env python
"""
TanzoGlyph Spiral Encoder Module
=============================

This module provides functionality to generate 2D spiral visualizations 
of TanzoGlyph encoded personality profiles ("soul prints").

The spiral encoder creates deterministic visual representations that can
serve as both a formal component of TanzoGlyph identity and as a visual
glyph for reference, display, and comparison.

Available spiral types:
- Archimedean: Points are distributed evenly along a spiral
- Logarithmic: Points follow a logarithmic growth pattern

Each character in the glyph string maps to a point on the spiral, with
optional color-coding and sizing based on the Unicode character class.
"""

import argparse
import hashlib
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import to_rgba

# Character class definitions for TanzoGlyph components
class GlyphClass(Enum):
    """Enum representing different character classes in a TanzoGlyph"""
    LATIN = 1      # Traits (Latin A-Z)
    CYRILLIC = 2   # Archetypes (Cyrillic)
    GREEK = 3      # Spiritual Arcs (Greek)
    KANA = 4       # Mood (Half-width Kana)
    BRAILLE = 5    # Scars (Braille)
    BLOCK = 6      # Projection (Block Drawing)
    GEOMETRIC = 7  # Intensity (Geometric Shapes)
    ARROW = 8      # Inflection (Arrows)
    OTHER = 9      # Any other characters

# Spiral type definitions
class SpiralType(Enum):
    """Available spiral types for visualization"""
    ARCHIMEDEAN = "archimedean"
    LOGARITHMIC = "logarithmic"


def determine_character_class(char: str) -> GlyphClass:
    """Determine the TanzoGlyph character class for a given Unicode character
    
    Args:
        char: A single Unicode character from a TanzoGlyph string
        
    Returns:
        The GlyphClass enum value corresponding to the character
    """
    code_point = ord(char)
    
    # Latin characters (traits)
    if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
        return GlyphClass.LATIN
    
    # Cyrillic characters (archetypes)
    elif '\u0410' <= char <= '\u042F' or '\u0430' <= char <= '\u044F':
        return GlyphClass.CYRILLIC
    
    # Greek characters (spiritual arcs)
    elif '\u0391' <= char <= '\u03A9' or '\u03B1' <= char <= '\u03C9':
        return GlyphClass.GREEK
    
    # Half-width Kana (mood)
    elif '\uFF66' <= char <= '\uFF9D':
        return GlyphClass.KANA
    
    # Braille (scars)
    elif '\u2800' <= char <= '\u28FF':
        return GlyphClass.BRAILLE
    
    # Block Drawing (projection)
    elif '\u2500' <= char <= '\u257F':
        return GlyphClass.BLOCK
    
    # Geometric Shapes (intensity)
    elif '\u25A0' <= char <= '\u25FF':
        return GlyphClass.GEOMETRIC
    
    # Arrows (inflection)
    elif '\u2190' <= char <= '\u21FF':
        return GlyphClass.ARROW
    
    # Other characters
    else:
        return GlyphClass.OTHER


def get_character_color(char_class: GlyphClass) -> str:
    """Get a color for a given character class
    
    Args:
        char_class: The GlyphClass enum value
        
    Returns:
        A color string in matplotlib format
    """
    color_map = {
        GlyphClass.LATIN: "#4287f5",      # Blue
        GlyphClass.CYRILLIC: "#f54242",   # Red
        GlyphClass.GREEK: "#42f5a7",      # Green
        GlyphClass.KANA: "#f5d442",       # Yellow
        GlyphClass.BRAILLE: "#f542d4",    # Pink
        GlyphClass.BLOCK: "#8742f5",      # Purple
        GlyphClass.GEOMETRIC: "#f59e42",  # Orange
        GlyphClass.ARROW: "#42d4f5",      # Cyan
        GlyphClass.OTHER: "#777777",      # Gray
    }
    return color_map.get(char_class, "#000000")


def get_character_size(char_class: GlyphClass) -> float:
    """Get a point size for a given character class
    
    Args:
        char_class: The GlyphClass enum value
        
    Returns:
        A size value for the point marker
    """
    size_map = {
        GlyphClass.LATIN: 80,
        GlyphClass.CYRILLIC: 90,
        GlyphClass.GREEK: 85,
        GlyphClass.KANA: 75,
        GlyphClass.BRAILLE: 70,
        GlyphClass.BLOCK: 85,
        GlyphClass.GEOMETRIC: 95,
        GlyphClass.ARROW: 80,
        GlyphClass.OTHER: 60,
    }
    return size_map.get(char_class, 70)


def generate_seed_from_glyph(glyph: str) -> int:
    """Generate a deterministic seed from a glyph string
    
    Args:
        glyph: The TanzoGlyph string
        
    Returns:
        An integer seed for random number generation
    """
    hash_val = hashlib.sha256(glyph.encode('utf-8')).hexdigest()
    return int(hash_val, 16) % (2**32)


def generate_spiral_points(
    glyph: str, 
    spiral_type: SpiralType = SpiralType.ARCHIMEDEAN,
    start_radius: float = 0.1,
    end_radius: float = 4.0,
    jitter: float = 0.02
) -> Tuple[List[float], List[float], List[GlyphClass]]:
    """Generate points along a spiral for a given glyph string
    
    Args:
        glyph: The TanzoGlyph string
        spiral_type: The type of spiral to generate
        start_radius: Initial radius of the spiral
        end_radius: Maximum radius of the spiral
        jitter: Amount of random variation to add to points
        
    Returns:
        Tuple of (x_coordinates, y_coordinates, character_classes)
    """
    # Set random seed based on glyph string for deterministic output
    seed = generate_seed_from_glyph(glyph)
    np.random.seed(seed)
    
    n_points = len(glyph)
    
    # Calculate angle distribution
    max_angle = 0
    if n_points > 0:
        # More points = more revolutions for better visualization
        revolutions = max(2, min(10, n_points / 10))
        max_angle = revolutions * 2 * math.pi
        angles = np.linspace(0, max_angle, n_points)
    else:
        angles = np.array([])
    
    # Calculate radii based on spiral type
    if spiral_type == SpiralType.ARCHIMEDEAN:
        # Archimedean spiral: r = a + b*θ
        # Distribute points evenly along the spiral
        b = (end_radius - start_radius) / max_angle if n_points > 0 else 0
        radii = start_radius + b * angles
    
    elif spiral_type == SpiralType.LOGARITHMIC:
        # Logarithmic spiral: r = a*e^(b*θ)
        # Points become more spread out as the spiral grows
        if n_points > 0:
            b = math.log(end_radius / start_radius) / max_angle
            radii = start_radius * np.exp(b * angles)
        else:
            radii = np.array([])
    
    else:
        # Default to Archimedean if type is not recognized
        b = (end_radius - start_radius) / max_angle if n_points > 0 else 0
        radii = start_radius + b * angles
    
    # Add some random jitter to make points more distinct
    jitter_values = np.random.normal(0, jitter, n_points) if n_points > 0 else np.array([])
    radii = radii + jitter_values
    
    # Convert polar coordinates to cartesian
    x_coords = radii * np.cos(angles)
    y_coords = radii * np.sin(angles)
    
    # Determine character classes
    char_classes = [determine_character_class(char) for char in glyph]
    
    return x_coords.tolist(), y_coords.tolist(), char_classes


def plot_spiral(
    glyph: str,
    spiral_type: SpiralType = SpiralType.ARCHIMEDEAN,
    start_radius: float = 0.1,
    end_radius: float = 4.0,
    jitter: float = 0.02,
    figure_size: Tuple[int, int] = (10, 10),
    background_color: str = "#FFFFFF",
    show_legend: bool = True,
    title: Optional[str] = None,
    dpi: int = 150
) -> Figure:
    """Create a matplotlib figure with the spiral visualization
    
    Args:
        glyph: The TanzoGlyph string
        spiral_type: Type of spiral (Archimedean or Logarithmic)
        start_radius: Initial radius of the spiral
        end_radius: Maximum radius of the spiral
        jitter: Amount of random variation to add to points
        figure_size: Tuple of (width, height) in inches
        background_color: Background color of the plot
        show_legend: Whether to show a legend for character classes
        title: Optional title for the plot
        dpi: Dots per inch for rendering
        
    Returns:
        A matplotlib Figure object
    """
    # Generate spiral points
    x_coords, y_coords, char_classes = generate_spiral_points(
        glyph, spiral_type, start_radius, end_radius, jitter
    )
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figure_size, dpi=dpi)
    
    # Set figure background color
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    
    # Plot points with colors and sizes based on character classes
    for i, char_class in enumerate(char_classes):
        color = get_character_color(char_class)
        size = get_character_size(char_class)
        ax.scatter(x_coords[i], y_coords[i], c=color, s=size, alpha=0.8, edgecolor='white', linewidth=0.5)
    
    # Add a small point at the origin
    ax.scatter(0, 0, c='black', s=20, alpha=0.8)
    
    # Set equal aspect ratio to preserve the spiral shape
    ax.set_aspect('equal')
    
    # Remove axis
    ax.axis('off')
    
    # Add title if provided
    if title:
        ax.set_title(title, fontsize=14, pad=20)
    
    # Add legend if requested
    if show_legend and char_classes:
        # Get unique character classes
        unique_classes = set(char_classes)
        
        # Create legend entries
        handles = []
        labels = []
        for cls in unique_classes:
            color = get_character_color(cls)
            handles.append(plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor=color, markersize=10))
            labels.append(cls.name.title())
        
        # Add the legend to the plot
        ax.legend(handles, labels, loc='upper right', framealpha=0.7)
    
    # Tight layout to eliminate extra whitespace
    plt.tight_layout()
    
    return fig


def save_spiral_image(
    glyph: str,
    output_path: str,
    spiral_type: SpiralType = SpiralType.ARCHIMEDEAN,
    start_radius: float = 0.1,
    end_radius: float = 4.0,
    jitter: float = 0.02,
    figure_size: Tuple[int, int] = (10, 10),
    background_color: str = "#FFFFFF",
    show_legend: bool = True,
    title: Optional[str] = None,
    dpi: int = 150
) -> str:
    """Generate a spiral visualization and save it to a file
    
    Args:
        glyph: The TanzoGlyph string
        output_path: Path where the image will be saved
        spiral_type: Type of spiral (Archimedean or Logarithmic)
        start_radius: Initial radius of the spiral
        end_radius: Maximum radius of the spiral
        jitter: Amount of random variation to add to points
        figure_size: Tuple of (width, height) in inches
        background_color: Background color of the plot
        show_legend: Whether to show a legend for character classes
        title: Optional title for the plot
        dpi: Dots per inch for rendering
        
    Returns:
        The path to the saved image file
    """
    # Generate the figure
    fig = plot_spiral(
        glyph, spiral_type, start_radius, end_radius, jitter,
        figure_size, background_color, show_legend, title, dpi
    )
    
    # Save to file
    plt.savefig(output_path, bbox_inches='tight', dpi=dpi)
    plt.close(fig)  # Close the figure to free memory
    
    return output_path


def generate_spiral_hash(glyph: str, spiral_type: SpiralType = SpiralType.ARCHIMEDEAN) -> str:
    """Generate a hash of the spiral configuration for a given glyph
    
    This hash can be used for verification or as an IPFS content identifier.
    
    Args:
        glyph: The TanzoGlyph string
        spiral_type: Type of spiral used
        
    Returns:
        SHA-256 hash of the spiral configuration
    """
    # Create a deterministic representation of the spiral configuration
    seed = generate_seed_from_glyph(glyph)
    config_str = f"{glyph}:{spiral_type.value}:{seed}"
    
    # Generate and return the hash
    return hashlib.sha256(config_str.encode('utf-8')).hexdigest()


def main():
    """Command-line interface for the spiral encoder"""
    parser = argparse.ArgumentParser(description="Generate spiral visualizations of TanzoGlyph strings")
    
    parser.add_argument("--glyph", type=str, required=True,
                        help="TanzoGlyph string to visualize")
    
    parser.add_argument("--output", type=str, required=True,
                        help="Output file path (.png or .svg)")
    
    parser.add_argument("--spiral-type", type=str, choices=["archimedean", "logarithmic"],
                       default="archimedean", help="Type of spiral to generate")
    
    parser.add_argument("--start-radius", type=float, default=0.1,
                       help="Initial radius of the spiral")
    
    parser.add_argument("--end-radius", type=float, default=4.0,
                       help="Maximum radius of the spiral")
    
    parser.add_argument("--jitter", type=float, default=0.02,
                       help="Amount of random variation in point placement")
    
    parser.add_argument("--figure-size", type=int, nargs=2, default=[10, 10],
                       help="Figure size in inches (width height)")
    
    parser.add_argument("--background", type=str, default="#FFFFFF",
                       help="Background color (hex code)")
    
    parser.add_argument("--no-legend", action="store_true",
                       help="Hide the character class legend")
    
    parser.add_argument("--title", type=str, default=None,
                       help="Title for the visualization")
    
    parser.add_argument("--dpi", type=int, default=150,
                       help="Dots per inch for rendering")
    
    parser.add_argument("--hash", action="store_true",
                       help="Print the spiral hash (for IPFS/verification)")
    
    args = parser.parse_args()
    
    # Convert spiral type string to enum
    spiral_type = SpiralType.ARCHIMEDEAN
    if args.spiral_type == "logarithmic":
        spiral_type = SpiralType.LOGARITHMIC
    
    # Save the spiral visualization
    output_path = save_spiral_image(
        args.glyph,
        args.output,
        spiral_type=spiral_type,
        start_radius=args.start_radius,
        end_radius=args.end_radius,
        jitter=args.jitter,
        figure_size=tuple(args.figure_size),
        background_color=args.background,
        show_legend=not args.no_legend,
        title=args.title,
        dpi=args.dpi
    )
    
    print(f"Spiral visualization saved to: {output_path}")
    
    # Print hash if requested
    if args.hash:
        spiral_hash = generate_spiral_hash(args.glyph, spiral_type)
        print(f"Spiral hash: {spiral_hash}")


if __name__ == "__main__":
    main()

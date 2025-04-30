"""TanzoGlyph Image Generation Module
=================================

This module provides functions for converting TanzoGlyph character streams
into visual representations as SVG images, allowing TanzoGlyphs to serve
as distinctive fingerprints or identifiers for profiles.
"""

import re
import math
import colorsys
from typing import Dict, List, Tuple, Optional, Union, Any

# Mapping of character blocks to colors
COLOR_MAP = {
    'traits': '#4a90e2',       # Latin - Blue
    'archetypes': '#e25a4a',   # Cyrillic - Red
    'spiritual_arcs': '#7ed321',  # Greek - Green
    'mood': '#f8e71c',         # Half-width Kana - Yellow
    'scars': '#bd10e0',        # Braille - Purple
    'projection': '#50e3c2',    # Block Drawing - Teal
    'intensity': '#ff9500',    # Geometric Shapes - Orange
    'inflection': '#4a4a4a'     # Arrows - Gray
}

def is_latin(char: str) -> bool:
    """Check if character is in Latin A-Z range"""
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'

def is_cyrillic(char: str) -> bool:
    """Check if character is Cyrillic"""
    return '\u0400' <= char <= '\u04FF'

def is_greek(char: str) -> bool:
    """Check if character is Greek"""
    return '\u0370' <= char <= '\u03FF'

def is_halfwidth_kana(char: str) -> bool:
    """Check if character is Half-width Kana"""
    return '\uFF66' <= char <= '\uFF9F'

def is_braille(char: str) -> bool:
    """Check if character is Braille"""
    return '\u2800' <= char <= '\u28FF'

def is_block_drawing(char: str) -> bool:
    """Check if character is Block Drawing"""
    return '\u2500' <= char <= '\u257F'

def is_geometric_shape(char: str) -> bool:
    """Check if character is a Geometric Shape"""
    return '\u25A0' <= char <= '\u25FF'

def is_arrow(char: str) -> bool:
    """Check if character is an Arrow"""
    return '\u2190' <= char <= '\u21FF'

def get_char_type(char: str) -> str:
    """Determine the character block type of a Unicode character"""
    if is_latin(char):
        return 'traits'
    elif is_cyrillic(char):
        return 'archetypes'
    elif is_greek(char):
        return 'spiritual_arcs'
    elif is_halfwidth_kana(char):
        return 'mood'
    elif is_braille(char):
        return 'scars'
    elif is_block_drawing(char):
        return 'projection'
    elif is_geometric_shape(char):
        return 'intensity'
    elif is_arrow(char):
        return 'inflection'
    else:
        return 'unknown'

def glyph_to_circular_svg(glyph: str, size: int = 200, background: str = 'none', 
                          inner_radius_percent: float = 30, 
                          border: bool = True) -> str:
    """Convert a TanzoGlyph to a circular SVG representation
    
    Args:
        glyph: The TanzoGlyph string to convert
        size: Width and height of the SVG in pixels
        background: Background color of the SVG ('none' for transparent)
        inner_radius_percent: Size of the inner empty space as percentage of total radius
        border: Whether to draw a circular border
        
    Returns:
        SVG image as a string
    """
    if not glyph:
        return f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"></svg>'
    
    center = size / 2
    outer_radius = min(center * 0.9, center * 0.9)  # 90% of available space
    inner_radius = outer_radius * (inner_radius_percent / 100)
    
    # Count the number of characters to distribute
    char_count = len(glyph)
    
    # Start building the SVG
    svg_parts = [f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">\n']
    
    # Add background if specified
    if background != 'none':
        svg_parts.append(f'<rect width="{size}" height="{size}" fill="{background}" />\n')
    
    # Add circular border if requested
    if border:
        svg_parts.append(f'<circle cx="{center}" cy="{center}" r="{outer_radius}" '
                       f'fill="none" stroke="#000" stroke-width="1" />\n')
    
    # Function to calculate position on the circle
    def get_position(index, total, radius):
        angle = 2 * math.pi * index / total
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)
        return x, y
    
    # Group elements by character block
    char_blocks = {}
    for i, char in enumerate(glyph):
        block_type = get_char_type(char)
        if block_type not in char_blocks:
            char_blocks[block_type] = []
        char_blocks[block_type].append((i, char))
    
    # Calculate segment radius for each character based on its position
    for block_type, chars in char_blocks.items():
        color = COLOR_MAP.get(block_type, '#999999')
        
        for idx, (original_idx, char) in enumerate(chars):
            # Calculate segment positioning
            angle_start = 2 * math.pi * original_idx / char_count
            angle_end = 2 * math.pi * (original_idx + 1) / char_count
            
            # Calculate arc path
            start_x = center + inner_radius * math.cos(angle_start)
            start_y = center + inner_radius * math.sin(angle_start)
            end_x = center + outer_radius * math.cos(angle_start)
            end_y = center + outer_radius * math.sin(angle_start)
            
            # Create a path for the segment
            svg_parts.append(f'<path d="M {start_x},{start_y} L {end_x},{end_y} '
                           f'A {outer_radius},{outer_radius} 0 0,1 '
                           f'{center + outer_radius * math.cos(angle_end)},'
                           f'{center + outer_radius * math.sin(angle_end)} '
                           f'L {center + inner_radius * math.cos(angle_end)},'
                           f'{center + inner_radius * math.sin(angle_end)} '
                           f'A {inner_radius},{inner_radius} 0 0,0 {start_x},{start_y}" '
                           f'fill="{color}" opacity="0.8" />\n')
            
            # Position the character at the midpoint of the outer edge
            mid_angle = (angle_start + angle_end) / 2
            mid_radius = (inner_radius + outer_radius) / 2
            char_x = center + mid_radius * math.cos(mid_angle)
            char_y = center + mid_radius * math.sin(mid_angle)
            
            # Add a small circle for the character position (optional)
            # svg_parts.append(f'<circle cx="{char_x}" cy="{char_y}" r="2" fill="#fff" />\n')
            
            # Add the Unicode character
            svg_parts.append(f'<text x="{char_x}" y="{char_y}" text-anchor="middle" '
                           f'dominant-baseline="middle" fill="#fff" '
                           f'font-size="{outer_radius * 0.15}px">{char}</text>\n')
    
    # Close the SVG
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

def glyph_to_grid_svg(glyph: str, size: int = 200, columns: int = 8, 
                      background: str = 'none', cell_padding: int = 2) -> str:
    """Convert a TanzoGlyph to a grid-based SVG representation
    
    Args:
        glyph: The TanzoGlyph string to convert
        size: Width and height of the SVG in pixels
        columns: Number of columns in the grid
        background: Background color of the SVG ('none' for transparent)
        cell_padding: Padding within each cell in pixels
        
    Returns:
        SVG image as a string
    """
    if not glyph:
        return f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"></svg>'
    
    # Calculate rows needed based on character count and columns
    char_count = len(glyph)
    rows = math.ceil(char_count / columns)
    
    # Calculate cell size
    cell_size = min(size / columns, size / rows)
    actual_width = columns * cell_size
    actual_height = rows * cell_size
    
    # Start building the SVG
    svg_parts = [f'<svg width="{actual_width}" height="{actual_height}" xmlns="http://www.w3.org/2000/svg">\n']
    
    # Add background if specified
    if background != 'none':
        svg_parts.append(f'<rect width="{actual_width}" height="{actual_height}" fill="{background}" />\n')
    
    # Add each character as a cell in the grid
    for i, char in enumerate(glyph):
        col = i % columns
        row = i // columns
        x = col * cell_size
        y = row * cell_size
        
        # Determine character block and color
        block_type = get_char_type(char)
        color = COLOR_MAP.get(block_type, '#999999')
        
        # Add cell background
        svg_parts.append(f'<rect x="{x + cell_padding}" y="{y + cell_padding}" '
                       f'width="{cell_size - 2*cell_padding}" height="{cell_size - 2*cell_padding}" '
                       f'fill="{color}" rx="{cell_padding}" ry="{cell_padding}" />\n')
        
        # Add the Unicode character
        svg_parts.append(f'<text x="{x + cell_size/2}" y="{y + cell_size/2}" text-anchor="middle" '
                       f'dominant-baseline="middle" fill="#fff" '
                       f'font-size="{cell_size * 0.6}px">{char}</text>\n')
    
    # Close the SVG
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

def glyph_to_fingerprint_svg(glyph: str, width: int = 200, height: int = 50, 
                            background: str = 'none', style: str = 'bars') -> str:
    """Convert a TanzoGlyph to a fingerprint-like SVG representation
    
    Args:
        glyph: The TanzoGlyph string to convert
        width: Width of the SVG in pixels
        height: Height of the SVG in pixels
        background: Background color of the SVG ('none' for transparent)
        style: Visual style ('bars', 'waves', or 'dots')
        
    Returns:
        SVG image as a string
    """
    if not glyph:
        return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"></svg>'
    
    # Start building the SVG
    svg_parts = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n']
    
    # Add background if specified
    if background != 'none':
        svg_parts.append(f'<rect width="{width}" height="{height}" fill="{background}" />\n')
    
    # Group characters by block type for color consistency
    block_groups = {}
    for char in glyph:
        block_type = get_char_type(char)
        if block_type not in block_groups:
            block_groups[block_type] = []
        block_groups[block_type].append(char)
    
    # Determine character distribution
    char_count = len(glyph)
    segment_width = width / char_count if char_count > 0 else 0
    
    if style == 'bars':
        # Generate bars based on character values
        for i, char in enumerate(glyph):
            x = i * segment_width
            
            # Get character info
            block_type = get_char_type(char)
            color = COLOR_MAP.get(block_type, '#999999')
            
            # Calculate height based on character code point
            bar_height = (ord(char) % 100) / 100 * height
            bar_y = height - bar_height
            
            # Draw the bar
            svg_parts.append(f'<rect x="{x}" y="{bar_y}" width="{segment_width * 0.8}" '
                           f'height="{bar_height}" fill="{color}" opacity="0.8" />\n')
    
    elif style == 'waves':
        # Create a continuous wave pattern
        path_by_block = {}
        
        for block_type in block_groups.keys():
            path_by_block[block_type] = ['M 0,{}'.format(height/2)]
        
        for i, char in enumerate(glyph):
            x = i * segment_width + segment_width/2
            block_type = get_char_type(char)
            
            # Calculate y-position based on character code point
            amplitude = height * 0.4
            y = height/2 + (((ord(char) % 100) / 100) * 2 - 1) * amplitude
            
            # Add curve point
            if i > 0:
                path_by_block[block_type].append(f'S {x},{y}')
            else:
                path_by_block[block_type].append(f'L {x},{y}')
        
        # Draw paths for each block type
        for block_type, path_parts in path_by_block.items():
            if len(path_parts) > 1:  # Only draw if there are points
                color = COLOR_MAP.get(block_type, '#999999')
                path_d = ' '.join(path_parts)
                svg_parts.append(f'<path d="{path_d}" fill="none" '
                               f'stroke="{color}" stroke-width="2" />\n')
    
    elif style == 'dots':
        # Create a dot pattern
        for i, char in enumerate(glyph):
            x = i * segment_width + segment_width/2
            block_type = get_char_type(char)
            color = COLOR_MAP.get(block_type, '#999999')
            
            # Calculate y-position and radius based on character
            y = height/2 + (((ord(char) % 100) / 100) * 2 - 1) * (height * 0.4)
            radius = (ord(char) % 5) + 2  # Vary size slightly
            
            # Draw the dot
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" />\n')
    
    # Close the SVG
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

def save_glyph_svg(glyph: str, filename: str, format_type: str = 'circular', **kwargs):
    """Save a TanzoGlyph as an SVG file
    
    Args:
        glyph: The TanzoGlyph string to convert
        filename: Output filename (should end with .svg)
        format_type: Type of visualization ('circular', 'grid', 'fingerprint')
        **kwargs: Additional arguments passed to the specific SVG generator
    """
    if format_type == 'circular':
        svg_content = glyph_to_circular_svg(glyph, **kwargs)
    elif format_type == 'grid':
        svg_content = glyph_to_grid_svg(glyph, **kwargs)
    elif format_type == 'fingerprint':
        svg_content = glyph_to_fingerprint_svg(glyph, **kwargs)
    else:
        raise ValueError(f"Unknown format type: {format_type}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)

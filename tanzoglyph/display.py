"""
TanzoGlyph Display Module
========================

This module provides functions for displaying TanzoGlyph character streams
in visually appealing formats, including a Matrix-style falling character effect.
"""

import os
import time
import random
import sys
from typing import List, Optional

def matrix_display(glyph: str, speed: float = 0.1, columns: int = 5, color: bool = True) -> None:
    """
    Display a TanzoGlyph string in a falling Matrix-style animation in the terminal.
    
    Args:
        glyph: The TanzoGlyph string to display
        speed: Delay between animation frames in seconds
        columns: Number of parallel falling columns
        color: Whether to use ANSI color codes
    """
    # Check if stdout is a terminal
    if not sys.stdout.isatty():
        print(glyph)
        return
    
    # Terminal escape codes for green text
    GREEN = '\033[32m' if color else ''
    BRIGHT_GREEN = '\033[92m' if color else ''
    RESET = '\033[0m' if color else ''
    
    try:
        # Get terminal size
        term_width = os.get_terminal_size().columns
        term_height = os.get_terminal_size().lines - 1  # Leave one line for prompt
    except (OSError, AttributeError):
        # Fallback if terminal size can't be determined
        term_width = 80
        term_height = 24
    
    # Adjust columns based on terminal width
    columns = min(columns, term_width // 4)
    
    # Split glyph into roughly equal chunks for each column
    chunk_size = max(1, len(glyph) // columns)
    chunks = [glyph[i:i+chunk_size] for i in range(0, len(glyph), chunk_size)]
    
    # Pad shorter chunks with spaces
    max_len = max(len(chunk) for chunk in chunks)
    chunks = [chunk.ljust(max_len) for chunk in chunks]
    
    # Calculate column positions
    col_width = term_width // columns
    positions = [col_width * i + col_width // 2 for i in range(columns)]
    
    # Initialize display matrix with spaces
    display = [[' ' for _ in range(term_width)] for _ in range(term_height)]
    
    # Animation state
    head_positions = [-1] * len(chunks)
    tail_positions = [-term_height] * len(chunks)
    
    # Clear screen and hide cursor
    print('\033[2J\033[?25l', end='')
    
    try:
        # Run animation
        while any(head < len(chunks[i]) for i, head in enumerate(head_positions)):
            # Update positions
            for i in range(len(chunks)):
                if head_positions[i] < len(chunks[i]) - 1:
                    head_positions[i] += 1
                    tail_positions[i] += 1
            
            # Clear display
            display = [[' ' for _ in range(term_width)] for _ in range(term_height)]
            
            # Update display matrix
            for i, chunk in enumerate(chunks):
                pos_x = positions[i]
                for j in range(tail_positions[i], head_positions[i] + 1):
                    if j >= 0 and j < len(chunk):
                        # Calculate vertical position in display
                        pos_y = head_positions[i] - j
                        if 0 <= pos_y < term_height:
                            # Add character to display
                            display[pos_y][pos_x] = chunk[j]
            
            # Render display
            print('\033[H', end='')  # Move cursor to top-left
            for y in range(term_height):
                line = []
                for x in range(term_width):
                    char = display[y][x]
                    # Highlight head characters with bright green
                    is_head = False
                    for i in range(len(chunks)):
                        if (y == head_positions[i] - (head_positions[i] - tail_positions[i]) and 
                            x == positions[i] and head_positions[i] >= 0):
                            is_head = True
                            break
                    
                    if char != ' ':
                        if is_head:
                            line.append(f"{BRIGHT_GREEN}{char}{RESET}")
                        else:
                            line.append(f"{GREEN}{char}{RESET}")
                    else:
                        line.append(char)
                print(''.join(line))
            
            # Delay
            time.sleep(speed)
    
    finally:
        # Show cursor again
        print('\033[?25h', end='')
        # Move to bottom of display
        print('\033[%d;0H' % term_height)

def matrix_effect_html(glyph: str, columns: int = 5) -> str:
    """
    Generate HTML/CSS for displaying a Matrix-like effect with the given glyph.
    
    Args:
        glyph: The TanzoGlyph string to display
        columns: Number of columns to split the glyph into
        
    Returns:
        HTML string with embedded CSS for Matrix effect
    """
    # Split glyph into columns
    chunk_size = max(1, len(glyph) // columns)
    chunks = [glyph[i:i+chunk_size] for i in range(0, len(glyph), chunk_size)]
    
    html = """
    <div class="matrix-container">
        <style>
            .matrix-container {
                background-color: #000;
                height: 400px;
                overflow: hidden;
                position: relative;
                width: 100%;
                font-family: monospace;
            }
            .matrix-column {
                position: absolute;
                top: 0;
                color: #0f0;
                font-size: 1.5em;
                line-height: 1.2;
                white-space: nowrap;
                text-align: center;
                animation-name: matrix-fall;
                animation-iteration-count: infinite;
                animation-timing-function: linear;
                transform-origin: top;
                width: calc(100% / %d);
            }
            @keyframes matrix-fall {
                from {
                    transform: translateY(-100%%);
                }
                to {
                    transform: translateY(400px);
                }
            }
            .glyph-character {
                display: block;
                text-shadow: 0 0 5px #0f0;
            }
            .glyph-character:first-child {
                color: #fff;
                text-shadow: 0 0 10px #0f0;
            }
        </style>
    """ % columns
    
    # Create columns with different animation durations
    for i, chunk in enumerate(chunks):
        # Calculate animation parameters for varied effect
        duration = random.uniform(5, 15)  # seconds
        delay = random.uniform(0, 3)  # seconds
        position = (100 / columns) * i  # percent
        
        html += f"""
        <div class="matrix-column" style="left: {position}%; animation-duration: {duration}s; animation-delay: {delay}s;">
        """
        
        # Add each character with a slight opacity variation
        for char in chunk:
            opacity = random.uniform(0.7, 1.0)
            html += f'<span class="glyph-character" style="opacity: {opacity};">{char}</span>'
            
        html += "</div>"
    
    html += "</div>"
    
    return html

def print_glyph(glyph: str, decode: bool = False) -> None:
    """
    Print a TanzoGlyph string with optional decoding information.
    
    Args:
        glyph: The TanzoGlyph string to print
        decode: Whether to print character block information
    """
    if not decode:
        print(glyph)
        return
    
    # Print with block identification
    blocks = [
        ('Latin (Traits)', r'[A-Za-z]'),
        ('Cyrillic (Archetypes)', r'[А-Яа-я]'),
        ('Greek (Spiritual Arcs)', r'[Α-Ωα-ω]'),
        ('Half-width Kana (Mood)', r'[ｦ-ﾝ]'),
        ('Braille (Scars)', r'[⠀-⣿]'),
        ('Block Drawing (Projection)', r'[▀-▟█-░]')
    ]
    
    import re
    
    print("=== TanzoGlyph Analysis ===")
    print(f"Full Glyph: {glyph}")
    print("\nComponents:")
    
    for name, pattern in blocks:
        matches = re.findall(pattern, glyph)
        if matches:
            chars = ''.join(matches)
            print(f"- {name}: {chars} ({len(chars)} characters)")
    
    print("\n===========================")

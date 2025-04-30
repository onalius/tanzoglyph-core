import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, Response
import yaml
import json
import tempfile

from tanzoglyph.encoder import encode_profile
from tanzoglyph.decoder import decode_glyph
from tanzoglyph.display import matrix_effect_html
from tanzoglyph.image_generator import glyph_to_circular_svg, glyph_to_grid_svg, glyph_to_fingerprint_svg

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tanzoglyph_dev_key")

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/glyph-images')
def glyph_images():
    """Render the TanzoGlyph image generator page."""
    # Use a sample glyph as default
    default_glyph = "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂"
    return render_template('glyph_images.html', default_glyph=default_glyph)

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    """Encode a YAML/JSON profile to TanzoGlyph."""
    result = None
    matrix_html = None
    
    if request.method == 'POST':
        try:
            # Check if a file was uploaded
            if 'file' in request.files and request.files['file'].filename:
                file = request.files['file']
                content = file.read().decode('utf-8')
                
                # Determine format based on file extension
                if file.filename.endswith('.yaml') or file.filename.endswith('.yml'):
                    profile = yaml.safe_load(content)
                elif file.filename.endswith('.json'):
                    profile = json.loads(content)
                else:
                    raise ValueError("Unsupported file format. Please upload a YAML or JSON file.")
            # Or if text was provided directly
            elif request.form.get('profile_text'):
                content = request.form.get('profile_text')
                try:
                    # Try parsing as JSON first
                    profile = json.loads(content)
                except json.JSONDecodeError:
                    # If that fails, try YAML
                    try:
                        profile = yaml.safe_load(content)
                    except yaml.YAMLError as e:
                        raise ValueError(f"Invalid YAML or JSON format: {str(e)}")
            else:
                raise ValueError("No file or text provided")
            
            # Encode the profile
            result = encode_profile(profile)
            
            # Generate matrix effect HTML if requested
            if request.form.get('matrix_effect') == 'on':
                matrix_html = matrix_effect_html(result)
            
            # Save to file if requested
            if request.form.get('save_file') == 'on':
                output_format = request.form.get('output_format', 'tomo')
                filename = f"output.{output_format}"
                
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}', mode='w') as temp:
                    temp.write(result)
                    temp_path = temp.name
                
                return send_file(temp_path, as_attachment=True, download_name=filename)
            
            flash('Encoding successful!', 'success')
            
        except Exception as e:
            logger.error(f"Encoding error: {str(e)}")
            flash(f"Error: {str(e)}", 'danger')
    
    return render_template('encode.html', result=result, matrix_html=matrix_html)

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    """Decode a TanzoGlyph back to a YAML/JSON profile."""
    result = None
    
    if request.method == 'POST':
        try:
            glyph_text = request.form.get('glyph_text', '')
            if not glyph_text:
                raise ValueError("No TanzoGlyph text provided")
            
            # Check if tomotanzo format is requested
            to_tomotanzo = request.form.get('to_tomotanzo') == 'on'
            
            # Decode the glyph
            decoded_profile = decode_glyph(glyph_text, to_tomotanzo=to_tomotanzo)
            
            # Format as requested
            output_format = request.form.get('output_format', 'yaml')
            if output_format == 'yaml':
                result = yaml.dump(decoded_profile, sort_keys=False, default_flow_style=False)
            else:  # json
                result = json.dumps(decoded_profile, indent=2)
            
            # Save to file if requested
            if request.form.get('save_file') == 'on':
                filename = f"decoded.{output_format}"
                
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}', mode='w') as temp:
                    temp.write(result)
                    temp_path = temp.name
                
                return send_file(temp_path, as_attachment=True, download_name=filename)
            
            flash('Decoding successful!', 'success')
            
            # Add format info to flash message
            if to_tomotanzo:
                flash('Decoded to tomotanzo-core format', 'info')
            
        except Exception as e:
            logger.error(f"Decoding error: {str(e)}")
            flash(f"Error: {str(e)}", 'danger')
    
    return render_template('decode.html', result=result)

@app.route('/api/encode', methods=['POST'])
def api_encode():
    """API endpoint for encoding profiles."""
    try:
        if request.is_json:
            profile = request.get_json()
        else:
            content = request.data.decode('utf-8')
            try:
                profile = json.loads(content)
            except json.JSONDecodeError:
                profile = yaml.safe_load(content)
        
        result = encode_profile(profile)
        return jsonify({'success': True, 'glyph': result})
    
    except Exception as e:
        logger.error(f"API encoding error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/decode', methods=['POST'])
def api_decode():
    """API endpoint for decoding glyphs."""
    try:
        data = request.get_json()
        if not data or 'glyph' not in data:
            return jsonify({'success': False, 'error': 'No glyph provided'}), 400
        
        glyph = data['glyph']
        to_tomotanzo = data.get('to_tomotanzo', False)
        decoded = decode_glyph(glyph, to_tomotanzo=to_tomotanzo)
        
        output_format = data.get('format', 'json')
        if output_format == 'yaml':
            result = yaml.dump(decoded, sort_keys=False, default_flow_style=False)
            return result, 200, {'Content-Type': 'text/yaml'}
        else:
            return jsonify({'success': True, 'profile': decoded})
    
    except Exception as e:
        logger.error(f"API decoding error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/glyph-image/<format_type>/<glyph>')
def glyph_image(format_type, glyph):
    """Generate an SVG image from a TanzoGlyph string."""
    try:
        # Validate format type
        if format_type not in ['circular', 'grid', 'fingerprint']:
            return jsonify({'error': 'Invalid format type'}), 400
        
        # Get parameters with defaults
        size = request.args.get('size', 200, type=int)
        background = request.args.get('background', 'none')
        
        # Generate SVG based on format type
        if format_type == 'circular':
            inner_radius = request.args.get('inner_radius', 30, type=int)
            border = request.args.get('border', 'true').lower() == 'true'
            svg_content = glyph_to_circular_svg(
                glyph, size=size, background=background,
                inner_radius_percent=inner_radius, border=border
            )
        elif format_type == 'grid':
            columns = request.args.get('columns', 8, type=int)
            cell_padding = request.args.get('padding', 2, type=int)
            svg_content = glyph_to_grid_svg(
                glyph, size=size, columns=columns,
                background=background, cell_padding=cell_padding
            )
        elif format_type == 'fingerprint':
            width = size
            height = request.args.get('height', size // 4, type=int)
            style = request.args.get('style', 'bars')
            if style not in ['bars', 'waves', 'dots']:
                style = 'bars'
            svg_content = glyph_to_fingerprint_svg(
                glyph, width=width, height=height,
                background=background, style=style
            )
        
        # Serve the SVG
        return Response(svg_content, mimetype='image/svg+xml')
    
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/glyph-image', methods=['POST'])
def api_glyph_image():
    """API endpoint for generating a TanzoGlyph image."""
    try:
        data = request.get_json()
        if not data or 'glyph' not in data:
            return jsonify({'success': False, 'error': 'No glyph provided'}), 400
        
        glyph = data['glyph']
        format_type = data.get('format', 'circular')
        
        # Additional parameters with defaults
        params = {}
        
        # Common parameters
        params['size'] = data.get('size', 200)
        params['background'] = data.get('background', 'none')
        
        # Format-specific parameters
        if format_type == 'circular':
            params['inner_radius_percent'] = data.get('inner_radius', 30)
            params['border'] = data.get('border', True)
            svg_content = glyph_to_circular_svg(glyph, **params)
        elif format_type == 'grid':
            params['columns'] = data.get('columns', 8)
            params['cell_padding'] = data.get('padding', 2)
            svg_content = glyph_to_grid_svg(glyph, **params)
        elif format_type == 'fingerprint':
            params['width'] = params.pop('size')  # Use size as width
            params['height'] = data.get('height', params['width'] // 4)
            params['style'] = data.get('style', 'bars')
            svg_content = glyph_to_fingerprint_svg(glyph, **params)
        else:
            return jsonify({'success': False, 'error': 'Invalid format type'}), 400
        
        # Return as SVG content
        return Response(svg_content, mimetype='image/svg+xml')
    
    except Exception as e:
        logger.error(f"API image generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html', error="Server error occurred"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

"""
Utility functions for Krishi Mitra
"""

import os
import io
import base64
from PIL import Image
import streamlit as st
from config import ALLOWED_IMAGE_TYPES, ALLOWED_VIDEO_TYPES, MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB

def validate_image(uploaded_file):
    """Validate uploaded image file."""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check extension
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in ALLOWED_IMAGE_TYPES:
        return False, f"Invalid format. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
    
    # Check size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_IMAGE_SIZE_MB:
        return False, f"File too large. Max size: {MAX_IMAGE_SIZE_MB}MB"
    
    return True, "Valid"

def validate_video(uploaded_file):
    """Validate uploaded video file."""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check extension
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in ALLOWED_VIDEO_TYPES:
        return False, f"Invalid format. Allowed: {', '.join(ALLOWED_VIDEO_TYPES)}"
    
    # Check size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_VIDEO_SIZE_MB:
        return False, f"File too large. Max size: {MAX_VIDEO_SIZE_MB}MB"
    
    return True, "Valid"

def compress_image(image_file, max_size=(800, 800), quality=85):
    """
    Compress and resize image for AI processing.
    Returns PIL Image object.
    """
    try:
        image = Image.open(image_file)
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize if larger than max_size
        if image.width > max_size[0] or image.height > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to buffer with compression
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        return Image.open(buffer)
    except Exception as e:
        st.error(f"Image processing error: {str(e)}")
        return None

def save_uploaded_file(uploaded_file, save_dir):
    """
    Save uploaded file to disk and return file path.
    """
    try:
        file_ext = uploaded_file.name.split('.')[-1]
        import uuid
        filename = f"{uuid.uuid4().hex}.{file_ext}"
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return filepath
    except Exception as e:
        st.error(f"File save error: {str(e)}")
        return None

def get_language_name(lang_code):
    """Get full language name from code."""
    from config import SUPPORTED_LANGUAGES
    return SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')

def format_datetime(dt_string):
    """Format datetime string for display."""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return dt_string
      

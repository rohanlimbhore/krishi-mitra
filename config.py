"""
Configuration file for Krishi Mitra - Farming Support Application
"""

import os
import streamlit as st

# =============================================================================
# GEMINI API CONFIGURATION
# =============================================================================
# IMPORTANT: Set your GEMINI_API_KEY in one of these ways:
# 1. Streamlit Cloud: Go to App Settings -> Secrets, add: GEMINI_API_KEY = "your_key"
# 2. Local development: Create .env file with GEMINI_API_KEY=your_key
# 3. Environment variable: export GEMINI_API_KEY=your_key

def get_gemini_api_key():
    """Retrieve Gemini API key from Streamlit secrets or environment variables."""
    try:
        # Try Streamlit secrets first (for cloud deployment)
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        # Fall back to environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("⚠️ GEMINI_API_KEY not found! Please set it in Streamlit Secrets or environment variables.")
            st.stop()
        return api_key

# =============================================================================
# SUPPORTED LANGUAGES
# =============================================================================
SUPPORTED_LANGUAGES = {
    'mr': 'Marathi',
    'hi': 'Hindi', 
    'en': 'English',
    'gu': 'Gujarati',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada'
}

# =============================================================================
# FILE UPLOAD CONFIGURATION
# =============================================================================
ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png']
ALLOWED_VIDEO_TYPES = ['mp4']
MAX_VIDEO_SIZE_MB = 200
MAX_IMAGE_SIZE_MB = 10

# =============================================================================
# DIRECTORY CONFIGURATION
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")
VIDEOS_DIR = os.path.join(UPLOAD_DIR, "videos")
DB_PATH = os.path.join(BASE_DIR, "krishi_mitra.db")

# Create directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# =============================================================================
# AI MODEL CONFIGURATION
# ============================================================================
GEMINI_MODEL_TEXT = "gemini-1.0-pro"
GEMINI_MODEL_VISION = "gemini-1.0-pro"



# =============================================================================
# APPLICATION METADATA
# =============================================================================
APP_NAME = "🌾 Krishi Mitra"
APP_TAGLINE = "Your Intelligent Farming Companion"
APP_DESCRIPTION = "AI-powered agricultural support for Indian farmers"

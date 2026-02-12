"""
Configuration file for Krishi Mitra - Farming Support Application
"""

import os
import streamlit as st

# =============================================================================
# DATABASE CONFIGURATION (SQLite or Supabase)
# =============================================================================
# Check for Supabase connection first, fallback to SQLite
DATABASE_URL = st.secrets.get("DATABASE_URL", None)

if DATABASE_URL:
    DB_TYPE = "postgresql"  # Supabase/PostgreSQL
    DB_PATH = None  # Not used for PostgreSQL
else:
    DB_TYPE = "sqlite"  # Local SQLite fallback
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "krishi_mitra.db")

# =============================================================================
# GEMINI API CONFIGURATION
# =============================================================================
def get_gemini_api_key():
    """Retrieve Gemini API key from Streamlit secrets or environment variables."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
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
# DIRECTORY CONFIGURATION (Only for SQLite/local uploads)
# =============================================================================
if DB_TYPE == "sqlite":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")
    VIDEOS_DIR = os.path.join(UPLOAD_DIR, "videos")
    
    # Create directories if they don't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
else:
    # For Supabase, you might want to use Supabase Storage later
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")
    VIDEOS_DIR = os.path.join(UPLOAD_DIR, "videos")
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)

# =============================================================================
# APPLICATION METADATA
# =============================================================================
APP_NAME = "🌾 Krishi Mitra"
APP_TAGLINE = "Your Intelligent Farming Companion"
APP_DESCRIPTION = "AI-powered agricultural support for Indian farmers"

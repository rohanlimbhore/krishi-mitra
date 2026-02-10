"""
Google Gemini AI Service for Krishi Mitra
Uses new google-genai library
"""

from google import genai
from PIL import Image
import streamlit as st
from config import get_gemini_api_key

class KrishiAI:
    def __init__(self):
        api_key = get_gemini_api_key()
        self.client = genai.Client(api_key=api_key)
        
        # Use only stable, working model names with models/ prefix
        self.models_to_try = [
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro-latest'
        ]
        self.current_model_index = 0
    
    def _try_generate(self, prompt, image=None):
        """Try generating with fallback models."""
        max_attempts = len(self.models_to_try)
        
        for attempt in range(max_attempts):
            try:
                model_name = self.models_to_try[self.current_model_index]
                
                # Create content
                if image:
                    contents = [prompt, image]
                else:
                    contents = prompt
                
                # Generate response
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                
                return response.text
                
            except Exception as e:
                error_str = str(e)
                # If any error (quota, 404, etc.), try next model
                self.current_model_index = (self.current_model_index + 1) % len(self.models_to_try)
                if attempt == max_attempts - 1:
                    return f"Error: {error_str}"
                continue
        
        return "Error: All models failed. Please try again later."
    
    def detect_language(self, text):
        """Detect language of input text."""
        prompt = f"""
        Detect the language of the following text and respond with ONLY the ISO 639-1 language code.
        Supported codes: mr (Marathi), hi (Hindi), en (English), gu (Gujarati), ta (Tamil), te (Telugu), kn (Kannada).
        If uncertain, default to 'en'.
        
        Text: "{text}"
        
        Respond with only the 2-letter code.
        """
        
        try:
            response = self._try_generate(prompt)
            lang_code = response.strip().lower()[:2]
            valid_codes = ['mr', 'hi', 'en', 'gu', 'ta', 'te', 'kn']
            return lang_code if lang_code in valid_codes else 'en'
        except:
            return 'en'
    
    def get_farming_response(self, query, language='en'):
        """Get AI response for farming questions."""
        language_names = {
            'mr': 'Marathi', 'hi': 'Hindi', 'en': 'English',
            'gu': 'Gujarati', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada'
        }
        lang_name = language_names.get(language, 'English')
        
        system_prompt = f"""
        You are Krishi Mitra, an expert agricultural advisor for Indian farmers.
        Respond ONLY in {lang_name} language.
        
        Farmer's Question: {query}
        """
        
        return self._try_generate(system_prompt)
    
    def analyze_crop_image(self, image, farmer_query="", language='en'):
        """Analyze crop image."""
        language_names = {
            'mr': 'Marathi', 'hi': 'Hindi', 'en': 'English',
            'gu': 'Gujarati', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada'
        }
        lang_name = language_names.get(language, 'English')
        
        prompt = f"""
        You are an agricultural expert. Analyze this crop image.
        Respond in {lang_name} language.
        
        Farmer's context: {farmer_query if farmer_query else "None"}
        
        Provide:
        1. Crop identification
        2. Health assessment
        3. Disease/Pest detection
        4. Treatment recommendations
        5. Care tips
        """
        
        return self._try_generate(prompt, image)
    
    def generate_crop_knowledge(self, crop_name, language='en'):
        """Generate crop lifecycle information."""
        language_names = {
            'mr': 'Marathi', 'hi': 'Hindi', 'en': 'English',
            'gu': 'Gujarati', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada'
        }
        lang_name = language_names.get(language, 'English')
        
        prompt = f"""
        You are an agricultural expert. Provide complete information about {crop_name}.
        Respond entirely in {lang_name} language.
        
        Include:
        - Crop overview
        - Complete lifecycle
        - Seasonal calendar
        - Input requirements
        - Economics
        - Best practices
        """
        
        return self._try_generate(prompt)
    
    def get_government_scheme_info(self, query, language='en'):
        """Provide government scheme information."""
        language_names = {
            'mr': 'Marathi', 'hi': 'Hindi', 'en': 'English',
            'gu': 'Gujarati', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada'
        }
        lang_name = language_names.get(language, 'English')
        
        prompt = f"""
        You are a government scheme expert for Indian agriculture.
        Respond in {lang_name} language.
        
        Query: {query}
        
        Provide:
        - Scheme overview
        - Eligibility criteria
        - Benefits
        - Application process
        - Contact information
        """
        
        return self._try_generate(prompt)

# Singleton instance
@st.cache_resource
def get_ai_service():
    return KrishiAI()
        

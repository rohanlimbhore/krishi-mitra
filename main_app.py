"""
🌾 Krishi Mitra - Main Application Features
Multi-language UI support
"""

import streamlit as st
from PIL import Image
from datetime import datetime
import os
import urllib.parse

from config import APP_NAME, APP_TAGLINE, SUPPORTED_LANGUAGES, IMAGES_DIR, VIDEOS_DIR
from database import create_post, get_all_posts, add_product, get_all_products, search_products
from ai_service import get_ai_service
from utils import (
    validate_image, validate_video, compress_image, 
    save_uploaded_file, get_language_name, format_datetime
)

# Initialize AI Service
ai_service = get_ai_service()

# Create upload directories
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# =============================================================================
# TRANSLATIONS - All UI text in different languages
# =============================================================================

TRANSLATIONS = {
    'en': {
        'home': '🏠 Home',
        'ai_assistant': '💬 AI Farming Assistant',
        'crop_diagnosis': '📸 Crop Diagnosis',
        'crop_knowledge': '📚 Crop Knowledge',
        'community': '👥 Farmer Community',
        'schemes': '🏛️ Government Schemes',
        'products': '🥬 Organic Products',
        'welcome': 'Welcome',
        'ask_question': 'Ask any farming-related question',
        'type_here': 'Type your question here...',
        'quick_questions': '💡 Quick Questions',
        'upload_image': '📤 Upload Image',
        'analyze': '🔍 Analyze Crop',
        'preview': '🖼️ Preview',
        'analysis_report': '📋 Analysis Report',
        'listen': '🔊 Listen',
        'enter_crop': 'Enter Crop Name',
        'generate': '📖 Generate Knowledge',
        'view_posts': '📰 View Posts',
        'create_post': '➕ Create Post',
        'your_name': 'Your Name',
        'share_experience': 'Share your experience or question',
        'attach_photo': 'Attach Photo (Optional)',
        'attach_video': 'Attach Video (Optional)',
        'post': 'Post to Community',
        'ask_scheme': 'Ask about any scheme',
        'popular_schemes': '📋 Popular Schemes',
        'browse_products': '🛒 Browse Products',
        'list_product': '➕ List Your Product',
        'product_name': 'Product Name',
        'quantity': 'Quantity',
        'location': 'Location/Village',
        'phone': 'Phone Number',
        'list': 'List Product',
        'search': '🔍 Search',
        'logout': '🚪 Logout',
        'language': 'Language',
        'select_feature': 'Select Feature'
    },
    'mr': {
        'home': '🏠 मुख्यपृष्ठ',
        'ai_assistant': '💬 कृषी सहाय्यक',
        'crop_diagnosis': '📸 पिक निदान',
        'crop_knowledge': '📚 पिक माहिती',
        'community': '👥 शेतकरी समुदाय',
        'schemes': '🏛️ सरकारी योजना',
        'products': '🥬 सेंद्रिय उत्पादने',
        'welcome': 'स्वागत आहे',
        'ask_question': 'कोणत्याही शेतीसंबंधित प्रश्न विचारा',
        'type_here': 'तुमचा प्रश्न येथे टाइप करा...',
        'quick_questions': '💡 जलद प्रश्न',
        'upload_image': '📤 प्रतिमा अपलोड करा',
        'analyze': '🔍 विश्लेषण करा',
        'preview': '🖼️ पूर्वावलोकन',
        'analysis_report': '📋 विश्लेषण अहवाल',
        'listen': '🔊 ऐका',
        'enter_crop': 'पिकाचे नाव टाका',
        'generate': '📖 माहिती मिळवा',
        'view_posts': '📰 पोस्ट पहा',
        'create_post': '➕ नवीन पोस्ट',
        'your_name': 'तुमचे नाव',
        'share_experience': 'तुमचा अनुभव किंवा प्रश्न शेअर करा',
        'attach_photo': 'फोटो जोडा (ऐच्छिक)',
        'attach_video': 'व्हिडिओ जोडा (ऐच्छिक)',
        'post': 'समुदायात पोस्ट करा',
        'ask_scheme': 'कोणत्याही योजनेबद्दल विचारा',
        'popular_schemes': '📋 लोकप्रिय योजना',
        'browse_products': '🛒 उत्पादने पहा',
        'list_product': '➕ तुमचे उत्पादन विका',
        'product_name': 'उत्पादनाचे नाव',
        'quantity': 'प्रमाण',
        'location': 'गाव/ठिकाण',
        'phone': 'फोन नंबर',
        'list': 'यादीत टाका',
        'search': '🔍 शोधा',
        'logout': '🚪 बाहेर पडा',
        'language': 'भाषा',
        'select_feature': 'वैशिष्ट्य निवडा'
    },
    'hi': {
        'home': '🏠 होम',
        'ai_assistant': '💬 कृषि सहायक',
        'crop_diagnosis': '📸 फसल निदान',
        'crop_knowledge': '📚 फसल जानकारी',
        'community': '👥 किसान समुदाय',
        'schemes': '🏛️ सरकारी योजनाएं',
        'products': '🥬 जैविक उत्पाद',
        'welcome': 'स्वागत है',
        'ask_question': 'कोई भी कृषि संबंधित प्रश्न पूछें',
        'type_here': 'अपना प्रश्न यहां टाइप करें...',
        'quick_questions': '💡 त्वरित प्रश्न',
        'upload_image': '📤 छवि अपलोड करें',
        'analyze': '🔍 विश्लेषण करें',
        'preview': '🖼️ पूर्वावलोकन',
        'analysis_report': '📋 विश्लेषण रिपोर्ट',
        'listen': '🔊 सुनें',
        'enter_crop': 'फसल का नाम दर्ज करें',
        'generate': '📖 जानकारी प्राप्त करें',
        'view_posts': '📰 पोस्ट देखें',
        'create_post': '➕ नई पोस्ट',
        'your_name': 'आपका नाम',
        'share_experience': 'अपना अनुभव या प्रश्न साझा करें',
        'attach_photo': 'फोटो जोड़ें (वैकल्पिक)',
        'attach_video': 'वीडियो जोड़ें (वैकल्पिक)',
        'post': 'समुदाय में पोस्ट करें',
        'ask_scheme': 'किसी भी योजना के बारे में पूछें',
        'popular_schemes': '📋 लोकप्रिय योजनाएं',
        'browse_products': '🛒 उत्पाद देखें',
        'list_product': '➕ अपना उत्पाद बेचें',
        'product_name': 'उत्पाद का नाम',
        'quantity': 'मात्रा',
        'location': 'गांव/स्थान',
        'phone': 'फोन नंबर',
        'list': 'सूचीबद्ध करें',
        'search': '🔍 खोजें',
        'logout': '🚪 लॉगआउट',
        'language': 'भाषा',
        'select_feature': 'सुविधा चुनें'
    },
    'gu': {
        'home': '🏠 હોમ',
        'ai_assistant': '💬 કૃષિ સહાયક',
        'crop_diagnosis': '📸 પાક નિદાન',
        'crop_knowledge': '📚 પાક માહિતી',
        'community': '👥 ખેડૂત સમુદાય',
        'schemes': '🏛️ સરકારી યોજનાઓ',
        'products': '🥬 જૈવિક ઉત્પાદનો',
        'welcome': 'સ્વાગત છે',
        'ask_question': 'કોઈપણ ખેતી સંબંધિત પ્રશ્ન પૂછો',
        'type_here': 'તમારો પ્રશ્ન અહીં ટાઈપ કરો...',
        'quick_questions': '💡 ઝડપી પ્રશ્નો',
        'upload_image': '📤 છબી અપલોડ કરો',
        'analyze': '🔍 વિશ્લેષણ કરો',
        'preview': '🖼️ પૂર્વાવલોકન',
        'analysis_report': '📋 વિશ્લેષણ અહેવાલ',
        'listen': '🔊 સાંભળો',
        'enter_crop': 'પાકનું નામ દાખલ કરો',
        'generate': '📖 માહિતી મેળવો',
        'view_posts': '📰 પોસ્ટ જુઓ',
        'create_post': '➕ નવી પોસ્ટ',
        'your_name': 'તમારું નામ',
        'share_experience': 'તમારો અનુભવ અથવા પ્રશ્ન શેર કરો',
        'attach_photo': 'ફોટો જોડો (વૈકલ્પિક)',
        'attach_video': 'વીડિયો જોડો (વૈકલ્પિક)',
        'post': 'સમુદાયમાં પોસ્ટ કરો',
        'ask_scheme': 'કોઈપણ યોજના વિશે પૂછો',
        'popular_schemes': '📋 લોકપ્રિય યોજનાઓ',
        'browse_products': '🛒 ઉત્પાદનો જુઓ',
        'list_product': '➕ તમારું ઉત્પાદન વેચો',
        'product_name': 'ઉત્પાદનનું નામ',
        'quantity': 'જથ્થો',
        'location': 'ગામ/સ્થાન',
        'phone': 'ફોન નંબર',
        'list': 'યાદીમાં મૂકો',
        'search': '🔍 શોધો',
        'logout': '🚪 લોગઆઉટ',
        'language': 'ભાષા',
        'select_feature': 'સુવિધા પસંદ કરો'
    },
    'ta': {
        'home': '🏠 முகப்பு',
        'ai_assistant': '💬 விவசாய உதவியாளர்',
        'crop_diagnosis': '📸 பயிர் கண்டறிதல்',
        'crop_knowledge': '📚 பயிர் தகவல்',
        'community': '👥 விவசாயி சமூகம்',
        'schemes': '🏛️ அரசு திட்டங்கள்',
        'products': '🥬 இயற்கை பொருட்கள்',
        'welcome': 'வரவேற்கிறோம்',
        'ask_question': 'எந்த விவசாய தொடர்பான கேள்வியும் கேளுங்கள்',
        'type_here': 'உங்கள் கேள்வியை இங்கே தட்டச்சு செய்க...',
        'quick_questions': '💡 விரைவான கேள்விகள்',
        'upload_image': '📤 படத்தை பதிவேற்றவும்',
        'analyze': '🔍 பகுப்பாய்வு செய்யவும்',
        'preview': '🖼️ முன்னோட்டம்',
        'analysis_report': '📋 பகுப்பாய்வு அறிக்கை',
        'listen': '🔊 கேளுங்கள்',
        'enter_crop': 'பயிரின் பெயரை உள்ளிடவும்',
        'generate': '📖 தகவலைப் பெறுங்கள்',
        'view_posts': '📰 பதிவுகளைக் காண்க',
        'create_post': '➕ புதிய பதிவு',
        'your_name': 'உங்கள் பெயர்',
        'share_experience': 'உங்கள் அனுபவம் அல்லது கேள்வியைப் பகிரவும்',
        'attach_photo': 'புகைப்படத்தை இணைக்கவும் (விரும்பினால்)',
        'attach_video': 'வீடியோவை இணைக்கவும் (விரும்பினால்)',
        'post': 'சமூகத்தில் பதிவு செய்யவும்',
        'ask_scheme': 'எந்த திட்டம் பற்றியும் கேளுங்கள்',
        'popular_schemes': '📋 பிரபலமான திட்டங்கள்',
        'browse_products': '🛒 பொருட்களைக் காண்க',
        'list_product': '➕ உங்கள் பொருளை விற்கவும்',
        'product_name': 'பொருளின் பெயர்',
        'quantity': 'அளவு',
        'location': 'கிராமம்/இடம்',
        'phone': 'தொலைபேசி எண்',
        'list': 'பட்டியலிடுங்கள்',
        'search': '🔍 தேடுங்கள்',
        'logout': '🚪 வெளியேறு',
        'language': 'மொழி',
        'select_feature': 'அம்சத்தைத் தேர்வு செய்க'
    },
    'te': {
        'home': '🏠 హోమ్',
        'ai_assistant': '💬 వ్యవసాయ సహాయకుడు',
        'crop_diagnosis': '📸 పంట నిర్ధారణ',
        'crop_knowledge': '📚 పంట సమాచారం',
        'community': '👥 రైతు సమాజం',
        'schemes': '🏛️ ప్రభుత్వ పథకాలు',
        'products': '🥬 సేంద్రీయ ఉత్పత్తులు',
        'welcome': 'స్వాగతం',
        'ask_question': 'ఏదైనా వ్యవసాయ సంబంధిత ప్రశ్న అడగండి',
        'type_here': 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...',
        'quick_questions': '💡 త్వరిత ప్రశ్నలు',
        'upload_image': '📤 చిత్రాన్ని అప్‌లోడ్ చేయండి',
        'analyze': '🔍 విశ్లేషణ చేయండి',
        'preview': '🖼️ మునుజూపు',
        'analysis_report': '📋 విశ్లేషణ నివేదిక',
        'listen': '🔊 వినండి',
        'enter_crop': 'పంట పేరును నమోదు చేయండి',
        'generate': '📖 సమాచారం పొందండి',
        'view_posts': '📰 పోస్ట్‌లను చూడండి',
        'create_post': '➕ కొత్త పోస్ట్',
        'your_name': 'మీ పేరు',
        'share_experience': 'మీ అనుభవం లేదా ప్రశ్నను పంచుకోండి',
        'attach_photo': 'ఫోటోను జోడించండి (ఐచ్ఛికం)',
        'attach_video': 'వీడియోను జోడించండి (ఐచ్ఛికం)',
        'post': 'సమాజంలో పోస్ట్ చేయండి',
        'ask_scheme': 'ఏదైనా పథకం గురించి అడగండి',
        'popular_schemes': '📋 ప్రజాదరణ పొందిన పథకాలు',
        'browse_products': '🛒 ఉత్పత్తులను చూడండి',
        'list_product': '➕ మీ ఉత్పత్తిని అమ్మండి',
        'product_name': 'ఉత్పత్తి పేరు',
        'quantity': 'పరిమాణం',
        'location': 'గ్రామం/స్థలం',
        'phone': 'ఫోన్ నంబర్',
        'list': 'జాబితాలో చేర్చండి',
        'search': '🔍 వెతకండి',
        'logout': '🚪 లాగౌట్',
        'language': 'భాష',
        'select_feature': 'ఫీచర్ ఎంచుకోండి'
    },
    'kn': {
        'home': '🏠 ಮುಖಪುಟ',
        'ai_assistant': '💬 ಕೃಷಿ ಸಹಾಯಕ',
        'crop_diagnosis': '📸 ಬೆಳೆ ನಿದಾನ',
        'crop_knowledge': '📚 ಬೆಳೆ ಮಾಹಿತಿ',
        'community': '👥 ರೈತರ ಸಮುದಾಯ',
        'schemes': '🏛️ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
        'products': '🥬 ಸಾವಯವ ಉತ್ಪನ್ನಗಳು',
        'welcome': 'ಸ್ವಾಗತ',
        'ask_question': 'ಯಾವುದೇ ಕೃಷಿ ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆ ಕೇಳಿ',
        'type_here': 'ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...',
        'quick_questions': '💡 ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು',
        'upload_image': '📤 ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'analyze': '🔍 ವಿಶ್ಲೇಷಣೆ ಮಾಡಿ',
        'preview': '🖼️ ಮುನ್ನೋಟ',
        'analysis_report': '📋 ವಿಶ್ಲೇಷಣೆ ವರದಿ',
        'listen': '🔊 ಕೇಳಿ',
        'enter_crop': 'ಬೆಳೆಯ ಹೆಸರನ್ನು ನಮೂದಿಸಿ',
        'generate': '📖 ಮಾಹಿತಿ ಪಡೆಯಿರಿ',
        'view_posts': '📰 ಪೋಸ್ಟ್‌ಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
        'create_post': '➕ ಹೊಸ ಪೋಸ್ಟ್',
        'your_name': 'ನಿಮ್ಮ ಹೆಸರು',
        'share_experience': 'ನಿಮ್ಮ ಅನುಭವ ಅಥವಾ ಪ್ರಶ್ನೆಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ',
        'attach_photo': 'ಫೋಟೋವನ್ನು ಲಗತ್ತಿಸಿ (ಐಚ್ಛಿಕ)',
        'attach_video': 'ವೀಡಿಯೊವನ್ನು ಲಗತ್ತಿಸಿ (ಐಚ್ಛಿಕ)',
        'post': 'ಸಮುದಾಯದಲ್ಲಿ ಪೋಸ್ಟ್ ಮಾಡಿ',
        'ask_scheme': 'ಯಾವುದೇ ಯೋಜನೆಯ ಬಗ್ಗೆ ಕೇಳಿ',
        'popular_schemes': '📋 ಜನಪ್ರಿಯ ಯೋಜನೆಗಳು',
        'browse_products': '🛒 ಉತ್ಪನ್ನಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
        'list_product': '➕ ನಿಮ್ಮ ಉತ್ಪನ್ನವನ್ನು ಮಾರಾಟ ಮಾಡಿ',
        'product_name': 'ಉತ್ಪನ್ನದ ಹೆಸರು',
        'quantity': 'ಪ್ರಮಾಣ',
        'location': 'ಗ್ರಾಮ/ಸ್ಥಳ',
        'phone': 'ಫೋನ್ ಸಂಖ್ಯೆ',
        'list': 'ಪಟ್ಟಿ ಮಾಡಿ',
        'search': '🔍 ಹುಡುಕಿ',
        'logout': '🚪 ಲಾಗ್ ಔಟ್',
        'language': 'ಭಾಷೆ',
        'select_feature': 'ವೈಶಿಷ್ಟ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ'
    }
}

def get_text(key, lang='en'):
    """Get translated text for given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'][key])

# =============================================================================
# VOICE FUNCTION (Simple Working Version)
# =============================================================================

def text_to_speech(text, lang_code='en', auto_play=True):
def text_to_speech(text, lang_code='en', auto_play=False):
    """
    Lightweight text-to-speech using browser's built-in speech synthesis.
    No external libraries needed - fast and no lag!
    """
    # Map language codes
    lang_map = {
        'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN',
        'gu': 'gu-IN', 'ta': 'ta-IN', 'te': 'te-IN', 'kn': 'kn-IN'
    }
    speech_lang = lang_map.get(lang_code, 'en-IN')
    
    # Clean text
    clean_text = text.replace('"', "'").replace('\n', ' ')[:300]
    
    # JavaScript for speech synthesis (built into browser)
    autoplay_js = "window.speechSynthesis.speak(msg);" if auto_play else ""
    
    html_code = f"""
    <div style="margin:10px 0;">
        <button onclick="speakText()" style="
            background-color:#4CAF50; 
            color:white; 
            padding:10px 20px; 
            border:none; 
            border-radius:5px; 
            cursor:pointer;
            font-size:16px;
        ">
            🔊 {get_text('listen', lang_code)}
        </button>
        <p style="font-size:11px; color:#666; margin-top:5px;">
            Click button to listen in {speech_lang}
        </p>
    </div>
    
    <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = '{speech_lang}';
                msg.rate = 0.9;
                msg.pitch = 1;
                window.speechSynthesis.speak(msg);
            }} else {{
                alert('Your browser does not support speech. Please use Chrome.');
            }}
        }}
        
        // Auto-play if enabled
        {autoplay_js}
    </script>
"""

return html_code

        
    

# =============================================================================
# MAIN APP FUNCTION
# =============================================================================

def run_main_app(user):
    """Run main application with all features."""
    
    # Get selected language
    selected_lang = st.session_state.get('selected_language', 'en')
    
    # =============================================================================
    # SIDEBAR NAVIGATION
    # =============================================================================
    st.sidebar.markdown(f"## 🌾 Krishi Mitra")
    st.sidebar.markdown(f"*{APP_TAGLINE}*")
    st.sidebar.markdown("---")
    
    # Navigation with translated labels
    page_options = [
        get_text('home', selected_lang),
        get_text('ai_assistant', selected_lang),
        get_text('crop_diagnosis', selected_lang),
        get_text('crop_knowledge', selected_lang),
        get_text('community', selected_lang),
        get_text('schemes', selected_lang),
        get_text('products', selected_lang)
    ]
    
    page = st.sidebar.radio(
        get_text('select_feature', selected_lang),
        options=page_options
    )
    
    st.sidebar.markdown("---")
    
    # =============================================================================
    # HOME PAGE
    # ============================================================================= 
    if page == get_text('home', selected_lang):
        st.markdown(f'<h1 style="text-align:center; color:#2E7D32;">🌾 Krishi Mitra</h1>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="text-align:center; color:#558B2F;">{get_text("welcome", selected_lang)}, {user["farmer_name"]}!</h3>', unsafe_allow_html=True)
        
        # User Guide
        st.markdown("---")
        st.subheader("📖 " + ("User Guide" if selected_lang == 'en' else 
                              "वापरकर्ता मार्गदर्शक" if selected_lang == 'mr' else
                              "उपयोगकर्ता गाइड" if selected_lang == 'hi' else
                              "વપરાશકર્તા માર્ગદર્શિકા" if selected_lang == 'gu' else
                              "பயனர் வழிகாட்டி" if selected_lang == 'ta' else
                              "వినియోగదారు గైడ్" if selected_lang == 'te' else
                              "ಬಳಕೆದಾರ ಮಾರ್ಗದರ್ಶಿ"))
        
        guide_text = {
            'en': """
            **How to use this app:**
            1. 💬 **AI Assistant** - Ask any farming question in your language
            2. 📸 **Crop Diagnosis** - Upload photo to detect diseases
            3. 📚 **Crop Knowledge** - Get complete information about any crop
            4. 👥 **Community** - Share with other farmers
            5. 🏛️ **Schemes** - Learn about government schemes
            6. 🥬 **Products** - Buy/Sell organic products
            
            **Voice Feature:** Click 🔊 button to listen to answers!
            """,
            'mr': """
            **अ‍ॅप कसे वापरावे:**
            1. 💬 **AI सहाय्यक** - तुमच्या भाषेत कोणत्याही प्रश्न विचारा
            2. 📸 **पिक निदान** - रोग शोधण्यासाठी फोटो अपलोड करा
            3. 📚 **पिक माहिती** - कोणत्याही पिकाबद्दल संपूर्ण माहिती मिळवा
            4. 👥 **समुदाय** - इतर शेतकऱ्यांसोबत शेअर करा
            5. 🏛️ **योजना** - सरकारी योजना जाणून घ्या
            6. 🥬 **उत्पादने** - सेंद्रिय उत्पादने खरेदी/विक्री करा
            
            **आवाज वैशिष्ट्य:** उत्तरे ऐकण्यासाठी 🔊 बटण दाबा!
            """,
            'hi': """
            **ऐप का उपयोग कैसे करें:**
            1. 💬 **AI सहायक** - अपनी भाषा में कोई भी प्रश्न पूछें
            2. 📸 **फसल निदान** - रोग का पता लगाने के लिए फोटो अपलोड करें
            3. 📚 **फसल जानकारी** - किसी भी फसल की पूरी जानकारी प्राप्त करें
            4. 👥 **समुदाय** - अन्य किसानों के साथ साझा करें
            5. 🏛️ **योजनाएं** - सरकारी योजनाओं के बारे में जानें
            6. 🥬 **उत्पाद** - जैविक उत्पाद खरीदें/बेचें
            
            **आवाज सुविधा:** उत्तर सुनने के लिए 🔊 बटन दबाएं!
            """,
            'gu': """
            **એપ્લિકેશનનો ઉપયોગ કેવી રીતે કરવો:**
            1. 💬 **AI સહાયક** - તમારી ભાષામાં કોઈપણ પ્રશ્ન પૂછો
            2. 📸 **પાક નિદાન** - રોગ શોધવા માટે ફોટો અપલોડ કરો
            3. 📚 **પાક માહિતી** - કોઈપણ પાક વિશે સંપૂર્ણ માહિતી મેળવો
            4. 👥 **સમુદાય** - અન્ય ખેડૂતો સાથે શેર કરો
            5. 🏛️ **યોજનાઓ** - સરકારી યોજનાઓ વિશે જાણો
            6. 🥬 **ઉત્પાદનો** - જૈવિક ઉત્પાદનો ખરીદો/વેચો
            
            **અવાજ સુવિધા:** જવાબ સાંભળવા માટે 🔊 બટન દબાવો!
            """,
            'ta': """
            **பயன்பாட்டை எவ்வாறு பயன்படுத்துவது:**
            1. 💬 **AI உதவியாளர்** - உங்கள் மொழியில் எந்த கேள்வியும் கேளுங்கள்
            2. 📸 **பயிர் கண்டறிதல்** - நோயைக் கண்டறிய புகைப்படத்தை பதிவேற்றவும்
            3. 📚 **பயிர் தகவல்** - எந்த பயிர் பற்றியும் முழு தகவல் பெறுங்கள்
            4. 👥 **சமூகம்** - பிற விவசாயிகளுடன் பகிர்ந்து கொள்ளுங்கள்
            5. 🏛️ **திட்டங்கள்** - அரசு திட்டங்கள் பற்றி அறிந்து கொள்ளுங்கள்
            6. 🥬 **பொருட்கள்** - இயற்கை பொருட்களை வாங்க/விற்க
            
            **குரல் அம்சம்:** பதில்களைக் கேட்க 🔊 பொத்தானை அழுத்தவும்!
            """,
            'te': """
            **అప్లికేషన్‌ను ఎలా ఉపయోగించాలి:**
            1. 💬 **AI సహాయకుడు** - మీ భాషలో ఏదైనా ప్రశ్న అడగండి
            2. 📸 **పంట నిర్ధారణ** - వ్యాధులను గుర్తించడానికి ఫోటో అప్‌లోడ్ చేయండి
            3. 📚 **పంట సమాచారం** - ఏదైనా పంట గురించి పూర్తి సమాచారం పొందండి
            4. 👥 **సమాజం** - ఇతర రైతులతో పంచుకోండి
            5. 🏛️ **పథకాలు** - ప్రభుత్వ పథకాల గురించి తెలుసుకోండి
            6. 🥬 **ఉత్పత్తులు** - సేంద్రీయ ఉత్పత్తులను కొనుగోలు/అమ్మండి
            
            **వాయిస్ ఫీచర్:** సమాధానాలు వినడానికి 🔊 బటన్ నొక్కండి!
            """,
            'kn': """
            **ಅಪ್ಲಿಕೇಶನ್ ಹೇಗೆ ಬಳಸುವುದು:**
            1. 💬 **AI ಸಹಾಯಕ** - ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಿ
            2. 📸 **ಬೆಳೆ ನಿದಾನ** - ರೋಗಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ
            3. 📚 **ಬೆಳೆ ಮಾಹಿತಿ** - ಯಾವುದೇ ಬೆಳೆಯ ಬಗ್ಗೆ ಸಂಪೂರ್ಣ ಮಾಹಿತಿ ಪಡೆಯಿರಿ
            4. 👥 **ಸಮುದಾಯ** - ಇತರ ರೈತರೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಿ
            5. 🏛️ **ಯೋಜನೆಗಳು** - ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ತಿಳಿಯಿರಿ
            6. 🥬 **ಉತ್ಪನ್ನಗಳು** - ಸಾವಯವ ಉತ್ಪನ್ನಗಳನ್ನು ಖರೀದಿಸಿ/ಮಾರಾಟ ಮಾಡಿ
            
            **ಧ್ವನಿ ವೈಶಿಷ್ಟ್ಯ:** ಉತ್ತರಗಳನ್ನು ಕೇಳಲು 🔊 ಬಟನ್ ಒತ್ತಿರಿ!
            """
        }
        
        st.markdown(guide_text.get(selected_lang, guide_text['en']))
        
        # Feature cards
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background-color:#F1F8E9; padding:20px; border-radius:10px; border-left:5px solid #689F38;">
                <h3>🤖 {get_text('ai_assistant', selected_lang).split(' ')[1]}</h3>
                <p>{get_text('ask_question', selected_lang)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color:#F1F8E9; padding:20px; border-radius:10px; border-left:5px solid #689F38;">
                <h3>📸 {get_text('crop_diagnosis', selected_lang).split(' ')[1]}</h3>
                <p>{get_text('upload_image', selected_lang)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background-color:#F1F8E9; padding:20px; border-radius:10px; border-left:5px solid #689F38;">
                <h3>👥 {get_text('community', selected_lang).split(' ')[1]}</h3>
                <p>{get_text('share_experience', selected_lang)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Stats
        st.markdown("---")
        st.subheader("📊 " + ("Platform Overview" if selected_lang == 'en' else "प्लॅटफॉर्म सिंहावलोकन" if selected_lang == 'mr' else "प्लेटफॉर्म अवलोकन"))
        
        col1, col2, col3 = st.columns(3)
        
        posts = get_all_posts(limit=1000)
        products = get_all_products(limit=1000)
        
        with col1:
            st.metric(get_text('community', selected_lang).split(' ')[1], len(posts))
        with col2:
            st.metric(get_text('products', selected_lang).split(' ')[1], len(products))
        with col3:
            st.metric(get_text('language', selected_lang), len(SUPPORTED_LANGUAGES))
        
        # Made with love footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-top: 20px;">
            <p style="font-size: 18px; color: #2E7D32; margin-bottom: 5px;">
                🌾 <strong>Krishi Mitra</strong> 
            </p>
            <p style="font-size: 14px; color: #558B2F;">
                Made with ❤️ for our Annadata (Food Providers)
            </p>
            <p style="font-size: 12px; color: #666;">
                Empowering Indian Farmers with AI Technology
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # =============================================================================
    # AI FARMING ASSISTANT
    # =============================================================================
    elif page == get_text('ai_assistant', selected_lang):
        st.header(get_text('ai_assistant', selected_lang))
        
        st.markdown(f"🌐 {get_text('language', selected_lang)}: **{get_language_name(selected_lang)}**")
        st.markdown(get_text('ask_question', selected_lang))
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for idx, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # Add listen button for old messages (manual play for history)
                if message["role"] == "assistant":
                    if st.button(get_text('listen', selected_lang), key=f"listen_{idx}"):
                        st.markdown(text_to_speech(message["content"], selected_lang, auto_play=False), unsafe_allow_html=True)
        
        # Text input
        user_query = st.chat_input(get_text('type_here', selected_lang))
        
        if user_query:
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_query
            })
            
            with st.chat_message("user"):
                st.write(user_query)
            
            with st.spinner("🤖 Thinking..."):
                response = ai_service.get_farming_response(user_query, selected_lang)
            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response,
                "language": selected_lang
            })
            
                with st.chat_message("assistant"):
                st.write(response)
                # Manual button - no auto-play (no lag)
                st.markdown(text_to_speech(response, selected_lang, auto_play=False), unsafe_allow_html=True)
                st.caption(f"Language: {get_language_name(selected_lang)}")
                            
        
    
    
    # =============================================================================
    # CROP DIAGNOSIS
    # =============================================================================
    elif page == get_text('crop_diagnosis', selected_lang):
        st.header(get_text('crop_diagnosis', selected_lang))
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(get_text('upload_image', selected_lang))
            uploaded_file = st.file_uploader(
                "Choose image", 
                type=['jpg', 'jpeg', 'png'],
                help="Upload clear photo"
            )
            
            additional_context = st.text_area(
                "Additional info (optional)",
                placeholder="Describe symptoms..."
            )
            
            analyze_btn = st.button(get_text('analyze', selected_lang), type="primary")
        
        with col2:
            st.subheader(get_text('preview', selected_lang))
            if uploaded_file:
                is_valid, msg = validate_image(uploaded_file)
                if is_valid:
                    image = Image.open(uploaded_file)
                    st.image(image, use_column_width=True)
                else:
                    st.error(msg)
        
        if analyze_btn and uploaded_file:
            is_valid, msg = validate_image(uploaded_file)
            if not is_valid:
                st.error(msg)
            else:
                with st.spinner("🧠 Analyzing..."):
                    compressed_image = compress_image(uploaded_file)
                    
                    if compressed_image:
                        analysis = ai_service.analyze_crop_image(
                            compressed_image, 
                            additional_context,
                            selected_lang
                        )
                        st.markdown("---")
                        st.subheader(get_text('analysis_report', selected_lang))
                        st.markdown(analysis)
                        
                        # AUTO-PLAY voice after analysis
                        st.markdown(text_to_speech(analysis, selected_lang, auto_play=True), unsafe_allow_html=True)
                        
                    else:
                        st.error("Failed to process image")
    
    # =============================================================================
    # CROP KNOWLEDGE
    # =============================================================================
    elif page == get_text('crop_knowledge', selected_lang):
        st.header(get_text('crop_knowledge', selected_lang))
        
        crop_name = st.text_input(
            get_text('enter_crop', selected_lang),
            placeholder="e.g., Wheat, Rice, Cotton..."
        )
        
        if st.button(get_text('generate', selected_lang), type="primary") and crop_name:
            with st.spinner("🌱 Generating..."):
                knowledge = ai_service.generate_crop_knowledge(crop_name, selected_lang)
                
                st.markdown("---")
                st.markdown(knowledge)
                
                if st.button(get_text('listen', selected_lang), key="listen_knowledge"):
                    st.markdown(text_to_speech(knowledge, selected_lang), unsafe_allow_html=True)
    
    # =============================================================================
    # FARMER COMMUNITY
    # =============================================================================
    elif page == get_text('community', selected_lang):
        st.header(get_text('community', selected_lang))
        
        tab1, tab2 = st.tabs([get_text('view_posts', selected_lang), get_text('create_post', selected_lang)])
        
        with tab1:
            st.subheader(get_text('view_posts', selected_lang))
            
            posts = get_all_posts(limit=20)
            
            if not posts:
                st.info("No posts yet!")
            else:
                for post in posts:
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color:white; border:1px solid #E0E0E0; border-radius:10px; padding:15px; margin-bottom:15px;">
                            <h4>👤 {post['farmer_name']}</h4>
                            <p>{post['content']}</p>
                            <small>🕐 {format_datetime(post['created_at'])}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if post['image_path'] and os.path.exists(post['image_path']):
                            st.image(post['image_path'], use_column_width=True)
                        
                        if post['video_path'] and os.path.exists(post['video_path']):
                            st.video(post['video_path'])
                        
                        st.markdown("---")
        
        with tab2:
            st.subheader(get_text('create_post', selected_lang))
            
            with st.form("post_form"):
                farmer_name = st.text_input(get_text('your_name', selected_lang), value=user['farmer_name'])
                content = st.text_area(
                    get_text('share_experience', selected_lang), 
                    placeholder="Share your experience..."
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    image_file = st.file_uploader(get_text('attach_photo', selected_lang), type=['jpg', 'jpeg', 'png'])
                with col2:
                    video_file = st.file_uploader(get_text('attach_video', selected_lang), type=['mp4'])
                
                submitted = st.form_submit_button(get_text('post', selected_lang), type="primary")
                
                if submitted:
                    if not content:
                        st.error("Please enter content!")
                    else:
                        image_path = None
                        video_path = None
                        
                        if image_file:
                            is_valid, msg = validate_image(image_file)
                            if not is_valid:
                                st.error(f"Image error: {msg}")
                                st.stop()
                            image_path = save_uploaded_file(image_file, IMAGES_DIR)
                        
                        if video_file:
                            is_valid, msg = validate_video(video_file)
                            if not is_valid:
                                st.error(f"Video error: {msg}")
                                st.stop()
                            video_path = save_uploaded_file(video_file, VIDEOS_DIR)
                        
                        post_id = create_post(farmer_name, content, image_path, video_path)
                        st.success("Posted successfully!")
                        st.balloons()
                        st.rerun()
    
    # =============================================================================
    # GOVERNMENT SCHEMES
    # =============================================================================
    elif page == get_text('schemes', selected_lang):
        st.header(get_text('schemes', selected_lang))
        
        scheme_query = st.text_input(
            get_text('ask_scheme', selected_lang),
            placeholder="e.g., PM-KISAN, Soil Health Card..."
        )
        
        if st.button(get_text('search', selected_lang), type="primary") and scheme_query:
            with st.spinner("🏛️ Fetching..."):
                info = ai_service.get_government_scheme_info(scheme_query, selected_lang)
                
                st.markdown("---")
                st.markdown(info)
                
                if st.button(get_text('listen', selected_lang), key="listen_scheme"):
                    st.markdown(text_to_speech(info, selected_lang), unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader(get_text('popular_schemes', selected_lang))
        
        schemes = [
            ("PM-KISAN", "Pradhan Mantri Kisan Samman Nidhi"),
            ("Soil Health Card", "Free soil testing"),
            ("KCC", "Kisan Credit Card"),
            ("PMFBY", "Crop Insurance"),
            ("MIDH", "Horticulture Mission"),
            ("NMOOP", "Oilseeds Mission")
        ]
        
        cols = st.columns(3)
        for idx, (short_name, full_name) in enumerate(schemes):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="background-color:#E8F5E9; padding:15px; border-radius:8px; border:1px solid #A5D6A7;">
                    <h4>{short_name}</h4>
                    <p>{full_name}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{get_text('search', selected_lang)} {short_name}", key=f"scheme_{idx}"):
                    st.session_state.scheme_query = short_name
                    st.rerun()
    
    # =============================================================================
    # ORGANIC PRODUCTS
    # =============================================================================
    elif page == get_text('products', selected_lang):
        st.header(get_text('products', selected_lang))
        
        tab1, tab2 = st.tabs([get_text('browse_products', selected_lang), get_text('list_product', selected_lang)])
        
        with tab1:
            st.subheader(get_text('browse_products', selected_lang))
            
            search = st.text_input(get_text('search', selected_lang))
            
            if search:
                products = search_products(search)
            else:
                products = get_all_products(limit=50)
            
            if not products:
                st.info("No products listed yet!")
            else:
                cols = st.columns(2)
                for idx, product in enumerate(products):
                    with cols[idx % 2]:
                        st.markdown(f"""
                        <div style="background-color:#FFF8E1; border:1px solid #FFE082; border-radius:10px; padding:15px; margin-bottom:15px;">
                            <h3>🥬 {product['product_name']}</h3>
                            <p><strong>Farmer:</strong> {product['farmer_name']}</p>
                            <p><strong>{get_text('quantity', selected_lang)}:</strong> {product['quantity']}</p>
                            <p><strong>{get_text('location', selected_lang)}:</strong> 📍 {product['location']}</p>
                            <p><strong>{get_text('phone', selected_lang)}:</strong> 📞 {product['phone_number']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with tab2:
            st.subheader(get_text('list_product', selected_lang))
            
            with st.form("product_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    farmer_name = st.text_input(get_text('your_name', selected_lang), value=user['farmer_name'])
                    product_name = st.text_input(get_text('product_name', selected_lang), placeholder="e.g., Organic Tomatoes")
                    quantity = st.text_input(get_text('quantity', selected_lang), placeholder="e.g., 50 kg")
                
                with col2:
                    location = st.text_input(get_text('location', selected_lang), value=user['location'])
                    phone = st.text_input(get_text('phone', selected_lang), value=user['mobile_email'])
                
                submitted = st.form_submit_button(get_text('list', selected_lang), type="primary")
                
                if submitted:
                    if not all([farmer_name, product_name, quantity, location, phone]):
                        st.error("Please fill all fields!")
                    elif len(phone) < 10:
                        st.error("Invalid phone number!")
                    else:
                        product_id = add_product(farmer_name, product_name, quantity, location, phone)
                        st.success("Listed successfully!")
                        st.balloons()
             # =============================================================================
    # FOOTER - All Languages
    # =============================================================================
    
    footer_text = {
        'en': {
            'made_with': 'Made with ❤️ for our Annadata',
            'copyright': '© 2026 Krishi Mitra. Empowering Indian Farmers.',
            'tagline': 'Your Intelligent Farming Companion'
        },
        'mr': {
            'made_with': 'आमच्या अन्नदात्यांसाठी ❤️ ने बनवले',
            'copyright': '© २०२६ कृषी मित्र. शेतकऱ्यांना सशक्त बनवणे.',
            'tagline': 'तुमचे बुद्धिमान शेती सहाय्यक'
        },
        'hi': {
            'made_with': 'हमारे अन्नदाताओं के लिए ❤️ से बनाया गया',
            'copyright': '© २०२६ कृषि मित्र. किसानों को सशक्त बनाना.',
            'tagline': 'आपका बुद्धिमान कृषि सहायक'
        },
        'gu': {
            'made_with': 'અમારા અન્નદાતા માટે ❤️ થી બનાવેલ',
            'copyright': '© ૨૦૨૬ કૃષિ મિત્ર. ખેડૂતોને સશક્ત બનાવવા.',
            'tagline': 'તમારું બુદ્ધિશાળી કૃષિ સહાયક'
        },
        'ta': {
            'made_with': 'எங்கள் அன்னதாதாக்களுக்காக ❤️ உடன் உருவாக்கப்பட்டது',
            'copyright': '© २०२६ கிருஷி மித்ரா. விவசாயிகளை வலுப்படுத்துதல்.',
            'tagline': 'உங்கள் புத்திசாலி விவசாய உதவியாளர்'
        },
        'te': {
            'made_with': 'మా అన్నదాతల కోసం ❤️ తో తయారు చేయబడింది',
            'copyright': '© २०२६ కృషి మిత్ర. రైతులను సశక్తీకరించడం.',
            'tagline': 'మీ తెలివైన వ్యవసాయ సహాయకుడు'
        },
        'kn': {
            'made_with': 'ನಮ್ಮ ಅನ್ನದಾತರಿಗಾಗಿ ❤️ ಯೊಂದಿಗೆ ತಯಾರಿಸಲಾಗಿದೆ',
            'copyright': '© २०२६ ಕೃಷಿ ಮಿತ್ರ. ರೈತರನ್ನು ಸಬಲೀಕರಣಗೊಳಿಸುವುದು.',
            'tagline': 'ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಕೃಷಿ ಸಹಾಯಕ'
        }
    }
    
    ft = footer_text.get(selected_lang, footer_text['en'])
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); padding: 25px; border-radius: 15px; margin-top: 20px; border: 2px solid #4CAF50;">
        <p style="font-size: 24px; margin-bottom: 10px;">🌾</p>
        <p style="font-size: 18px; color: #1B5E20; margin-bottom: 5px; font-weight: bold;">
            <strong>Krishi Mitra</strong>
        </p>
        <p style="font-size: 16px; color: #2E7D32; margin-bottom: 5px;">
            {ft['tagline']}
        </p>
        <p style="font-size: 14px; color: #388E3C; margin-bottom: 10px;">
            {ft['made_with']}
        </p>
        <p style="font-size: 12px; color: #666; border-top: 1px solid #A5D6A7; padding-top: 10px; margin-top: 10px;">
            {ft['copyright']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.rerun()
   

"""
🌾 Krishi Mitra - Main Application Features
Multi-language UI support - NO VOICE for smooth performance
"""

import streamlit as st
from PIL import Image
from datetime import datetime
import os

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
        'ask_question': 'Ask any farming-related question in your language',
        'type_here': 'Type your question here...',
        'quick_questions': '💡 Quick Questions',
        'upload_image': '📤 Upload Image',
        'analyze': '🔍 Analyze Crop',
        'preview': '🖼️ Preview',
        'analysis_report': '📋 Analysis Report',
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
        'select_feature': 'Select Feature',
        'user_guide': '📖 User Guide',
        'how_to_use': 'How to use this app:',
        'feature_1': '💬 AI Assistant - Ask any farming question',
        'feature_2': '📸 Crop Diagnosis - Upload photo to detect diseases',
        'feature_3': '📚 Crop Knowledge - Get complete crop information',
        'feature_4': '👥 Community - Share with other farmers',
        'feature_5': '🏛️ Schemes - Learn about government schemes',
        'feature_6': '🥬 Products - Buy/Sell organic products',
        'platform_overview': '📊 Platform Overview',
        'made_with_love': 'Made with ❤️ for our Annadata',
        'copyright': '© 2026 Krishi Mitra. Empowering Indian Farmers.',
        'tagline': 'Your Intelligent Farming Companion'
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
        'ask_question': 'तुमच्या भाषेत कोणत्याही शेतीसंबंधित प्रश्न विचारा',
        'type_here': 'तुमचा प्रश्न येथे टाइप करा...',
        'quick_questions': '💡 जलद प्रश्न',
        'upload_image': '📤 प्रतिमा अपलोड करा',
        'analyze': '🔍 विश्लेषण करा',
        'preview': '🖼️ पूर्वावलोकन',
        'analysis_report': '📋 विश्लेषण अहवाल',
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
        'select_feature': 'वैशिष्ट्य निवडा',
        'user_guide': '📖 वापरकर्ता मार्गदर्शक',
        'how_to_use': 'अ‍ॅप कसे वापरावे:',
        'feature_1': '💬 AI सहाय्यक - कोणत्याही प्रश्न विचारा',
        'feature_2': '📸 पिक निदान - रोग शोधण्यासाठी फोटो अपलोड करा',
        'feature_3': '📚 पिक माहिती - संपूर्ण माहिती मिळवा',
        'feature_4': '👥 समुदाय - इतर शेतकऱ्यांसोबत शेअर करा',
        'feature_5': '🏛️ योजना - सरकारी योजना जाणून घ्या',
        'feature_6': '🥬 उत्पादने - सेंद्रिय उत्पादने खरेदी/विक्री करा',
        'platform_overview': '📊 प्लॅटफॉर्म सिंहावलोकन',
        'made_with_love': 'आमच्या अन्नदात्यांसाठी ❤️ ने बनवले',
        'copyright': '© २०२६ कृषी मित्र. शेतकऱ्यांना सशक्त बनवणे.',
        'tagline': 'तुमचे बुद्धिमान शेती सहाय्यक'
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
        'ask_question': 'अपनी भाषा में कोई भी कृषि संबंधित प्रश्न पूछें',
        'type_here': 'अपना प्रश्न यहां टाइप करें...',
        'quick_questions': '💡 त्वरित प्रश्न',
        'upload_image': '📤 छवि अपलोड करें',
        'analyze': '🔍 विश्लेषण करें',
        'preview': '🖼️ पूर्वावलोकन',
        'analysis_report': '📋 विश्लेषण रिपोर्ट',
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
        'select_feature': 'सुविधा चुनें',
        'user_guide': '📖 उपयोगकर्ता गाइड',
        'how_to_use': 'ऐप का उपयोग कैसे करें:',
        'feature_1': '💬 AI सहायक - कोई भी प्रश्न पूछें',
        'feature_2': '📸 फसल निदान - रोग का पता लगाने के लिए फोटो अपलोड करें',
        'feature_3': '📚 फसल जानकारी - पूरी जानकारी प्राप्त करें',
        'feature_4': '👥 समुदाय - अन्य किसानों के साथ साझा करें',
        'feature_5': '🏛️ योजनाएं - सरकारी योजनाओं के बारे में जानें',
        'feature_6': '🥬 उत्पाद - जैविक उत्पाद खरीदें/बेचें',
        'platform_overview': '📊 प्लेटफॉर्म अवलोकन',
        'made_with_love': 'हमारे अन्नदाताओं के लिए ❤️ से बनाया गया',
        'copyright': '© २०२६ कृषि मित्र. किसानों को सशक्त बनाना.',
        'tagline': 'आपका बुद्धिमान कृषि सहायक'
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
        'ask_question': 'તમારી ભાષામાં કોઈપણ ખેતી સંબંધિત પ્રશ્ન પૂછો',
        'type_here': 'તમારો પ્રશ્ન અહીં ટાઈપ કરો...',
        'quick_questions': '💡 ઝડપી પ્રશ્નો',
        'upload_image': '📤 છબી અપલોડ કરો',
        'analyze': '🔍 વિશ્લેષણ કરો',
        'preview': '🖼️ પૂર્વાવલોકન',
        'analysis_report': '📋 વિશ્લેષણ અહેવાલ',
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
        'select_feature': 'સુવિધા પસંદ કરો',
        'user_guide': '📖 વપરાશકર્તા માર્ગદર્શિકા',
        'how_to_use': 'એપ્લિકેશનનો ઉપયોગ કેવી રીતે કરવો:',
        'feature_1': '💬 AI સહાયક - કોઈપણ પ્રશ્ન પૂછો',
        'feature_2': '📸 પાક નિદાન - રોગ શોધવા માટે ફોટો અપલોડ કરો',
        'feature_3': '📚 પાક માહિતી - સંપૂર્ણ માહિતી મેળવો',
        'feature_4': '👥 સમુદાય - અન્ય ખેડૂતો સાથે શેર કરો',
        'feature_5': '🏛️ યોજનાઓ - સરકારી યોજનાઓ વિશે જાણો',
        'feature_6': '🥬 ઉત્પાદનો - જૈવિક ઉત્પાદનો ખરીદો/વેચો',
        'platform_overview': '📊 પ્લેટફોર્મ અવલોકન',
        'made_with_love': 'અમારા અન્નદાતા માટે ❤️ થી બનાવેલ',
        'copyright': '© ૨૦૨૬ કૃષિ મિત્ર. ખેડૂતોને સશક્ત બનાવવા.',
        'tagline': 'તમારું બુદ્ધિશાળી કૃષિ સહાયક'
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
        'ask_question': 'உங்கள் மொழியில் எந்த விவசாய தொடர்பான கேள்வியும் கேளுங்கள்',
        'type_here': 'உங்கள் கேள்வியை இங்கே தட்டச்சு செய்க...',
        'quick_questions': '💡 விரைவான கேள்விகள்',
        'upload_image': '📤 படத்தை பதிவேற்றவும்',
        'analyze': '🔍 பகுப்பாய்வு செய்யவும்',
        'preview': '🖼️ முன்னோட்டம்',
        'analysis_report': '📋 பகுப்பாய்வு அறிக்கை',
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
        'select_feature': 'அம்சத்தைத் தேர்வு செய்க',
        'user_guide': '📖 பயனர் வழிகாட்டி',
        'how_to_use': 'பயன்பாட்டை எவ்வாறு பயன்படுத்துவது:',
        'feature_1': '💬 AI உதவியாளர் - எந்த கேள்வியும் கேளுங்கள்',
        'feature_2': '📸 பயிர் கண்டறிதல் - நோயைக் கண்டறிய புகைப்படத்தை பதிவேற்றவும்',
        'feature_3': '📚 பயிர் தகவல் - முழு தகவல் பெறுங்கள்',
        'feature_4': '👥 சமூகம் - பிற விவசாயிகளுடன் பகிர்ந்து கொள்ளுங்கள்',
        'feature_5': '🏛️ திட்டங்கள் - அரசு திட்டங்கள் பற்றி அறிந்து கொள்ளுங்கள்',
        'feature_6': '🥬 பொருட்கள் - இயற்கை பொருட்களை வாங்க/விற்க',
        'platform_overview': '📊 தள கண்ணோட்டம்',
        'made_with_love': 'எங்கள் அன்னதாதாக்களுக்காக ❤️ உடன் உருவாக்கப்பட்டது',
        'copyright': '© २०२६ கிருஷி மித்ரா. விவசாயிகளை வலுப்படுத்துதல்.',
        'tagline': 'உங்கள் புத்திசாலி விவசாய உதவியாளர்'
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
        'ask_question': 'మీ భాషలో ఏదైనా వ్యవసాయ సంబంధిత ప్రశ్న అడగండి',
        'type_here': 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...',
        'quick_questions': '💡 త్వరిత ప్రశ్నలు',
        'upload_image': '📤 చిత్రాన్ని అప్‌లోడ్ చేయండి',
        'analyze': '🔍 విశ్లేషణ చేయండి',
        'preview': '🖼️ మునుజూపు',
        'analysis_report': '📋 విశ్లేషణ నివేదిక',
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
        'select_feature': 'ఫీచర్ ఎంచుకోండి',
        'user_guide': '📖 వినియోగదారు గైడ్',
        'how_to_use': 'అప్లికేషన్‌ను ఎలా ఉపయోగించాలి:',
        'feature_1': '💬 AI సహాయకుడు - ఏదైనా ప్రశ్న అడగండి',
        'feature_2': '📸 పంట నిర్ధారణ - వ్యాధులను గుర్తించడానికి ఫోటో అప్‌లోడ్ చేయండి',
        'feature_3': '📚 పంట సమాచారం - పూర్తి సమాచారం పొందండి',
        'feature_4': '👥 సమాజం - ఇతర రైతులతో పంచుకోండి',
        'feature_5': '🏛️ పథకాలు - ప్రభుత్వ పథకాల గురించి తెలుసుకోండి',
        'feature_6': '🥬 ఉత్పత్తులు - సేంద్రీయ ఉత్పత్తులను కొనుగోలు/అమ్మండి',
        'platform_overview': '📊 ప్లాట్‌ఫారమ్ అవలోకనం',
        'made_with_love': 'మా అన్నదాతల కోసం ❤️ తో తయారు చేయబడింది',
        'copyright': '© २०२६ కృషి మిత్ర. రైతులను సశక్తీకరించడం.',
        'tagline': 'మీ తెలివైన వ్యవసాయ సహాయకుడు'
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
        'ask_question': 'ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಯಾವುದೇ ಕೃಷಿ ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆ ಕೇಳಿ',
        'type_here': 'ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...',
        'quick_questions': '💡 ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು',
        'upload_image': '📤 ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'analyze': '🔍 ವಿಶ್ಲೇಷಣೆ ಮಾಡಿ',
        'preview': '🖼️ ಮುನ್ನೋಟ',
        'analysis_report': '📋 ವಿಶ್ಲೇಷಣೆ ವರದಿ',
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
        'select_feature': 'ವೈಶಿಷ್ಟ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'user_guide': '📖 ಬಳಕೆದಾರ ಮಾರ್ಗದರ್ಶಿ',
        'how_to_use': 'ಅಪ್ಲಿಕೇಶನ್ ಹೇಗೆ ಬಳಸುವುದು:',
        'feature_1': '💬 AI ಸಹಾಯಕ - ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಿ',
        'feature_2': '📸 ಬೆಳೆ ನಿದಾನ - ರೋಗಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'feature_3': '📚 ಬೆಳೆ ಮಾಹಿತಿ - ಸಂಪೂರ್ಣ ಮಾಹಿತಿ ಪಡೆಯಿರಿ',
        'feature_4': '👥 ಸಮುದಾಯ - ಇತರ ರೈತರೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಿ',
        'feature_5': '🏛️ ಯೋಜನೆಗಳು - ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ತಿಳಿಯಿರಿ',
        'feature_6': '🥬 ಉತ್ಪನ್ನಗಳು - ಸಾವಯವ ಉತ್ಪನ್ನಗಳನ್ನು ಖರೀದಿಸಿ/ಮಾರಾಟ ಮಾಡಿ',
        'platform_overview': '📊 ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ಅವಲೋಕನ',
        'made_with_love': 'ನಮ್ಮ ಅನ್ನದಾತರಿಗಾಗಿ ❤️ ಯೊಂದಿಗೆ ತಯಾರಿಸಲಾಗಿದೆ',
        'copyright': '© २०२६ ಕೃಷಿ ಮಿತ್ರ. ರೈತರನ್ನು ಸಬಲೀಕರಣಗೊಳಿಸುವುದು.',
        'tagline': 'ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಕೃಷಿ ಸಹಾಯಕ'
    }
}

def get_text(key, lang='en'):
    """Get translated text for given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'][key])

# =============================================================================
# GLOBAL CSS
# =============================================================================

def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Sora', sans-serif !important; }

    /* ── Page background ── */
    [data-testid="stAppViewContainer"] {
        background: #f0fdf6;
    }
    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 960px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a3d2e 0%, #0f5c40 40%, #166f4e 100%) !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * {
        color: #e0f5eb !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        display: block !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.14) !important;
        border-color: rgba(56, 239, 125, 0.3) !important;
    }
    [data-testid="stSidebar"] .stRadio [data-checked="true"] + label,
    [data-testid="stSidebar"] input[type="radio"]:checked + div {
        background: linear-gradient(135deg, rgba(17,153,142,0.5), rgba(56,239,125,0.3)) !important;
    }
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border-color: rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !
        important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #c0392b, #e74c3c) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 10px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(231,76,60,0.4) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background: #e8f5ee !important;
        border-radius: 14px !important;
        padding: 6px !important;
        border: 1px solid #c8e6d4 !important;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #4a7a60 !important;
        transition: all 0.25s !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0f8a72, #2dd47a) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(17,153,142,0.3) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
        background: transparent !important;
    }

    /* ── Inputs ── */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        border-radius: 12px !important;
        border: 2px solid #d4ede3 !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-family: 'Sora', sans-serif !important;
        background: #f8fdfb !important;
        transition: all 0.25s !important;
        color: #1a1a1a !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #11998e !important;
        background: white !important;
        box-shadow: 0 0 0 4px rgba(17,153,142,0.1) !important;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        font-weight: 600 !important;
        font-size: 13px !important;
        color: #2d4a3e !important;
    }

    /* ── Buttons ── */
    .stButton > button[kind="primary"],
    .stButton > button[type="primary"] {
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #0f8a72, #2dd47a) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(17,153,142,0.3) !important;
        transition: all 0.25s !important;
    }
    .stButton > button {
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        font-family: 'Sora', sans-serif !important;
        border: 1.5px solid #c8e6d4 !important;
        transition: all 0.2s !important;
        background: white !important;
        color: #1a6644 !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(17,153,142,0.2) !important;
        border-color: #11998e !important;
    }

    /* ── Metrics ── */
    div[data-testid="metric-container"] {
        background: white !important;
        border-radius: 16px !important;
        padding: 20px !important;
        border: 1px solid #d4ede3 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
        text-align: center !important;
    }
    div[data-testid="metric-container"] label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #6b9c80 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #0f8a72 !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        border-radius: 14px !important;
        border: 2px dashed #b8ddc9 !important;
        background: #f8fdfb !important;
        padding: 16px !important;
        transition: all 0.25s !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #11998e !important;
        background: #f0faf5 !important;
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 4px !important;
    }

    /* ── Alerts ── */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border: none !important;
        font-size: 14px !important;
    }

    /* ── Forms ── */
    [data-testid="stForm"] {
        background: white !important;
        border-radius: 20px !important;
        padding: 24px !important;
        border: 1px solid #d4ede3 !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
    }

    /* ── Section headers ── */
    h1, h2, h3 {
        color: #0a3d2e !important;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #b8ddc9; border-radius: 4px; }

    /* ── Page header banner ── */
    .km-page-banner {
        background: linear-gradient(135deg, #0a3d2e 0%, #11998e 60%, #38ef7d 100%);
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 24px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .km-page-banner::after {
        content: '';
        position: absolute;
        right: -20px; top: -20px;
        width: 120px; height: 120px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }
    .km-page-banner h2 {
        color: white !important;
        margin: 0 0 4px 0;
        font-size: 22px;
        font-weight: 700;
    }
    .km-page-banner p {
        color: rgba(255,255,255,0.8);
        margin: 0;
        font-size: 13px;
    }

    /* ── Card ── */
    .km-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #d4ede3;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 14px;
        transition: all 0.25s;
    }
    .km-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(17,153,142,0.12);
        border-color: #99d4b8;
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN APP FUNCTION
# =============================================================================

def run_main_app(user):
    """Run main application with all features."""

    inject_global_css()

    selected_lang = st.session_state.get('selected_language', 'en')

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align:center; padding: 12px 0 20px;">
                <div style="font-size:48px; margin-bottom:6px;">🌾</div>
                <div style="font-size:20px; font-weight:800; color:white; letter-spacing:-0.3px;">Krishi Mitra</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.6); margin-top:3px;">{APP_TAGLINE}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background:rgba(255,255,255,0.1); border-radius:12px; padding:10px 14px; margin-bottom:16px; border:1px solid rgba(255,255,255,0.15);">
                <div style="font-size:12px; color:rgba(255,255,255,0.6);">Logged in as</div>
                <div style="font-size:14px; font-weight:700; color:white; margin-top:2px;">👤 {user['farmer_name']}</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.5);">📍 {user['location']}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(255,255,255,0.12); margin:0 0 12px;'>", unsafe_allow_html=True)

        page_options = [
            get_text('home', selected_lang),
            get_text('ai_assistant', selected_lang),
            get_text('crop_diagnosis', selected_lang),
            get_text('crop_knowledge', selected_lang),
            get_text('community', selected_lang),
            get_text('schemes', selected_lang),
            get_text('products', selected_lang)
        ]

        st.markdown(f"<div style='font-size:11px; font-weight:700; color:rgba(255,255,255,0.45); letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;'>{get_text('select_feature', selected_lang)}</div>", unsafe_allow_html=True)

        page = st.radio("", options=page_options, label_visibility="collapsed")

        st.markdown("<hr style='border-color:rgba(255,255,255,0.12); margin:14px 0;'>", unsafe_allow_html=True)

        st.markdown(f"<div style='font-size:11px; font-weight:700; color:rgba(255,255,255,0.45); letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;'>🌐 {get_text('language', selected_lang)}</div>", unsafe_allow_html=True)

        lang_options = {
            'en': 'English', 'mr': 'मराठी (Marathi)', 'hi': 'हिन्दी (Hindi)',
            'gu': 'ગુજરાતી (Gujarati)', 'ta': 'தமிழ் (Tamil)',
            'te': 'తెలుగు (Telugu)', 'kn': 'ಕನ್ನಡ (Kannada)'
        }

        selected_lang_key = st.selectbox(
            "Language", options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=list(lang_options.keys()).index(selected_lang),
            key='language_selector', label_visibility="collapsed"
        )

        if selected_lang_key != selected_lang:
            st.session_state['selected_language'] = selected_lang_key
            st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.button(f"{get_text('logout', selected_lang)}", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # ── HOME PAGE ──
    if page == get_text('home', selected_lang):
        st.markdown(f"""
            <div class="km-page-banner">
                <h2>🌾 {get_text('welcome', selected_lang)}, {user['farmer_name']}!</h2>
                <p>{get_text('tagline', selected_lang)}</p>
            </div>
        """, unsafe_allow_html=True)

        features = [
            ('💬', get_text('ai_assistant', selected_lang), get_text('feature_1', selected_lang)),
            ('📸', get_text('crop_diagnosis', selected_lang), get_text('feature_2', selected_lang)),
            ('📚', get_text('crop_knowledge', selected_lang), get_text('feature_3', selected_lang)),
            ('👥', get_text('community', selected_lang), get_text('feature_4', selected_lang)),
            ('🏛️', get_text('schemes', selected_lang), get_text('feature_5', selected_lang)),
            ('🥬', get_text('products', selected_lang), get_text('feature_6', selected_lang)),
        ]

        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        for i, (icon, title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="km-card" style="text-align:center; padding:22px 16px;">
                        <div style="font-size:36px; margin-bottom:10px;">{icon}</div>
                        <div style="font-size:13px; font-weight:700; color:#0a3d2e; margin-bottom:6px;">{title}</div>
                        <div style="font-size:11.5px; color:#6b9c80; line-height:1.5;">{desc}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:13px; font-weight:700; color:#0a3d2e; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:12px;">{get_text('platform_overview', selected_lang)}</div>""", unsafe_allow_html=True)

        posts = get_all_posts(limit=1000)
        products_list = get_all_products(limit=1000)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📰 Community Posts", len(posts))
        with col2:
            st.metric("🥬 Products Listed", len(products_list))
        with col3:
            st.metric("🌐 Languages", len(SUPPORTED_LANGUAGES))

        ft = TRANSLATIONS.get(selected_lang, TRANSLATIONS['en'])
        st.markdown(f"""
            <div style="text-align:center; background:linear-gradient(135deg,#0a3d2e,#11998e); border-radius:20px; padding:28px; margin-top:24px; color:white;">
                <div style="font-size:36px; margin-bottom:8px;">🌾</div>
                <div style="font-size:18px; font-weight:800; margin-bottom:4px;">Krishi Mitra</div>
                <div style="font-size:13px; color:rgba(255,255,255,0.75); margin-bottom:6px;">{ft['tagline']}</div>
                <div style="font-size:13px; color:rgba(255,255,255,0.65);">{ft['made_with_love']}</div>
                <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.15); font-size:11px; color:rgba(255,255,255,0.45);">{ft['copyright']}</div>
            </div>
        """, unsafe_allow_html=True)

    # ── AI ASSISTANT ──
    elif page == get_text('ai_assistant', selected_lang):
        st.markdown(f"""
            <div class="km-page-banner">
                <h2>{get_text('ai_assistant', selected_lang)}</h2>
                <p>🌐 {get_text('language', selected_lang)}: <strong>{get_language_name(selected_lang)}</strong> · {get_text('ask_question', selected_lang)}</p>
            </div>
        """, unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for idx, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "language" in message:
                    st.caption(f"{get_text('language', selected_lang)}: {get_language_name(message['language'])}")

        user_query = st.chat_input(get_text('type_here', selected_lang))

        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)
            with st.spinner("🤖 Thinking..."):
                response = ai_service.get_farming_response(user_query, selected_lang)
            st.session_state.chat_history.append({"role": "assistant", "content": response, "language": selected_lang})
            with st.chat_message("assistant"):
                st.write(response)
                st.caption(f"{get_text('language', selected_lang)}: {get_language_name(selected_lang)}")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:13px; font-weight:700; color:#0a3d2e; margin-bottom:10px;">{get_text('quick_questions', selected_lang)}</div>""", unsafe_allow_html=True)

        quick_questions = {
            'en': ["How to control aphids?", "Best fertilizer for rice", "Organic pest control", "Water management"],
            'mr': ["अ‍ॅफिड्स कसे नियंत्रित करावे?", "भातासाठी सर्वोत्तम खत", "सेंद्रिय कीटक नियंत्रण", "पाणी व्यवस्थापन"],
            'hi': ["एफिड्स को कैसे नियंत्रित करें?", "चावल के लिए उर्वरक", "जैविक कीट नियंत्रण", "जल प्रबंधन"],
            'gu': ["એફિડ્સને કેવી રીતે નિયંત્રિત કરવા?", "ધાન્ય માટે ખાતર", "જૈવિક જીવાત નિયંત્રણ", "પાણીનું વ્યવસ્થાપન"],
            'ta': ["அஃபிட்களை கட்டுப்படுத்துவது?", "நெல்லுக்கு உரம்", "உயிரியல் பூச்சி கட்டுப்பாடு", "நீர் மேலாண்மை"],
            'te': ["ఎఫిడ్లను నియంత్రించడం?", "వరికి ఎరువు", "సేంద్రీయ పురుగు నియంత్రణ", "నీటి నిర్వహణ"],
            'kn': ["ಎಫಿಡ್‌ಗಳನ್ನು ನಿಯಂತ್ರಿಸುವುದು?", "ಭತ್ತಕ್ಕೆ ಗೊಬ್ಬರ", "ಸಾವಯವ ಕೀಟ ನಿಯಂತ್ರಣ", "ನೀರಿನ ವ್ಯವಸ್ಥಾಪನೆ"]
        }

        questions = quick_questions.get(selected_lang, quick_questions['en'])
        cols = st.columns(len(questions))
        for idx, question in enumerate(questions):
            with cols[idx]:
                if st.button(question[:18] + "…" if len(question) > 18 else question, key=f"quick_{idx}"):
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    st.rerun()

    # ── CROP DIAGNOSIS ──
    elif page == get_text('crop_diagnosis', selected_lang):
        st.markdown(f"""
            <div class="km-page-banner">
                <h2>{get_text('crop_diagnosis', selected_lang)}</h2>
                <p>Upload a clear photo of your crop to detect diseases and get recommendations.</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"<div style='font-weight:700; color:#0a3d2e; margin-bottom:8px;'>{get_text('upload_image', selected_lang)}</div>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Choose image", type=['jpg', 'jpeg', 'png'], help="Upload clear photo", label_visibility="collapsed")
            additional_context = st.text_area("Additional info (optional)", placeholder="Describe symptoms...")
            analyze_btn = st.button(get_text('analyze', selected_lang), type="primary", use_container_width=True)

        with col2:
            st.markdown(f"<div style='font-weight:700; color:#0a3d2e; margin-bottom:8px;'>{get_text('preview', selected_lang)}</div>", unsafe_allow_html=True)
            if uploaded_file:
                is_valid, msg = validate_image(uploaded_file)
                if is_valid:
                    image = Image.open(uploaded_file)
                    st.image(image, use_column_width=True)
                else:
                    st.error(msg)
            else:
                st.markdown("""
                    <div style="background:#f8fdfb; border:2px dashed #c8e6d4; border-radius:16px; padding:48px 24px; text-align:center; color:#a0bdb3;">
                        <div style="font-size:40px; margin-bottom:8px;">🖼️</div>
                        <div style="font-size:13px;">Image preview will appear here</div>
                    </div>
                """, unsafe_allow_html=True)

        if analyze_btn and uploaded_file:
            is_valid, msg = validate_image(uploaded_file)
            if not is_valid:
                st.error(msg)
            else:
                with st.spinner("🧠 Analyzing your crop..."):
                    compressed_image = compress_image(uploaded_file)
                    if compressed_image:
                        analysis = ai_service.analyze_crop_image(compressed_image, additional_context, selected_lang)
                        st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#f0faf5,#e8f5ee); border-radius:16px; padding:20px 24px; border:1px solid #c8e6d4; margin-top:16px;">
                                <div style="font-size:15px; font-weight:700; color:#0a3d2e; margin-bottom:12px;">📋 {get_text('analysis_report', selected_lang)}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(analysis)
                    else:
                        st.error("Failed to process image")

    # ── CROP KNOWLEDGE ──
    elif page == get_text('crop_knowledge', selected_lang):
        st.markdown(f"""
        <div class="km-page-banner">
        <h2>{get_text('crop_knowledge', selected_lang)}</h2>
        <p>Get complete growing guides, pest management, and harvest tips for any crop.</p>
        </div>
        """, unsafe_allow_html=True)

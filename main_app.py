"""
🌾 Krishi Mitra - Main Application Features
All features after login
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
# VOICE AND AUDIO FUNCTIONS
# =============================================================================

def text_to_speech(text, lang_code='en'):
    """
    Simple text-to-speech using Google Translate TTS.
    Returns an audio player that works on all devices.
    """
    import urllib.parse
    import base64
    
    # Map language codes
    lang_map = {
        'en': 'en', 'hi': 'hi', 'mr': 'mr',
        'gu': 'gu', 'ta': 'ta', 'te': 'te', 'kn': 'kn'
    }
    speech_lang = lang_map.get(lang_code, 'en')
    
    # Clean and limit text
    clean_text = text.replace('"', "'").replace('\n', ' ')[:300]
    
    # Encode text for URL
    encoded_text = urllib.parse.quote(clean_text)
    
    # Create Google TTS URL
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={speech_lang}&client=tw-ob&q={encoded_text}"
    
    # Return simple HTML audio player
    audio_html = f"""
    <div style="margin:10px 0;">
        <audio controls style="width:100%; height:40px;">
            <source src="{tts_url}" type="audio/mpeg">
            Your browser does not support audio.
        </audio>
        <p style="font-size:11px; color:#666; margin-top:5px;">
            🔊 Click play button to listen in {speech_lang.upper()}
        </p>
    </div>
    """
    
    return audio_html
    

def voice_input_widget():
    """
    Simple voice input using Streamlit's native audio recorder.
    """
    st.markdown("### 🎤 Voice Input")
    st.info("Click 'Browse files' to upload audio or type your question below")
    
    # Allow audio file upload as voice input
    audio_file = st.file_uploader("Upload voice recording (optional)", type=['wav', 'mp3', 'ogg'])
    
    if audio_file:
        st.audio(audio_file)
        st.warning("⚠️ Voice-to-text processing would require additional API. Please type your question for now.")
    
    return None
    

def run_main_app(user):
    """Run main application with all features."""
    
    # =============================================================================
    # SIDEBAR NAVIGATION
    # =============================================================================
    st.sidebar.markdown(f"## 🌾 Krishi Mitra")
    st.sidebar.markdown(f"*{APP_TAGLINE}*")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Select Feature",
        [
            "🏠 Home",
            "💬 AI Farming Assistant", 
            "📸 Crop Diagnosis",
            "📚 Crop Knowledge",
            "👥 Farmer Community",
            "🏛️ Government Schemes",
            "🥬 Organic Products"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Supported Languages:**
    - मराठी (Marathi)
    - हिंदी (Hindi)
    - English
    - ગુજરાતી (Gujarati)
    - தமிழ் (Tamil)
    - తెలుగు (Telugu)
    - ಕನ್ನಡ (Kannada)
    
    AI automatically detects your language!
    """)
    
    # =============================================================================
    # HOME PAGE
    # =============================================================================
    if page == "🏠 Home":
        st.markdown('<h1 style="text-align:center; color:#2E7D32;">🌾 Krishi Mitra</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center; color:#558B2F;">Your Intelligent Farming Companion</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color:#F1F8E9; padding:20px; border-radius:10px; border-left:5px solid #689F38;">
                <h3>🤖 AI Assistant</h3>
                <p>Get instant answers to all your farming questions in your preferred language.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color:#F1F8E9; padding:20px; border-radius:10px; border-left:5px solid #689F38;">
                <h3>📸 Crop Doctor</h3>
                <p>Upload crop photos for instant disease detection and treatment advice.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color:#F1F8E9; padding:20px; border-radius:10px; border-left:5px solid #689F38;">
                <h3>👥 Community</h3>
                <p>Connect with fellow farmers, share experiences, and learn together.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        st.subheader("📊 Platform Overview")
        col1, col2, col3 = st.columns(3)
        
        posts = get_all_posts(limit=1000)
        products = get_all_products(limit=1000)
        
        with col1:
            st.metric("Community Posts", len(posts))
        with col2:
            st.metric("Organic Listings", len(products))
        with col3:
            st.metric("Supported Languages", len(SUPPORTED_LANGUAGES))
        
        st.markdown("---")
        st.markdown("""
        ### 🚀 How to Use Krishi Mitra
        
        1. **Select a feature** from the sidebar menu
        2. **Type in your language** - AI will automatically understand and respond
        3. **Upload images** for crop diagnosis (JPG, PNG supported)
        4. **Share posts** with images and videos (MP4, max 200MB)
        5. **Browse products** from organic farmers near you
        """)
            # =============================================================================
    # AI FARMING ASSISTANT
    # =============================================================================
    elif page == "💬 AI Farming Assistant":
        st.header("💬 AI Farming Assistant")
        
        # Get selected language
        selected_lang = st.session_state.get('selected_language', 'en')
        lang_name = get_language_name(selected_lang)
        
        st.markdown(f"🌐 Current Language: **{lang_name}**")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for idx, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # Add listen button for assistant messages
                if message["role"] == "assistant":
                    if st.button("🔊 Listen", key=f"listen_{idx}"):
                        st.markdown(text_to_speech(message["content"], selected_lang), unsafe_allow_html=True)
                
                if "language" in message:
                    st.caption(f"Language: {get_language_name(message['language'])}")
        
        # Text input
        user_query = st.chat_input("Type your farming question here...")
        
        if user_query:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_query
            })
            
            with st.chat_message("user"):
                st.write(user_query)
            
            # Get response
            with st.spinner("🤖 Thinking..."):
                response = ai_service.get_farming_response(user_query, selected_lang)
            
            # Add assistant message
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response,
                "language": selected_lang
            })
            
            with st.chat_message("assistant"):
                st.write(response)
                # Add listen button
                if st.button("🔊 Listen to Answer", key=f"listen_new_{len(st.session_state.chat_history)}"):
                    st.markdown(text_to_speech(response, selected_lang), unsafe_allow_html=True)
                st.caption(f"Language: {get_language_name(selected_lang)}")
        
        # Quick questions
        st.markdown("---")
        st.subheader("💡 Quick Questions")
        
        quick_questions = {
            'en': ["How to control aphids?", "Best fertilizer for rice", "Organic pest control", "Water management"],
            'hi': ["एफिड्स को कैसे नियंत्रित करें?", "चावल के लिए उर्वरक", "जैविक कीट नियंत्रण", "जल प्रबंधन"],
            'mr': ["अ‍ॅफिड्स कसे नियंत्रित करावे?", "भातासाठी खत", "सेंद्रिय कीटक नियंत्रण", "पाणी व्यवस्थापन"],
            'gu': ["એફિડ્સને કેવી રીતે નિયંત્રિત કરવા?", "ધાન્ય માટે ખાતર", "જૈવિક જીવાત નિયંત્રણ", "પાણીનું વ્યવસ્થાપન"],
            'ta': ["அஃபிட்களை கட்டுப்படுத்துவது?", "நெல்லுக்கு உரம்", "உயிரியல் பூச்சி கட்டுப்பாடு", "நீர் மேலாண்மை"],
            'te': ["ఎఫిడ్లను నియంత్రించడం?", "వరికి ఎరువు", "సేంద్రీయ పురుగు నియంత్రణ", "నీటి నిర్వహణ"],
            'kn': ["ಎಫಿಡ್‌ಗಳನ್ನು ನಿಯಂತ್ರಿಸುವುದು?", "ಭತ್ತಕ್ಕೆ ಗೊಬ್ಬರ", "ಸಾವಯವ ಕೀಟ ನಿಯಂತ್ರಣ", "ನೀರಿನ ವ್ಯವಸ್ಥಾಪನೆ"]
        }
        
        questions = quick_questions.get(selected_lang, quick_questions['en'])
        
        cols = st.columns(len(questions))
        for idx, question in enumerate(questions):
            with cols[idx]:
                if st.button(question[:15] + "...", key=f"quick_{idx}"):
                    st.session_state.chat_history.append({
                        "role": "user", 
                        "content": question
                    })
                    st.rerun()
                    
            
                    
    
    # =============================================================================
    # CROP DIAGNOSIS
    # =============================================================================
    elif page == "📸 Crop Diagnosis":
        st.header("📸 Smart Crop Diagnosis")
        st.markdown("Upload a crop photo and get complete agricultural intelligence!")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Image")
            uploaded_file = st.file_uploader(
                "Choose a crop image", 
                type=['jpg', 'jpeg', 'png'],
                help="Upload clear photo of crop, leaf, or pest"
            )
            
            additional_context = st.text_area(
                "Additional Context (Optional)",
                placeholder="Describe any symptoms, when they started, weather conditions, etc."
            )
            
            analyze_btn = st.button("🔍 Analyze Crop", type="primary")
        
        with col2:
            st.subheader("🖼️ Preview")
            if uploaded_file:
                is_valid, msg = validate_image(uploaded_file)
                if is_valid:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                else:
                    st.error(msg)
            else:
                st.info("Image preview will appear here")
        
        # Analysis
        if analyze_btn and uploaded_file:
            is_valid, msg = validate_image(uploaded_file)
            if not is_valid:
                st.error(msg)
            else:
                with st.spinner("🧠 Analyzing crop image... This may take a moment"):
                    # Compress image for AI
                    compressed_image = compress_image(uploaded_file)
                    
                    if compressed_image:
                        # Get selected language from session
                        context_lang = st.session_state.get('selected_language', 'en')
                        
                        # Get comprehensive analysis
                        analysis = ai_service.analyze_crop_image(
                            compressed_image, 
                            additional_context,
                            context_lang
                        )
                        
                                                st.markdown("---")
                        st.subheader("📋 Analysis Report")
                        st.markdown(analysis)
                        
                        # ADD THIS FOR VOICE
                        if st.button("🔊 Listen to Analysis", key="listen_analysis"):
                            st.markdown(text_to_speech(analysis, context_lang), unsafe_allow_html=True)
                            
                            
                    else:
                        st.error("Failed to process image")
    
    # =============================================================================
    # CROP KNOWLEDGE
    # =============================================================================
    elif page == "📚 Crop Knowledge":
        st.header("📚 AI-Generated Crop Knowledge")
        st.markdown("Enter any crop name to get complete lifecycle information!")
        
        crop_name = st.text_input(
            "Enter Crop Name",
            placeholder="e.g., Wheat, Tomato, Sugarcane, Cotton..."
        )
        
        if st.button("📖 Generate Knowledge", type="primary") and crop_name:
            with st.spinner(f"🌱 Generating comprehensive knowledge for {crop_name}..."):
                # Detect language from crop name
                lang = st.session_state.get('selected_language', 'en')
                knowledge = ai_service.generate_crop_knowledge(crop_name, lang)
                
                st.markdown("---")
                st.markdown(knowledge)
                
                # Related crops suggestion
                st.markdown("---")
                st.subheader("🌾 Explore Related Crops")
                related = st.columns(4)
                suggestions = ["Rice", "Wheat", "Cotton", "Sugarcane"]
                
                for idx, suggestion in enumerate(suggestions):
                    with related[idx]:
                        if st.button(suggestion, key=f"rel_{idx}"):
                            st.rerun()
    
       # =============================================================================
    # FARMER COMMUNITY
    # =============================================================================
    elif page == "👥 Farmer Community":
        st.header("👥 Farmer Community")
        
        tab1, tab2 = st.tabs(["📰 View Posts", "➕ Create Post"])
        
        # View Posts Tab
        with tab1:
            st.subheader("Recent Community Posts")
            
            posts = get_all_posts(limit=20)
            
            if not posts:
                st.info("No posts yet. Be the first to share!")
            else:
                for post in posts:
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color:white; border:1px solid #E0E0E0; border-radius:10px; padding:15px; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                            <h4>👤 {post['farmer_name']}</h4>
                            <p>{post['content']}</p>
                            <small>🕐 {format_datetime(post['created_at'])}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display media if exists
                        if post['image_path'] and os.path.exists(post['image_path']):
                            st.image(post['image_path'], use_column_width=True)
                        
                        if post['video_path'] and os.path.exists(post['video_path']):
                            st.video(post['video_path'])
                        
                        st.markdown("---")
        
        # Create Post Tab
        with tab2:
            st.subheader("Create New Post")
            
            with st.form("post_form"):
                # Auto-fill farmer name from logged in user
                farmer_name = st.text_input("Your Name", value=user['farmer_name'])
                content = st.text_area(
                    "Share your experience or question", 
                    placeholder="Share farming tips, ask questions, or post updates..."
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    image_file = st.file_uploader(
                        "Attach Photo (Optional)", 
                        type=['jpg', 'jpeg', 'png']
                    )
                with col2:
                    video_file = st.file_uploader(
                        "Attach Video (Optional)", 
                        type=['mp4'],
                        help="Max 200MB"
                    )
                
                submitted = st.form_submit_button("Post to Community", type="primary")
                
                if submitted:
                    if not content:
                        st.error("Please enter content!")
                    else:
                        # Validate and save files
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
                        
                        # Save post
                        post_id = create_post(farmer_name, content, image_path, video_path)
                        st.success("Post created successfully!")
                        st.balloons()
                        st.rerun()
                        
    
    # =============================================================================
    # GOVERNMENT SCHEMES
    # =============================================================================
    elif page == "🏛️ Government Schemes":
        st.header("🏛️ Government Scheme Information")
        st.markdown("Get detailed information about Indian government farming schemes!")
        
        scheme_query = st.text_input(
            "Ask about any scheme",
            placeholder="e.g., PM-KISAN, Soil Health Card, FPO Scheme, Crop Insurance..."
        )
        
        if st.button("🔍 Get Information", type="primary") and scheme_query:
            with st.spinner("🏛️ Fetching scheme details..."):
                lang = st.session_state.get('selected_language', 'en')
                info = ai_service.get_government_scheme_info(scheme_query, lang)
                
                st.markdown("---")
                st.markdown(info)
        
        st.markdown("---")
        st.subheader("📋 Popular Schemes")
        
        schemes = [
            ("PM-KISAN", "Pradhan Mantri Kisan Samman Nidhi"),
            ("Soil Health Card", "Free soil testing and recommendations"),
            ("KCC", "Kisan Credit Card scheme"),
            ("PMFBY", "Pradhan Mantri Fasal Bima Yojana"),
            ("MIDH", "Mission for Integrated Development of Horticulture"),
            ("NMOOP", "National Mission on Oilseeds and Oil Palm")
        ]
        
        cols = st.columns(3)
        for idx, (short_name, full_name) in enumerate(schemes):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="background-color:#E8F5E9; padding:15px; border-radius:8px; border:1px solid #A5D6A7;">
                        <h4>{short_name}</h4>
                        <p>{full_name}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Learn about {short_name}", key=f"scheme_{idx}"):
                        st.session_state.scheme_query = short_name
                        st.rerun()
    
    # =============================================================================
    # ORGANIC PRODUCTS
    # =============================================================================
    elif page == "🥬 Organic Products":
        st.header("🥬 Organic Product Listings")
        
        tab1, tab2 = st.tabs(["🛒 Browse Products", "➕ List Your Product"])
        
        # Browse Tab
        with tab1:
            st.subheader("Available Organic Products")
            
            search = st.text_input("🔍 Search products, locations, or farmers")
            
            if search:
                products = search_products(search)
            else:
                products = get_all_products(limit=50)
            
            if not products:
                st.info("No products listed yet. Be the first to sell!")
            else:
                cols = st.columns(2)
                for idx, product in enumerate(products):
                    with cols[idx % 2]:
                        st.markdown(f"""
                        <div style="background-color:#FFF8E1; border:1px solid #FFE082; border-radius:10px; padding:15px; margin-bottom:15px;">
                            <h3>🥬 {product['product_name']}</h3>
                            <p><strong>Farmer:</strong> {product['farmer_name']}</p>
                            <p><strong>Quantity:</strong> {product['quantity']}</p>
                            <p><strong>Location:</strong> 📍 {product['location']}</p>
                            <p><strong>Contact:</strong> 📞 {product['phone_number']}</p>
                            <small>Listed on: {format_datetime(product['created_at'])}</small>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Add Product Tab
        with tab2:
            st.subheader("List Your Organic Product")
            
            with st.form("product_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Auto-fill from user profile
                    farmer_name = st.text_input("Your Name *", value=user['farmer_name'])
                    product_name = st.text_input("Product Name *", placeholder="e.g., Organic Tomatoes")
                    quantity = st.text_input("Available Quantity *", placeholder="e.g., 50 kg, 100 dozen")
                
                with col2:
                    location = st.text_input("Location/Village *", value=user['location'])
                    phone = st.text_input("Phone Number *", value=user['mobile_email'])
                
                submitted = st.form_submit_button("List Product", type="primary")
                
                if submitted:
                    if not all([farmer_name, product_name, quantity, location, phone]):
                        st.error("Please fill all required fields!")
                    elif len(phone) < 10:
                        st.error("Please enter valid phone number!")
                    else:
                        product_id = add_product(
                            farmer_name, product_name, quantity, location, phone
                        )
                        st.success("Product listed successfully!")
                        st.balloons()
                        st.rerun()
    
    # =============================================================================
    # FOOTER
    # =============================================================================
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🌾 <strong>Krishi Mitra</strong> - Empowering Indian Farmers with AI</p>
        <p style="font-size: 0.8rem;">Made with ❤️ for our Annadata (food providers)</p>
    </div>
    """, unsafe_allow_html=True)

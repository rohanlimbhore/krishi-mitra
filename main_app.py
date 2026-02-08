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
    Convert text to speech using browser's built-in speech synthesis.
    Returns HTML/JavaScript code.
    """
    # Map language codes to speech synthesis codes
    lang_map = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'mr': 'mr-IN',
        'gu': 'gu-IN',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'kn': 'kn-IN'
    }
    
    speech_lang = lang_map.get(lang_code, 'en-IN')
    
    # Clean text for JavaScript (remove quotes and newlines)
    clean_text = text.replace('"', "'").replace('\n', ' ').replace('\r', '')
    # Limit text length for speech
    if len(clean_text) > 500:
        clean_text = clean_text[:500] + "... (text truncated for audio)"
    
    html_code = f"""
    <script>
    function speakText() {{
        if ('speechSynthesis' in window) {{
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            var text = "{clean_text}";
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = '{speech_lang}';
            utterance.rate = 0.9;  // Slightly slower for clarity
            utterance.pitch = 1;
            
            // Try to find appropriate voice
            var voices = window.speechSynthesis.getVoices();
            var selectedVoice = voices.find(voice => voice.lang.includes('{speech_lang.split("-")[0]}'));
            if (selectedVoice) {{
                utterance.voice = selectedVoice;
            }}
            
            window.speechSynthesis.speak(utterance);
        }} else {{
            alert("Sorry, your browser doesn't support text-to-speech!");
        }}
    }}
    
    // Auto-speak after a short delay
    setTimeout(speakText, 1000);
    </script>
    
    <button onclick="speakText()" style="
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
    ">
        🔊 Listen Again
    </button>
    """
    
    return html_code

def voice_input_button(key="voice_input"):
    """
    Create a voice input button using Web Speech API.
    """
    html_code = """
    <script>
    function startVoiceInput() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            var recognition = new SpeechRecognition();
            
            recognition.lang = document.getElementById('selectedLang')?.value || 'en-IN';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                document.getElementById('voiceStatus').innerHTML = '🎤 Listening... Speak now';
                document.getElementById('voiceStatus').style.color = 'red';
            };
            
            recognition.onresult = function(event) {
                var transcript = event.results[0][0].transcript;
                document.getElementById('voiceInputResult').value = transcript;
                document.getElementById('voiceStatus').innerHTML = '✅ Voice captured! Click Send';
                document.getElementById('voiceStatus').style.color = 'green';
                
                // Trigger Streamlit to update
                var event = new Event('input', { bubbles: true });
                document.getElementById('voiceInputResult').dispatchEvent(event);
            };
            
            recognition.onerror = function(event) {
                document.getElementById('voiceStatus').innerHTML = '❌ Error: ' + event.error;
                document.getElementById('voiceStatus').style.color = 'red';
            };
            
            recognition.onend = function() {
                if (document.getElementById('voiceStatus').innerHTML.includes('Listening')) {
                    document.getElementById('voiceStatus').innerHTML = '⏹️ Stopped listening';
                    document.getElementById('voiceStatus').style.color = 'gray';
                }
            };
            
            recognition.start();
        } else {
            alert('Sorry, voice input is not supported in your browser. Please use Chrome or Edge.');
        }
    }
    </script>
    
    <input type="hidden" id="selectedLang" value="">
    
    <button onclick="startVoiceInput()" style="
        background-color: #FF9800;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin-right: 10px;
    ">
        🎤 Speak
    </button>
    
    <span id="voiceStatus" style="font-weight: bold;">Click mic to speak</span>
    
    <input type="text" id="voiceInputResult" style="display:none;">
    """
    
    return html_code

def get_language_code_from_name(lang_name):
    """Convert full language name to code."""
    lang_map = {
        'English': 'en',
        'Hindi': 'hi',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Kannada': 'kn'
    }
    return lang_map.get(lang_name, 'en')

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
        st.markdown("Ask any farming-related question. I will respond in your language automatically!")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "language" in message:
                    st.caption(f"Detected: {get_language_name(message['language'])}")
        
        # Chat input
        user_query = st.chat_input("Type your farming question here...")
        
        if user_query:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_query
            })
            
            with st.chat_message("user"):
                st.write(user_query)
            
            # Detect language and get response
            with st.spinner("🤖 Thinking..."):
                detected_lang = ai_service.detect_language(user_query)
                response = ai_service.get_farming_response(user_query, detected_lang)
            
            # Add assistant message
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response,
                "language": detected_lang
            })
            
            with st.chat_message("assistant"):
                st.write(response)
                st.caption(f"Detected: {get_language_name(detected_lang)}")
        
        # Quick question buttons
        st.markdown("---")
        st.subheader("💡 Quick Questions")
        
        quick_questions = [
            "How to control aphids in cotton?",
            "Best fertilizer for paddy rice",
            "Organic pest control methods",
            "Water management in wheat",
            "Government subsidy for drip irrigation"
        ]
        
        cols = st.columns(len(quick_questions))
        for idx, question in enumerate(quick_questions):
            with cols[idx]:
                if st.button(question, key=f"quick_{idx}"):
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
                        # Detect language from context or default to English
                        context_lang = 'en'
                        if additional_context:
                            context_lang = ai_service.detect_language(additional_context)
                        
                        # Get comprehensive analysis
                        analysis = ai_service.analyze_crop_image(
                            compressed_image, 
                            additional_context,
                            context_lang
                        )
                        
                        st.markdown("---")
                        st.subheader("📋 Analysis Report")
                        st.markdown(analysis)
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
                lang = ai_service.detect_language(crop_name)
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
                lang = ai_service.detect_language(scheme_query)
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

    
    

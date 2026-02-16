"""
🌾 Krishi Mitra - Professional Farming Support Application
"""

import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import os

# Must be first
st.set_page_config(
    page_title="Krishi Mitra - Farming Assistant",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Database setup
DB_PATH = "krishi_mitra.db"

def init_user_db():
    """Initialize user database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile_email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            farmer_name TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(mobile_email, password, farmer_name, location):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (mobile_email, password_hash, farmer_name, location)
            VALUES (?, ?, ?, ?)
        ''', (mobile_email, password_hash, farmer_name, location))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "Mobile number or Email already registered!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def login_user(mobile_email, password):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute('''
            SELECT * FROM users WHERE mobile_email = ? AND password_hash = ?
        ''', (mobile_email, password_hash))
        user = cursor.fetchone()
        conn.close()
        if user:
            return True, {
                'id': user[0],
                'mobile_email': user[1],
                'farmer_name': user[3],
                'location': user[4]
            }
        return False, "Invalid credentials!"
    except Exception as e:
        return False, f"Error: {str(e)}"

# =============================================================================
# PROFESSIONAL UI WITH ANIMATIONS
# =============================================================================

def show_login_page():
    """Display professional login page with animations."""
        # Professional CSS with WOW background
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* ============================================
           WOW BACKGROUND - Animated Farming Scene
           ============================================ */
        .main {
            background: linear-gradient(180deg, 
                #87CEEB 0%,      /* Sky blue */
                #E0F6FF 20%,     /* Light sky */
                #90EE90 40%,     /* Grass start */
                #228B22 60%,     /* Forest green */
                #006400 80%,     /* Dark green */
                #1a4d1a 100%     /* Deep green */
            );
            background-attachment: fixed;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated sun */
        .main::before {
            content: '';
            position: fixed;
            top: 50px;
            right: 50px;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, #FFD700 0%, #FFA500 50%, transparent 70%);
            border-radius: 50%;
            animation: sunPulse 4s ease-in-out infinite;
            z-index: 0;
        }
        
        @keyframes sunPulse {
            0%, 100% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; }
        }
        
        /* Floating clouds */
        .main::after {
            content: '☁️ ☁️ ☁️';
            position: fixed;
            top: 80px;
            left: -100%;
            font-size: 60px;
            opacity: 0.6;
            animation: cloudsMove 20s linear infinite;
            z-index: 0;
        }
        
        @keyframes cloudsMove {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* Animated grass/waves at bottom */
        .grass-waves {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 150px;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23228B22' fill-opacity='0.3' d='M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,165.3C1248,149,1344,107,1392,85.3L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
            background-size: cover;
            animation: waveMove 10s ease-in-out infinite;
            z-index: 0;
        }
        
        @keyframes waveMove {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        /* ============================================
           GLASS CARD - Enhanced
           ============================================ */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 
                0 25px 50px -12px rgba(0, 0, 0, 0.25),
                0 0 0 1px rgba(255, 255, 255, 0.3),
                inset 0 0 80px rgba(255, 255, 255, 0.5);
            border: 2px solid rgba(255, 255, 255, 0.6);
            max-width: 440px;
            margin: 0 auto;
            animation: slideUp 0.8s ease-out;
            position: relative;
            z-index: 10;
        }
        
        /* Shiny border effect */
        .glass-card::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #FFD700, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
            border-radius: 32px;
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .glass-card:hover::before {
            opacity: 0.5;
            animation: borderRotate 3s linear infinite;
        }
        
        @keyframes borderRotate {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* ============================================
           LOGO - Enhanced with glow
           ============================================ */
        .logo-container {
            text-align: center;
            margin-bottom: 24px;
        }
        
        .logo-icon {
            font-size: 80px;
            animation: bounceRotate 3s infinite;
            display: inline-block;
            filter: drop-shadow(0 10px 20px rgba(34, 139, 34, 0.3));
        }
        
        @keyframes bounceRotate {
            0%, 100% { 
                transform: translateY(0) rotate(0deg); 
            }
            25% { 
                transform: translateY(-15px) rotate(5deg); 
            }
            50% { 
                transform: translateY(0) rotate(0deg); 
            }
            75% { 
                transform: translateY(-10px) rotate(-5deg); 
            }
        }
        
        .app-title {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(135deg, #228B22, #006400);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 0;
            letter-spacing: -1px;
        }
        
        .app-tagline {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 8px;
            font-weight: 500;
        }
        
        /* ============================================
           TABS - Modern pill style
           ============================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(245, 245, 245, 0.8);
            border-radius: 16px;
            padding: 8px;
            backdrop-filter: blur(10px);
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            border-radius: 12px;
            padding: 14px 24px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #228B22, #32CD32);
            color: white;
            box-shadow: 0 8px 20px rgba(34, 139, 34, 0.3);
            transform: scale(1.02);
        }
        
        /* ============================================
           INPUTS - Floating label style
           ============================================ */
        div[data-testid="stTextInput"] {
            position: relative;
        }
        
        div[data-testid="stTextInput"] input {
            border-radius: 16px;
            border: 2px solid #e8e8e8;
            padding: 18px 16px;
            font-size: 15px;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        div[data-testid="stTextInput"] input:focus {
            border-color: #228B22;
            background: white;
            box-shadow: 0 0 0 4px rgba(34, 139, 34, 0.1), 0 4px 20px rgba(34, 139, 34, 0.1);
            transform: translateY(-2px);
        }
        
        /* ============================================
           BUTTON - 3D effect
           ============================================ */
        .stButton > button {
            width: 100%;
            border-radius: 16px;
            padding: 18px;
            font-size: 16px;
            font-weight: 700;
            background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);
            color: white;
            border: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 
                0 4px 15px rgba(34, 139, 34, 0.4),
                0 8px 0 #1a6b1a,
                inset 0 1px 0 rgba(255,255,255,0.3);
            position: relative;
            top: 0;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 
                0 8px 25px rgba(34, 139, 34, 0.5),
                0 12px 0 #1a6b1a,
                inset 0 1px 0 rgba(255,255,255,0.3);
        }
        
        .stButton > button:active {
            transform: translateY(4px);
            box-shadow: 
                0 2px 10px rgba(34, 139, 34, 0.4),
                0 4px 0 #1a6b1a,
                inset 0 1px 0 rgba(255,255,255,0.3);
        }
        
        /* ============================================
           FEATURE CARDS - 3D hover
           ============================================ */
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 28px;
        }
        
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 
                0 4px 6px rgba(0,0,0,0.05),
                0 10px 20px rgba(0,0,0,0.02);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.5s;
        }
        
        .feature-card:hover::before {
            left: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 20px 40px rgba(0,0,0,0.1),
                0 0 0 2px rgba(34, 139, 34, 0.1);
        }
        
        .feature-icon-small {
            font-size: 36px;
            margin-bottom: 12px;
            transition: transform 0.3s;
        }
        
        .feature-card:hover .feature-icon-small {
            transform: scale(1.2) rotate(10deg);
        }
        
        .feature-title {
            font-size: 13px;
            font-weight: 700;
            color: #333;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* ============================================
           FOOTER - Enhanced
           ============================================ */
        .footer {
            text-align: center;
            margin-top: 32px;
            padding-top: 24px;
            border-top: 2px solid rgba(0,0,0,0.05);
        }
        
        .footer-text {
            color: #888;
            font-size: 13px;
            line-height: 1.6;
        }
        
        .heart {
            color: #e74c3c;
            animation: heartbeat 1.5s ease-in-out infinite;
            display: inline-block;
        }
        
        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            10% { transform: scale(1.1); }
            20% { transform: scale(1); }
            30% { transform: scale(1.1); }
        }
        
        /* ============================================
           MESSAGES - Modern alerts
           ============================================ */
        .stAlert {
            border-radius: 16px;
            border: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Success message styling */
        .stAlert[data-baseweb="notification"] {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            border-left: 4px solid #28a745;
        }
        
        /* Error message styling */
        .stAlert[data-baseweb="notification"][kind="error"] {
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            border-left: 4px solid #dc3545;
        }
        
        /* ============================================
           HIDE ELEMENTS
           ============================================ */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ============================================
           FLOATING ELEMENTS
           ============================================ */
        .floating-leaf {
            position: fixed;
            font-size: 30px;
            animation: floatLeaf 15s linear infinite;
            opacity: 0.3;
            z-index: 1;
        }
        
        @keyframes floatLeaf {
            0% {
                transform: translateY(100vh) rotate(0deg);
                left: 10%;
            }
            100% {
                transform: translateY(-100px) rotate(360deg);
                left: 90%;
            }
        }
        </style>
        
        <!-- Floating leaves -->
        <div class="floating-leaf" style="animation-delay: 0s;">🍃</div>
        <div class="floating-leaf" style="animation-delay: 5s; font-size: 20px;">🌿</div>
        <div class="floating-leaf" style="animation-delay: 10s; font-size: 25px;">🌾</div>
        
        <!-- Grass waves -->
        <div class="grass-waves"></div>
    """, unsafe_allow_html=True)
    # Modern tabs
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            login_email = st.text_input(
                "📱 Mobile Number or Email",
                placeholder="Enter your mobile or email",
                key="login_email"
            )
            
            login_password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            col_forgot, col_login = st.columns([1, 1])
            
            with col_forgot:
                st.markdown("<p style='color: #11998e; font-size: 12px; margin-top: 10px; cursor: pointer;'>Forgot password?</p>", 
                           unsafe_allow_html=True)
            
            with col_login:
                login_btn = st.button("Sign In →", type="primary", use_container_width=True)
            
            if login_btn:
                if login_email and login_password:
                    with st.spinner(""):
                        success, result = login_user(login_email, login_password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = result
                            st.success("✨ Welcome back, " + result['farmer_name'] + "!")
                            st.rerun()
                        else:
                            st.error("❌ " + result)
                else:
                    st.warning("⚠️ Please fill all fields")
        
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            reg_name = st.text_input(
                "👤 Full Name",
                placeholder="Your full name",
                key="reg_name"
            )
            
            reg_mobile = st.text_input(
                "📱 Mobile Number",
                placeholder="10 digit mobile number",
                key="reg_mobile"
            )
            
            reg_location = st.text_input(
                "📍 Village/District",
                placeholder="Your location",
                key="reg_location"
            )
            
            reg_password = st.text_input(
                "🔒 Create Password",
                type="password",
                placeholder="Min 6 characters",
                key="reg_password"
            )
            
            reg_confirm = st.text_input(
                "🔒 Confirm Password",
                type="password",
                placeholder="Re-enter password",
                key="reg_confirm"
            )
            
            if st.button("Create Account →", type="primary", use_container_width=True):
                if all([reg_name, reg_mobile, reg_location, reg_password]):
                    if reg_password == reg_confirm:
                        if len(reg_password) >= 6:
                            success, msg = register_user(reg_mobile, reg_password, reg_name, reg_location)
                            if success:
                                st.success("✅ " + msg + " Please sign in.")
                            else:
                                st.error("❌ " + msg)
                        else:
                            st.warning("⚠️ Password must be 6+ characters")
                    else:
                        st.error("❌ Passwords don't match!")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        # Feature cards grid
        st.markdown('''
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon-small">🤖</div>
                    <div class="feature-title">AI Assistant</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-small">📸</div>
                    <div class="feature-title">Crop Scan</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-small">👥</div>
                    <div class="feature-title">Community</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-small">🏛️</div>
                    <div class="feature-title">Govt Schemes</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        # Footer
        st.markdown('''
            <div class="footer">
                <p class="footer-text">
                    Made with <span class="heart">❤️</span> for Indian Farmers<br>
                    © 2026 Krishi Mitra
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Initialize
init_user_db()

# Check login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login or main app
if not st.session_state.logged_in:
    show_login_page()
else:
    # CONNECT TO MAIN APP
    from main_app import run_main_app
    run_main_app(st.session_state.user)
    

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
    
    # Professional CSS with animations
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Animated gradient background */
        .main {
            background: linear-gradient(-45deg, #11998e, #38ef7d, #11998e, #0f9b0f);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Glassmorphism card */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.3);
            max-width: 420px;
            margin: 0 auto;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Logo animation */
        .logo-container {
            text-align: center;
            margin-bottom: 24px;
        }
        
        .logo-icon {
            font-size: 72px;
            animation: bounce 2s infinite;
            display: inline-block;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .app-title {
            font-size: 32px;
            font-weight: 700;
            color: #1a1a1a;
            text-align: center;
            margin: 0;
            letter-spacing: -0.5px;
        }
        
        .app-tagline {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 8px;
            font-weight: 400;
        }
        
        /* Modern tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: #f5f5f5;
            border-radius: 12px;
            padding: 6px;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            border-radius: 10px;
            padding: 12px 20px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        }
        
        /* Modern inputs */
        div[data-testid="stTextInput"] input {
            border-radius: 12px;
            border: 2px solid #e8e8e8;
            padding: 16px;
            font-size: 15px;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        div[data-testid="stTextInput"] input:focus {
            border-color: #11998e;
            background: white;
            box-shadow: 0 0 0 4px rgba(17, 153, 142, 0.1);
        }
        
        /* Modern button */
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            padding: 16px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            border: none;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(17, 153, 142, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Feature cards */
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 24px;
        }
        
        .feature-card {
            background: white;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        
        .feature-icon-small {
            font-size: 32px;
            margin-bottom: 8px;
        }
        
        .feature-title {
            font-size: 12px;
            font-weight: 600;
            color: #333;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid #e8e8e8;
        }
        
        .footer-text {
            color: #888;
            font-size: 12px;
        }
        
        .heart {
            color: #e74c3c;
            animation: heartbeat 1.5s infinite;
        }
        
        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        /* Success/Error messages */
        .stAlert {
            border-radius: 12px;
            border: none;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Loading animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #11998e;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center layout
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        # Glass card container
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Animated logo
        st.markdown('''
            <div class="logo-container">
                <div class="logo-icon">🌾</div>
                <h1 class="app-title">Krishi Mitra</h1>
                <p class="app-tagline">Your Intelligent Farming Companion</p>
            </div>
        ''', unsafe_allow_html=True)
        
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
    

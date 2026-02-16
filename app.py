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
# PROFESSIONAL UI WITH WOW BACKGROUND
# =============================================================================

def show_login_page():
    """Display professional login page with animated background."""
    
    # Professional CSS - Simplified but effective
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Animated gradient background - Sky to Farm */
        .stApp {
            background: linear-gradient(180deg, 
                #87CEEB 0%,      
                #B0E0E6 15%,     
                #98FB98 35%,     
                #90EE90 50%,     
                #228B22 70%,     
                #006400 100%     
            );
            background-attachment: fixed;
        }
        
        /* Main container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Glass card */
        div[data-testid="stVerticalBlock"] > div {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            border: 2px solid rgba(255, 255, 255, 0.5);
            max-width: 420px;
            margin: 0 auto;
        }
        
        /* Logo animation */
        .logo-icon {
            font-size: 72px;
            text-align: center;
            animation: bounce 2s infinite;
            display: block;
            margin-bottom: 10px;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
        
        /* Title styling */
        h1 {
            font-size: 32px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #228B22, #006400);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 5px !important;
        }
        
        /* Tagline */
        .tagline {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: #f0f0f0;
            border-radius: 12px;
            padding: 6px;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            border-radius: 10px;
            padding: 12px;
            font-weight: 600;
            font-size: 14px;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #228B22, #32CD32) !important;
            color: white !important;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            padding: 15px;
            font-size: 15px;
            background: #fafafa;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #228B22;
            box-shadow: 0 0 0 3px rgba(34, 139, 34, 0.1);
        }
        
        /* Buttons */
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            padding: 15px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #228B22, #32CD32) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(34, 139, 34, 0.3);
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(34, 139, 34, 0.4);
        }
        
        /* Feature cards */
        .feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 25px;
        }
        
        .feature-box {
            background: white;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .feature-emoji {
            font-size: 32px;
            margin-bottom: 8px;
        }
        
        .feature-text {
            font-size: 12px;
            font-weight: 600;
            color: #333;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #888;
            font-size: 12px;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    # Center layout
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        # Logo
        st.markdown('<div class="logo-icon">🌾</div>', unsafe_allow_html=True)
        st.markdown('<h1>Krishi Mitra</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline">Your Intelligent Farming Companion</p>', unsafe_allow_html=True)
        
        # Tabs
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
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("<p style='color: #666; font-size: 12px; margin-top: 10px;'>Forgot password?</p>", 
                           unsafe_allow_html=True)
            
            with col2:
                login_btn = st.button("Sign In →", type="primary", use_container_width=True)
            
            if login_btn:
                if login_email and login_password:
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
        
        # Feature boxes using columns
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌟 What You Get")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
                <div style="background: white; padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div style="font-size: 32px; margin-bottom: 8px;">🤖</div>
                    <div style="font-size: 12px; font-weight: 600;">AI Assistant</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="background: white; padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div style="font-size: 32px; margin-bottom: 8px;">👥</div>
                    <div style="font-size: 12px; font-weight: 600;">Community</div>
                </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown("""
                <div style="background: white; padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div style="font-size: 32px; margin-bottom: 8px;">📸</div>
                    <div style="font-size: 12px; font-weight: 600;">Crop Scan</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="background: white; padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div style="font-size: 32px; margin-bottom: 8px;">🏛️</div>
                    <div style="font-size: 12px; font-weight: 600;">Govt Schemes</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div class="footer">
                <p>Made with ❤️ for Indian Farmers</p>
                <p>© 2026 Krishi Mitra</p>
            </div>
        """, unsafe_allow_html=True)

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
    

"""
🌾 Krishi Mitra - Intelligent Farming Support Application
Main Entry Point with Login System
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

# Database setup for users
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
    """Hash password for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(mobile_email, password, farmer_name, location):
    """Register new user."""
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
    """Verify login credentials."""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE mobile_email = ? AND password_hash = ?
        ''', (mobile_email, password_hash))
        
        # THIS WAS MISSING - Added now
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
# BEAUTIFUL UI - Only this part changed
# =============================================================================

def show_login_page():
    """Display beautiful login page."""
    
    # Custom CSS for beautiful UI
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 400px;
            margin: 0 auto;
        }
        
        .logo-text {
            font-size: 60px;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .app-title {
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            color: #1B5E20;
            margin: 0;
        }
        
        .app-tagline {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: #f0f0f0;
            border-radius: 10px;
            padding: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            border-radius: 8px;
            padding: 12px 20px;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: white;
        }
        
        div[data-testid="stTextInput"] input {
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            padding: 15px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        div[data-testid="stTextInput"] input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 3px rgba(76,175,80,0.1);
        }
        
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            padding: 15px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: white;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(76,175,80,0.3);
        }
        
        .feature-box {
            background: #F1F8E9;
            padding: 20px;
            border-radius: 15px;
            margin-top: 30px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin: 10px 0;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .feature-icon {
            font-size: 28px;
            margin-right: 15px;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #888;
            font-size: 12px;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    # Center the login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and Header
        st.markdown('<div class="logo-text">🌾</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="app-title">Krishi Mitra</h1>', unsafe_allow_html=True)
        st.markdown('<p class="app-tagline">Your Intelligent Farming Companion</p>', unsafe_allow_html=True)
        
        # Login/Register Tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            login_email = st.text_input(
                "📱 Mobile Number or Email",
                placeholder="e.g., 9876543210 or farmer@email.com",
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
                login_btn = st.button("Login →", type="primary", use_container_width=True)
            
            if login_btn:
                if login_email and login_password:
                    success, result = login_user(login_email, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = result
                        st.success("✅ Welcome back, " + result['farmer_name'] + "!")
                        st.rerun()
                    else:
                        st.error("❌ " + result)
                else:
                    st.warning("⚠️ Please fill all fields")
        
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            reg_name = st.text_input(
                "👤 Full Name",
                placeholder="e.g., Ramesh Patil",
                key="reg_name"
            )
            
            reg_mobile = st.text_input(
                "📱 Mobile Number",
                placeholder="e.g., 9876543210",
                key="reg_mobile"
            )
            
            reg_location = st.text_input(
                "📍 Village/Location",
                placeholder="e.g., Pune, Maharashtra",
                key="reg_location"
            )
            
            reg_password = st.text_input(
                "🔒 Create Password",
                type="password",
                placeholder="Minimum 6 characters",
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
                                st.success("✅ " + msg + " Please login.")
                            else:
                                st.error("❌ " + msg)
                        else:
                            st.warning("⚠️ Password must be at least 6 characters")
                    else:
                        st.error("❌ Passwords don't match!")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        # Features Section
        st.markdown("""
            <div class="feature-box">
                <h3 style="text-align: center; color: #1B5E20; margin-bottom: 20px;">
                    🌟 What You Get
                </h3>
                <div class="feature-item">
                    <span class="feature-icon">🤖</span>
                    <div>
                        <strong>AI Farming Assistant</strong><br>
                        <small style="color: #666;">Get answers in your language</small>
                    </div>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📸</span>
                    <div>
                        <strong>Crop Disease Detection</strong><br>
                        <small style="color: #666;">Upload photo, get instant diagnosis</small>
                    </div>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">👥</span>
                    <div>
                        <strong>Farmer Community</strong><br>
                        <small style="color: #666;">Connect with other farmers</small>
                    </div>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🏛️</span>
                    <div>
                        <strong>Government Schemes</strong><br>
                        <small style="color: #666;">Learn about benefits & subsidies</small>
                    </div>
                </div>
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
    

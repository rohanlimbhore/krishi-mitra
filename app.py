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
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Sora', sans-serif !important;
        }

        /* ── Full page animated background ── */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, #0a4f3f, #166f4e, #1a9e5c, #38ef7d, #11998e, #0a4f3f);
            background-size: 500% 500%;
            animation: gradientBG 18s ease infinite;
            min-height: 100vh;
        }

        [data-testid="stAppViewContainer"] > .main {
            background: transparent !important;
        }

        @keyframes gradientBG {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Floating leaf particles overlay */
        [data-testid="stAppViewContainer"]::before {
            content: "🌿 🍃 🌱 🌾 🌿 🍃";
            position: fixed;
            top: -60px;
            left: 0;
            width: 100%;
            font-size: 28px;
            letter-spacing: 60px;
            opacity: 0.12;
            animation: floatLeaves 20s linear infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes floatLeaves {
            0%   { transform: translateY(0px) rotate(0deg); }
            100% { transform: translateY(110vh) rotate(360deg); }
        }

        /* ── Remove Streamlit default padding ── */
        .main .block-container {
            padding-top: 2.5rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 480px !important;
        }

        /* ── Glass Card: target the middle column ── */
        div[data-testid="column"]:nth-child(2) > div:first-child {
            background: rgba(255, 255, 255, 0.96) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 28px !important;
            padding: 2.5rem 2rem !important;
            box-shadow: 0 32px 64px -16px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.4) inset !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            animation: slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
            position: relative;
            z-index: 1;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(40px) scale(0.97); }
            to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px !important;
            background: #f0faf5 !important;
            border-radius: 14px !important;
            padding: 6px !important;
            border: 1px solid #d4ede3 !important;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 1 !important;
            border-radius: 10px !important;
            padding: 10px 16px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            color: #555 !important;
            transition: all 0.25s ease !important;
            background: transparent !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #0f8a72, #2dd47a) !important;
            color: white !important;
            box-shadow: 0 4px 16px rgba(17, 153, 142, 0.35) !important;
        }

        /* Hide default tab indicator underline */
        .stTabs [data-baseweb="tab-highlight"] {
            background: transparent !important;
            height: 0 !important;
        }

        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ── Inputs ── */
        div[data-testid="stTextInput"] input {
            border-radius: 14px !important;
            border: 2px solid #e2ede9 !important;
            padding: 14px 16px !important;
            font-size: 15px !important;
            font-family: 'Sora', sans-serif !important;
            transition: all 0.3s ease !important;
            background: #f8fdfb !important;
            color: #1a1a1a !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #11998e !important;
            background: white !important;
            box-shadow: 0 0 0 4px rgba(17, 153, 142, 0.12) !important;
            outline: none !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #b0c4bc !important;
        }

        div[data-testid="stTextInput"] label {
            font-weight: 600 !important;
            font-size: 13px !important;
            color: #2d4a3e !important;
            letter-spacing: 0.3px !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            width: 100% !important;
            border-radius: 14px !important;
            padding: 14px 20px !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            font-family: 'Sora', sans-serif !important;
            background: linear-gradient(135deg, #0f8a72 0%, #1db37a 50%, #38ef7d 100%) !important;
            background-size: 200% 200% !important;
            color: white !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            letter-spacing: 0.4px !important;
            text-transform: uppercase !important;
            box-shadow: 0 6px 20px rgba(17, 153, 142, 0.3) !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 30px rgba(17, 153, 142, 0.45) !important;
            background-position: right center !important;
        }

        .stButton > button:active {
            transform: translateY(-1px) !important;
        }

        /* ── Alerts ── */
        div[data-testid="stAlert"] {
            border-radius: 14px !important;
            border: none !important;
            font-family: 'Sora', sans-serif !important;
            font-size: 14px !important;
        }

        /* ── Hide Streamlit branding ── */
        #MainMenu { visibility: hidden; }
        footer     { visibility: hidden; }
        header     { visibility: hidden; }

        /* ── Spinner ── */
        div[data-testid="stSpinner"] {
            text-align: center;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(17,153,142,0.4); border-radius: 4px; }

        /* ── Logo animation ── */
        @keyframes bounce {
            0%, 100% { transform: translateY(0px) rotate(-3deg); }
            50%       { transform: translateY(-12px) rotate(3deg); }
        }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            50%       { transform: scale(1.25); }
        }

        @keyframes shimmer {
            0%   { background-position: -200% center; }
            100% { background-position: 200% center; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Center layout — middle column is the card
    col1, col2, col3 = st.columns([0.2, 2.6, 0.2])

    with col2:

        # ── Animated Logo Header ──
        st.markdown('''
            <div style="text-align:center; margin-bottom: 20px;">
                <div style="font-size:74px; display:inline-block; animation: bounce 2.5s ease-in-out infinite;">🌾</div>
                <h1 style="
                    font-size: 34px;
                    font-weight: 800;
                    margin: 4px 0 0 0;
                    background: linear-gradient(135deg, #0a4f3f, #11998e, #38ef7d);
                    background-size: 200% auto;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    animation: shimmer 3s linear infinite;
                    letter-spacing: -0.5px;
                ">Krishi Mitra</h1>
                <p style="color: #6b8f7e; font-size: 13.5px; margin-top: 6px; font-weight: 400; letter-spacing: 0.3px;">
                    Your Intelligent Farming Companion
                </p>
                <div style="width: 48px; height: 3px; background: linear-gradient(90deg, #11998e, #38ef7d); border-radius: 2px; margin: 12px auto 0;"></div>
            </div>
        ''', unsafe_allow_html=True)

        # ── Tabs ──
        tab1, tab2 = st.tabs(["🔐  Sign In", "📝  Create Account"])

        with tab1:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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
                st.markdown(
                    "<p style='color:#11998e; font-size:12.5px; margin-top:10px; cursor:pointer; font-weight:600;'>Forgot password?</p>",
                    unsafe_allow_html=True
                )

            with col_login:
                login_btn = st.button("Sign In →", type="primary", use_container_width=True)

            if login_btn:
                if login_email and login_password:
                    with st.spinner("Signing you in..."):
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
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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
                "📍 Village / District",
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

        # ── Divider ──
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="display:flex; align-items:center; gap:12px; margin: 8px 0 16px;">
                <div style="flex:1; height:1px; background: linear-gradient(90deg, transparent, #d4ede3);"></div>
                <span style="color:#a0bdb3; font-size:12px; font-weight:500; white-space:nowrap;">Why Krishi Mitra?</span>
                <div style="flex:1; height:1px; background: linear-gradient(90deg, #d4ede3, transparent);"></div>
            </div>
        """, unsafe_allow_html=True)

        # ── Feature Cards ──
        st.markdown('''
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px;">
                <div style="
                    background: linear-gradient(135deg, #f0fdf8, #e6f9ef);
                    padding: 16px 12px;
                    border-radius: 16px;
                    text-align: center;
                    border: 1px solid #c8edda;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size:30px; margin-bottom:6px;">🤖</div>
                    <div style="font-size:12px; font-weight:700; color:#1a4a35;">AI Assistant</div>
                    <div style="font-size:10px; color:#6b9c80; margin-top:2px;">Smart crop advice</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #f0fdf8, #e6f9ef);
                    padding: 16px 12px;
                    border-radius: 16px;
                    text-align: center;
                    border: 1px solid #c8edda;
                ">
                    <div style="font-size:30px; margin-bottom:6px;">📸</div>
                    <div style="font-size:12px; font-weight:700; color:#1a4a35;">Crop Scan</div>
                    <div style="font-size:10px; color:#6b9c80; margin-top:2px;">Disease detection</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #f0fdf8, #e6f9ef);
                    padding: 16px 12px;
                    border-radius: 16px;
                    text-align: center;
                    border: 1px solid #c8edda;
                ">
                    <div style="font-size:30px; margin-bottom:6px;">👥</div>
                    <div style="font-size:12px; font-weight:700; color:#1a4a35;">Community</div>
                    <div style="font-size:10px; color:#6b9c80; margin-top:2px;">Connect & share</div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #f0fdf8, #e6f9ef);
                    padding: 16px 12px;
                    border-radius: 16px;
                    text-align: center;
                    border: 1px solid #c8edda;
                ">
                    <div style="font-size:30px; margin-bottom:6px;">🏛️</div>
                    <div style="font-size:12px; font-weight:700; color:#1a4a35;">Govt Schemes</div>
                    <div style="font-size:10px; color:#6b9c80; margin-top:2px;">Latest subsidies</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

        # ── Footer ──
        st.markdown('''
            <div style="
                text-align: center;
                padding-top: 16px;
                border-top: 1px solid #e2ede9;
            ">
                <p style="color: #a0bdb3; font-size: 12px; margin: 0; line-height: 1.8;">
                    Made with <span style="color:#e74c3c; animation: heartbeat 1.5s infinite; display:inline-block;">❤️</span> for Indian Farmers<br>
                    <span style="font-weight:600; color:#6b9c80;">© 2026 Krishi Mitra</span>
                </p>
            </div>
        ''', unsafe_allow_html=True)


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

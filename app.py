"""
🌾 Krishi Mitra - Professional Farming App
"""

import streamlit as st
import sqlite3
import hashlib

# Page config
st.set_page_config(
    page_title="Krishi Mitra",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Database
DB_PATH = "krishi_mitra.db"

def init_user_db():
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
# FIXED PROFESSIONAL UI - No White Boxes
# =============================================================================

def show_login_page():
    
    # CSS that actually works - targets Streamlit's containers
    st.markdown("""
        <style>
        /* Import font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global font */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Gradient background on main app */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* REMOVE ALL DEFAULT CONTAINER STYLES */
        div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        div[data-testid="stVerticalBlock"] > div {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
            box-shadow: none !important;
        }
        
        /* Hide default streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container padding */
        .main .block-container {
            padding: 20px;
            max-width: 450px;
        }
        
        /* LOGO SECTION - Outside card */
        .logo-container {
            text-align: center;
            margin-bottom: 25px;
            color: white;
        }
        
        .logo-emoji {
            font-size: 60px;
            margin-bottom: 5px;
            display: block;
        }
        
        .logo-title {
            font-size: 26px;
            font-weight: 700;
            margin: 0;
            color: white;
        }
        
        .logo-subtitle {
            font-size: 13px;
            opacity: 0.9;
            margin-top: 3px;
            color: white;
        }
        
        /* MAIN CARD - Single white container */
        .login-card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        
        /* TABS - Clean style */
        .stTabs {
            margin-bottom: 20px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 5px;
            background: #f3f4f6;
            border-radius: 10px;
            padding: 4px;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            border-radius: 8px;
            padding: 10px;
            font-weight: 600;
            font-size: 13px;
            height: auto;
        }
        
        .stTabs [aria-selected="true"] {
            background: #667eea !important;
            color: white !important;
        }
        
        /* INPUT FIELDS - Remove containers */
        div[data-testid="stTextInput"] {
            margin-bottom: 12px !important;
        }
        
        div[data-testid="stTextInput"] > div {
            background: transparent !important;
            border: none !important;
        }
        
        div[data-testid="stTextInput"] input {
            border-radius: 10px;
            border: 1.5px solid #e5e7eb;
            padding: 12px 14px;
            font-size: 14px;
            background: #f9fafb;
            width: 100%;
        }
        
        div[data-testid="stTextInput"] input:focus {
            border-color: #667eea;
            background: white;
            outline: none;
        }
        
        /* BUTTON - Clean */
        .stButton {
            margin-top: 5px;
        }
        
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            padding: 12px;
            font-size: 15px;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
        }
        
        /* FORM CONTAINER - Remove extra padding */
        div[data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }
        
        /* FEATURES ROW */
        .features-row {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }
        
        .feature-box {
            text-align: center;
            flex: 1;
        }
        
        .feature-icon {
            font-size: 22px;
            margin-bottom: 4px;
        }
        
        .feature-name {
            font-size: 10px;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
        }
        
        /* FOOTER */
        .app-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
            font-size: 12px;
        }
        
        /* ALERTS - Clean */
        .stAlert {
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # LOGO - Outside card, centered
    st.markdown("""
        <div class="logo-container">
            <span class="logo-emoji">🌾</span>
            <h1 class="logo-title">Krishi Mitra</h1>
            <p class="logo-subtitle">Smart Farming Solutions</p>
        </div>
    """, unsafe_allow_html=True)
    
    # MAIN CARD START
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # TABS
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        # Use form for clean grouping
        with st.form("login_form", clear_on_submit=False):
            login_email = st.text_input(
                "Mobile/Email",
                placeholder="Enter mobile number or email",
                label_visibility="collapsed"
            )
            
            login_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                label_visibility="collapsed"
            )
            
            # Forgot password link
            st.markdown("<p style='text-align: right; margin: -5px 0 10px 0;'><span style='color: #667eea; font-size: 12px; cursor: pointer;'>Forgot password?</span></p>", 
                       unsafe_allow_html=True)
            
            submit_login = st.form_submit_button("Sign In →", use_container_width=True)
            
            if submit_login:
                if login_email and login_password:
                    success, result = login_user(login_email, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = result
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Please fill all fields")
    
    with tab2:
        with st.form("register_form", clear_on_submit=False):
            reg_name = st.text_input(
                "Full Name",
                placeholder="Your full name",
                label_visibility="collapsed"
            )
            
            reg_mobile = st.text_input(
                "Mobile",
                placeholder="10 digit mobile number",
                label_visibility="collapsed"
            )
            
            reg_location = st.text_input(
                "Location",
                placeholder="Village / District / State",
                label_visibility="collapsed"
            )
            
            reg_password = st.text_input(
                "Password",
                type="password",
                placeholder="Create password (min 6 chars)",
                label_visibility="collapsed"
            )
            
            submit_reg = st.form_submit_button("Create Account →", use_container_width=True)
            
            if submit_reg:
                if all([reg_name, reg_mobile, reg_location, reg_password]):
                    if len(reg_password) >= 6:
                        success, msg = register_user(reg_mobile, reg_password, reg_name, reg_location)
                        if success:
                            st.success("Account created! Please sign in.")
                        else:
                            st.error(msg)
                    else:
                        st.warning("Password too short")
                else:
                    st.warning("Please fill all fields")
    
    # FEATURES INSIDE CARD
    st.markdown("""
        <div class="features-row">
            <div class="feature-box">
                <div class="feature-icon">🤖</div>
                <div class="feature-name">AI Help</div>
            </div>
            <div class="feature-box">
                <div class="feature-icon">📸</div>
                <div class="feature-name">Scan</div>
            </div>
            <div class="feature-box">
                <div class="feature-icon">👥</div>
                <div class="feature-name">Community</div>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🏛️</div>
                <div class="feature-name">Schemes</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # CARD END
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FOOTER
    st.markdown("""
        <div class="app-footer">
            Made with ❤️ for Indian Farmers • 2026
        </div>
    """, unsafe_allow_html=True)

# Initialize
init_user_db()

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Route
if not st.session_state.logged_in:
    show_login_page()
else:
    from main_app import run_main_app
    run_main_app(st.session_state.user)
    

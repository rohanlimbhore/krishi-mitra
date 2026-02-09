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
    layout="wide",
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
        conn = sqlite3.connect(DB_PATH, check_safe_thread=False)
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
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, user
        else:
            return False, "Invalid credentials!"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Initialize database
init_user_db()

# =============================================================================
# SESSION STATE
# =============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "show_register" not in st.session_state:
    st.session_state.show_register = False

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown("""
<style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background-color: #F1F8E9;
        border-radius: 15px;
        border: 2px solid #4CAF50;
        margin-top: 50px;
    }
    .login-header {
        text-align: center;
        color: #2E7D32;
        font-size: 2rem;
        margin-bottom: 20px;
    }
    .login-input {
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
    }
    .switch-btn {
        background: none;
        border: none;
        color: #1565C0;
        text-decoration: underline;
    }
    .welcome-banner {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# LOGIN PAGE
# =============================================================================
def show_login():
    st.markdown('<div class="login-header">🌾 Krishi Mitra</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; margin-bottom:30px;">Your Intelligent Farming Companion</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        if not st.session_state.show_register:
            # LOGIN FORM
            st.subheader("🔐 Login")
            
            mobile_email = st.text_input(
                "Mobile Number or Email",
                placeholder="Enter mobile or email",
                key="login_mobile"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_pass"
            )
            
            if st.button("Login", type="primary"):
                if mobile_email and password:
                    success, result = login_user(mobile_email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = {
                            "id": result[0],
                            "mobile_email": result[1],
                            "farmer_name": result[3],
                            "location": result[4]
                        }
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Please fill all fields!")
            
            st.markdown("---")
            st.markdown("New farmer?")
            if st.button("Create Account", key="switch_to_register"):
                st.session_state.show_register = True
                st.rerun()
        
        else:
            # REGISTER FORM
            st.subheader("📝 Register")
            
            farmer_name = st.text_input("Your Full Name", placeholder="Enter your name")
            mobile_email = st.text_input(
                "Mobile Number or Email", 
                placeholder="Enter mobile or email (this will be your username)"
            )
            location = st.text_input("Your Village/Location", placeholder="Enter your location")
            password = st.text_input("Create Password", type="password", placeholder="Min 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Register", type="primary"):
                if not all([farmer_name, mobile_email, location, password]):
                    st.warning("Please fill all fields!")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters!")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    success, message = register_user(mobile_email, password, farmer_name, location)
                    if success:
                        st.success(message)
                        st.info("Please login now!")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(message)
            
            st.markdown("---")
            st.markdown("Already have account?")
            if st.button("Back to Login", key="switch_to_login"):
                st.session_state.show_register = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# LOGOUT FUNCTION
# =============================================================================
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# =============================================================================
# MAIN APP ROUTING
# =============================================================================
if not st.session_state.logged_in:
    show_login()
else:
    # Show welcome banner
    st.markdown(f"""
    <div class="welcome-banner">
        <h4>👋 Welcome, {st.session_state.user['farmer_name']}!</h4>
        <p>📍 {st.session_state.user['location']} | 📱 {st.session_state.user['mobile_email']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button in top right
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout"):
            logout()
    
    st.markdown("---")
    
    # Import and run main app
    from main_app import run_main_app
    run_main_app(st.session_state.user)
        

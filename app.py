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
        

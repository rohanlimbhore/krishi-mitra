"""
Database operations for Krishi Mitra using SQLite
"""

import sqlite3
import json
from datetime import datetime
from config import DB_PATH

def get_db_connection():
    """Create database connection."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Community Posts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            content TEXT NOT NULL,
            image_path TEXT,
            video_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    
    # Organic Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS organic_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity TEXT NOT NULL,
            location TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Conversation History Table (optional, for context)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# =============================================================================
# COMMUNITY POSTS OPERATIONS
# =============================================================================

def create_post(farmer_name, content, image_path=None, video_path=None):
    """Create a new community post."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO community_posts (farmer_name, content, image_path, video_path)
        VALUES (?, ?, ?, ?)
    ''', (farmer_name, content, image_path, video_path))
    
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def get_all_posts(limit=50, offset=0):
    """Retrieve all community posts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM community_posts 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    
    posts = cursor.fetchall()
    conn.close()
    return [dict(post) for post in posts]

# =============================================================================
# ORGANIC PRODUCTS OPERATIONS
# =============================================================================

def add_product(farmer_name, product_name, quantity, location, phone_number):
    """Add new organic product listing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO organic_products (farmer_name, product_name, quantity, location, phone_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (farmer_name, product_name, quantity, location, phone_number))
    
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id

def get_all_products(limit=100):
    """Retrieve all organic products."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM organic_products 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products]

def search_products(search_term):
    """Search products by name or location."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM organic_products 
        WHERE product_name LIKE ? OR location LIKE ? OR farmer_name LIKE ?
        ORDER BY created_at DESC
    ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products]
    # Add this function for user management
def create_user(mobile_email, password_hash, farmer_name, location):
    """Create new user account."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (mobile_email, password_hash, farmer_name, location)
            VALUES (?, ?, ?, ?)
        ''', (mobile_email, password_hash, farmer_name, location))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(mobile_email, password_hash):
    """Verify user login."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM users 
        WHERE mobile_email = ? AND password_hash = ?
    ''', (mobile_email, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    return user
    

# Initialize database on import
init_database()
      # Users Table - ADD THIS
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


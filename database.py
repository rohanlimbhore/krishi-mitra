"""
Database operations for Krishi Mitra
Supports both SQLite (local) and PostgreSQL (Supabase)
"""

import os
from datetime import datetime
from config import DATABASE_URL, DB_TYPE, DB_PATH

def get_db_connection():
    """Create database connection based on configuration."""
    if DB_TYPE == "postgresql":
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Fix: Use connect_timeout and options to force IPv4
        conn = psycopg2.connect(
            DATABASE_URL, 
            sslmode='require',
            connect_timeout=10
        )
        return conn
    else:
        # SQLite fallback
        import sqlite3
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
        


def init_database():
    """Initialize database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DB_TYPE == "postgresql":
        # PostgreSQL syntax
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_posts (
                id SERIAL PRIMARY KEY,
                farmer_name TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT,
                video_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS organic_products (
                id SERIAL PRIMARY KEY,
                farmer_name TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity TEXT NOT NULL,
                location TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id TEXT,
                role TEXT,
                content TEXT,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        # SQLite syntax
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

def create_post(farmer_name, content, image_path=None, video_path=None):
    """Create a new community post."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DB_TYPE == "postgresql":
        cursor.execute('''
            INSERT INTO community_posts (farmer_name, content, image_path, video_path)
            VALUES (%s, %s, %s, %s)
        ''', (farmer_name, content, image_path, video_path))
    else:
        cursor.execute('''
            INSERT INTO community_posts (farmer_name, content, image_path, video_path)
            VALUES (?, ?, ?, ?)
        ''', (farmer_name, content, image_path, video_path))
    
    conn.commit()
    
    if DB_TYPE == "postgresql":
        cursor.execute("SELECT LASTVAL()")
        post_id = cursor.fetchone()[0]
    else:
        post_id = cursor.lastrowid
    
    conn.close()
    return post_id

def get_all_posts(limit=50, offset=0):
    """Retrieve all community posts."""
    conn = get_db_connection()
    
    if DB_TYPE == "postgresql":
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM community_posts 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        ''', (limit, offset))
    else:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM community_posts 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
    
    posts = cursor.fetchall()
    conn.close()
    
    return [dict(post) for post in posts]

def add_product(farmer_name, product_name, quantity, location, phone_number):
    """Add new organic product listing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DB_TYPE == "postgresql":
        cursor.execute('''
            INSERT INTO organic_products (farmer_name, product_name, quantity, location, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        ''', (farmer_name, product_name, quantity, location, phone_number))
    else:
        cursor.execute('''
            INSERT INTO organic_products (farmer_name, product_name, quantity, location, phone_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (farmer_name, product_name, quantity, location, phone_number))
    
    conn.commit()
    
    if DB_TYPE == "postgresql":
        cursor.execute("SELECT LASTVAL()")
        product_id = cursor.fetchone()[0]
    else:
        product_id = cursor.lastrowid
    
    conn.close()
    return product_id

def get_all_products(limit=100):
    """Retrieve all organic products."""
    conn = get_db_connection()
    
    if DB_TYPE == "postgresql":
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM organic_products 
            ORDER BY created_at DESC 
            LIMIT %s
        ''', (limit,))
    else:
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
    
    search_pattern = f'%{search_term}%'
    
    if DB_TYPE == "postgresql":
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM organic_products 
            WHERE product_name ILIKE %s OR location ILIKE %s OR farmer_name ILIKE %s
            ORDER BY created_at DESC
        ''', (search_pattern, search_pattern, search_pattern))
    else:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM organic_products 
            WHERE product_name LIKE ? OR location LIKE ? OR farmer_name LIKE ?
            ORDER BY created_at DESC
        ''', (search_pattern, search_pattern, search_pattern))
    
    products = cursor.fetchall()
    conn.close()
    
    return [dict(product) for product in products]
def register_user(farmer_name, mobile_email, location, password_hash=None):
    """Register a new farmer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if DB_TYPE == "postgresql":
            cursor.execute('''
                INSERT INTO users (farmer_name, mobile_email, location, password_hash)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (mobile_email) DO NOTHING
            ''', (farmer_name, mobile_email, location, password_hash))
        else:
            cursor.execute('''
                INSERT OR IGNORE INTO users (farmer_name, mobile_email, location, password_hash)
                VALUES (?, ?, ?, ?)
            ''', (farmer_name, mobile_email, location, password_hash))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False
    finally:
        conn.close()

def record_login(mobile_email, ip_address=None, device_info=None):
    """Record user login."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update last_login in users table
        if DB_TYPE == "postgresql":
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE mobile_email = %s
            ''', (mobile_email,))
            
            # Get user_id
            cursor.execute('SELECT id FROM users WHERE mobile_email = %s', (mobile_email,))
            user = cursor.fetchone()
            
            if user:
                # Add to login_history
                cursor.execute('''
                    INSERT INTO login_history (user_id, ip_address, device_info)
                    VALUES (%s, %s, %s)
                ''', (user[0], ip_address, device_info))
        else:
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE mobile_email = ?
            ''', (mobile_email,))
            
            cursor.execute('SELECT id FROM users WHERE mobile_email = ?', (mobile_email,))
            user = cursor.fetchone()
            
            if user:
                cursor.execute('''
                    INSERT INTO login_history (user_id, ip_address, device_info)
                    VALUES (?, ?, ?)
                ''', (user[0], ip_address, device_info))
        
        conn.commit()
    except Exception as e:
        print(f"Error recording login: {e}")
    finally:
        conn.close()

def get_all_users():
    """Get all registered users."""
    conn = get_db_connection()
    
    if DB_TYPE == "postgresql":
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
    else:
        cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, farmer_name, mobile_email, location, created_at, last_login 
        FROM users 
        ORDER BY created_at DESC
    ''')
    
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]

def get_login_history(limit=100):
    """Get login history with user details."""
    conn = get_db_connection()
    
    if DB_TYPE == "postgresql":
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT lh.id, u.farmer_name, u.mobile_email, lh.login_time, lh.ip_address
            FROM login_history lh
            JOIN users u ON lh.user_id = u.id
            ORDER BY lh.login_time DESC
            LIMIT %s
        ''', (limit,))
    else:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT lh.id, u.farmer_name, u.mobile_email, lh.login_time, lh.ip_address
            FROM login_history lh
            JOIN users u ON lh.user_id = u.id
            ORDER BY lh.login_time DESC
            LIMIT ?
        ''', (limit,))
    
    history = cursor.fetchall()
    conn.close()
    
    return [dict(h) for h in history]
            

# Initialize database on import
init_database()
    # Users Table - Track registered farmers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            farmer_name TEXT NOT NULL,
            mobile_email TEXT UNIQUE NOT NULL,
            location TEXT,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Login History Table - Track every login
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            device_info TEXT
        )
    ''')

              

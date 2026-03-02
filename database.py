"""
Database operations for Krishi Mitra
Uses SQLite local database
"""

import sqlite3

DB_PATH = "krishi_mitra.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            mobile_email TEXT UNIQUE NOT NULL,
            location TEXT,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            device_info TEXT
        )
    ''')

    conn.commit()
    conn.close()


# --- Community Posts ---

def create_post(farmer_name, content, image_path=None, video_path=None):
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


# --- Organic Products ---

def add_product(farmer_name, product_name, quantity, location, phone_number):
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
    conn = get_db_connection()
    cursor = conn.cursor()
    search_pattern = f'%{search_term}%'
    cursor.execute('''
        SELECT * FROM organic_products 
        WHERE product_name LIKE ? OR location LIKE ? OR farmer_name LIKE ?
        ORDER BY created_at DESC
    ''', (search_pattern, search_pattern, search_pattern))
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products]


# --- User Management ---

def register_user(farmer_name, mobile_email, location, password_hash=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, farmer_name, mobile_email, location, created_at, last_login 
        FROM users ORDER BY created_at DESC
    ''')
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]


def get_login_history(limit=100):
    conn = get_db_connection()
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

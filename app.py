"""
Krishi Mitra - AI Farming Assistant (Fixed Version)
"""
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Krishi Mitra", page_icon="🌾", layout="wide")

# API Key Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        st.error("Add GEMINI_API_KEY in Streamlit Secrets!")
        st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Database Setup
DB_PATH = "krishi_mitra.db"
UPLOAD_DIR = "uploads"
os.makedirs(f"{UPLOAD_DIR}/images", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/videos", exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts 
                 (id INTEGER PRIMARY KEY, farmer_name TEXT, content TEXT, 
                  image_path TEXT, video_path TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, farmer_name TEXT, product_name TEXT, 
                  quantity TEXT, location TEXT, phone TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# AI Functions
def detect_lang(text):
    try:
        r = model.generate_content(f"Detect language of '{text}'. Reply only with: mr/hi/en/gu/ta/te/kn")
        return r.text.strip()[:2] if r.text.strip()[:2] in ['mr','hi','en','gu','ta','te','kn'] else 'en'
    except:
        return 'en'

def get_ai_response(query, lang):
    langs = {'mr':'Marathi','hi':'Hindi','en':'English','gu':'Gujarati','ta':'Tamil','te':'Telugu','kn':'Kannada'}
    prompt = f"""You are Krishi Mitra, expert farming advisor. Respond in {langs.get(lang,'English')}.
    Question: {query}
    Give practical, detailed advice for Indian farmers."""
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_crop(image, context, lang):
    langs = {'mr':'Marathi','hi':'Hindi','en':'English','gu':'Gujarati','ta':'Tamil','te':'Telugu','kn':'Kannada'}
    prompt = f"""Analyze this crop image. Respond in {langs.get(lang,'English')}.
    Provide: Crop ID, Health status, Diseases/Pests, Soil needs, Water needs, 
    Climate, Growth stages, Nutrients, Prevention, Best practices, Mistakes to avoid.
    Context: {context}"""
    try:
        return model.generate_content([prompt, image]).text
    except Exception as e:
        return f"Error: {str(e)}"

def get_crop_info(crop, lang):
    langs = {'mr':'Marathi','hi':'Hindi','en':'English','gu':'Gujarati','ta':'Tamil','te':'Telugu','kn':'Kannada'}
    prompt = f"""Give complete guide for {crop} in {langs.get(lang,'English')}.
    Include: Lifecycle, Season, Inputs per acre, Economics, Yield factors, Success tips."""
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

def get_scheme_info(query, lang):
    langs = {'mr':'Marathi','hi':'Hindi','en':'English','gu':'Gujarati','ta':'Tamil','te':'Telugu','kn':'Kannada'}
    prompt = f"""Explain Indian government farming scheme: {query}
    Respond in {langs.get(lang,'English')}. Include: Overview, Eligibility, Benefits, 
    Application process, Documents, Contact info."""
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

# Database Functions
def add_post(name, content, img_path=None, vid_path=None):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO posts (farmer_name, content, image_path, video_path) VALUES (?,?,?,?)",
              (name, content, img_path, vid_path))
    conn.commit()
    conn.close()

def get_posts():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_product(name, prod, qty, loc, phone):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO products (farmer_name, product_name, quantity, location, phone) VALUES (?,?,?,?,?)",
              (name, prod, qty, loc, phone))
    conn.commit()
    conn.close()

def get_products():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY created_at DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# UI Helper
def compress_img(file):
    try:
        img = Image.open(file)
        if img.mode in ('RGBA','LA','P'):
            bg = Image.new('RGB', img.size, (255,255,255))
            bg.paste(img, mask=img.split()[-1] if img.mode=='RGBA' else None)
            img = bg
        img.thumbnail((800,800))
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85)
        buf.seek(0)
        return Image.open(buf)
    except:
        return None

def save_file(file, folder):
    try:
        ext = file.name.split('.')[-1]
        fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(file.name)}.{ext}"
        path = os.path.join(UPLOAD_DIR, folder, fname)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        return path
    except:
        return None

# Sidebar
st.sidebar.title("🌾 Krishi Mitra")
page = st.sidebar.radio("Menu", ["Home","AI Assistant","Crop Diagnosis","Crop Guide","Community","Schemes","Market"])

# Pages
if page == "Home":
    st.title("🌾 Krishi Mitra")
    st.subheader("Your AI Farming Companion")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Languages", "7")
    col2.metric("Features", "6")
    col3.metric("Powered by", "Gemini AI")
    
    st.info("💡 Select a feature from the sidebar to get started!")
    st.markdown("""
    **Features:**
    - 💬 AI Assistant - Ask any farming question
    - 📸 Crop Diagnosis - Upload photos for analysis
    - 📚 Crop Guide - Complete crop information
    - 👥 Community - Connect with farmers
    - 🏛️ Schemes - Government scheme info
    - 🛒 Market - Buy/Sell organic products
    """)

elif page == "AI Assistant":
    st.header("💬 AI Farming Assistant")
    
    if "chat" not in st.session_state:
        st.session_state.chat = []
    
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    q = st.chat_input("Ask your farming question...")
    if q:
        st.session_state.chat.append({"role":"user","content":q})
        with st.chat_message("user"):
            st.write(q)
        
        with st.spinner("Thinking..."):
            lang = detect_lang(q)
            ans = get_ai_response(q, lang)
        
        st.session_state.chat.append({"role":"assistant","content":ans})
        with st.chat_message("assistant"):
            st.write(ans)
            st.caption(f"Language: {lang}")

elif page == "Crop Diagnosis":
    st.header("📸 Crop Diagnosis")
    
    col1, col2 = st.columns(2)
    with col1:
        file = st.file_uploader("Upload crop photo", type=['jpg','jpeg','png'])
        ctx = st.text_area("Additional context (optional)")
        analyze = st.button("Analyze", type="primary")
    
    with col2:
        if file:
            st.image(file, use_column_width=True)
    
    if analyze and file:
        with st.spinner("Analyzing..."):
            img = compress_img(file)
            if img:
                lang = detect_lang(ctx) if ctx else 'en'
                result = analyze_crop(img, ctx, lang)
                st.markdown("---")
                st.markdown(result)
            else:
                st.error("Could not process image")

elif page == "Crop Guide":
    st.header("📚 Crop Guide")
    crop = st.text_input("Enter crop name (e.g., Wheat, Tomato, Rice)")
    
    if st.button("Get Information", type="primary") and crop:
        with st.spinner("Generating..."):
            lang = detect_lang(crop)
            info = get_crop_info(crop, lang)
            st.markdown(info)

elif page == "Community":
    st.header("👥 Farmer Community")
    tab1, tab2 = st.tabs(["View Posts", "Create Post"])
    
    with tab1:
        posts = get_posts()
        if not posts:
            st.info("No posts yet. Be the first!")
        for p in posts:
            with st.container():
                st.write(f"**{p['farmer_name']}** - {p['created_at']}")
                st.write(p['content'])
                if p['image_path'] and os.path.exists(p['image_path']):
                    st.image(p['image_path'])
                if p['video_path'] and os.path.exists(p['video_path']):
                    st.video(p['video_path'])
                st.divider()
    
    with tab2:
        with st.form("post"):
            name = st.text_input("Your Name")
            content = st.text_area("Share your experience")
            img = st.file_uploader("Photo (optional)", type=['jpg','jpeg','png'])
            vid = st.file_uploader("Video (optional)", type=['mp4'])
            submit = st.form_submit_button("Post")
            
            if submit and name and content:
                img_path = save_file(img, "images") if img else None
                vid_path = save_file(vid, "videos") if vid else None
                add_post(name, content, img_path, vid_path)
                st.success("Posted!")
                st.rerun()

elif page == "Schemes":
    st.header("🏛️ Government Schemes")
    query = st.text_input("Ask about any scheme (e.g., PM-KISAN, Soil Health Card)")
    
    if st.button("Get Info", type="primary") and query:
        with st.spinner("Fetching..."):
            lang = detect_lang(query)
            info = get_scheme_info(query, lang)
            st.markdown(info)

elif page == "Market":
    st.header("🛒 Organic Market")
    tab1, tab2 = st.tabs(["Browse", "Sell Product"])
    
    with tab1:
        products = get_products()
        if not products:
            st.info("No products listed")
        for p in products:
            with st.container():
                st.markdown(f"""
                **{p['product_name']}**  
                Farmer: {p['farmer_name']} | Qty: {p['quantity']}  
                📍 {p['location']} | 📞 {p['phone']}
                """)
                st.divider()
    
    with tab2:
        with st.form("sell"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Your Name")
                prod = st.text_input("Product Name")
                qty = st.text_input("Quantity")
            with c2:
                loc = st.text_input("Location")
                phone = st.text_input("Phone")
            submit = st.form_submit_button("List Product")
            
            if submit and all([name, prod, qty, loc, phone]):
                add_product(name, prod, qty, loc, phone)
                st.success("Product listed!")
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ for Indian Farmers")
    

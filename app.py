import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="API Test", page_icon="🧪")

st.title("🧪 API Key Test")

# Get API key
api_key = None
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ API key found in secrets")
except:
    st.error("❌ API key NOT found in secrets!")
    st.info("Go to Streamlit Cloud → Settings → Secrets → Add GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        st.success("✅ API key configured with Google")
        
        # List models
        st.subheader("Available Models:")
        try:
            models = genai.list_models()
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    st.code(m.name)
        except Exception as e:
            st.error(f"Cannot list models: {e}")
        
        # Test generation
        st.subheader("Test AI Response:")
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say 'Hello Farmer' in Hindi")
            st.success("✅ AI is working!")
            st.write("Response:", response.text)
        except Exception as e:
            st.error(f"AI test failed: {e}")
            
    except Exception as e:
        st.error(f"Configuration error: {e}")

st.markdown("---")
st.info("After testing, restore your original app.py code")
    

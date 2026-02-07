import streamlit as st
import google.generativeai as genai

st.title("API Test")

# Get API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ API key found in secrets")
except:
    api_key = None
    st.error("❌ API key not found in secrets")

if api_key:
    try:
        genai.configure(api_key=api_key)
        st.success("✅ API key configured")
        
        # List available models
        st.subheader("Available Models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.write(f"- {m.name}")
        
        # Test simple generation
        st.subheader("Test Generation:")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello in Hindi")
        st.write("Response:", response.text)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

import streamlit as st

st.title("Krishi Mitra - API Test Mode")

# Test which page to show
page = st.sidebar.radio("Test", ["API Test", "Main App"])

if page == "API Test":
    import test_api
else:
    try:
        from main_app import run_main_app
        user = {"farmer_name": "Test User", "location": "Test", "mobile_email": "test@test.com"}
        run_main_app(user)
    except Exception as e:
        st.error(f"Main app error: {str(e)}")
      

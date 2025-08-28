import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv()

def test_setup():
    st.title("🧪 Legal AI Setup Test")
    
    # Test environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        st.success("✅ OpenAI API key found")
    else:
        st.error("❌ OpenAI API key not found or invalid")
    
    # Test OpenAI connection
    try:
        client = openai.OpenAI(api_key=api_key)
        st.success("✅ OpenAI client initialized")
    except Exception as e:
        st.error(f"❌ OpenAI client error: {str(e)}")
    
    st.info("🎉 Setup test complete!")

if __name__ == "__main__":
    test_setup()

import streamlit as st
import os
from dotenv import load_dotenv
from src.pdf_utils import extract_text_from_pdf
from src.style_analyzer import analyze_style, configure_genai
from src.content_generator import generate_content

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Style Mimic AI", page_icon="✍️", layout="wide")

st.title("✍️ Style Mimic AI")
st.markdown("Extract writing style from a PDF and generate new content in that style.")

# Sidebar for API Key
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        configure_genai(api_key)
        st.success("API Key configured!")
    else:
        st.warning("Please enter your Google Gemini API Key to proceed.")

# Main content
if api_key:
    uploaded_file = st.file_uploader("Upload a PDF file to analyze style", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)
        
        if text:
            st.success("Text extracted successfully!")
            
            if st.button("Analyze Style"):
                with st.spinner("Analyzing writing style..."):
                    style_profile = analyze_style(text)
                    st.session_state.style_profile = style_profile
            
            if 'style_profile' in st.session_state:
                st.subheader("Style Analysis Profile")
                st.info(st.session_state.style_profile)
                
                st.divider()
                st.subheader("Generate New Content")
                topic = st.text_input("Enter a topic for new content")
                
                if st.button("Generate Content"):
                    if topic:
                        with st.spinner("Generating content..."):
                            generated_content = generate_content(topic, st.session_state.style_profile)
                            st.session_state.generated_content = generated_content
                    else:
                        st.warning("Please enter a topic.")
                
                if 'generated_content' in st.session_state:
                    st.subheader("Generated Content")
                    st.markdown(st.session_state.generated_content)
                    
                    st.divider()
                    with st.spinner("Predicting engagement metrics..."):
                        from src.engagement_predictor import predict_engagement
                        metrics = predict_engagement(st.session_state.generated_content, topic)
                        st.subheader("🔮 Predicted Engagement Metrics")
                        st.info(metrics)
        else:
            st.error("Could not extract text from the PDF.")
else:
    st.info("Please configure your API key in the sidebar to start.")

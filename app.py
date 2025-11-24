import streamlit as st
import os
from dotenv import load_dotenv
from src.pdf_utils import extract_text_from_pdf
from src.style_analyzer import analyze_style, configure_genai
from src.content_generator import generate_content

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Style Mimic AI", page_icon="✍️", layout="wide")

# Add custom CSS for the share icons
st.markdown("""
<style>
    .share-icons {
        display: flex;
        gap: 15px;
        align-items: center;
        margin-bottom: 20px;
        padding: 10px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    .share-icon {
        font-size: 20px;
        cursor: pointer;
        padding: 8px 12px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .share-icon:hover {
        background-color: #e0e0e0;
        transform: scale(1.1);
    }
    .like-icon {
        color: #ff6b6b;
    }
    .copy-icon {
        color: #4CAF50;
    }
    .download-icon {
        color: #2196F3;
    }
</style>
""", unsafe_allow_html=True)

st.title("✍️ Style Mimic AI")
st.markdown("Extract writing style from a PDF and generate new content in that style.")

# Share icons section
st.markdown("""
<div class="share-icons">
    <span class="share-icon copy-icon" title="Copy Link">✔</span>
    <span class="share-icon copy-icon" title="Save">✔</span>
    <span class="share-icon like-icon" title="Like">❤️</span>
    <span style="margin-left: auto; font-weight: bold;">Share</span>
</div>
""", unsafe_allow_html=True)

# Alternative method using columns (simpler approach)
col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
with col1:
    if st.button("✔", help="Copy Link"):
        st.toast("Link copied to clipboard!")
with col2:
    if st.button("✔", help="Save"):
        st.toast("Content saved!")
with col3:
    if st.button("❤️", help="Like"):
        st.toast("Thank you for your feedback!")
with col4:
    st.markdown("**Share**")

st.markdown("---")  # Add a separator

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
                    
                    # Add share icons for generated content
                    st.markdown("""
                    <div class="share-icons">
                        <span class="share-icon copy-icon" title="Copy Content">✔</span>
                        <span class="share-icon download-icon" title="Download">✔</span>
                        <span class="share-icon like-icon" title="Like Content">❤️</span>
                        <span style="margin-left: auto; font-weight: bold;">Share Content</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(st.session_state.generated_content)
        else:
            st.error("Could not extract text from the PDF.")
else:
    st.info("Please configure your API key in the sidebar to start.")
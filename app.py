# import streamlit as st
# import os
# from dotenv import load_dotenv
# from src.pdf_utils import extract_text_from_pdf
# from src.style_analyzer import analyze_style, configure_genai
# from src.content_generator import generate_content

# # Load environment variables
# load_dotenv()

# st.set_page_config(page_title="Style Mimic AI", page_icon="✍️", layout="wide")

# st.title("✍️ Style Mimic AI")
# st.markdown("Extract writing style from a PDF and generate new content in that style.")

# # Sidebar for API Key
# with st.sidebar:
#     st.header("Configuration")
#     api_key = st.text_input("Enter Google Gemini API Key", type="password")
#     if not api_key:
#         api_key = os.getenv("GOOGLE_API_KEY")
    
#     if api_key:
#         configure_genai(api_key)
#         st.success("API Key configured!")
#     else:
#         st.warning("Please enter your Google Gemini API Key to proceed.")

# # Main content
# if api_key:
#     uploaded_file = st.file_uploader("Upload a PDF file to analyze style", type="pdf")

#     if uploaded_file is not None:
#         with st.spinner("Extracting text from PDF..."):
#             text = extract_text_from_pdf(uploaded_file)
        
#         if text:
#             st.success("Text extracted successfully!")
            
#             if st.button("Analyze Style"):
#                 with st.spinner("Analyzing writing style..."):
#                     style_profile = analyze_style(text)
#                     st.session_state.style_profile = style_profile
            
#             if 'style_profile' in st.session_state:
#                 st.subheader("Style Analysis Profile")
#                 st.info(st.session_state.style_profile)
                
#                 st.divider()
#                 st.subheader("Generate New Content")
#                 topic = st.text_input("Enter a topic for new content")
                
#                 if st.button("Generate Content"):
#                     if topic:
#                         with st.spinner("Generating content..."):
#                             generated_content = generate_content(topic, st.session_state.style_profile)
#                             st.session_state.generated_content = generated_content
#                     else:
#                         st.warning("Please enter a topic.")
                
#                 if 'generated_content' in st.session_state:
#                     st.subheader("Generated Content")
#                     st.markdown(st.session_state.generated_content)
#         else:
#             st.error("Could not extract text from the PDF.")
# else:
#     st.info("Please configure your API key in the sidebar to start.")



import streamlit as st
import os
from dotenv import load_dotenv
from src.pdf_utils import extract_text_from_pdf
from src.style_analyzer import analyze_style, configure_genai
from src.content_generator import generate_content

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Content Generator", page_icon="✍️", layout="wide")

st.title("✍️ Generate New Content")
st.markdown("Create new content based on your requirements using AI.")

# Load API key from .env file
api_key = os.getenv("GOOGLE_API_KEY")

# Configure GenAI if API key is available
if api_key:
    try:
        configure_genai(api_key)
        st.sidebar.success("✅ API Key loaded from .env file!")
    except Exception as e:
        st.sidebar.error(f"❌ Error configuring API: {e}")
else:
    st.sidebar.error("❌ GOOGLE_API_KEY not found in .env file")

# Sidebar instructions
with st.sidebar:
    st.header("Configuration")
    if api_key:
        st.success("✅ API Key loaded from .env file!")
    else:
        st.error("❌ GOOGLE_API_KEY not found in .env file")
    
    st.markdown("---")
    st.subheader("How to use:")
    st.markdown("""
    1. Ensure GOOGLE_API_KEY is in your .env file
    2. Enter your content topic
    3. Optional: Upload a PDF for style reference
    4. Click 'Generate Content'
    """)

# Main content area - ALWAYS VISIBLE
st.header("📝 Content Creation")

# Check if API key is available for functionality
if not api_key:
    st.error("""
    ## 🔧 Setup Required
    
    Please add your Google Gemini API key to the `.env` file:
    
    1. Create a `.env` file in your project root
    2. Add this line: `GOOGLE_API_KEY=your_actual_api_key_here`
    3. Restart the application
    
    Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)
    """)
    st.stop()

# If API key is available, show the main functionality
try:
    # Topic input
    topic = st.text_input(
        "**Enter your content topic:**",
        placeholder="e.g., The Future of Artificial Intelligence, Benefits of Healthy Eating, Digital Transformation..."
    )
    
    # Content options
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "**Content Type:**",
            ["Blog Post", "Article", "Essay", "Report", "Creative Writing", "Technical Document"],
            help="Select the type of content you want to generate"
        )
    
    with col2:
        content_length = st.selectbox(
            "**Content Length:**",
            ["Short (300-500 words)", "Medium (500-800 words)", "Long (800-1200 words)"],
            help="Choose the desired length of the generated content"
        )
    
    # Optional PDF upload section
    with st.expander("🎨 Optional: Apply Specific Writing Style from PDF", expanded=False):
        st.write("Upload a PDF document to extract and mimic its writing style:")
        uploaded_file = st.file_uploader(
            "Choose PDF file",
            type="pdf",
            help="Upload a document whose writing style you want to mimic",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.info(f"📄 File uploaded: {uploaded_file.name}")
            
            with st.spinner("Extracting text from PDF..."):
                text = extract_text_from_pdf(uploaded_file)
            
            if text and text.strip():
                st.success("✅ Text extracted successfully!")
                
                if st.button("Analyze Writing Style from PDF"):
                    with st.spinner("Analyzing writing style..."):
                        try:
                            style_profile = analyze_style(text)
                            st.session_state.style_profile = style_profile
                            st.success("🎭 Writing style analyzed and saved!")
                            
                            with st.expander("View Style Analysis"):
                                st.text_area("Style Profile", value=style_profile, height=200, label_visibility="collapsed")
                        except Exception as e:
                            st.error(f"Error analyzing style: {e}")
            else:
                st.error("❌ Could not extract text from the PDF. The file might be scanned or corrupted.")
    
    # Additional instructions
    additional_instructions = st.text_area(
        "**Additional Instructions (Optional):**",
        placeholder="Any specific requirements, key points to include, tone preferences, or special instructions...",
        height=100
    )
    
    # Generate button
    if st.button("🚀 Generate Content", type="primary", use_container_width=True):
        if not topic or not topic.strip():
            st.warning("⚠️ Please enter a topic for your content.")
        else:
            with st.spinner("🤖 Generating your content... This may take a few moments."):
                try:
                    # Prepare style profile
                    if 'style_profile' in st.session_state:
                        base_style = st.session_state.style_profile
                        style_source = "custom writing style"
                    else:
                        base_style = f"Professional {content_type.lower()} style"
                        style_source = "standard professional style"
                    
                    # Enhanced style instructions
                    enhanced_style = f"""
                    WRITING STYLE PROFILE:
                    {base_style}
                    
                    CONTENT REQUIREMENTS:
                    - Type: {content_type}
                    - Length: {content_length}
                    - Tone: Professional and engaging
                    - Structure: Well-organized with clear paragraphs
                    
                    TOPIC: {topic}
                    """
                    
                    # Add additional instructions if provided
                    if additional_instructions and additional_instructions.strip():
                        enhanced_style += f"\nADDITIONAL INSTRUCTIONS: {additional_instructions}"
                    
                    # Generate content
                    generated_content = generate_content(topic, enhanced_style)
                    
                    if generated_content and not generated_content.startswith("Error generating content:"):
                        st.session_state.generated_content = generated_content
                        st.session_state.generation_topic = topic
                        st.success(f"✅ Content generated successfully using {style_source}!")
                    else:
                        st.error(f"❌ Failed to generate content: {generated_content}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating content: {str(e)}")
    
    # Display generated content if available
    if 'generated_content' in st.session_state:
        st.divider()
        st.header("📄 Generated Content")
        
        if 'generation_topic' in st.session_state:
            st.subheader(f"Topic: {st.session_state.generation_topic}")
        
        # Content display with nice formatting
        st.markdown(st.session_state.generated_content)
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download as Text File",
                data=st.session_state.generated_content,
                file_name=f"generated_content_{topic.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 Generate New Content", use_container_width=True):
                for key in ['generated_content', 'generation_topic']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

except Exception as e:
    st.error(f"An error occurred in the application: {str(e)}")

# Footer
st.divider()
st.caption("Powered by Google Gemini AI • Generate high-quality content effortlessly")
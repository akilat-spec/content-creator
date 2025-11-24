import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def configure_genai(api_key):
    """Configures the Google Generative AI with the provided API key."""
    genai.configure(api_key=api_key)

def analyze_style(text):
    """
    Analyzes the writing style of the provided text using an LLM.

    Args:
        text: The text to analyze.

    Returns:
        str: The analysis of the writing style.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Analyze the writing style of the following text. 
        Please provide a detailed breakdown of the following elements:

        1.  **Tone**: (e.g., formal, friendly, conversational, technical, narrative, academic, marketing, etc.)
        2.  **Sentence Structure Patterns**: (e.g., simple, complex, compound, varied length, etc.)
        3.  **Vocabulary Level**: (e.g., simple, advanced, corporate, jargon-heavy, etc.)
        4.  **Formatting Style**: (e.g., bullet points, paragraphs, headings, storytelling, etc.)
        5.  **Rhythm and Flow**: (e.g., fast-paced, slow and deliberate, staccato, smooth, etc.)
        6.  **Typical Paragraph Length**: (e.g., short, medium, long)
        7.  **Recurring Stylistic Patterns**: (Any other notable observations)

        Text to analyze:
        {text[:10000]} 
        """ 
        # Truncating to 10000 chars to avoid token limits for this demo, 
        # though Gemini has a large context window.

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing style: {e}"

import google.generativeai as genai

def generate_content(topic, style_profile):
    """
    Generates new content based on a topic and a style profile.

    Args:
        topic: The topic for the new content.
        style_profile: The analyzed style profile to emulate.

    Returns:
        str: The generated content.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        You are a professional content creator. 
        Your task is to write a piece of content about the following topic: "{topic}".

        CRITICAL INSTRUCTION: You MUST strictly adhere to the following writing style profile:
        
        {style_profile}

        Ensure the tone, vocabulary, sentence structure, and formatting match the profile exactly.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

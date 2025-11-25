import google.generativeai as genai

def predict_engagement(content, topic):
    """
    Predicts engagement metrics for the given content using an LLM.

    Args:
        content: The generated content to analyze.
        topic: The topic of the content.

    Returns:
        str: Predicted engagement metrics.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Act as a social media analytics expert. 
        Analyze the following content about "{topic}" and predict potential engagement metrics.
        
        Content:
        {content[:5000]}

        Based on the quality, style, and topic relevance, estimate the following metrics:
        1. Estimated Reach (e.g., "10,000 - 15,000 views")
        2. Potential Likes (e.g., "500 - 800 likes")
        3. Potential Shares (e.g., "50 - 100 shares")
        4. Engagement Score (1-10) with a brief explanation.

        Provide the output in a clear, concise format suitable for display in a dashboard.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error predicting engagement: {e}"

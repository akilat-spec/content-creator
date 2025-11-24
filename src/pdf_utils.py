import pypdf

def extract_text_from_pdf(file_obj):
    """
    Extracts text from a PDF file object.

    Args:
        file_obj: A file-like object containing the PDF data.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        pdf_reader = pypdf.PdfReader(file_obj)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        return f"Error reading PDF: {e}"
    
    return text

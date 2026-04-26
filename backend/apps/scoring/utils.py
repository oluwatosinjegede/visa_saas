def extract_text_from_file(file):
    """
    Handles basic file decoding.
    Can be extended later for PDF/DOCX parsing.
    """
    try:
        return file.read().decode('utf-8', errors='ignore')
    except Exception:
        return ""
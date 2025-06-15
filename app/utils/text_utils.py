import re

def extract_specialty_from_response(response_text, language='ar'):
    patterns = {
        'ar': r'طبيب\s+([\u0600-\u06FF\s]+)',
        'fr': r'médecin\s+([a-zA-Zéèêàçâîôûùëïü\s]+)',
        'en': r'doctor\s+([a-zA-Z\s]+)'
    }
    pattern = patterns.get(language)
    if pattern:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    keywords = {
        'ar': 'طبيب',
        'fr': 'médecin',
        'en': 'doctor'
    }
    keyword = keywords.get(language)
    if keyword and keyword in response_text:
        return response_text.split(keyword)[-1].strip().split('.')[0]
    return None

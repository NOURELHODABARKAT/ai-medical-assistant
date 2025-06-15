from flask import Blueprint, request, jsonify
import google.generativeai as genai
import logging
from app.config import Config

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUPPORTED_LANGUAGES = {"ar", "fr", "en"}

SYSTEM_PROMPTS = {
    'ar': "أنت مساعد طبي محترف. مهمتك فقط تحديد التخصص الطبي المناسب حسب الأعراض المقدمة، بدون أي شرح إضافي ولا أية تفاصيل غير ضرورية.",
    'fr': "Vous êtes un assistant médical professionnel. Votre tâche consiste uniquement à indiquer la spécialité médicale appropriée selon les symptômes fournis, sans explications supplémentaires.",
    'en': "You are a professional medical assistant. Your task is to only recommend the appropriate medical specialty based on the provided symptoms, without any extra explanation."
}

USER_PROMPTS = {
    'ar': "أعاني من الأعراض التالية: {}. ما التخصص الطبي المناسب؟",
    'fr': "Je souffre des symptômes suivants : {}. Quelle spécialité médicale devrais-je consulter ?",
    'en': "I have the following symptoms: {}. What medical specialty should I consult?"
}

@api_bp.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400

        raw_symptoms = data.get('symptoms')
        if not raw_symptoms:
            return jsonify({'error': 'Missing "symptoms" field.'}), 400

        language = data.get('language', 'ar').lower()
        if language not in SUPPORTED_LANGUAGES:
            return jsonify({'error': f'Unsupported language. Supported: {", ".join(SUPPORTED_LANGUAGES)}.'}), 400

        # Normalize symptoms to a list
        if isinstance(raw_symptoms, str):
            symptoms = [s.strip() for s in raw_symptoms.replace("،", ",").split(",") if s.strip()]
        elif isinstance(raw_symptoms, list):
            symptoms = [str(s).strip() for s in raw_symptoms if str(s).strip()]
        else:
            return jsonify({'error': '"symptoms" must be a non-empty list of strings or a comma-separated string.'}), 400

        if not symptoms:
            return jsonify({'error': '"symptoms" must be a non-empty list of strings or a comma-separated string.'}), 400

        symptoms_list = ", ".join(symptoms)
        system_message = SYSTEM_PROMPTS[language]
        user_message = USER_PROMPTS[language].format(symptoms_list)

        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro" if you have access

        prompt = f"{system_message}\n{user_message}"

        response = model.generate_content(prompt)
        recommendation = response.text.strip()

        return jsonify({'recommendation': recommendation})

    except Exception as e:
        logger.exception("Unexpected error occurred during diagnosis.")
        return jsonify({'error': 'Internal server error. Please try again later.'}), 500
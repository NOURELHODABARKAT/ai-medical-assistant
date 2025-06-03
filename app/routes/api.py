from flask import Blueprint, request, jsonify
import openai
from app.config import Config

api_bp = Blueprint('api', __name__)
openai.api_key = Config.OPENAI_API_KEY

@api_bp.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    language = data.get('language', 'ar')  

    if not symptoms:
        return jsonify({'error': 'يرجى إدخال الأعراض'}), 400

    symptoms_list = ", ".join(symptoms)

    
    system_prompts = {
        'ar': "أنت مساعد طبي محترف. قم بتحديد التخصص الطبي المناسب حسب الأعراض المقدمة، دون أي شرح إضافي.",
        'fr': "Vous êtes un assistant médical professionnel. Indiquez uniquement la spécialité médicale appropriée selon les symptômes donnés.",
        'en': "You are a professional medical assistant. Only recommend the appropriate medical specialty based on the symptoms provided."
    }

    user_prompts = {
        'ar': f"أعاني من الأعراض التالية: {symptoms_list}. ما التخصص الطبي المناسب؟",
        'fr': f"Je souffre des symptômes suivants : {symptoms_list}. Quelle est la spécialité médicale appropriée ?",
        'en': f"I have the following symptoms: {symptoms_list}. What is the appropriate medical specialty?"
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompts.get(language, system_prompts['ar'])},
                {"role": "user", "content": user_prompts.get(language, user_prompts['ar'])}
            ],
            temperature=0.2
        )

        diagnosis = response["choices"][0]["message"]["content"]
        return jsonify({'specialty': diagnosis.strip()})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

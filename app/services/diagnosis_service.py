import json, os, logging, re
from html import escape
import redis
from flask import jsonify
from app.config import Config
import google.generativeai as genai
from app.utils.geo_utils import haversine
from app.utils.text_utils import extract_specialty_from_response

logger = logging.getLogger(__name__)
redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'), decode_responses=True)

STEPS = {
    'ar': [
        "ما هو تاريخ ميلادك؟",
        "ما هي الأعراض التي تعاني منها حاليًا؟",
        "متى بدأت هذه الأعراض؟ وكيف تطورت مع مرور الوقت؟",
        "هل زرت طبيبًا من أجل هذه الأعراض؟ وهل تناولت أي دواء؟",
        "هل تعاني من أمراض مزمنة أو أجريت عمليات جراحية سابقًا؟",
        "هل تتناول أي أدوية بشكل دائم؟",
        "هل لدى أحد أفراد عائلتك أمراض مزمنة أو وراثية؟",
        "ما هو نمط حياتك اليومي؟ هل تعمل؟ هل تمارس الرياضة؟ هل تدخن؟",
        "أين تسكن؟ هل تعيش في بيئة ملوثة أو فيها ظروف خاصة؟",
        "هل يوجد صلة قرابة بين والديك؟"
    ],
    'fr': [
        "Quelle est votre date de naissance ?",
        "Quels sont les symptômes que vous ressentez actuellement ?",
        "Quand vos symptômes ont-ils commencé ? Et comment ont-ils évolué ?",
        "Avez-vous consulté un médecin pour ces symptômes ? Avez-vous pris des médicaments ?",
        "Souffrez-vous de maladies chroniques ou avez-vous subi des opérations chirurgicales ?",
        "Prenez-vous des médicaments de façon régulière ?",
        "Des membres de votre famille souffrent-ils de maladies chroniques ou héréditaires ?",
        "Quel est votre mode de vie ? Travaillez-vous ? Faites-vous du sport ? Fumez-vous ?",
        "Où habitez-vous ? Vivez-vous dans un environnement particulier ou pollué ?",
        "Y a-t-il un lien de parenté entre vos parents ?"
    ],
    'en': [
        "What is your date of birth?",
        "What symptoms are you currently experiencing?",
        "When did your symptoms start? How have they progressed over time?",
        "Have you seen a doctor for these symptoms? Did you take any medication?",
        "Do you suffer from any chronic conditions or have you had surgeries before?",
        "Are you currently on any regular medications?",
        "Do any of your family members have chronic or hereditary diseases?",
        "What is your lifestyle like? Do you work? Do you exercise? Do you smoke?",
        "Where do you live? Do you live in any particular or polluted environment?",
        "Is there any consanguinity between your parents?"
    ]
}

SYSTEM_PROMPTS = {
    'ar': "أنت مساعد طبي محترف تتعامل مع مستخدم جزائري. اسأل المريض عن تاريخه الصحي خطوة بخطوة، ثم وجّه المريض إلى الطبيب المختص المناسب حسب جميع المعلومات المقدمة فقط، بدون شرح إضافي.",
    'fr': "Vous êtes un assistant médical professionnel pour un utilisateur algérien. Posez des questions sur l'historique médical du patient étape par étape, puis orientez le patient vers le médecin spécialiste approprié en fonction des informations fournies uniquement, sans explication supplémentaire.",
    'en': "You are a professional medical assistant for an Algerian user. Ask the patient about their medical history step by step, then direct the patient to the appropriate specialist doctor based only on the provided information, with no additional explanation."
}

def build_diagnosis_prompt(answers: list, questions: list, lang: str) -> str:
    formatted = "\n".join(f"{questions[i]} {answers[i]}" for i in range(len(answers)))
    system_instruction = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS['ar'])
    return f"{system_instruction}\n{formatted}"

def load_doctors_by_specialty(specialty):
    path = os.path.join(os.path.dirname(__file__), '../../data/doctors.json')
    with open(path, 'r', encoding='utf-8') as file:
        doctors = json.load(file)
    return [doc for doc in doctors if specialty in doc['specialty']]

def sort_doctors_by_distance(user_lat, user_lon, doctors):
    for doc in doctors:
        doc['distance'] = round(haversine(user_lat, user_lon, doc['lat'], doc['lon']), 2)
    return sorted(doctors, key=lambda d: d['distance'])

def handle_diagnosis(request, session):
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'Invalid or missing JSON data'}), 400

        session_id = data.get('session_id')
        language = data.get('language', 'ar')
        answer = escape(data.get('answer', '').strip())
        supported_languages = ['ar', 'fr', 'en']
        if language not in supported_languages:
            return jsonify({'error': 'Unsupported language'}), 400

        if 'user' not in session:
            return jsonify({'error': 'Unauthorized'}), 401

        step_questions = STEPS.get(language)
        if not step_questions:
            return jsonify({'error': 'Unsupported language'}), 400

        session_data_json = redis_client.get(session_id)
        session_data = json.loads(session_data_json) if session_data_json else {'step': 0, 'answers': []}

        if session_data['step'] > 0 and answer:
            session_data['answers'].append(answer)

        if session_data['step'] == len(step_questions):
            prompt = build_diagnosis_prompt(session_data['answers'], step_questions, language)
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                model = genai.GenerativeModel(Config.GEMINI_MODEL_NAME)
                response = model.generate_content(prompt)
                recommendation = response.text.strip()
            except Exception as e:
                logger.exception(f"Gemini API error: {str(e)}")
                return jsonify({'error': 'Failed to process diagnosis'}), 500

            user_lat = data.get('lat')
            user_lon = data.get('lon')
            specialty = extract_specialty_from_response(recommendation, language)
            doctors = []
            if specialty and user_lat and user_lon:
                doctors = load_doctors_by_specialty(specialty)
                doctors = sort_doctors_by_distance(float(user_lat), float(user_lon), doctors)
                doctors = doctors[:3]

            redis_client.delete(session_id)
            return jsonify({
                'recommendation': recommendation,
                'specialty': specialty,
                'doctors': doctors,
                'done': True
            })

        else:
            question = step_questions[session_data['step']]
            session_data['step'] += 1
            redis_client.set(session_id, json.dumps(session_data))
            return jsonify({'question': question, 'done': False})

    except Exception as e:
        logger.exception("Unexpected error in interactive diagnosis.")
        return jsonify({'error': 'Internal server error'}), 500
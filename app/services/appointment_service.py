from app.firebase_setup import db
from datetime import datetime
import uuid

def is_duplicate_appointment(user_email, date, time):
    existing = db.collection('appointments')\
        .where('user_email', '==', user_email)\
        .where('date', '==', date)\
        .where('time', '==', time)\
        .get()
    return len(existing) > 0

def create_appointment_record(user_email, doctor, date, time, note):
    appointment_id = str(uuid.uuid4())
    appointment = {
        'id': appointment_id,
        'user_email': user_email,
        'doctor': doctor,
        'date': date,
        'time': time,
        'note': note,
        'created_at': datetime.utcnow().isoformat()
    }
    db.collection('appointments').document(appointment_id).set(appointment)
    return appointment
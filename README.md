# 🩺 AI Medical Assistant

A multilingual (Arabic, French, English) AI-powered medical assistant built with Flask and Google Gemini. It conducts an interactive step-by-step health diagnosis and recommends the appropriate medical specialty and nearby doctors based on user input and location.

---

## ✨ Features

- 💬 Multilingual support (AR, FR, EN)
- 🧠 Smart medical specialty recommendation using Google Gemini
- 📍 Nearest doctor suggestion based on user location
- 🧾 Session tracking using Redis
- 🛡️ Rate limiting to prevent abuse (Flask-Limiter)

---

## 🛠️ Tech Stack

- Python 3 / Flask
- Google Generative AI (Gemini API)
- Redis
- Flask-Limiter
- JSON data for doctor list
- Haversine formula for distance calculation

---

## 🚀 Installation

```bash
git clone https://github.com/NOURELHODABARKAT/ai-medical-assistant.git
cd ai-medical-assistant
python3 -m venv venv
source venv/bin/activate   # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
## Environment Setup
Create a .env file or set the following environment variables:

env
Copy
Edit
REDIS_URL=redis://localhost:6379
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_MODEL_NAME=gemini-1.5-flash
Make sure Redis is running locally or via Redis Cloud.
## Usage
✅ Main Endpoint
POST /api/diagnose

Example Request Payload:
json
Copy
Edit
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "language": "en",
  "answer": "I've had chest pain for the past two days.",
  "lat": 36.75,
  "lon": 3.06
}
Example Response:
During interaction:

json
Copy
Edit
{ "question": "What symptoms are you currently experiencing?", "done": false }
When complete:

json
Copy
Edit
{
  "recommendation": "You should see a cardiologist.",
  "specialty": "Cardiology",
  "doctors": [
    {
      "name": "Dr. Amina Yacine",
      "specialty": "Cardiology",
      "lat": 36.76,
      "lon": 3.05,
      "distance": 1.2
    }
  ],
  "done": true
}
esting
Generate a session_id using uuid.uuid4()

Use Postman or curl to simulate the flow

Redis is used to manage conversation state

🤝 Contributing
Contributions are welcome!
Feel free to:

Fork the repository

Create a new branch

Submit a pull request with your improvements

📜 License
MIT License. Open source and free to use.

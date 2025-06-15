
# 🧠 AI Medical Assistant (Flask)

A secure, multilingual medical assistant web app built with Flask.  
Users can register, verify emails, log in via email or Google, and book medical appointments.  
Powered by Firebase, secured with JWT, and integrated with SendGrid for email notifications.

---

## 📦 Features

- ✅ User registration with email verification via SendGrid  
- 🔐 Secure login with JWT-based authentication  
- 🟢 Google OAuth2 login  
- 📅 Appointment creation with email confirmation  
- 🔎 View personal or doctor-specific appointments  
- 🌍 Multilingual support (Arabic, English, French) – (planned)  
- ☁️ Firebase for database  
- 🧪 Ready for testing & documentation

---

## 🗂️ Project Structure

```

app/
├── routes/
│   ├── auth.py                # Registration, login, OAuth
│   └── appointments.py        # Appointment creation & retrieval
├── services/
│   └── mail\_service.py        # SendGrid email helpers
├── utils/
│   └── jwt\_utils.py           # JWT encode/decode + decorator
├── firebase\_setup.py          # Firestore connection setup
├── config.py                  # App configuration and API keys
tests/
└── test\_auth.py, test\_appointments.py (to be added)

````

---

## 🚀 How to Run Locally

1. **Clone the repo:**

```bash
git clone https://github.com/NOURELHODABARKAT/ai-medical-assistant.git
cd ai-medical-assistant
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set environment variables (create a `.env` file):**

```
SENDGRID_API_KEY=your_sendgrid_api_key
SECRET_KEY=your_flask_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

4. **Run the app:**

```bash
flask run
```

Access the app at: `http://localhost:5000`

---

## 🔐 Authentication

* JWT token is issued at login and stored in an HTTP-only cookie.
* For protected routes, token is validated using `@jwt_required`.
* Google login supported using `flask-oauthlib`.

---

## 📮 Email Sending

Emails are sent using [SendGrid](https://sendgrid.com/):

* 📧 Email verification after registration
* 📅 Appointment confirmation upon creation

---

## 📬 API Endpoints

### 🔑 Auth Routes

| Method | Endpoint                      | Description                  |
| ------ | ----------------------------- | ---------------------------- |
| POST   | `/auth/register`              | Register new user            |
| GET    | `/auth/verify-email/<token>`  | Verify email with token      |
| POST   | `/auth/login`                 | Log in with email & password |
| GET    | `/auth/google-login`          | Google OAuth login redirect  |
| GET    | `/auth/google-login/callback` | Google OAuth callback        |
| POST   | `/auth/logout`                | Log out & remove session     |

### 📅 Appointment Routes

| Method | Endpoint                              | Description                            |
| ------ | ------------------------------------- | -------------------------------------- |
| POST   | `/appointments`                       | Create a new appointment               |
| GET    | `/appointments`                       | Get current user’s appointments        |
| GET    | `/appointments/by-doctor/<doctor_id>` | Get appointments for a specific doctor |

---

## ✅ Tests

🧪 Unit tests are being added under `/tests` using `pytest`.

---

## 📄 License

This project is licensed under the **MIT License**.
Made with ❤️ by [@NOURELHODABARKAT](https://github.com/NOURELHODABARKAT)


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_verification_email(to_email, token):
    """
    Sends a verification email using SendGrid.
    """
    verification_link = f"http://localhost:5000/auth/verify-email/{token}"  #
    message = Mail(
        from_email='medX@gmail.com', 
        to_emails=to_email,
        subject='Email Verification',
        html_content=f'<p>Click the link below to verify your email:</p><a href="{verification_link}">Verify Email</a>'
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
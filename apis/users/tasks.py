from .utils import send_email
from core.celery import app
from django.template.loader import get_template
from core.settings import SENDER_EMAIL


@app.task()
def send_password_reset_mail(user_data, email_subject):
    html_template = get_template("emails/request_password_reset.html")
    html_alternative = html_template.render(user_data)
    send_email(email_subject, SENDER_EMAIL, html_alternative, user_data["email"])
    return "Password Reset Mail Sent."

from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_response_email(message):
    subject = f"Ответ на вашу заявку: {message.subject}"
    body = render_to_string('emails/response_email.txt', {
        'message': message,
    })

    send_mail(
        subject,
        body,
        'noreply@yourdomain.com',  # Замените на ваш реальный email
        [message.email],
        fail_silently=False,
    )
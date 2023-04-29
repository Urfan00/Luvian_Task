from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_activation_email(email, activation_link):
    print(email)
    subject = 'Activate your account'
    message = f'Please click the following link to activate your account: {activation_link}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, message, from_email, to_email)

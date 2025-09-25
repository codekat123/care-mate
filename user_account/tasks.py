from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@shared_task
def send_reset_email(subject, message, from_email, recipient_list, html_message=None):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=html_message
    )

@shared_task
def send_validation_email(domain,protocal,uid,token,name,user_email):
    subject = 'please active your email'
    activation_link = f"{protocal}://{domain}{reverse('user_account:verify_email',args=[token,uid])}"
    context = {
        'name':name,
        'link':activation_link,
    }
    message = render_to_string('user_account/activation.html',context)
    mail = EmailMultiAlternatives(subject,message,settings.DEFAULT_FROM_EMAIL,user_email)
    mail.attach_alternative(message,'text/html')
    mail.send()
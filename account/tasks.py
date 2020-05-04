from celery import shared_task

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from account.activation_tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import JsonResponse

from datetime import datetime

from account.models import Account


@shared_task
def send_email(current_site, account_id, to_email, template):

    if current_site is None or account_id is None or to_email is None or template is None:
        return False

    account_obj = Account.objects.get(id=account_id)

    mail_subject = 'Activate your account.'
    message = render_to_string(template, {
        'account': account_obj,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(account_obj.id)),
        'token': account_activation_token.make_token(account_obj)
    })

    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()

@shared_task
def remove_unactive_accounts():
    qs = Account.objects.filter(is_active=False)
    today = datetime.today()

    for acc in qs:
        delta = today - acc.date_joined.replace(tzinfo=None)
        if delta.days >= 1:
            Account.objects.get(email=acc.email).delete()

    return True
from django.core.mail import send_mail
from celery import shared_task
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def some_task(*args, **kwargs):
    send_mail("subject", "message", "apptestbis@gmail.com", ["adrien.gutleben@gmail.com"])
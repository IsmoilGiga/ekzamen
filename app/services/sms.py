import logging

import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class SmsError(APIException):
    status_code = 503
    default_detail = "SMS yuborib bo'lmadi. Birozdan keyin urinib ko'ring."


def send_sms(phone, code):
    if settings.SMS_BACKEND == "console":
        print(f"[SMS] {phone} -> Tasdiqlash kodingiz: {code}")
    else:
        _eskiz(phone, code)
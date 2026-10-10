import random

from rest_framework.serializers import ValidationError

from app.models import PhoneCode
from app.services.sms import send_sms

ERROR = "Kod topilmadi, muddati tugagan yoki urinishlar tugagan"
NOT_CONFIRMED = "Avval kodni tasdiqlang yoki kod muddati tugagan"


def send_verification_code(user):
    code = str(random.randint(100000, 999999))    # 6 xonali kod

    # faqat oxirgi kod ishlaydi
    PhoneCode.objects.filter(user=user).delete()
    PhoneCode.objects.create(user=user, code=code)

    send_sms(user.phone, code)


def confirm_code(user, code):
    record = PhoneCode.objects.filter(user=user).first()

    if record is None or record.is_expired():
        raise ValidationError({"detail": ERROR})
    if record.attempts >= PhoneCode.MAX_ATTEMPTS:
        raise ValidationError({"detail": ERROR})

    if record.code != code:
        record.attempts += 1
        record.save()
        raise ValidationError({"detail": "Kod noto'g'ri"})

    record.is_confirmed = True
    record.save()


def finish_code(user):
    record = PhoneCode.objects.filter(
        user=user, is_confirmed=True
    ).first()

    if record is None or record.is_expired():
        raise ValidationError({"detail": NOT_CONFIRMED})

    record.delete()
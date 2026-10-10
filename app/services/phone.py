import re

from rest_framework.serializers import ValidationError


def normalize_phone(raw):
    digits = re.sub(r"\D", "", str(raw))     # faqat raqamlar qoladi

    if len(digits) == 9:                     # 901234567 -> 998901234567
        digits = "998" + digits

    if not re.fullmatch(r"998\d{9}", digits):
        raise ValidationError("Raqam +998 XX XXX XX XX ko'rinishida bo'lsin")
    return digits
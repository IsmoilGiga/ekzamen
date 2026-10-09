from rest_framework.generics import CreateAPIView
from app.models import EmailVerification, CustomUser
from app.serializers import UserRegisterSerializer, VerifyPhoneSerializer, ResendCodeSerializer, \
    ForgotPasswordSerializer, ConfirmPasswordSerializer, ResetPasswordSerializer
from app.services import send_verification_code, confirm_code, finish_code
from datetime import timedelta, timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.services.pre_token import get_user, make_pre_token


from app.services import send_verification_code, confirm_code, finish_code
from app.services.pre_token import make_pre_token, get_user
from app.services.sms import SmsError
from app.models import PhoneCode


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            send_verification_code(user)
        except SmsError:
            user.delete()
            raise
        return Response(
            {"phone": user.phone, "pre_token": make_pre_token(user.id)},
            status=201,
        )


class VerifyPhoneView(generics.GenericAPIView):
    serializer_class = VerifyPhoneSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_user(data["pre_token"])
        confirm_code(user, data["code"])     # 1. tasdiqla
        user.is_active = True                # 2. ishingni qil
        user.save()
        finish_code(user)                    # 3. yop
        return Response(
            {"detail": "Raqam tasdiqlandi. Endi login qiling."}
        )



RESEND_INTERVAL = timedelta(seconds=60)


class ResendCodeView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(serializer.validated_data["pre_token"])

        record = PhoneCode.objects.filter(user=user).first()
        now = timezone.now()
        if record and now - record.created_at < RESEND_INTERVAL:
            return Response(
                {"detail": "1 daqiqada faqat 1 marta"}, status=429
            )

        send_verification_code(user)
        # yangi pre_token — yana 30 daqiqa
        return Response({"pre_token": make_pre_token(user.id)})

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        user = CustomUser.objects.filter(phone=phone, is_active=True).first()
        if user:
            send_verification_code(user)   # register'dagi funksiya

        # raqam yo'q bo'lsa ham javob bir xil (user_id=0)
        user_id = user.id if user else 0
        return Response({"pre_token": make_pre_token(user_id)})

class ConfirmPasswordView(generics.GenericAPIView):
    serializer_class = ConfirmPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_user(data["pre_token"])
        confirm_code(user, data["code"])
        return Response({"detail": "Kod to'g'ri. Yangi parol kiriting."})

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_user(data["pre_token"])
        finish_code(user)          # kod tasdiqlanmagan bo'lsa — 400
        user.set_password(data["new_password"])
        user.save()
        return Response({"detail": "Parol yangilandi."})
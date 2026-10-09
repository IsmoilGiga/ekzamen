from rest_framework import serializers

from app.models import CustomUser, Product
from app.services.phone import normalize_phone


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        return normalize_phone(value)

class ConfirmPasswordSerializer(serializers.Serializer):
    pre_token = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)

class CustomUserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "email", "is_active", "date_joined",
        ]
        read_only_fields = fields

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "is_active"]


class ResendCodeSerializer(serializers.Serializer):
    pre_token = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    pre_token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Parollar bir xil emas"}
            )
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)   # "+998 90 123 45 67" ham sig'sin

    class Meta:
        model = CustomUser
        fields = ["id", "phone", "first_name", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def validate_phone(self, value):
        phone = normalize_phone(value)
        if CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Bu raqam band")
        return phone

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class VerifyPhoneSerializer(serializers.Serializer):
    pre_token = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)


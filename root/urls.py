from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from app.views import (
    RegisterAPIView,
    VerifyEmailView,
)
from app.views.auth import ResendCodeView, ForgotPasswordView, ConfirmPasswordView, ResetPasswordView

schema_view = get_schema_view(
    openapi.Info(
        title="p18",
        default_version="v1",
        description="dumbular",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("admin/", admin.site.urls),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("confirm-password/", ConfirmPasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("register/", RegisterAPIView.as_view()),
    path("verify-email/", VerifyEmailView.as_view()),
    path("resend-code/", ResendCodeView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()),

    path("swagger/",schema_view.with_ui("swagger", cache_timeout=0),name="schema-swagger-ui",),
]
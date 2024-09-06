from .views import *

from django.urls import path

urlpatterns=[
    path("register/" ,UserRegistration.as_view(),name="UserCreation"),
    path("login/" ,UserLogin.as_view(),name="UserAuth"),
    path("otp/" ,VerifyOTPView.as_view(),name="OTP"),
    path("verify/" ,VerifyToken.as_view(),name="Token"),
            ]
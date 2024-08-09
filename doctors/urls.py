from .views import *

from django.urls import path

urlpatterns=[
    path("category/" ,DoctorsCategories.as_view(),name="DoctorCategoryCreation"),
    path("register/" ,DoctorRegistration.as_view(),name="DoctorRegistration"),
    path("login/" ,DoctorLogin.as_view(),name="DoctorLogin"),
    path("otp/" ,VerifyDoctorOTPView.as_view(),name="DoctorOTP"),
            ]
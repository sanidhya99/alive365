from .views import *

from django.urls import path

urlpatterns=[
    path("category/" ,DoctorsCategories.as_view(),name="DoctorCategoryCreation"),
    path("register/" ,DoctorRegistration.as_view(),name="DoctorRegistration"),
    path("login/" ,DoctorLogin.as_view(),name="DoctorLogin"),
    path("otp/" ,VerifyDoctorOTPView.as_view(),name="DoctorOTP"),
    path("top/" , GetFamousDoctors.as_view(),name="FamousDoctors"),
    path("list/" , GetDoctors.as_view(),name="GetDoctors"),
    path("appoitments/" , GetDateWiseAppointments.as_view(),name="GetDateWiseAppointment"),
    path('slots/', DoctorTimeSlotView.as_view(), name='DoctorTimeSlots'),
    path('alter/<int:id>/', EditDoctor.as_view(), name='DoctorAlter'),
    path('get/<int:id>/', GetDoctor.as_view(), name='DoctorGet'),
    path('analytics/', GetAnalytics.as_view(), name='DcotorAnalytics'),
            ]

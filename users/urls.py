from .views import *

from django.urls import path

urlpatterns=[
    path("location/" ,UserLocation.as_view(),name="UserLocation"),
    path("book/appointment/" ,BookAppointment.as_view(),name="UserBookAppoitnment"),
    path("get/appointment/" ,GetAppointments.as_view(),name="UserGetAppointment"),
    path("get/future/appointment/" ,GetFutureUserAppointments.as_view(),name="UserGetFutureAppointment"),
    path("get/past/appointment/" ,GetPastUserAppointments.as_view(),name="UserGetPastAppointment"),
    path("offers/" ,GetUserOffers.as_view(),name="UserGetOffers"),
            ]
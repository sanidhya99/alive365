from rest_framework import serializers
from .models import *

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['time_slot']

class AppointmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'

class FutureAppointmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['doctor', 'date', 'time_slot']

class UserOffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOffers
        fields = '__all__'


class PastAppointmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['doctor', 'date', 'time_slot']        

class DateWiseAppointmentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Appointments
        fields = ['Patient','time_slot',]        
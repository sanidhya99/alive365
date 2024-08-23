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
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    class Meta:
        model = Appointments
        fields = ['doctor_name', 'date', 'time_slot']

class UserOffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOffers
        fields = '__all__'


class PastAppointmentDetailSerializer(serializers.ModelSerializer):
    # doctor_name = serializers.CharField(source='name')
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    class Meta:
        model = Appointments
        fields = ['doctor_name', 'date', 'time_slot']        

class DateWiseAppointmentSerializer(serializers.ModelSerializer):  
    # patient_name = serializers.CharField(source='name')
    # patient_name = serializers.CharField(source='patient.name', read_only=True)
    class Meta:
        model = Appointments
        fields = ['patient_offline','time_slot',"reason"]        
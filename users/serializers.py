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
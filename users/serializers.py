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
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointments
        fields = ['patient_name', 'time_slot', 'reason']

    def get_patient_name(self, obj):
        if obj.patient:
            return obj.patient.name
        return obj.patient_offline

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # If the patient field is null, remove it from the representation
        if not instance.patient:
            representation.pop('patient_name', None)
        return representation    
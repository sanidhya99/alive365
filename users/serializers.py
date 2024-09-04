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
        fields = ['doctor_name', 'date', 'time_slot','mode','paid']

class UserOffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOffers
        fields = '__all__'


class PastAppointmentDetailSerializer(serializers.ModelSerializer):
    # doctor_name = serializers.CharField(source='name')
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    class Meta:
        model = Appointments
        fields = ['doctor_name', 'date', 'time_slot','mode','paid']        

class DateWiseAppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointments
        fields = ['id','patient_name', 'time_slot', 'reason','paid','doctor','date','address','gender','age','phone','paid','mode']

    def get_patient_name(self, obj):
        if obj.patient:
            return obj.patient.name
        elif obj.patient_offline:
            return obj.patient_offline
        return None  # Return None if neither patient nor patient_offline is available

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove patient_name from the representation if it's None
        if representation.get('patient_name') is None:
            representation.pop('patient_name', None)
        return representation
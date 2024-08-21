from rest_framework import serializers
from .models import *
from users.models import Appointments
from django.utils import timezone
from datetime import timedelta


class DoctorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        fields = '__all__'

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

class FamousDoctorsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    appointments_last_7_days = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = ['name', 'category', 'rating', 'time_slot', 'appointments_last_7_days']

    def get_appointments_last_7_days(self, obj):
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        return Appointments.objects.filter(doctor=obj, date__range=[seven_days_ago, today]).count()


class DoctorTimeSlotSerializer(serializers.ModelSerializer):
    first_time_slot = serializers.SerializerMethodField()
    last_time_slot = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = ['id', 'name', 'first_time_slot', 'last_time_slot']

    def get_first_time_slot(self, obj):
        # Extract the first time slot if it exists
        if obj.time_slot and len(obj.time_slot) > 0:
            return obj.time_slot[0]
        return None

    def get_last_time_slot(self, obj):
        # Extract the last time slot if it exists
        if obj.time_slot and len(obj.time_slot) > 0:
            return obj.time_slot[-1]
        return None        

